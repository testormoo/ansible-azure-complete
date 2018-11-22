#!/usr/bin/python
#
# Copyright (c) 2018 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_datafactorypipeline
version_added: "2.8"
short_description: Manage Azure Pipeline instance.
description:
    - Create, update and delete instance of Azure Pipeline.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    name:
        description:
            - The pipeline name.
        required: True
    if_match:
        description:
            - ETag of the pipeline entity.  Should only be specified for update, for which it should match existing entity or can be * for unconditional update.
    additional_properties:
        description:
            - Unmatched properties from the message are deserialized this collection
    description:
        description:
            - The description of the pipeline.
    activities:
        description:
            - List of activities in pipeline.
        type: list
        suboptions:
            additional_properties:
                description:
                    - Unmatched properties from the message are deserialized this collection
            name:
                description:
                    - Activity name.
                    - Required when C(state) is I(present).
            description:
                description:
                    - Activity description.
            depends_on:
                description:
                    - Activity depends on condition.
                type: list
                suboptions:
                    additional_properties:
                        description:
                            - Unmatched properties from the message are deserialized this collection
                    activity:
                        description:
                            - Activity name.
                            - Required when C(state) is I(present).
                    dependency_conditions:
                        description:
                            - Match-Condition for the dependency.
                            - Required when C(state) is I(present).
                        type: list
            user_properties:
                description:
                    - Activity user properties.
                type: list
                suboptions:
                    name:
                        description:
                            - User proprety name.
                            - Required when C(state) is I(present).
                    value:
                        description:
                            - "User proprety value. Type: string (or Expression with resultType string)."
                            - Required when C(state) is I(present).
            type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    parameters:
        description:
            - List of parameters for pipeline.
    variables:
        description:
            - List of variables for pipeline.
    concurrency:
        description:
            - The max number of concurrent runs for the pipeline.
    annotations:
        description:
            - List of tags that can be used for describing the Pipeline.
        type: list
    folder:
        description:
            - The folder that this Pipeline is in. If not specified, Pipeline will appear at the root level.
        suboptions:
            name:
                description:
                    - The name of the folder that this Pipeline is in.
    state:
      description:
        - Assert the state of the Pipeline.
        - Use 'present' to create or update an Pipeline and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Pipeline
    azure_rm_datafactorypipeline:
      resource_group: exampleResourceGroup
      factory_name: exampleFactoryName
      name: examplePipeline
      if_match: NOT FOUND
      activities:
        - name: ExampleForeachActivity
          type: ForEach
      parameters: {
  "OutputBlobNameList": {
    "type": "Array"
  }
}
      variables: {
  "TestVariableArray": {
    "type": "Array"
  }
}
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: "/subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/exampleFactoryN
            ame/pipelines/examplePipeline"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPipeline(AzureRMModuleBase):
    """Configuration class for an Azure RM Pipeline resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            factory_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            additional_properties=dict(
                type='dict'
            ),
            description=dict(
                type='str'
            ),
            activities=dict(
                type='list'
            ),
            parameters=dict(
                type='dict'
            ),
            variables=dict(
                type='dict'
            ),
            concurrency=dict(
                type='int'
            ),
            annotations=dict(
                type='list'
            ),
            folder=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.factory_name = None
        self.name = None
        self.if_match = None
        self.pipeline = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPipeline, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.pipeline[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_pipeline()

        if not old_response:
            self.log("Pipeline instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Pipeline instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.pipeline, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Pipeline instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_pipeline()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Pipeline instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_pipeline()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_pipeline():
                time.sleep(20)
        else:
            self.log("Pipeline instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_pipeline(self):
        '''
        Creates or updates Pipeline with the specified configuration.

        :return: deserialized Pipeline instance state dictionary
        '''
        self.log("Creating / Updating the Pipeline instance {0}".format(self.name))

        try:
            response = self.mgmt_client.pipelines.create_or_update(resource_group_name=self.resource_group,
                                                                   factory_name=self.factory_name,
                                                                   pipeline_name=self.name,
                                                                   pipeline=self.pipeline)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Pipeline instance.')
            self.fail("Error creating the Pipeline instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_pipeline(self):
        '''
        Deletes specified Pipeline instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Pipeline instance {0}".format(self.name))
        try:
            response = self.mgmt_client.pipelines.delete(resource_group_name=self.resource_group,
                                                         factory_name=self.factory_name,
                                                         pipeline_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Pipeline instance.')
            self.fail("Error deleting the Pipeline instance: {0}".format(str(e)))

        return True

    def get_pipeline(self):
        '''
        Gets the properties of the specified Pipeline.

        :return: deserialized Pipeline instance state dictionary
        '''
        self.log("Checking if the Pipeline instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.pipelines.get(resource_group_name=self.resource_group,
                                                      factory_name=self.factory_name,
                                                      pipeline_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Pipeline instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Pipeline instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMPipeline()


if __name__ == '__main__':
    main()

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
short_description: Manage Pipeline instance.
description:
    - Create, update and delete instance of Pipeline.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    pipeline_name:
        description:
            - The I(pipeline) name.
        required: True
    if_match:
        description:
            - "ETag of the I(pipeline) entity.  Should only be specified for update, for which it should match existing entity or can be * for unconditional
               update."
    pipeline:
        description:
            - Pipeline resource definition.
        required: True
        suboptions:
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
                        required: True
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
                                required: True
                            dependency_conditions:
                                description:
                                    - Match-Condition for the dependency.
                                required: True
                                type: list
                    user_properties:
                        description:
                            - Activity user properties.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - User proprety name.
                                required: True
                            value:
                                description:
                                    - "User proprety value. Type: string (or Expression with resultType string)."
                                required: True
                    type:
                        description:
                            - Constant filled by server.
                        required: True
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
      pipeline_name: examplePipeline
      if_match: NOT FOUND
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


class AzureRMPipelines(AzureRMModuleBase):
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
            pipeline_name=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            pipeline=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.factory_name = None
        self.pipeline_name = None
        self.if_match = None
        self.pipeline = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPipelines, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "additional_properties":
                    self.pipeline["additional_properties"] = kwargs[key]
                elif key == "description":
                    self.pipeline["description"] = kwargs[key]
                elif key == "activities":
                    self.pipeline["activities"] = kwargs[key]
                elif key == "parameters":
                    self.pipeline["parameters"] = kwargs[key]
                elif key == "variables":
                    self.pipeline["variables"] = kwargs[key]
                elif key == "concurrency":
                    self.pipeline["concurrency"] = kwargs[key]
                elif key == "annotations":
                    self.pipeline["annotations"] = kwargs[key]
                elif key == "folder":
                    self.pipeline["folder"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Pipeline instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Pipeline instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_pipeline()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_pipeline(self):
        '''
        Creates or updates Pipeline with the specified configuration.

        :return: deserialized Pipeline instance state dictionary
        '''
        self.log("Creating / Updating the Pipeline instance {0}".format(self.pipeline_name))

        try:
            response = self.mgmt_client.pipelines.create_or_update(resource_group_name=self.resource_group,
                                                                   factory_name=self.factory_name,
                                                                   pipeline_name=self.pipeline_name,
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
        self.log("Deleting the Pipeline instance {0}".format(self.pipeline_name))
        try:
            response = self.mgmt_client.pipelines.delete(resource_group_name=self.resource_group,
                                                         factory_name=self.factory_name,
                                                         pipeline_name=self.pipeline_name)
        except CloudError as e:
            self.log('Error attempting to delete the Pipeline instance.')
            self.fail("Error deleting the Pipeline instance: {0}".format(str(e)))

        return True

    def get_pipeline(self):
        '''
        Gets the properties of the specified Pipeline.

        :return: deserialized Pipeline instance state dictionary
        '''
        self.log("Checking if the Pipeline instance {0} is present".format(self.pipeline_name))
        found = False
        try:
            response = self.mgmt_client.pipelines.get(resource_group_name=self.resource_group,
                                                      factory_name=self.factory_name,
                                                      pipeline_name=self.pipeline_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Pipeline instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Pipeline instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMPipelines()


if __name__ == '__main__':
    main()

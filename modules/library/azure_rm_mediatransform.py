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
module: azure_rm_mediatransform
version_added: "2.8"
short_description: Manage Azure Transform instance.
description:
    - Create, update and delete instance of Azure Transform.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    name:
        description:
            - The Transform name.
        required: True
    description:
        description:
            - An optional verbose description of the Transform.
    on_error:
        description:
            - "A Transform can define more than one outputs. This property defines what the service should do when one output fails - either continue to
               produce other outputs, or, stop the other outputs. The overall Job state will not reflect failures of outputs that are specified with
               'C(continue_job)'. The default is 'C(stop_processing_job)'."
        choices:
            - 'stop_processing_job'
            - 'continue_job'
    relative_priority:
        description:
            - "Sets the relative priority of the TransformOutputs within a Transform. This sets the priority that the service uses for processing
               TransformOutputs. The default priority is C(normal)."
        choices:
            - 'low'
            - 'normal'
            - 'high'
    preset:
        description:
            - Preset that describes the operations that will be used to modify, transcode, or extract insights from the source file to generate the output.
            - Required when C(state) is I(present).
        suboptions:
            odatatype:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Transform.
        - Use 'present' to create or update an Transform and 'absent' to delete it.
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
  - name: Create (or update) Transform
    azure_rm_mediatransform:
      resource_group: contosoresources
      account_name: contosomedia
      name: createdTransform
      description: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contosoresources/providers/Microsoft.Media/mediaservices/contosomedia/transfo
            rms/transformToUpdate"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMTransform(AzureRMModuleBase):
    """Configuration class for an Azure RM Transform resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            on_error=dict(
                type='str',
                choices=['stop_processing_job',
                         'continue_job']
            ),
            relative_priority=dict(
                type='str',
                choices=['low',
                         'normal',
                         'high']
            ),
            preset=dict(
                type='dict',
                options=dict(
                    odatatype=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.name = None
        self.description = None
        self.outputs = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMTransform, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.outputs[key] = kwargs[key]

        dict_camelize(self.outputs, ['on_error'], True)
        dict_camelize(self.outputs, ['relative_priority'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_transform()

        if not old_response:
            self.log("Transform instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Transform instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.outputs, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Transform instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_transform()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Transform instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_transform()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Transform instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_transform(self):
        '''
        Creates or updates Transform with the specified configuration.

        :return: deserialized Transform instance state dictionary
        '''
        self.log("Creating / Updating the Transform instance {0}".format(self.name))

        try:
            response = self.mgmt_client.transforms.create_or_update(resource_group_name=self.resource_group,
                                                                    account_name=self.account_name,
                                                                    transform_name=self.name,
                                                                    outputs=self.outputs)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Transform instance.')
            self.fail("Error creating the Transform instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_transform(self):
        '''
        Deletes specified Transform instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Transform instance {0}".format(self.name))
        try:
            response = self.mgmt_client.transforms.delete(resource_group_name=self.resource_group,
                                                          account_name=self.account_name,
                                                          transform_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Transform instance.')
            self.fail("Error deleting the Transform instance: {0}".format(str(e)))

        return True

    def get_transform(self):
        '''
        Gets the properties of the specified Transform.

        :return: deserialized Transform instance state dictionary
        '''
        self.log("Checking if the Transform instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.transforms.get(resource_group_name=self.resource_group,
                                                       account_name=self.account_name,
                                                       transform_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Transform instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Transform instance.')
        if found is True:
            return response.as_dict()

        return False


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
            else:
                key = list(old[0])[0]
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
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


def main():
    """Main execution"""
    AzureRMTransform()


if __name__ == '__main__':
    main()

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
module: azure_rm_applicationinsightsapikey
version_added: "2.8"
short_description: Manage Azure A P I Key instance.
description:
    - Create, update and delete instance of Azure A P I Key.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Application Insights component resource.
        required: True
    name:
        description:
            - The name of the API Key.
    linked_read_properties:
        description:
            - The read access rights of this API Key.
        type: list
    linked_write_properties:
        description:
            - The write access rights of this API Key.
        type: list
    state:
      description:
        - Assert the state of the A P I Key.
        - Use 'present' to create or update an A P I Key and 'absent' to delete it.
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
  - name: Create (or update) A P I Key
    azure_rm_applicationinsightsapikey:
      resource_group: my-resource-group
      name: my-component
      name: test2
      linked_read_properties:
        - [
  "/subscriptions/subid/resourceGroups/my-resource-group/providers/Microsoft.Insights/components/my-component/api",
  "/subscriptions/subid/resourceGroups/my-resource-group/providers/Microsoft.Insights/components/my-component/agentconfig"
]
      linked_write_properties:
        - [
  "/subscriptions/subid/resourceGroups/my-resource-group/providers/Microsoft.Insights/components/my-component/annotations"
]
'''

RETURN = '''
id:
    description:
        - The unique ID of the API key inside an Applciation Insights component. It is auto generated when the API key is created.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourcegroups/my-resource-group/providers/Microsoft.Insights/components/my-component/apikeys/fe2e0138-47c1-46c5-8726-872f5
            4c1ca08"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAPIKey(AzureRMModuleBase):
    """Configuration class for an Azure RM A P I Key resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            linked_read_properties=dict(
                type='list'
            ),
            linked_write_properties=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.api_key_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAPIKey, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.api_key_properties[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_apikey()

        if not old_response:
            self.log("A P I Key instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("A P I Key instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.api_key_properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the A P I Key instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apikey()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("A P I Key instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apikey()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("A P I Key instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_apikey(self):
        '''
        Creates or updates A P I Key with the specified configuration.

        :return: deserialized A P I Key instance state dictionary
        '''
        self.log("Creating / Updating the A P I Key instance {0}".format(self.key_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.api_keys.create(resource_group_name=self.resource_group,
                                                            resource_name=self.name,
                                                            api_key_properties=self.api_key_properties)
            else:
                response = self.mgmt_client.api_keys.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the A P I Key instance.')
            self.fail("Error creating the A P I Key instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apikey(self):
        '''
        Deletes specified A P I Key instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the A P I Key instance {0}".format(self.key_id))
        try:
            response = self.mgmt_client.api_keys.delete(resource_group_name=self.resource_group,
                                                        resource_name=self.name,
                                                        key_id=self.key_id)
        except CloudError as e:
            self.log('Error attempting to delete the A P I Key instance.')
            self.fail("Error deleting the A P I Key instance: {0}".format(str(e)))

        return True

    def get_apikey(self):
        '''
        Gets the properties of the specified A P I Key.

        :return: deserialized A P I Key instance state dictionary
        '''
        self.log("Checking if the A P I Key instance {0} is present".format(self.key_id))
        found = False
        try:
            response = self.mgmt_client.api_keys.get(resource_group_name=self.resource_group,
                                                     resource_name=self.name,
                                                     key_id=self.key_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("A P I Key instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the A P I Key instance.')
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


def main():
    """Main execution"""
    AzureRMAPIKey()


if __name__ == '__main__':
    main()

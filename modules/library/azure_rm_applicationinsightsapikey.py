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
short_description: Manage A P I Key instance.
description:
    - Create, update and delete instance of A P I Key.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    resource_name:
        description:
            - The name of the Application Insights component resource.
        required: True
    api_key_properties:
        description:
            - Properties that need to be specified to create an API key of a Application Insights component.
        required: True
        suboptions:
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
      resource_name: my-component
      api_key_properties:
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


class AzureRMAPIKeys(AzureRMModuleBase):
    """Configuration class for an Azure RM A P I Key resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            api_key_properties=dict(
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
        self.resource_name = None
        self.api_key_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAPIKeys, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "name":
                    self.api_key_properties["name"] = kwargs[key]
                elif key == "linked_read_properties":
                    self.api_key_properties["linked_read_properties"] = kwargs[key]
                elif key == "linked_write_properties":
                    self.api_key_properties["linked_write_properties"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if A P I Key instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the A P I Key instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apikey()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("A P I Key instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apikey()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apikey():
                time.sleep(20)
        else:
            self.log("A P I Key instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
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
                                                            resource_name=self.resource_name,
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
                                                        resource_name=self.resource_name,
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
                                                     resource_name=self.resource_name,
                                                     key_id=self.key_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("A P I Key instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the A P I Key instance.')
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
    AzureRMAPIKeys()


if __name__ == '__main__':
    main()

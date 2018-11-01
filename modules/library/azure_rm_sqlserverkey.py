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
module: azure_rm_sqlserverkey
version_added: "2.8"
short_description: Manage Server Key instance.
description:
    - Create, update and delete instance of Server Key.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    key_name:
        description:
            - "The name of the server key to be operated on (updated or created). The key name is required to be in the format of 'vault_key_version'. For
               example, if the keyId is https://YourVaultName.vault.azure.net/keys/YourKeyName/01234567890123456789012345678901, then the server key name
               should be formatted as: YourVaultName_YourKeyName_01234567890123456789012345678901"
        required: True
    kind:
        description:
            - Kind of encryption protector. This is metadata used for the Azure portal experience.
    server_key_type:
        description:
            - "The server key type like 'C(service_managed)', 'C(azure_key_vault)'."
        required: True
        choices:
            - 'service_managed'
            - 'azure_key_vault'
    uri:
        description:
            - The URI of the server key.
    thumbprint:
        description:
            - Thumbprint of the server key.
    creation_date:
        description:
            - The server key creation date.
    state:
      description:
        - Assert the state of the Server Key.
        - Use 'present' to create or update an Server Key and 'absent' to delete it.
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
  - name: Create (or update) Server Key
    azure_rm_sqlserverkey:
      resource_group: sqlcrudtest-7398
      server_name: sqlcrudtest-4645
      key_name: someVault_someKey_01234567890123456789012345678901
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-7398/providers/Microsoft.Sql/servers/sqlcrudtest-4645/keys/someVa
            ult_someKey_01234567890123456789012345678901"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMServerKeys(AzureRMModuleBase):
    """Configuration class for an Azure RM Server Key resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            key_name=dict(
                type='str',
                required=True
            ),
            kind=dict(
                type='str'
            ),
            server_key_type=dict(
                type='str',
                choices=['service_managed',
                         'azure_key_vault'],
                required=True
            ),
            uri=dict(
                type='str'
            ),
            thumbprint=dict(
                type='str'
            ),
            creation_date=dict(
                type='datetime'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.key_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServerKeys, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "kind":
                    self.parameters["kind"] = kwargs[key]
                elif key == "server_key_type":
                    self.parameters["server_key_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "uri":
                    self.parameters["uri"] = kwargs[key]
                elif key == "thumbprint":
                    self.parameters["thumbprint"] = kwargs[key]
                elif key == "creation_date":
                    self.parameters["creation_date"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_serverkey()

        if not old_response:
            self.log("Server Key instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Server Key instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Server Key instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Server Key instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_serverkey()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Server Key instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_serverkey()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_serverkey():
                time.sleep(20)
        else:
            self.log("Server Key instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_serverkey(self):
        '''
        Creates or updates Server Key with the specified configuration.

        :return: deserialized Server Key instance state dictionary
        '''
        self.log("Creating / Updating the Server Key instance {0}".format(self.key_name))

        try:
            response = self.mgmt_client.server_keys.create_or_update(resource_group_name=self.resource_group,
                                                                     server_name=self.server_name,
                                                                     key_name=self.key_name,
                                                                     parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Server Key instance.')
            self.fail("Error creating the Server Key instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serverkey(self):
        '''
        Deletes specified Server Key instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Server Key instance {0}".format(self.key_name))
        try:
            response = self.mgmt_client.server_keys.delete(resource_group_name=self.resource_group,
                                                           server_name=self.server_name,
                                                           key_name=self.key_name)
        except CloudError as e:
            self.log('Error attempting to delete the Server Key instance.')
            self.fail("Error deleting the Server Key instance: {0}".format(str(e)))

        return True

    def get_serverkey(self):
        '''
        Gets the properties of the specified Server Key.

        :return: deserialized Server Key instance state dictionary
        '''
        self.log("Checking if the Server Key instance {0} is present".format(self.key_name))
        found = False
        try:
            response = self.mgmt_client.server_keys.get(resource_group_name=self.resource_group,
                                                        server_name=self.server_name,
                                                        key_name=self.key_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Server Key instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Server Key instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMServerKeys()


if __name__ == '__main__':
    main()

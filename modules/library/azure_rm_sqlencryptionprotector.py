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
module: azure_rm_sqlencryptionprotector
version_added: "2.8"
short_description: Manage Encryption Protector instance.
description:
    - Create, update and delete instance of Encryption Protector.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the encryption protector to be updated.
        required: True
    kind:
        description:
            - Kind of encryption protector. This is metadata used for the Azure portal experience.
    server_key_name:
        description:
            - The name of the server key.
    server_key_type:
        description:
            - "The encryption protector type like 'C(service_managed)', 'C(azure_key_vault)'."
            - Required when C(state) is I(present).
        choices:
            - 'service_managed'
            - 'azure_key_vault'
    state:
      description:
        - Assert the state of the Encryption Protector.
        - Use 'present' to create or update an Encryption Protector and 'absent' to delete it.
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
  - name: Create (or update) Encryption Protector
    azure_rm_sqlencryptionprotector:
      resource_group: sqlcrudtest-7398
      server_name: sqlcrudtest-4645
      name: current
      server_key_name: someVault_someKey_01234567890123456789012345678901
      server_key_type: AzureKeyVault
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-7398/providers/Microsoft.Sql/servers/sqlcrudtest-4645/encryptionP
            rotector/current"
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


class AzureRMEncryptionProtectors(AzureRMModuleBase):
    """Configuration class for an Azure RM Encryption Protector resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            kind=dict(
                type='str'
            ),
            server_key_name=dict(
                type='str'
            ),
            server_key_type=dict(
                type='str',
                choices=['service_managed',
                         'azure_key_vault']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEncryptionProtectors, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "server_key_name":
                    self.parameters["server_key_name"] = kwargs[key]
                elif key == "server_key_type":
                    self.parameters["server_key_type"] = _snake_to_camel(kwargs[key], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_encryptionprotector()

        if not old_response:
            self.log("Encryption Protector instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Encryption Protector instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Encryption Protector instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_encryptionprotector()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Encryption Protector instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_encryptionprotector()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_encryptionprotector():
                time.sleep(20)
        else:
            self.log("Encryption Protector instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_encryptionprotector(self):
        '''
        Creates or updates Encryption Protector with the specified configuration.

        :return: deserialized Encryption Protector instance state dictionary
        '''
        self.log("Creating / Updating the Encryption Protector instance {0}".format(self.name))

        try:
            response = self.mgmt_client.encryption_protectors.create_or_update(resource_group_name=self.resource_group,
                                                                               server_name=self.server_name,
                                                                               encryption_protector_name=self.name,
                                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Encryption Protector instance.')
            self.fail("Error creating the Encryption Protector instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_encryptionprotector(self):
        '''
        Deletes specified Encryption Protector instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Encryption Protector instance {0}".format(self.name))
        try:
            response = self.mgmt_client.encryption_protectors.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Encryption Protector instance.')
            self.fail("Error deleting the Encryption Protector instance: {0}".format(str(e)))

        return True

    def get_encryptionprotector(self):
        '''
        Gets the properties of the specified Encryption Protector.

        :return: deserialized Encryption Protector instance state dictionary
        '''
        self.log("Checking if the Encryption Protector instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.encryption_protectors.get(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  encryption_protector_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Encryption Protector instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Encryption Protector instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMEncryptionProtectors()


if __name__ == '__main__':
    main()

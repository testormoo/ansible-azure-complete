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
short_description: Manage Azure Encryption Protector instance.
description:
    - Create, update and delete instance of Azure Encryption Protector.

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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMEncryptionProtector(AzureRMModuleBase):
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

        super(AzureRMEncryptionProtector, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['server_key_type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Encryption Protector instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
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
    AzureRMEncryptionProtector()


if __name__ == '__main__':
    main()

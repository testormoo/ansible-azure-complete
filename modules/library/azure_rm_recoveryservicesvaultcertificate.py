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
module: azure_rm_recoveryservicesvaultcertificate
version_added: "2.8"
short_description: Manage Vault Certificate instance.
description:
    - Create, update and delete instance of Vault Certificate.

options:
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True
    name:
        description:
            - I(certificate) friendly name.
        required: True
    auth_type:
        description:
            - Specifies the authentication type.
        choices:
            - 'invalid'
            - 'acs'
            - 'aad'
            - 'access_control_service'
            - 'azure_active_directory'
    certificate:
        description:
            - The base64 encoded certificate raw data string
    state:
      description:
        - Assert the state of the Vault Certificate.
        - Use 'present' to create or update an Vault Certificate and 'absent' to delete it.
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
  - name: Create (or update) Vault Certificate
    azure_rm_recoveryservicesvaultcertificate:
      resource_group: BCDRIbzRG
      vault_name: BCDRIbzVault
      name: BCDRIbzVault77777777-d41f-4550-9f70-7708a3a2283b-12-18-2017-vaultcredentials
'''

RETURN = '''
id:
    description:
        - Resource Id represents the complete path to the resource.
    returned: always
    type: str
    sample: "/Subscriptions/77777777-d41f-4550-9f70-7708a3a2283b/resourceGroups/BCDRIbzRG/providers/Microsoft.RecoveryServices/vaults/BCDRIbzVault/certificat
            es/BCDRIbzVault77777777-d41f-4550-9f70-7708a3a2283b-12-18-2017-vaultcredentials"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.recoveryservices import RecoveryServicesClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVaultCertificates(AzureRMModuleBase):
    """Configuration class for an Azure RM Vault Certificate resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vault_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            auth_type=dict(
                type='str',
                choices=['invalid',
                         'acs',
                         'aad',
                         'access_control_service',
                         'azure_active_directory']
            ),
            certificate=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.vault_name = None
        self.name = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVaultCertificates, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "auth_type":
                    ev = kwargs[key]
                    if ev == 'acs':
                        ev = 'ACS'
                    elif ev == 'aad':
                        ev = 'AAD'
                    self.properties["auth_type"] = _snake_to_camel(ev, True)
                elif key == "certificate":
                    self.properties["certificate"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_vaultcertificate()

        if not old_response:
            self.log("Vault Certificate instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Vault Certificate instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Vault Certificate instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_vaultcertificate()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Vault Certificate instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_vaultcertificate()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_vaultcertificate():
                time.sleep(20)
        else:
            self.log("Vault Certificate instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_vaultcertificate(self):
        '''
        Creates or updates Vault Certificate with the specified configuration.

        :return: deserialized Vault Certificate instance state dictionary
        '''
        self.log("Creating / Updating the Vault Certificate instance {0}".format(self.))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.vault_certificates.create(resource_group_name=self.resource_group,
                                                                      vault_name=self.vault_name,
                                                                      certificate_name=self.name)
            else:
                response = self.mgmt_client.vault_certificates.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Vault Certificate instance.')
            self.fail("Error creating the Vault Certificate instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_vaultcertificate(self):
        '''
        Deletes specified Vault Certificate instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Vault Certificate instance {0}".format(self.))
        try:
            response = self.mgmt_client.vault_certificates.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Vault Certificate instance.')
            self.fail("Error deleting the Vault Certificate instance: {0}".format(str(e)))

        return True

    def get_vaultcertificate(self):
        '''
        Gets the properties of the specified Vault Certificate.

        :return: deserialized Vault Certificate instance state dictionary
        '''
        self.log("Checking if the Vault Certificate instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.vault_certificates.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Vault Certificate instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Vault Certificate instance.')
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
    AzureRMVaultCertificates()


if __name__ == '__main__':
    main()

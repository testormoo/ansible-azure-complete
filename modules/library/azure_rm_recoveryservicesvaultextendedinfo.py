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
module: azure_rm_recoveryservicesvaultextendedinfo
version_added: "2.8"
short_description: Manage Vault Extended Info instance.
description:
    - Create, update and delete instance of Vault Extended Info.

options:
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True
    resource_resource_extended_info_details:
        description:
            - Details of ResourceExtendedInfo
        required: True
        suboptions:
            e_tag:
                description:
                    - Optional ETag.
            integrity_key:
                description:
                    - Integrity key.
            encryption_key:
                description:
                    - Encryption key.
            encryption_key_thumbprint:
                description:
                    - Encryption key thumbprint.
            algorithm:
                description:
                    - Algorithm for Vault ExtendedInfo
    state:
      description:
        - Assert the state of the Vault Extended Info.
        - Use 'present' to create or update an Vault Extended Info and 'absent' to delete it.
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
  - name: Create (or update) Vault Extended Info
    azure_rm_recoveryservicesvaultextendedinfo:
      resource_group: Default-RecoveryServices-ResourceGroup
      vault_name: swaggerExample
'''

RETURN = '''
id:
    description:
        - Resource Id represents the complete path to the resource.
    returned: always
    type: str
    sample: "/subscriptions/77777777-b0c6-47a2-b37c-d8e65a629c18/resourceGroups/Default-RecoveryServices-ResourceGroup/providers/Microsoft.RecoveryServices/v
            aults/swaggerExample/extendedInformation/vaultExtendedInfo"
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


class AzureRMVaultExtendedInfo(AzureRMModuleBase):
    """Configuration class for an Azure RM Vault Extended Info resource"""

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
            resource_resource_extended_info_details=dict(
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
        self.vault_name = None
        self.resource_resource_extended_info_details = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVaultExtendedInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "e_tag":
                    self.resource_resource_extended_info_details["e_tag"] = kwargs[key]
                elif key == "integrity_key":
                    self.resource_resource_extended_info_details["integrity_key"] = kwargs[key]
                elif key == "encryption_key":
                    self.resource_resource_extended_info_details["encryption_key"] = kwargs[key]
                elif key == "encryption_key_thumbprint":
                    self.resource_resource_extended_info_details["encryption_key_thumbprint"] = kwargs[key]
                elif key == "algorithm":
                    self.resource_resource_extended_info_details["algorithm"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_vaultextendedinfo()

        if not old_response:
            self.log("Vault Extended Info instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Vault Extended Info instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Vault Extended Info instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Vault Extended Info instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_vaultextendedinfo()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Vault Extended Info instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_vaultextendedinfo()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_vaultextendedinfo():
                time.sleep(20)
        else:
            self.log("Vault Extended Info instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_vaultextendedinfo(self):
        '''
        Creates or updates Vault Extended Info with the specified configuration.

        :return: deserialized Vault Extended Info instance state dictionary
        '''
        self.log("Creating / Updating the Vault Extended Info instance {0}".format(self.vault_name))

        try:
            response = self.mgmt_client.vault_extended_info.create_or_update(resource_group_name=self.resource_group,
                                                                             vault_name=self.vault_name,
                                                                             resource_resource_extended_info_details=self.resource_resource_extended_info_details)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Vault Extended Info instance.')
            self.fail("Error creating the Vault Extended Info instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_vaultextendedinfo(self):
        '''
        Deletes specified Vault Extended Info instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Vault Extended Info instance {0}".format(self.vault_name))
        try:
            response = self.mgmt_client.vault_extended_info.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Vault Extended Info instance.')
            self.fail("Error deleting the Vault Extended Info instance: {0}".format(str(e)))

        return True

    def get_vaultextendedinfo(self):
        '''
        Gets the properties of the specified Vault Extended Info.

        :return: deserialized Vault Extended Info instance state dictionary
        '''
        self.log("Checking if the Vault Extended Info instance {0} is present".format(self.vault_name))
        found = False
        try:
            response = self.mgmt_client.vault_extended_info.get(resource_group_name=self.resource_group,
                                                                vault_name=self.vault_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Vault Extended Info instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Vault Extended Info instance.')
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
    AzureRMVaultExtendedInfo()


if __name__ == '__main__':
    main()

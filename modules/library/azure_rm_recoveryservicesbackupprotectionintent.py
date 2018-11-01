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
module: azure_rm_recoveryservicesbackupprotectionintent
version_added: "2.8"
short_description: Manage Protection Intent instance.
description:
    - Create, update and delete instance of Protection Intent.

options:
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    fabric_name:
        description:
            - Fabric name associated with the backup item.
        required: True
    intent_object_name:
        description:
            - Intent object name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    e_tag:
        description:
            - Optional ETag.
    backup_management_type:
        description:
            - Type of backup managemenent for the backed up item.
        choices:
            - 'invalid'
            - 'azure_iaas_vm'
            - 'mab'
            - 'dpm'
            - 'azure_backup_server'
            - 'azure_sql'
            - 'azure_storage'
            - 'azure_workload'
            - 'default_backup'
    source_resource_id:
        description:
            - ARM ID of the resource to be backed up.
    item_id:
        description:
            - ID of the item which is getting C(protected), In case of Azure Vm , it is ProtectedItemId
    policy_id:
        description:
            - ID of the backup policy with which this item is backed up.
    protection_state:
        description:
            - Backup state of this backup item.
        choices:
            - 'invalid'
            - 'not_protected'
            - 'protecting'
            - 'protected'
            - 'protection_failed'
    protection_intent_item_type:
        description:
            - Constant filled by server.
        required: True
    state:
      description:
        - Assert the state of the Protection Intent.
        - Use 'present' to create or update an Protection Intent and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Protection Intent
    azure_rm_recoveryservicesbackupprotectionintent:
      vault_name: myVault
      resource_group: myRG
      fabric_name: Azure
      intent_object_name: vm;iaasvmcontainerv2;chamsrgtest;chamscandel
      location: eastus
      source_resource_id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/chamsrgtest/providers/Microsoft.Compute/virtualMachines/chamscandel
      policy_id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myRG/providers/Microsoft.RecoveryServices/vaults/myVault/backupPolicies/myPolicy
'''

RETURN = '''
id:
    description:
        - Resource Id represents the complete path to the resource.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myRG/providers/Microsoft.RecoveryServices/vaults/myVault/backupFabrics/Azure/
            backupProtectionIntent/vm;iaasvmcontainerv2;chamsrgtest;chamscandel"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMProtectionIntent(AzureRMModuleBase):
    """Configuration class for an Azure RM Protection Intent resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            vault_name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            fabric_name=dict(
                type='str',
                required=True
            ),
            intent_object_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            e_tag=dict(
                type='str'
            ),
            backup_management_type=dict(
                type='str',
                choices=['invalid',
                         'azure_iaas_vm',
                         'mab',
                         'dpm',
                         'azure_backup_server',
                         'azure_sql',
                         'azure_storage',
                         'azure_workload',
                         'default_backup']
            ),
            source_resource_id=dict(
                type='str'
            ),
            item_id=dict(
                type='str'
            ),
            policy_id=dict(
                type='str'
            ),
            protection_state=dict(
                type='str',
                choices=['invalid',
                         'not_protected',
                         'protecting',
                         'protected',
                         'protection_failed']
            ),
            protection_intent_item_type=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.vault_name = None
        self.resource_group = None
        self.fabric_name = None
        self.intent_object_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProtectionIntent, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "e_tag":
                    self.parameters["e_tag"] = kwargs[key]
                elif key == "backup_management_type":
                    ev = kwargs[key]
                    if ev == 'azure_iaas_vm':
                        ev = 'AzureIaasVM'
                    elif ev == 'mab':
                        ev = 'MAB'
                    elif ev == 'dpm':
                        ev = 'DPM'
                    self.parameters.setdefault("properties", {})["backup_management_type"] = _snake_to_camel(ev, True)
                elif key == "source_resource_id":
                    self.parameters.setdefault("properties", {})["source_resource_id"] = kwargs[key]
                elif key == "item_id":
                    self.parameters.setdefault("properties", {})["item_id"] = kwargs[key]
                elif key == "policy_id":
                    self.parameters.setdefault("properties", {})["policy_id"] = kwargs[key]
                elif key == "protection_state":
                    self.parameters.setdefault("properties", {})["protection_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "protection_intent_item_type":
                    self.parameters.setdefault("properties", {})["protection_intent_item_type"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_protectionintent()

        if not old_response:
            self.log("Protection Intent instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Protection Intent instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Protection Intent instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Protection Intent instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_protectionintent()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Protection Intent instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_protectionintent()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_protectionintent():
                time.sleep(20)
        else:
            self.log("Protection Intent instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_protectionintent(self):
        '''
        Creates or updates Protection Intent with the specified configuration.

        :return: deserialized Protection Intent instance state dictionary
        '''
        self.log("Creating / Updating the Protection Intent instance {0}".format(self.intent_object_name))

        try:
            response = self.mgmt_client.protection_intent.create_or_update(vault_name=self.vault_name,
                                                                           resource_group_name=self.resource_group,
                                                                           fabric_name=self.fabric_name,
                                                                           intent_object_name=self.intent_object_name,
                                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Protection Intent instance.')
            self.fail("Error creating the Protection Intent instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_protectionintent(self):
        '''
        Deletes specified Protection Intent instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Protection Intent instance {0}".format(self.intent_object_name))
        try:
            response = self.mgmt_client.protection_intent.delete(vault_name=self.vault_name,
                                                                 resource_group_name=self.resource_group,
                                                                 fabric_name=self.fabric_name,
                                                                 intent_object_name=self.intent_object_name)
        except CloudError as e:
            self.log('Error attempting to delete the Protection Intent instance.')
            self.fail("Error deleting the Protection Intent instance: {0}".format(str(e)))

        return True

    def get_protectionintent(self):
        '''
        Gets the properties of the specified Protection Intent.

        :return: deserialized Protection Intent instance state dictionary
        '''
        self.log("Checking if the Protection Intent instance {0} is present".format(self.intent_object_name))
        found = False
        try:
            response = self.mgmt_client.protection_intent.get(vault_name=self.vault_name,
                                                              resource_group_name=self.resource_group,
                                                              fabric_name=self.fabric_name,
                                                              intent_object_name=self.intent_object_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Protection Intent instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Protection Intent instance.')
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
    AzureRMProtectionIntent()


if __name__ == '__main__':
    main()

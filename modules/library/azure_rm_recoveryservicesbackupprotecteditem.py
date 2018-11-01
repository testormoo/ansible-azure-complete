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
module: azure_rm_recoveryservicesbackupprotecteditem
version_added: "2.8"
short_description: Manage Protected Item instance.
description:
    - Create, update and delete instance of Protected Item.

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
    container_name:
        description:
            - Container name associated with the backup item.
        required: True
    protected_item_name:
        description:
            - Item name to be backed up.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as C(default).
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
    workload_type:
        description:
            - Type of workload this item represents.
        choices:
            - 'invalid'
            - 'vm'
            - 'file_folder'
            - 'azure_sql_db'
            - 'sqldb'
            - 'exchange'
            - 'sharepoint'
            - 'vmware_vm'
            - 'system_state'
            - 'client'
            - 'generic_data_source'
            - 'sql_data_base'
            - 'azure_file_share'
            - 'sap_hana_database'
    container_name:
        description:
            - Unique name of container
    source_resource_id:
        description:
            - ARM ID of the resource to be backed up.
    policy_id:
        description:
            - ID of the backup policy with which this item is backed up.
    last_recovery_point:
        description:
            - Timestamp when the last (latest) backup copy was created for this backup item.
    backup_set_name:
        description:
            - Name of the backup set the backup item belongs to
    create_mode:
        description:
            - Create mode to indicate recovery of existing soft deleted data source or creation of new data source.
        choices:
            - 'invalid'
            - 'default'
            - 'recover'
    protected_item_type:
        description:
            - Constant filled by server.
        required: True
    state:
      description:
        - Assert the state of the Protected Item.
        - Use 'present' to create or update an Protected Item and 'absent' to delete it.
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
  - name: Create (or update) Protected Item
    azure_rm_recoveryservicesbackupprotecteditem:
      vault_name: NetSDKTestRsVault
      resource_group: SwaggerTestRg
      fabric_name: Azure
      container_name: IaasVMContainer;iaasvmcontainerv2;netsdktestrg;netvmtestv2vm1
      protected_item_name: VM;iaasvmcontainerv2;netsdktestrg;netvmtestv2vm1
      location: eastus
      source_resource_id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/netsdktestrg/providers/Microsoft.Compute/virtualMachines/netvmtestv2vm1
      policy_id: /Subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/SwaggerTestRg/providers/Microsoft.RecoveryServices/vaults/NetSDKTestRsVault/backupPolicies/DefaultPolicy
'''

RETURN = '''
id:
    description:
        - Resource Id represents the complete path to the resource.
    returned: always
    type: str
    sample: id
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


class AzureRMProtectedItems(AzureRMModuleBase):
    """Configuration class for an Azure RM Protected Item resource"""

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
            container_name=dict(
                type='str',
                required=True
            ),
            protected_item_name=dict(
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
            workload_type=dict(
                type='str',
                choices=['invalid',
                         'vm',
                         'file_folder',
                         'azure_sql_db',
                         'sqldb',
                         'exchange',
                         'sharepoint',
                         'vmware_vm',
                         'system_state',
                         'client',
                         'generic_data_source',
                         'sql_data_base',
                         'azure_file_share',
                         'sap_hana_database']
            ),
            container_name=dict(
                type='str'
            ),
            source_resource_id=dict(
                type='str'
            ),
            policy_id=dict(
                type='str'
            ),
            last_recovery_point=dict(
                type='datetime'
            ),
            backup_set_name=dict(
                type='str'
            ),
            create_mode=dict(
                type='str',
                choices=['invalid',
                         'default',
                         'recover']
            ),
            protected_item_type=dict(
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
        self.container_name = None
        self.protected_item_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProtectedItems, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "workload_type":
                    ev = kwargs[key]
                    if ev == 'vm':
                        ev = 'VM'
                    elif ev == 'sqldb':
                        ev = 'SQLDB'
                    elif ev == 'vmware_vm':
                        ev = 'VMwareVM'
                    elif ev == 'sql_data_base':
                        ev = 'SQLDataBase'
                    elif ev == 'sap_hana_database':
                        ev = 'SAPHanaDatabase'
                    self.parameters.setdefault("properties", {})["workload_type"] = _snake_to_camel(ev, True)
                elif key == "container_name":
                    self.parameters.setdefault("properties", {})["container_name"] = kwargs[key]
                elif key == "source_resource_id":
                    self.parameters.setdefault("properties", {})["source_resource_id"] = kwargs[key]
                elif key == "policy_id":
                    self.parameters.setdefault("properties", {})["policy_id"] = kwargs[key]
                elif key == "last_recovery_point":
                    self.parameters.setdefault("properties", {})["last_recovery_point"] = kwargs[key]
                elif key == "backup_set_name":
                    self.parameters.setdefault("properties", {})["backup_set_name"] = kwargs[key]
                elif key == "create_mode":
                    self.parameters.setdefault("properties", {})["create_mode"] = _snake_to_camel(kwargs[key], True)
                elif key == "protected_item_type":
                    self.parameters.setdefault("properties", {})["protected_item_type"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_protecteditem()

        if not old_response:
            self.log("Protected Item instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Protected Item instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Protected Item instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Protected Item instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_protecteditem()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Protected Item instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_protecteditem()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_protecteditem():
                time.sleep(20)
        else:
            self.log("Protected Item instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_protecteditem(self):
        '''
        Creates or updates Protected Item with the specified configuration.

        :return: deserialized Protected Item instance state dictionary
        '''
        self.log("Creating / Updating the Protected Item instance {0}".format(self.protected_item_name))

        try:
            response = self.mgmt_client.protected_items.create_or_update(vault_name=self.vault_name,
                                                                         resource_group_name=self.resource_group,
                                                                         fabric_name=self.fabric_name,
                                                                         container_name=self.container_name,
                                                                         protected_item_name=self.protected_item_name,
                                                                         parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Protected Item instance.')
            self.fail("Error creating the Protected Item instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_protecteditem(self):
        '''
        Deletes specified Protected Item instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Protected Item instance {0}".format(self.protected_item_name))
        try:
            response = self.mgmt_client.protected_items.delete(vault_name=self.vault_name,
                                                               resource_group_name=self.resource_group,
                                                               fabric_name=self.fabric_name,
                                                               container_name=self.container_name,
                                                               protected_item_name=self.protected_item_name)
        except CloudError as e:
            self.log('Error attempting to delete the Protected Item instance.')
            self.fail("Error deleting the Protected Item instance: {0}".format(str(e)))

        return True

    def get_protecteditem(self):
        '''
        Gets the properties of the specified Protected Item.

        :return: deserialized Protected Item instance state dictionary
        '''
        self.log("Checking if the Protected Item instance {0} is present".format(self.protected_item_name))
        found = False
        try:
            response = self.mgmt_client.protected_items.get(vault_name=self.vault_name,
                                                            resource_group_name=self.resource_group,
                                                            fabric_name=self.fabric_name,
                                                            container_name=self.container_name,
                                                            protected_item_name=self.protected_item_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Protected Item instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Protected Item instance.')
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
    AzureRMProtectedItems()


if __name__ == '__main__':
    main()

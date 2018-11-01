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
module: azure_rm_storageaccount
version_added: "2.8"
short_description: Manage Storage Account instance.
description:
    - Create, update and delete instance of Storage Account.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    account_name:
        description:
            - "The name of the C(storage) account within the specified resource group. C(storage) account names must be between 3 and 24 characters in
               length and use numbers and lower-case letters only."
        required: True
    sku:
        description:
            - Required. Gets or sets the sku name.
        required: True
        suboptions:
            name:
                description:
                    - "Gets or sets the sku name. Required for account creation; optional for update. Note that in older versions, sku name was called
                       accountType."
                required: True
                choices:
                    - 'standard_lrs'
                    - 'standard_grs'
                    - 'standard_ragrs'
                    - 'standard_zrs'
                    - 'premium_lrs'
                    - 'premium_zrs'
            restrictions:
                description:
                    - The restrictions because of which SKU cannot be used. This is empty if there are no restrictions.
                type: list
                suboptions:
                    reason_code:
                        description:
                            - "The reason for the restriction. As of now this can be 'C(quota_id)' or 'C(not_available_for_subscription)'. Quota Id is set
                               when the SKU has requiredQuotas parameter as the subscription does not belong to that quota. The
                               'C(not_available_for_subscription)' is related to capacity at DC."
                        choices:
                            - 'quota_id'
                            - 'not_available_for_subscription'
    kind:
        description:
            - Required. Indicates the type of C(storage) account.
        required: True
        choices:
            - 'storage'
            - 'storage_v2'
            - 'blob_storage'
            - 'file_storage'
            - 'block_blob_storage'
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    identity:
        description:
            - The identity of the resource.
        suboptions:
            type:
                description:
                    - The identity type.
                required: True
    custom_domain:
        description:
            - "User domain assigned to the C(storage) account. Name is the CNAME source. Only one custom domain is supported per C(storage) account at this
               time. To clear the existing custom domain, use an empty string for the custom domain name property."
        suboptions:
            name:
                description:
                    - Gets or sets the custom domain name assigned to the storage account. Name is the CNAME source.
                required: True
            use_sub_domain:
                description:
                    - Indicates whether indirect CName validation is enabled. Default value is false. This should only be set on updates.
    encryption:
        description:
            - "Provides the encryption settings on the account. If left unspecified the account encryption settings will remain the same. The default
               setting is unencrypted."
        suboptions:
            services:
                description:
                    - List of services which support encryption.
                suboptions:
                    blob:
                        description:
                            - The encryption function of the blob storage service.
                        suboptions:
                            enabled:
                                description:
                                    - A boolean indicating whether or not the service encrypts the data as it is stored.
                    file:
                        description:
                            - The encryption function of the file storage service.
                        suboptions:
                            enabled:
                                description:
                                    - A boolean indicating whether or not the service encrypts the data as it is stored.
            key_source:
                description:
                    - "The encryption keySource (provider). Possible values (case-insensitive):  C(microsoft._storage), C(microsoft._keyvault)."
                required: True
                choices:
                    - 'microsoft._storage'
                    - 'microsoft._keyvault'
            key_vault_properties:
                description:
                    - Properties provided by key vault.
                suboptions:
                    key_name:
                        description:
                            - The name of KeyVault key.
                    key_version:
                        description:
                            - The version of KeyVault key.
                    key_vault_uri:
                        description:
                            - The Uri of KeyVault.
    network_rule_set:
        description:
            - Network rule set
        suboptions:
            bypass:
                description:
                    - "Specifies whether traffic is bypassed for C(logging)/C(metrics)/C(azure_services). Possible values are any combination of
                       C(logging)|C(metrics)|C(azure_services) (For example, 'C(logging), C(metrics)'), or C(none) to bypass C(none) of those traffics."
                choices:
                    - 'none'
                    - 'logging'
                    - 'metrics'
                    - 'azure_services'
            virtual_network_rules:
                description:
                    - Sets the virtual network rules
                type: list
                suboptions:
                    virtual_network_resource_id:
                        description:
                            - "Resource ID of a subnet, for example:
                               /subscriptions/{subscriptionId}/resourceGroups/{groupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{su
                              bnetName}."
                        required: True
                    action:
                        description:
                            - The action of virtual network rule.
                        choices:
                            - 'allow'
                    state:
                        description:
                            - Gets the state of virtual network rule.
                        choices:
                            - 'provisioning'
                            - 'deprovisioning'
                            - 'succeeded'
                            - 'failed'
                            - 'network_source_deleted'
            ip_rules:
                description:
                    - Sets the IP ACL rules
                type: list
                suboptions:
                    ip_address_or_range:
                        description:
                            - Specifies the IP or IP range in CIDR format. Only IPV4 address is allowed.
                        required: True
                    action:
                        description:
                            - The action of IP ACL rule.
                        choices:
                            - 'allow'
            default_action:
                description:
                    - Specifies the default action of C(allow) or C(deny) when no other rules match.
                required: True
                choices:
                    - 'allow'
                    - 'deny'
    access_tier:
        description:
            - Required for C(storage) accounts where I(kind) = C(blob_storage). The access tier used for billing.
        choices:
            - 'hot'
            - 'cool'
    enable_azure_files_aad_integration:
        description:
            - Enables Azure Files AAD Integration for SMB if sets to true.
    enable_https_traffic_only:
        description:
            - Allows https traffic only to C(storage) service if sets to true.
    is_hns_enabled:
        description:
            - Account HierarchicalNamespace enabled if sets to true.
    state:
      description:
        - Assert the state of the Storage Account.
        - Use 'present' to create or update an Storage Account and 'absent' to delete it.
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
  - name: Create (or update) Storage Account
    azure_rm_storageaccount:
      resource_group: res9101
      account_name: sto4445
      sku:
        name: Standard_GRS
      kind: Storage
      location: eastus
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/{subscription-id}/resourceGroups/res9407/providers/Microsoft.Storage/storageAccounts/sto8596
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storage import StorageManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMStorageAccounts(AzureRMModuleBase):
    """Configuration class for an Azure RM Storage Account resource"""

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
            sku=dict(
                type='dict',
                required=True
            ),
            kind=dict(
                type='str',
                choices=['storage',
                         'storage_v2',
                         'blob_storage',
                         'file_storage',
                         'block_blob_storage'],
                required=True
            ),
            location=dict(
                type='str'
            ),
            identity=dict(
                type='dict'
            ),
            custom_domain=dict(
                type='dict'
            ),
            encryption=dict(
                type='dict'
            ),
            network_rule_set=dict(
                type='dict'
            ),
            access_tier=dict(
                type='str',
                choices=['hot',
                         'cool']
            ),
            enable_azure_files_aad_integration=dict(
                type='str'
            ),
            enable_https_traffic_only=dict(
                type='str'
            ),
            is_hns_enabled=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStorageAccounts, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'standard_lrs':
                            ev['name'] = 'Standard_LRS'
                        elif ev['name'] == 'standard_grs':
                            ev['name'] = 'Standard_GRS'
                        elif ev['name'] == 'standard_ragrs':
                            ev['name'] = 'Standard_RAGRS'
                        elif ev['name'] == 'standard_zrs':
                            ev['name'] = 'Standard_ZRS'
                        elif ev['name'] == 'premium_lrs':
                            ev['name'] = 'Premium_LRS'
                        elif ev['name'] == 'premium_zrs':
                            ev['name'] = 'Premium_ZRS'
                    self.parameters["sku"] = ev
                elif key == "kind":
                    self.parameters["kind"] = _snake_to_camel(kwargs[key], True)
                elif key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "identity":
                    self.parameters["identity"] = kwargs[key]
                elif key == "custom_domain":
                    self.parameters["custom_domain"] = kwargs[key]
                elif key == "encryption":
                    ev = kwargs[key]
                    if 'key_source' in ev:
                        if ev['key_source'] == 'microsoft._storage':
                            ev['key_source'] = 'Microsoft.Storage'
                        elif ev['key_source'] == 'microsoft._keyvault':
                            ev['key_source'] = 'Microsoft.Keyvault'
                    self.parameters["encryption"] = ev
                elif key == "network_rule_set":
                    ev = kwargs[key]
                    if 'bypass' in ev:
                        if ev['bypass'] == 'none':
                            ev['bypass'] = 'None'
                        elif ev['bypass'] == 'logging':
                            ev['bypass'] = 'Logging'
                        elif ev['bypass'] == 'metrics':
                            ev['bypass'] = 'Metrics'
                        elif ev['bypass'] == 'azure_services':
                            ev['bypass'] = 'AzureServices'
                    if 'default_action' in ev:
                        if ev['default_action'] == 'allow':
                            ev['default_action'] = 'Allow'
                        elif ev['default_action'] == 'deny':
                            ev['default_action'] = 'Deny'
                    self.parameters["network_rule_set"] = ev
                elif key == "access_tier":
                    self.parameters["access_tier"] = _snake_to_camel(kwargs[key], True)
                elif key == "enable_azure_files_aad_integration":
                    self.parameters["enable_azure_files_aad_integration"] = kwargs[key]
                elif key == "enable_https_traffic_only":
                    self.parameters["enable_https_traffic_only"] = kwargs[key]
                elif key == "is_hns_enabled":
                    self.parameters["is_hns_enabled"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_storageaccount()

        if not old_response:
            self.log("Storage Account instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Storage Account instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Storage Account instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Storage Account instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_storageaccount()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Storage Account instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_storageaccount()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_storageaccount():
                time.sleep(20)
        else:
            self.log("Storage Account instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_storageaccount(self):
        '''
        Creates or updates Storage Account with the specified configuration.

        :return: deserialized Storage Account instance state dictionary
        '''
        self.log("Creating / Updating the Storage Account instance {0}".format(self.account_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.storage_accounts.create(resource_group_name=self.resource_group,
                                                                    account_name=self.account_name,
                                                                    parameters=self.parameters)
            else:
                response = self.mgmt_client.storage_accounts.update(resource_group_name=self.resource_group,
                                                                    account_name=self.account_name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Storage Account instance.')
            self.fail("Error creating the Storage Account instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_storageaccount(self):
        '''
        Deletes specified Storage Account instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Storage Account instance {0}".format(self.account_name))
        try:
            response = self.mgmt_client.storage_accounts.delete(resource_group_name=self.resource_group,
                                                                account_name=self.account_name)
        except CloudError as e:
            self.log('Error attempting to delete the Storage Account instance.')
            self.fail("Error deleting the Storage Account instance: {0}".format(str(e)))

        return True

    def get_storageaccount(self):
        '''
        Gets the properties of the specified Storage Account.

        :return: deserialized Storage Account instance state dictionary
        '''
        self.log("Checking if the Storage Account instance {0} is present".format(self.account_name))
        found = False
        try:
            response = self.mgmt_client.storage_accounts.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Storage Account instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Storage Account instance.')
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
    AzureRMStorageAccounts()


if __name__ == '__main__':
    main()

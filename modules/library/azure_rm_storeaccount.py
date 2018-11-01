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
module: azure_rm_storeaccount
version_added: "2.8"
short_description: Manage Account instance.
description:
    - Create, update and delete instance of Account.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
        required: True
    account_name:
        description:
            - The name of the Data Lake Store account.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    identity:
        description:
            - The Key Vault encryption identity, if any.
        suboptions:
            type:
                description:
                    - "The type of encryption being used. Currently the only supported type is 'SystemAssigned'."
                required: True
    default_group:
        description:
            - The default owner group for all new folders and files created in the Data Lake Store account.
    encryption_config:
        description:
            - The Key Vault encryption configuration.
        suboptions:
            type:
                description:
                    - "The type of encryption configuration being used. Currently the only supported types are 'C(user_managed)' and 'C(service_managed)'."
                required: True
                choices:
                    - 'user_managed'
                    - 'service_managed'
            key_vault_meta_info:
                description:
                    - The Key Vault information for connecting to user managed encryption keys.
                suboptions:
                    key_vault_resource_id:
                        description:
                            - The resource identifier for the user managed Key Vault being used to encrypt.
                        required: True
                    encryption_key_name:
                        description:
                            - The name of the user managed encryption key.
                        required: True
                    encryption_key_version:
                        description:
                            - The version of the user managed encryption key.
                        required: True
    encryption_state:
        description:
            - The current state of encryption for this Data Lake Store account.
        choices:
            - 'enabled'
            - 'disabled'
    firewall_rules:
        description:
            - The list of firewall rules associated with this Data Lake Store account.
        type: list
        suboptions:
            name:
                description:
                    - The unique name of the firewall rule to create.
                required: True
            start_ip_address:
                description:
                    - The start IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
                required: True
            end_ip_address:
                description:
                    - The end IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
                required: True
    virtual_network_rules:
        description:
            - The list of virtual network rules associated with this Data Lake Store account.
        type: list
        suboptions:
            name:
                description:
                    - The unique name of the virtual network rule to create.
                required: True
            subnet_id:
                description:
                    - The resource identifier for the subnet.
                required: True
    firewall_state:
        description:
            - The current state of the IP address firewall for this Data Lake Store account.
        choices:
            - 'enabled'
            - 'disabled'
    firewall_allow_azure_ips:
        description:
            - "The current state of allowing or disallowing IPs originating within Azure through the firewall. If the firewall is C(C(C(C(disabled)))), this
               is not enforced."
        choices:
            - 'enabled'
            - 'disabled'
    trusted_id_providers:
        description:
            - The list of trusted I(identity) providers associated with this Data Lake Store account.
        type: list
        suboptions:
            name:
                description:
                    - The unique name of the trusted identity provider to create.
                required: True
            id_provider:
                description:
                    - The URL of this trusted identity provider.
                required: True
    trusted_id_provider_state:
        description:
            - The current state of the trusted I(identity) provider feature for this Data Lake Store account.
        choices:
            - 'enabled'
            - 'disabled'
    new_tier:
        description:
            - The commitment tier to use for next month.
        choices:
            - 'consumption'
            - 'commitment_1_tb'
            - 'commitment_10_tb'
            - 'commitment_100_tb'
            - 'commitment_500_tb'
            - 'commitment_1_pb'
            - 'commitment_5_pb'
    state:
      description:
        - Assert the state of the Account.
        - Use 'present' to create or update an Account and 'absent' to delete it.
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
  - name: Create (or update) Account
    azure_rm_storeaccount:
      resource_group: contosorg
      account_name: contosoadla
      location: eastus
      identity:
        type: SystemAssigned
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: 34adfa4f-cedf-4dc0-ba29-b6d1a69ab345
state:
    description:
        - "The state of the Data Lake Store account. Possible values include: 'Active', 'Suspended'"
    returned: always
    type: str
    sample: Active
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.store import DataLakeStoreAccountManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAccounts(AzureRMModuleBase):
    """Configuration class for an Azure RM Account resource"""

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
            location=dict(
                type='str'
            ),
            identity=dict(
                type='dict'
            ),
            default_group=dict(
                type='str'
            ),
            encryption_config=dict(
                type='dict'
            ),
            encryption_state=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            firewall_rules=dict(
                type='list'
            ),
            virtual_network_rules=dict(
                type='list'
            ),
            firewall_state=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            firewall_allow_azure_ips=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            trusted_id_providers=dict(
                type='list'
            ),
            trusted_id_provider_state=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            new_tier=dict(
                type='str',
                choices=['consumption',
                         'commitment_1_tb',
                         'commitment_10_tb',
                         'commitment_100_tb',
                         'commitment_500_tb',
                         'commitment_1_pb',
                         'commitment_5_pb']
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

        super(AzureRMAccounts, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "identity":
                    self.parameters["identity"] = kwargs[key]
                elif key == "default_group":
                    self.parameters["default_group"] = kwargs[key]
                elif key == "encryption_config":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'user_managed':
                            ev['type'] = 'UserManaged'
                        elif ev['type'] == 'service_managed':
                            ev['type'] = 'ServiceManaged'
                    self.parameters["encryption_config"] = ev
                elif key == "encryption_state":
                    self.parameters["encryption_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "firewall_rules":
                    self.parameters["firewall_rules"] = kwargs[key]
                elif key == "virtual_network_rules":
                    self.parameters["virtual_network_rules"] = kwargs[key]
                elif key == "firewall_state":
                    self.parameters["firewall_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "firewall_allow_azure_ips":
                    self.parameters["firewall_allow_azure_ips"] = _snake_to_camel(kwargs[key], True)
                elif key == "trusted_id_providers":
                    self.parameters["trusted_id_providers"] = kwargs[key]
                elif key == "trusted_id_provider_state":
                    self.parameters["trusted_id_provider_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "new_tier":
                    ev = kwargs[key]
                    if ev == 'commitment_1_tb':
                        ev = 'Commitment_1TB'
                    elif ev == 'commitment_10_tb':
                        ev = 'Commitment_10TB'
                    elif ev == 'commitment_100_tb':
                        ev = 'Commitment_100TB'
                    elif ev == 'commitment_500_tb':
                        ev = 'Commitment_500TB'
                    elif ev == 'commitment_1_pb':
                        ev = 'Commitment_1PB'
                    elif ev == 'commitment_5_pb':
                        ev = 'Commitment_5PB'
                    self.parameters["new_tier"] = _snake_to_camel(ev, True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataLakeStoreAccountManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_account()

        if not old_response:
            self.log("Account instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Account instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Account instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Account instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_account()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Account instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_account()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_account():
                time.sleep(20)
        else:
            self.log("Account instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_account(self):
        '''
        Creates or updates Account with the specified configuration.

        :return: deserialized Account instance state dictionary
        '''
        self.log("Creating / Updating the Account instance {0}".format(self.account_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.accounts.create(resource_group_name=self.resource_group,
                                                            account_name=self.account_name,
                                                            parameters=self.parameters)
            else:
                response = self.mgmt_client.accounts.update(resource_group_name=self.resource_group,
                                                            account_name=self.account_name,
                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Account instance.')
            self.fail("Error creating the Account instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_account(self):
        '''
        Deletes specified Account instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Account instance {0}".format(self.account_name))
        try:
            response = self.mgmt_client.accounts.delete(resource_group_name=self.resource_group,
                                                        account_name=self.account_name)
        except CloudError as e:
            self.log('Error attempting to delete the Account instance.')
            self.fail("Error deleting the Account instance: {0}".format(str(e)))

        return True

    def get_account(self):
        '''
        Gets the properties of the specified Account.

        :return: deserialized Account instance state dictionary
        '''
        self.log("Checking if the Account instance {0} is present".format(self.account_name))
        found = False
        try:
            response = self.mgmt_client.accounts.get(resource_group_name=self.resource_group,
                                                     account_name=self.account_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Account instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Account instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMAccounts()


if __name__ == '__main__':
    main()

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
short_description: Manage Azure Account instance.
description:
    - Create, update and delete instance of Azure Account.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
        required: True
    name:
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
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
                    encryption_key_name:
                        description:
                            - The name of the user managed encryption key.
                            - Required when C(state) is I(present).
                    encryption_key_version:
                        description:
                            - The version of the user managed encryption key.
                            - Required when C(state) is I(present).
    encryption_state:
        description:
            - "The current state of encryption for this Data Lake Store account. Possible values include: 'Enabled', 'Disabled'"
        type: bool
    firewall_rules:
        description:
            - The list of firewall rules associated with this Data Lake Store account.
        type: list
        suboptions:
            name:
                description:
                    - The unique name of the firewall rule to create.
                    - Required when C(state) is I(present).
            start_ip_address:
                description:
                    - The start IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
                    - Required when C(state) is I(present).
            end_ip_address:
                description:
                    - The end IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
                    - Required when C(state) is I(present).
    virtual_network_rules:
        description:
            - The list of virtual network rules associated with this Data Lake Store account.
        type: list
        suboptions:
            name:
                description:
                    - The unique name of the virtual network rule to create.
                    - Required when C(state) is I(present).
            subnet_id:
                description:
                    - The resource identifier for the subnet.
                    - Required when C(state) is I(present).
    firewall_state:
        description:
            - "The current state of the IP address firewall for this Data Lake Store account. Possible values include: 'Enabled', 'Disabled'"
        type: bool
    firewall_allow_azure_ips:
        description:
            - "The current state of allowing or disallowing IPs originating within Azure through the firewall. If the firewall is disabled, this is not
               enforced. Possible values include: 'Enabled', 'Disabled'"
        type: bool
    trusted_id_providers:
        description:
            - The list of trusted I(identity) providers associated with this Data Lake Store account.
        type: list
        suboptions:
            name:
                description:
                    - The unique name of the trusted identity provider to create.
                    - Required when C(state) is I(present).
            id_provider:
                description:
                    - The URL of this trusted identity provider.
                    - Required when C(state) is I(present).
    trusted_id_provider_state:
        description:
            - "The current state of the trusted I(identity) provider feature for this Data Lake Store account. Possible values include: 'Enabled',
               'Disabled'"
        type: bool
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
      name: contosoadla
      location: eastus
      identity:
        type: SystemAssigned
      default_group: test_default_group
      encryption_config:
        type: UserManaged
        key_vault_meta_info:
          key_vault_resource_id: 34adfa4f-cedf-4dc0-ba29-b6d1a69ab345
          encryption_key_name: test_encryption_key_name
          encryption_key_version: encryption_key_version
      encryption_state: encryption_state
      firewall_rules:
        - name: test_rule
          start_ip_address: 1.1.1.1
          end_ip_address: 2.2.2.2
      firewall_state: firewall_state
      firewall_allow_azure_ips: firewall_allow_azure_ips
      trusted_id_providers:
        - name: test_trusted_id_provider_name
          id_provider: https://sts.windows.net/ea9ec534-a3e3-4e45-ad36-3afc5bb291c1
      trusted_id_provider_state: trusted_id_provider_state
      new_tier: Consumption
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMAccount(AzureRMModuleBase):
    """Configuration class for an Azure RM Account resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            identity=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str'
                    )
                )
            ),
            default_group=dict(
                type='str'
            ),
            encryption_config=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str',
                        choices=['user_managed',
                                 'service_managed']
                    ),
                    key_vault_meta_info=dict(
                        type='dict',
                        options=dict(
                            key_vault_resource_id=dict(
                                type='str'
                            ),
                            encryption_key_name=dict(
                                type='str'
                            ),
                            encryption_key_version=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            encryption_state=dict(
                type='bool'
            ),
            firewall_rules=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    start_ip_address=dict(
                        type='str'
                    ),
                    end_ip_address=dict(
                        type='str'
                    )
                )
            ),
            virtual_network_rules=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    subnet_id=dict(
                        type='str'
                    )
                )
            ),
            firewall_state=dict(
                type='bool'
            ),
            firewall_allow_azure_ips=dict(
                type='bool'
            ),
            trusted_id_providers=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    id_provider=dict(
                        type='str'
                    )
                )
            ),
            trusted_id_provider_state=dict(
                type='bool'
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAccount, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['encryption_config', 'type'], True)
        dict_map(self.parameters, ['encryption_state'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.parameters, ['firewall_state'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.parameters, ['firewall_allow_azure_ips'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.parameters, ['trusted_id_provider_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.parameters, ['new_tier'], True)
        dict_map(self.parameters, ['new_tier'], {'commitment_1_tb': 'Commitment_1TB', 'commitment_10_tb': 'Commitment_10TB', 'commitment_100_tb': 'Commitment_100TB', 'commitment_500_tb': 'Commitment_500TB', 'commitment_1_pb': 'Commitment_1PB', 'commitment_5_pb': 'Commitment_5PB'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Account instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_account()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Account instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_account()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Account instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None)
                })
        return self.results

    def create_update_account(self):
        '''
        Creates or updates Account with the specified configuration.

        :return: deserialized Account instance state dictionary
        '''
        self.log("Creating / Updating the Account instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.accounts.create(resource_group_name=self.resource_group,
                                                            account_name=self.name,
                                                            parameters=self.parameters)
            else:
                response = self.mgmt_client.accounts.update(resource_group_name=self.resource_group,
                                                            account_name=self.name,
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
        self.log("Deleting the Account instance {0}".format(self.name))
        try:
            response = self.mgmt_client.accounts.delete(resource_group_name=self.resource_group,
                                                        account_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Account instance.')
            self.fail("Error deleting the Account instance: {0}".format(str(e)))

        return True

    def get_account(self):
        '''
        Gets the properties of the specified Account.

        :return: deserialized Account instance state dictionary
        '''
        self.log("Checking if the Account instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.accounts.get(resource_group_name=self.resource_group,
                                                     account_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Account instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Account instance.')
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def main():
    """Main execution"""
    AzureRMAccount()


if __name__ == '__main__':
    main()

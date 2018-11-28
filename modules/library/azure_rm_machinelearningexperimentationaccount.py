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
module: azure_rm_machinelearningexperimentationaccount
version_added: "2.8"
short_description: Manage Azure Account instance.
description:
    - Create, update and delete instance of Azure Account.

options:
    resource_group:
        description:
            - The name of the resource group to which the machine learning team account belongs.
        required: True
    name:
        description:
            - The name of the machine learning team account.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    vso_account_id:
        description:
            - The fully qualified arm id of the vso account to be used for this team account.
            - Required when C(state) is I(present).
    description:
        description:
            - The description of this workspace.
    friendly_name:
        description:
            - The friendly name for this workspace. This will be the workspace name in the arm id when the workspace object gets created
    key_vault_id:
        description:
            - The fully qualified arm id of the user key vault.
            - Required when C(state) is I(present).
    seats:
        description:
            - The no of users/seats who can access this team account. This property defines the charge on the team account.
    storage_account:
        description:
            - The properties of the storage account for the machine learning team account.
            - Required when C(state) is I(present).
        suboptions:
            storage_account_id:
                description:
                    - The fully qualified arm Id of the storage account.
                    - Required when C(state) is I(present).
            access_key:
                description:
                    - The access key to the storage account.
                    - Required when C(state) is I(present).
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
    azure_rm_machinelearningexperimentationaccount:
      resource_group: accountcrud-1234
      name: accountcrud5678
      location: eastus
      vso_account_id: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/accountcrud-1234/providers/microsoft.visualstudio/account/vsotest
      key_vault_id: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/accountcrud-1234/providers/Microsoft.KeyVault/vaults/testkv
      storage_account:
        storage_account_id: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/accountcrud-1234/providers/Microsoft.Storage/storageAccounts/testStorageAccount
        access_key: key
'''

RETURN = '''
id:
    description:
        - The resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/accountcrud-1234/providers/Microsoft.MachineLearningExperimentation/accounts/
            accountcrud5678"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.machinelearningexperimentation import MLTeamAccountManagementClient
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
            vso_account_id=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            friendly_name=dict(
                type='str'
            ),
            key_vault_id=dict(
                type='str'
            ),
            seats=dict(
                type='str'
            ),
            storage_account=dict(
                type='dict',
                options=dict(
                    storage_account_id=dict(
                        type='str'
                    ),
                    access_key=dict(
                        type='str'
                    )
                )
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


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MLTeamAccountManagementClient,
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
                'id': response.get('id', None)
                })
        return self.results

    def create_update_account(self):
        '''
        Creates or updates Account with the specified configuration.

        :return: deserialized Account instance state dictionary
        '''
        self.log("Creating / Updating the Account instance {0}".format(self.name))

        try:
            response = self.mgmt_client.accounts.create_or_update(resource_group_name=self.resource_group,
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


def main():
    """Main execution"""
    AzureRMAccount()


if __name__ == '__main__':
    main()

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
module: azure_rm_storagemanagementpolicy
version_added: "2.8"
short_description: Manage Management Policy instance.
description:
    - Create, update and delete instance of Management Policy.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    account_name:
        description:
            - "The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and
               use numbers and lower-case letters only."
        required: True
    management_policy_name:
        description:
            - "The name of the Storage Account Management I(policy). It should always be 'default'"
        required: True
    policy:
        description:
            - "The Storage Account ManagementPolicies Rules, in JSON format. See more details in:
               https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts."
    state:
      description:
        - Assert the state of the Management Policy.
        - Use 'present' to create or update an Management Policy and 'absent' to delete it.
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
  - name: Create (or update) Management Policy
    azure_rm_storagemanagementpolicy:
      resource_group: res7687
      account_name: sto9699
      management_policy_name: default
      policy: NOT FOUND
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/{subscription-id}/resourceGroups/res7231/providers/Microsoft.Storage/storageAccounts/sto288/managementPolicies/default
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


class AzureRMManagementPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Management Policy resource"""

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
            management_policy_name=dict(
                type='str',
                required=True
            ),
            policy=dict(
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
        self.management_policy_name = None
        self.policy = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagementPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_managementpolicy()

        if not old_response:
            self.log("Management Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Management Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Management Policy instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Management Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managementpolicy()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Management Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managementpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_managementpolicy():
                time.sleep(20)
        else:
            self.log("Management Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_managementpolicy(self):
        '''
        Creates or updates Management Policy with the specified configuration.

        :return: deserialized Management Policy instance state dictionary
        '''
        self.log("Creating / Updating the Management Policy instance {0}".format(self.management_policy_name))

        try:
            response = self.mgmt_client.management_policies.create_or_update(resource_group_name=self.resource_group,
                                                                             account_name=self.account_name,
                                                                             management_policy_name=self.management_policy_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Management Policy instance.')
            self.fail("Error creating the Management Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_managementpolicy(self):
        '''
        Deletes specified Management Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Management Policy instance {0}".format(self.management_policy_name))
        try:
            response = self.mgmt_client.management_policies.delete(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   management_policy_name=self.management_policy_name)
        except CloudError as e:
            self.log('Error attempting to delete the Management Policy instance.')
            self.fail("Error deleting the Management Policy instance: {0}".format(str(e)))

        return True

    def get_managementpolicy(self):
        '''
        Gets the properties of the specified Management Policy.

        :return: deserialized Management Policy instance state dictionary
        '''
        self.log("Checking if the Management Policy instance {0} is present".format(self.management_policy_name))
        found = False
        try:
            response = self.mgmt_client.management_policies.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                management_policy_name=self.management_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Management Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Management Policy instance.')
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
    AzureRMManagementPolicies()


if __name__ == '__main__':
    main()

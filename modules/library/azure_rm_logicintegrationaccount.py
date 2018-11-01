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
module: azure_rm_logicintegrationaccount
version_added: "2.8"
short_description: Manage Integration Account instance.
description:
    - Create, update and delete instance of Integration Account.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    integration_account:
        description:
            - The integration account.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            sku:
                description:
                    - The sku.
                suboptions:
                    name:
                        description:
                            - The sku name.
                        required: True
                        choices:
                            - 'not_specified'
                            - 'free'
                            - 'basic'
                            - 'standard'
    state:
      description:
        - Assert the state of the Integration Account.
        - Use 'present' to create or update an Integration Account and 'absent' to delete it.
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
  - name: Create (or update) Integration Account
    azure_rm_logicintegrationaccount:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      integration_account:
        location: westus
        sku:
          name: Standard
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/testIntegrati
            onAccount"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIntegrationAccounts(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            integration_account_name=dict(
                type='str',
                required=True
            ),
            integration_account=dict(
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
        self.integration_account_name = None
        self.integration_account = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccounts, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.integration_account["location"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'not_specified':
                            ev['name'] = 'NotSpecified'
                        elif ev['name'] == 'free':
                            ev['name'] = 'Free'
                        elif ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                    self.integration_account["sku"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccount()

        if not old_response:
            self.log("Integration Account instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Integration Account instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccount()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccount()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccount():
                time.sleep(20)
        else:
            self.log("Integration Account instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccount(self):
        '''
        Creates or updates Integration Account with the specified configuration.

        :return: deserialized Integration Account instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account instance {0}".format(self.integration_account_name))

        try:
            response = self.mgmt_client.integration_accounts.create_or_update(resource_group_name=self.resource_group,
                                                                              integration_account_name=self.integration_account_name,
                                                                              integration_account=self.integration_account)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account instance.')
            self.fail("Error creating the Integration Account instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccount(self):
        '''
        Deletes specified Integration Account instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account instance {0}".format(self.integration_account_name))
        try:
            response = self.mgmt_client.integration_accounts.delete(resource_group_name=self.resource_group,
                                                                    integration_account_name=self.integration_account_name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account instance.')
            self.fail("Error deleting the Integration Account instance: {0}".format(str(e)))

        return True

    def get_integrationaccount(self):
        '''
        Gets the properties of the specified Integration Account.

        :return: deserialized Integration Account instance state dictionary
        '''
        self.log("Checking if the Integration Account instance {0} is present".format(self.integration_account_name))
        found = False
        try:
            response = self.mgmt_client.integration_accounts.get(resource_group_name=self.resource_group,
                                                                 integration_account_name=self.integration_account_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account instance.')
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
    AzureRMIntegrationAccounts()


if __name__ == '__main__':
    main()
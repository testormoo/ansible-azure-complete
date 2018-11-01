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
module: azure_rm_csmaccount
version_added: "2.8"
short_description: Manage Account instance.
description:
    - Create, update and delete instance of Account.

options:
    resource_group:
        description:
            - Name of the resource group within the Azure subscription.
        required: True
    body:
        description:
            - The request data.
        required: True
        suboptions:
            account_name:
                description:
                    - The account name.
            location:
                description:
                    - The Azure instance location.
            operation_type:
                description:
                    - The type of the operation.
    resource_name:
        description:
            - Name of the resource.
        required: True
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
    azure_rm_csmaccount:
      resource_group: VS-Example-Group
      body:
        account_name: Example
        location: Central US
        operation_type: create
      resource_name: Example
'''

RETURN = '''
id:
    description:
        - Unique identifier of the resource.
    returned: always
    type: str
    sample: /subscriptions/0de7f055-dbea-498d-8e9e-da287eedca90/resourceGroups/VS-Example-Group/providers/Microsoft.VisualStudio/account/Example
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.csm import VisualStudioResourceProviderClient
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
            body=dict(
                type='dict',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.body = dict()
        self.resource_name = None

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
                if key == "account_name":
                    self.body["account_name"] = kwargs[key]
                elif key == "location":
                    self.body["location"] = kwargs[key]
                elif key == "operation_type":
                    self.body["operation_type"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(VisualStudioResourceProviderClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

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
        self.log("Creating / Updating the Account instance {0}".format(self.resource_name))

        try:
            response = self.mgmt_client.accounts.create_or_update(resource_group_name=self.resource_group,
                                                                  body=self.body,
                                                                  resource_name=self.resource_name)
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
        self.log("Deleting the Account instance {0}".format(self.resource_name))
        try:
            response = self.mgmt_client.accounts.delete(resource_group_name=self.resource_group,
                                                        resource_name=self.resource_name)
        except CloudError as e:
            self.log('Error attempting to delete the Account instance.')
            self.fail("Error deleting the Account instance: {0}".format(str(e)))

        return True

    def get_account(self):
        '''
        Gets the properties of the specified Account.

        :return: deserialized Account instance state dictionary
        '''
        self.log("Checking if the Account instance {0} is present".format(self.resource_name))
        found = False
        try:
            response = self.mgmt_client.accounts.get(resource_group_name=self.resource_group,
                                                     resource_name=self.resource_name)
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
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMAccounts()


if __name__ == '__main__':
    main()

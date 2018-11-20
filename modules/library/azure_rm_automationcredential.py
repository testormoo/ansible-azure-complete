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
module: azure_rm_automationcredential
version_added: "2.8"
short_description: Manage Credential instance.
description:
    - Create, update and delete instance of Credential.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    name:
        description:
            - The parameters supplied to the create or update credential operation.
        required: True
    name:
        description:
            - Gets or sets the name of the credential.
            - Required when C(state) is I(present).
    user_name:
        description:
            - Gets or sets the user name of the credential.
            - Required when C(state) is I(present).
    password:
        description:
            - Gets or sets the password of the credential.
            - Required when C(state) is I(present).
    description:
        description:
            - Gets or sets the description of the credential.
    state:
      description:
        - Assert the state of the Credential.
        - Use 'present' to create or update an Credential and 'absent' to delete it.
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
  - name: Create (or update) Credential
    azure_rm_automationcredential:
      resource_group: rg
      automation_account_name: myAutomationAccount18
      name: myCredential
      name: myCredential
      user_name: mylingaiah
      password: myPassw0rd
      description: my description goes here
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount18/credentials/myCredential
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMCredential(AzureRMModuleBase):
    """Configuration class for an Azure RM Credential resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            user_name=dict(
                type='str'
            ),
            password=dict(
                type='str',
                no_log=True
            ),
            description=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCredential, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "user_name":
                    self.parameters["user_name"] = kwargs[key]
                elif key == "password":
                    self.parameters["password"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_credential()

        if not old_response:
            self.log("Credential instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Credential instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Credential instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_credential()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Credential instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_credential()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_credential():
                time.sleep(20)
        else:
            self.log("Credential instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_credential(self):
        '''
        Creates or updates Credential with the specified configuration.

        :return: deserialized Credential instance state dictionary
        '''
        self.log("Creating / Updating the Credential instance {0}".format(self.name))

        try:
            response = self.mgmt_client.credential.create_or_update(resource_group_name=self.resource_group,
                                                                    automation_account_name=self.automation_account_name,
                                                                    credential_name=self.name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Credential instance.')
            self.fail("Error creating the Credential instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_credential(self):
        '''
        Deletes specified Credential instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Credential instance {0}".format(self.name))
        try:
            response = self.mgmt_client.credential.delete(resource_group_name=self.resource_group,
                                                          automation_account_name=self.automation_account_name,
                                                          credential_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Credential instance.')
            self.fail("Error deleting the Credential instance: {0}".format(str(e)))

        return True

    def get_credential(self):
        '''
        Gets the properties of the specified Credential.

        :return: deserialized Credential instance state dictionary
        '''
        self.log("Checking if the Credential instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.credential.get(resource_group_name=self.resource_group,
                                                       automation_account_name=self.automation_account_name,
                                                       credential_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Credential instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Credential instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def main():
    """Main execution"""
    AzureRMCredential()


if __name__ == '__main__':
    main()

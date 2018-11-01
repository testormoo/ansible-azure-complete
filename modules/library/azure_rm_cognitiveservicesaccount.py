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
module: azure_rm_cognitiveservicesaccount
version_added: "2.8"
short_description: Manage Account instance.
description:
    - Create, update and delete instance of Account.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription."
        required: True
    account_name:
        description:
            - The name of Cognitive Services account.
        required: True
    sku:
        description:
            - Required. Gets or sets the SKU of the resource.
        required: True
        suboptions:
            name:
                description:
                    - Gets or sets the sku name. Required for account creation, optional for update.
                required: True
                choices:
                    - 'f0'
                    - 'p0'
                    - 'p1'
                    - 'p2'
                    - 's0'
                    - 's1'
                    - 's2'
                    - 's3'
                    - 's4'
                    - 's5'
                    - 's6'
    kind:
        description:
            - Required. Gets or sets the Kind of the resource.
        required: True
        choices:
            - 'bing._autosuggest.v7'
            - 'bing._custom_search'
            - 'bing._search.v7'
            - 'bing._speech'
            - 'bing._spell_check.v7'
            - 'computer_vision'
            - 'content_moderator'
            - 'custom_speech'
            - 'custom_vision._prediction'
            - 'custom_vision._training'
            - 'emotion'
            - 'face'
            - 'luis'
            - 'qn_amaker'
            - 'speaker_recognition'
            - 'speech_translation'
            - 'text_analytics'
            - 'text_translation'
            - 'web_lm'
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
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
    azure_rm_cognitiveservicesaccount:
      resource_group: felixwa-01
      account_name: testCreate1
      sku:
        name: S0
      kind: Emotion
      location: eastus
'''

RETURN = '''
id:
    description:
        - The id of the created account
    returned: always
    type: str
    sample: /subscriptions/f9b96b36-1f5e-4021-8959-51527e26e6d3/resourceGroups/bvttest/providers/Microsoft.CognitiveServices/accounts/bingSearch
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
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
            sku=dict(
                type='dict',
                required=True
            ),
            kind=dict(
                type='str',
                choices=['bing._autosuggest.v7',
                         'bing._custom_search',
                         'bing._search.v7',
                         'bing._speech',
                         'bing._spell_check.v7',
                         'computer_vision',
                         'content_moderator',
                         'custom_speech',
                         'custom_vision._prediction',
                         'custom_vision._training',
                         'emotion',
                         'face',
                         'luis',
                         'qn_amaker',
                         'speaker_recognition',
                         'speech_translation',
                         'text_analytics',
                         'text_translation',
                         'web_lm'],
                required=True
            ),
            location=dict(
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

        super(AzureRMAccounts, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                        if ev['name'] == 'f0':
                            ev['name'] = 'F0'
                        elif ev['name'] == 'p0':
                            ev['name'] = 'P0'
                        elif ev['name'] == 'p1':
                            ev['name'] = 'P1'
                        elif ev['name'] == 'p2':
                            ev['name'] = 'P2'
                        elif ev['name'] == 's0':
                            ev['name'] = 'S0'
                        elif ev['name'] == 's1':
                            ev['name'] = 'S1'
                        elif ev['name'] == 's2':
                            ev['name'] = 'S2'
                        elif ev['name'] == 's3':
                            ev['name'] = 'S3'
                        elif ev['name'] == 's4':
                            ev['name'] = 'S4'
                        elif ev['name'] == 's5':
                            ev['name'] = 'S5'
                        elif ev['name'] == 's6':
                            ev['name'] = 'S6'
                    self.parameters["sku"] = ev
                elif key == "kind":
                    ev = kwargs[key]
                    if ev == 'luis':
                        ev = 'LUIS'
                    elif ev == 'qn_amaker':
                        ev = 'QnAMaker'
                    elif ev == 'web_lm':
                        ev = 'WebLM'
                    self.parameters["kind"] = _snake_to_camel(ev, True)
                elif key == "location":
                    self.parameters["location"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CognitiveServicesManagementClient,
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
                                                            account_name=self.account_name)
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
            response = self.mgmt_client.accounts.get()
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

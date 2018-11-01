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
module: azure_rm_logicintegrationaccountpartner
version_added: "2.8"
short_description: Manage Integration Account Partner instance.
description:
    - Create, update and delete instance of Integration Account Partner.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    partner_name:
        description:
            - The integration account I(partner) name.
        required: True
    partner:
        description:
            - The integration account partner.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            partner_type:
                description:
                    - The partner type.
                required: True
                choices:
                    - 'not_specified'
                    - 'b2_b'
            metadata:
                description:
                    - The metadata.
            content:
                description:
                    - The partner content.
                required: True
                suboptions:
                    b2b:
                        description:
                            - The B2B partner content.
                        suboptions:
                            business_identities:
                                description:
                                    - The list of partner business identities.
                                type: list
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                        required: True
                                    value:
                                        description:
                                            - The user defined business identity value.
                                        required: True
    state:
      description:
        - Assert the state of the Integration Account Partner.
        - Use 'present' to create or update an Integration Account Partner and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Partner
    azure_rm_logicintegrationaccountpartner:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      partner_name: testPartner
      partner:
        location: westus
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/flowrg/providers/Microsoft.Logic/integrationAccounts/testIntegrationAccount/p
            artners/testPartner"
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


class AzureRMIntegrationAccountPartners(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Partner resource"""

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
            partner_name=dict(
                type='str',
                required=True
            ),
            partner=dict(
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
        self.partner_name = None
        self.partner = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountPartners, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                supports_check_mode=True,
                                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.partner["location"] = kwargs[key]
                elif key == "partner_type":
                    self.partner["partner_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "metadata":
                    self.partner["metadata"] = kwargs[key]
                elif key == "content":
                    self.partner["content"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountpartner()

        if not old_response:
            self.log("Integration Account Partner instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Partner instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Integration Account Partner instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Partner instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountpartner()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Partner instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountpartner()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccountpartner():
                time.sleep(20)
        else:
            self.log("Integration Account Partner instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccountpartner(self):
        '''
        Creates or updates Integration Account Partner with the specified configuration.

        :return: deserialized Integration Account Partner instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Partner instance {0}".format(self.partner_name))

        try:
            response = self.mgmt_client.integration_account_partners.create_or_update(resource_group_name=self.resource_group,
                                                                                      integration_account_name=self.integration_account_name,
                                                                                      partner_name=self.partner_name,
                                                                                      partner=self.partner)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Partner instance.')
            self.fail("Error creating the Integration Account Partner instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountpartner(self):
        '''
        Deletes specified Integration Account Partner instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Partner instance {0}".format(self.partner_name))
        try:
            response = self.mgmt_client.integration_account_partners.delete(resource_group_name=self.resource_group,
                                                                            integration_account_name=self.integration_account_name,
                                                                            partner_name=self.partner_name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Partner instance.')
            self.fail("Error deleting the Integration Account Partner instance: {0}".format(str(e)))

        return True

    def get_integrationaccountpartner(self):
        '''
        Gets the properties of the specified Integration Account Partner.

        :return: deserialized Integration Account Partner instance state dictionary
        '''
        self.log("Checking if the Integration Account Partner instance {0} is present".format(self.partner_name))
        found = False
        try:
            response = self.mgmt_client.integration_account_partners.get(resource_group_name=self.resource_group,
                                                                         integration_account_name=self.integration_account_name,
                                                                         partner_name=self.partner_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Partner instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Partner instance.')
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
    AzureRMIntegrationAccountPartners()


if __name__ == '__main__':
    main()

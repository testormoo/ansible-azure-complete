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
module: azure_rm_logicintegrationaccount_facts
version_added: "2.8"
short_description: Get Azure Integration Account facts.
description:
    - Get facts of Azure Integration Account.

options:
    resource_group:
        description:
            - The resource group name.
    top:
        description:
            - The number of items to be included in the result.
    name:
        description:
            - The integration account name.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Integration Account
    azure_rm_logicintegrationaccount_facts:
      resource_group: resource_group_name
      top: top

  - name: Get instance of Integration Account
    azure_rm_logicintegrationaccount_facts:
      resource_group: resource_group_name
      name: integration_account_name

  - name: List instances of Integration Account
    azure_rm_logicintegrationaccount_facts:
      top: top
'''

RETURN = '''
integration_accounts:
    description: A list of dictionaries containing facts for Integration Account.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/testI
                    ntegrationAccount"
        name:
            description:
                - Gets the resource name.
            returned: always
            type: str
            sample: IntegrationAccount5892
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: tags
        properties:
            description:
                - The integration account properties.
            returned: always
            type: str
            sample: {}
        sku:
            description:
                - The sku.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The sku name. Possible values include: 'NotSpecified', 'Free', 'Basic', 'Standard'"
                    returned: always
                    type: str
                    sample: Standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIntegrationAccountsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            name=dict(
                type='str'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.top = None
        self.name = None
        self.tags = None
        super(AzureRMIntegrationAccountsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None:
            self.results['integration_accounts'] = self.list_by_resource_group()
        elif (self.resource_group is not None and
                self.name is not None):
            self.results['integration_accounts'] = self.get()
        else:
            self.results['integration_accounts'] = self.list_by_subscription()
        return self.results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_accounts.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IntegrationAccounts.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_accounts.get(resource_group_name=self.resource_group,
                                                                 integration_account_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IntegrationAccounts.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_accounts.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IntegrationAccounts.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'properties': d.get('properties', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            }
        }
        return d


def main():
    AzureRMIntegrationAccountsFacts()


if __name__ == '__main__':
    main()

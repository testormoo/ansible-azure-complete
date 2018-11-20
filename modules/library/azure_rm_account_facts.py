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
module: azure_rm_account_facts
version_added: "2.8"
short_description: Get Azure Account facts.
description:
    - Get facts of Azure Account.

options:
    resource_group:
        description:
            - The name of the Azure Resource Group.
    name:
        description:
            - The name of the Maps Account.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Account
    azure_rm_account_facts:
      resource_group: resource_group_name
      name: account_name

  - name: List instances of Account
    azure_rm_account_facts:
      resource_group: resource_group_name

  - name: List instances of Account
    azure_rm_account_facts:
'''

RETURN = '''
accounts:
    description: A list of dictionaries containing facts for Account.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The fully qualified Maps Account resource identifier.
            returned: always
            type: str
            sample: /subscriptions/21a9967a-e8a9-4656-a70b-96ff1c4d05a0/resourceGroups/myResourceGroup/providers/Microsoft.Maps/accounts/myMapsAccount
        name:
            description:
                - The name of the Maps Account, which is unique within a Resource Group.
            returned: always
            type: str
            sample: myMapsAccount
        location:
            description:
                - The location of the resource.
            returned: always
            type: str
            sample: global
        tags:
            description:
                - "Gets a list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource
                   groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no
                   greater than 256 characters."
            returned: always
            type: complex
            sample: "{\n  'test': 'true'\n}"
        sku:
            description:
                - The SKU of this account.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - The name of the SKU, in standard format (such as S0).
                    returned: always
                    type: str
                    sample: S0
                tier:
                    description:
                        - Gets the sku tier. This is based on the SKU name.
                    returned: always
                    type: str
                    sample: Standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.maps import MapsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAccountsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
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
        self.name = None
        self.tags = None
        super(AzureRMAccountsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MapsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['accounts'] = self.get()
        elif self.resource_group is not None:
            self.results['accounts'] = self.list_by_resource_group()
        else:
            self.results['accounts'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.accounts.get(resource_group_name=self.resource_group,
                                                     account_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Accounts.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.accounts.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Accounts.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.accounts.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Accounts.')

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
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None)
            }
        }
        return d


def main():
    AzureRMAccountsFacts()


if __name__ == '__main__':
    main()

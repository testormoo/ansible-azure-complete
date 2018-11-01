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
module: azure_rm_storetrustedidprovider_facts
version_added: "2.8"
short_description: Get Azure Trusted Id Provider facts.
description:
    - Get facts of Azure Trusted Id Provider.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
        required: True
    account_name:
        description:
            - The name of the Data Lake Store account.
        required: True
    trusted_id_provider_name:
        description:
            - The name of the trusted identity provider to retrieve.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Trusted Id Provider
    azure_rm_storetrustedidprovider_facts:
      resource_group: resource_group_name
      account_name: account_name
      trusted_id_provider_name: trusted_id_provider_name

  - name: List instances of Trusted Id Provider
    azure_rm_storetrustedidprovider_facts:
      resource_group: resource_group_name
      account_name: account_name
'''

RETURN = '''
trusted_id_providers:
    description: A list of dictionaries containing facts for Trusted Id Provider.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: 34adfa4f-cedf-4dc0-ba29-b6d1a69ab345
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: test_trusted_id_provider_name
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.store import DataLakeStoreAccountManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTrustedIdProvidersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            trusted_id_provider_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.account_name = None
        self.trusted_id_provider_name = None
        super(AzureRMTrustedIdProvidersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataLakeStoreAccountManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.trusted_id_provider_name is not None:
            self.results['trusted_id_providers'] = self.get()
        else:
            self.results['trusted_id_providers'] = self.list_by_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.trusted_id_providers.get(resource_group_name=self.resource_group,
                                                                 account_name=self.account_name,
                                                                 trusted_id_provider_name=self.trusted_id_provider_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for TrustedIdProviders.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.trusted_id_providers.list_by_account(resource_group_name=self.resource_group,
                                                                             account_name=self.account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for TrustedIdProviders.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMTrustedIdProvidersFacts()


if __name__ == '__main__':
    main()

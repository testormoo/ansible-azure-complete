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
module: azure_rm_accountdatalakestoreaccount_facts
version_added: "2.8"
short_description: Get Azure Data Lake Store Account facts.
description:
    - Get facts of Azure Data Lake Store Account.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
        required: True
    account_name:
        description:
            - The name of the Data Lake Analytics account.
        required: True
    filter:
        description:
            - OData filter. Optional.
    top:
        description:
            - The number of items to return. Optional.
    skip:
        description:
            - The number of items to skip over before returning elements. Optional.
    select:
        description:
            - OData Select statement. Limits the properties on each entry to just those requested, e.g. Categories?$select=CategoryName,Description. Optional.
    orderby:
        description:
            - "OrderBy clause. One or more comma-separated expressions with an optional 'asc' (the default) or 'desc' depending on the order you'd like the
               values sorted, e.g. Categories?$orderby=CategoryName desc. Optional."
    count:
        description:
            - "The Boolean value of true or false to request a count of the matching resources included with the resources in the response, e.g.
               Categories?$count=true. Optional."
    name:
        description:
            - The name of the Data Lake Store account to retrieve

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Data Lake Store Account
    azure_rm_accountdatalakestoreaccount_facts:
      resource_group: resource_group_name
      account_name: account_name
      filter: filter
      top: top
      skip: skip
      select: select
      orderby: orderby
      count: count

  - name: Get instance of Data Lake Store Account
    azure_rm_accountdatalakestoreaccount_facts:
      resource_group: resource_group_name
      account_name: account_name
      name: data_lake_store_account_name
'''

RETURN = '''
data_lake_store_accounts:
    description: A list of dictionaries containing facts for Data Lake Store Account.
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
            sample: test_adls
        suffix:
            description:
                - The optional suffix for the Data Lake Store account.
            returned: always
            type: str
            sample: test_suffix
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.account import DataLakeAnalyticsAccountManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDataLakeStoreAccountsFacts(AzureRMModuleBase):
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
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            ),
            select=dict(
                type='str'
            ),
            orderby=dict(
                type='str'
            ),
            count=dict(
                type='str'
            ),
            name=dict(
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
        self.filter = None
        self.top = None
        self.skip = None
        self.select = None
        self.orderby = None
        self.count = None
        self.name = None
        super(AzureRMDataLakeStoreAccountsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataLakeAnalyticsAccountManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['data_lake_store_accounts'] = self.list_by_account()
        elif self.name is not None:
            self.results['data_lake_store_accounts'] = self.get()
        return self.results

    def list_by_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.data_lake_store_accounts.list_by_account(resource_group_name=self.resource_group,
                                                                                 account_name=self.account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DataLakeStoreAccounts.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.data_lake_store_accounts.get(resource_group_name=self.resource_group,
                                                                     account_name=self.account_name,
                                                                     data_lake_store_account_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DataLakeStoreAccounts.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'suffix': d.get('suffix', None)
        }
        return d


def main():
    AzureRMDataLakeStoreAccountsFacts()


if __name__ == '__main__':
    main()

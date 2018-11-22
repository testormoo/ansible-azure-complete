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
module: azure_rm_storeaccount_facts
version_added: "2.8"
short_description: Get Azure Account facts.
description:
    - Get facts of Azure Account.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
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
            - "A Boolean value of true or false to request a count of the matching resources included with the resources in the response, e.g.
               Categories?$count=true. Optional."
    name:
        description:
            - The name of the Data Lake Store account.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Account
    azure_rm_storeaccount_facts:
      resource_group: resource_group_name
      filter: filter
      top: top
      skip: skip
      select: select
      orderby: orderby
      count: count

  - name: Get instance of Account
    azure_rm_storeaccount_facts:
      resource_group: resource_group_name
      name: account_name
'''

RETURN = '''
accounts:
    description: A list of dictionaries containing facts for Account.
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
            sample: contosoadla
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: eastus2
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: "{\n  'test_key': 'test_value'\n}"
        identity:
            description:
                - The Key Vault encryption identity, if any.
            returned: always
            type: complex
            sample: identity
            contains:
                type:
                    description:
                        - "The type of encryption being used. Currently the only supported type is 'SystemAssigned'."
                    returned: always
                    type: str
                    sample: SystemAssigned
        state:
            description:
                - "The state of the Data Lake Store account. Possible values include: 'Active', 'Suspended'"
            returned: always
            type: str
            sample: Active
        endpoint:
            description:
                - The full CName endpoint for this account.
            returned: always
            type: str
            sample: testadlfs17607.azuredatalakestore.net
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.store import DataLakeStoreAccountManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAccountFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
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
        self.filter = None
        self.top = None
        self.skip = None
        self.select = None
        self.orderby = None
        self.count = None
        self.name = None
        self.tags = None
        super(AzureRMAccountFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataLakeStoreAccountManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['accounts'] = self.get()
        else:
            self.results['accounts'] = self.list_by_resource_group()
        return self.results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.accounts.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Account.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.accounts.get(resource_group_name=self.resource_group,
                                                     account_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Account.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'identity': {
                'type': d.get('identity', {}).get('type', None)
            },
            'state': d.get('state', None),
            'endpoint': d.get('endpoint', None)
        }
        return d


def main():
    AzureRMAccountFacts()


if __name__ == '__main__':
    main()

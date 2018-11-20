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
module: azure_rm_datacatalogadccatalog_facts
version_added: "2.8"
short_description: Get Azure A D C Catalog facts.
description:
    - Get facts of Azure A D C Catalog.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    name:
        description:
            - The name of the data catlog in the specified subscription and resource group.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of A D C Catalog
    azure_rm_datacatalogadccatalog_facts:
      resource_group: resource_group_name
      name: self.config.catalog_name
'''

RETURN = '''
adc_catalogs:
    description: A list of dictionaries containing facts for A D C Catalog.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/12345678-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataCatalog/catalogs/exampleCatalog
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: exampleCatalog
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: North US
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'mykey': 'myvalue',\n  'mykey2': 'myvalue2'\n}"
        sku:
            description:
                - "Azure data catalog SKU. Possible values include: 'Free', 'Standard'"
            returned: always
            type: str
            sample: Standard
        units:
            description:
                - Azure data catalog units.
            returned: always
            type: int
            sample: 1
        admins:
            description:
                - Azure data catalog admin list.
            returned: always
            type: complex
            sample: admins
            contains:
        users:
            description:
                - Azure data catalog user list.
            returned: always
            type: complex
            sample: users
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datacatalog import DataCatalogRestClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMADCCatalogsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
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
        super(AzureRMADCCatalogsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataCatalogRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['adc_catalogs'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.adc_catalogs.get(resource_group_name=self.resource_group,
                                                         self.config.catalog_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ADCCatalogs.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'sku': d.get('sku', None),
            'units': d.get('units', None),
            'admins': {
            },
            'users': {
            }
        }
        return d


def main():
    AzureRMADCCatalogsFacts()


if __name__ == '__main__':
    main()

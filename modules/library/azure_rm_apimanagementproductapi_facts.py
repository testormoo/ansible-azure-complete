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
module: azure_rm_apimanagementproductapi_facts
version_added: "2.8"
short_description: Get Azure Product Api facts.
description:
    - Get facts of Azure Product Api.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    product_id:
        description:
            - Product identifier. Must be unique in the current API Management service instance.
        required: True
    filter:
        description:
            - | Field       | Supported operators    | Supported functions                         |
            - |-------------|------------------------|---------------------------------------------|
            - | id          | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | name        | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | description | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | serviceUrl  | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | path        | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Product Api
    azure_rm_apimanagementproductapi_facts:
      resource_group: resource_group_name
      name: service_name
      product_id: product_id
      filter: filter
      top: top
      skip: skip
'''

RETURN = '''
product_api:
    description: A list of dictionaries containing facts for Product Api.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProductApiFacts(AzureRMModuleBase):
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
            product_id=dict(
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
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.product_id = None
        self.filter = None
        self.top = None
        self.skip = None
        super(AzureRMProductApiFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['product_api'] = self.list_by_product()
        return self.results

    def list_by_product(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.product_api.list_by_product(resource_group_name=self.resource_group,
                                                                    service_name=self.name,
                                                                    product_id=self.product_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ProductApi.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMProductApiFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_azurestackproduct_facts
version_added: "2.8"
short_description: Get Azure Product facts.
description:
    - Get facts of Azure Product.

options:
    resource_group:
        description:
            - Name of the resource group.
        required: True
    registration_name:
        description:
            - Name of the Azure Stack registration.
        required: True
    product_name:
        description:
            - Name of the product.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Product
    azure_rm_azurestackproduct_facts:
      resource_group: resource_group
      registration_name: registration_name
      product_name: product_name
'''

RETURN = '''
products:
    description: A list of dictionaries containing facts for Product.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ID of the resource.
            returned: always
            type: str
            sample: "/subscriptions/dd8597b4-8739-4467-8b10-f8679f62bfbf/resourceGroups/azurestack/providers/Microsoft.AzureStack/registrations/testregistrat
                    ion/products/Microsoft.OSTCExtensions.VMAccessForLinux.1.4.7.1"
        name:
            description:
                - Name of the resource.
            returned: always
            type: str
            sample: testregistration/Microsoft.OSTCExtensions.VMAccessForLinux.1.4.7.1
        offer:
            description:
                - The offer representing the product.
            returned: always
            type: str
            sample: offer
        sku:
            description:
                - The product SKU.
            returned: always
            type: str
            sample: sku
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.azurestack import AzureStackManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProductsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registration_name=dict(
                type='str',
                required=True
            ),
            product_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.registration_name = None
        self.product_name = None
        super(AzureRMProductsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureStackManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['products'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.products.get(resource_group=self.resource_group,
                                                     registration_name=self.registration_name,
                                                     product_name=self.product_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Products.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'offer': d.get('offer', None),
            'sku': d.get('sku', None)
        }
        return d


def main():
    AzureRMProductsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_apimanagementproductpolicy_facts
version_added: "2.8"
short_description: Get Azure Product Policy facts.
description:
    - Get facts of Azure Product Policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    product_id:
        description:
            - Product identifier. Must be unique in the current API Management service instance.
        required: True
    policy_id:
        description:
            - The identifier of the Policy.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Product Policy
    azure_rm_apimanagementproductpolicy_facts:
      resource_group: resource_group_name
      service_name: service_name
      product_id: product_id
      policy_id: policy_id

  - name: List instances of Product Policy
    azure_rm_apimanagementproductpolicy_facts:
      resource_group: resource_group_name
      service_name: service_name
      product_id: product_id
'''

RETURN = '''
product_policy:
    description: A list of dictionaries containing facts for Product Policy.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/products/kjoshiarmTemplateProduct4/polici
                    es/policy"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: policy
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProductPolicyFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            product_id=dict(
                type='str',
                required=True
            ),
            policy_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.service_name = None
        self.product_id = None
        self.policy_id = None
        super(AzureRMProductPolicyFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.policy_id is not None:
            self.results['product_policy'] = self.get()
        else:
            self.results['product_policy'] = self.list_by_product()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.product_policy.get(resource_group_name=self.resource_group,
                                                           service_name=self.service_name,
                                                           product_id=self.product_id,
                                                           policy_id=self.policy_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ProductPolicy.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_product(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.product_policy.list_by_product(resource_group_name=self.resource_group,
                                                                       service_name=self.service_name,
                                                                       product_id=self.product_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ProductPolicy.')

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
    AzureRMProductPolicyFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_apimanagementservice_facts
version_added: "2.8"
short_description: Get Azure Api Management Service facts.
description:
    - Get facts of Azure Api Management Service.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Api Management Service
    azure_rm_apimanagementservice_facts:
      resource_group: resource_group_name
      name: service_name

  - name: List instances of Api Management Service
    azure_rm_apimanagementservice_facts:
      resource_group: resource_group_name
'''

RETURN = '''
api_management_service:
    description: A list of dictionaries containing facts for Api Management Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: apimService1
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        sku:
            description:
                - SKU properties of the API Management service.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "Name of the Sku. Possible values include: 'Developer', 'Standard', 'Premium', 'Basic'"
                    returned: always
                    type: str
                    sample: Premium
                capacity:
                    description:
                        - Capacity of the SKU (number of deployed units of the SKU). The default value is 1.
                    returned: always
                    type: int
                    sample: 1
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: Central US
        etag:
            description:
                - ETag of the resource.
            returned: always
            type: str
            sample: AAAAAAAYP5M=
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiManagementServiceFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
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
        super(AzureRMApiManagementServiceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['api_management_service'] = self.get()
        else:
            self.results['api_management_service'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_management_service.get(resource_group_name=self.resource_group,
                                                                   service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api Management Service.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_management_service.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api Management Service.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            },
            'location': d.get('location', None),
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMApiManagementServiceFacts()


if __name__ == '__main__':
    main()

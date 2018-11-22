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
module: azure_rm_eventhubnamespace_facts
version_added: "2.8"
short_description: Get Azure Namespace facts.
description:
    - Get facts of Azure Namespace.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    name:
        description:
            - The Namespace name
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Namespace
    azure_rm_eventhubnamespace_facts:
      resource_group: resource_group_name
      name: namespace_name

  - name: List instances of Namespace
    azure_rm_eventhubnamespace_facts:
      resource_group: resource_group_name
'''

RETURN = '''
namespaces:
    description: A list of dictionaries containing facts for Namespace.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/5f750a97-50d9-4e36-8081-c9ee4c0210d4/resourceGroups/ArunMonocle/providers/Microsoft.EventHub/namespaces/sdk-Namespace-5849
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: sdk-Namespace-5849
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: South Central US
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'tag1': 'value1',\n  'tag2': 'value2'\n}"
        sku:
            description:
                - Properties of sku resource
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "Name of this SKU. Possible values include: 'Basic', 'Standard'"
                    returned: always
                    type: str
                    sample: Standard
                tier:
                    description:
                        - "The billing tier of this particular SKU. Possible values include: 'Basic', 'Standard'"
                    returned: always
                    type: str
                    sample: Standard
                capacity:
                    description:
                        - The Event Hubs throughput units, vaule should be 0 to 20 throughput units.
                    returned: always
                    type: int
                    sample: 1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventhub import EventHubManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNamespaceFacts(AzureRMModuleBase):
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
        super(AzureRMNamespaceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['namespaces'] = self.get()
        else:
            self.results['namespaces'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.namespaces.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Namespace.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.namespaces.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Namespace.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            }
        }
        return d


def main():
    AzureRMNamespaceFacts()


if __name__ == '__main__':
    main()

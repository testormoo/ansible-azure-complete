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
module: azure_rm_csmaccount_facts
version_added: "2.8"
short_description: Get Azure Account facts.
description:
    - Get facts of Azure Account.

options:
    resource_group:
        description:
            - Name of the resource group within the Azure subscription.
        required: True
    resource_name:
        description:
            - Name of the resource.
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
    azure_rm_csmaccount_facts:
      resource_group: resource_group_name
      resource_name: resource_name

  - name: List instances of Account
    azure_rm_csmaccount_facts:
      resource_group: resource_group_name
'''

RETURN = '''
accounts:
    description: A list of dictionaries containing facts for Account.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Unique identifier of the resource.
            returned: always
            type: str
            sample: /subscriptions/0de7f055-dbea-498d-8e9e-da287eedca90/resourceGroups/VS-Example-Group/providers/Microsoft.VisualStudio/account/Example
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: Central US
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: VS-Example-Group
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        properties:
            description:
                - Resource properties.
            returned: always
            type: complex
            sample: "{\n  'AccountURL': ''\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.csm import VisualStudioResourceProviderClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAccountsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
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
        self.resource_name = None
        self.tags = None
        super(AzureRMAccountsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(VisualStudioResourceProviderClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_name is not None:
            self.results['accounts'] = self.get()
        else:
            self.results['accounts'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.accounts.get(resource_group_name=self.resource_group,
                                                     resource_name=self.resource_name)
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

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'location': d.get('location', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'properties': d.get('properties', None)
        }
        return d


def main():
    AzureRMAccountsFacts()


if __name__ == '__main__':
    main()

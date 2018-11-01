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
module: azure_rm_csmextension_facts
version_added: "2.8"
short_description: Get Azure Extension facts.
description:
    - Get facts of Azure Extension.

options:
    resource_group:
        description:
            - Name of the resource group within the Azure subscription.
        required: True
    account_resource_name:
        description:
            - The name of the Visual Studio Team Services account resource.
        required: True
    extension_resource_name:
        description:
            - The name of the extension.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Extension
    azure_rm_csmextension_facts:
      resource_group: resource_group_name
      account_resource_name: account_resource_name
      extension_resource_name: extension_resource_name

  - name: List instances of Extension
    azure_rm_csmextension_facts:
      resource_group: resource_group_name
      account_resource_name: account_resource_name
'''

RETURN = '''
extensions:
    description: A list of dictionaries containing facts for Extension.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Unique identifier of the resource.
            returned: always
            type: str
            sample: "/subscriptions/0de7f055-dbea-498d-8e9e-da287eedca90/resourceGroups/VS-Example-Group/providers/Microsoft.VisualStudio/account/ExampleAcco
                    unt/extension/ms.example"
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
            sample: ms.example
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        plan:
            description:
                - The extension plan that was purchased.
            returned: always
            type: complex
            sample: plan
            contains:
                name:
                    description:
                        - Name of the plan.
                    returned: always
                    type: str
                    sample: ExamplePlan
                product:
                    description:
                        - Product name.
                    returned: always
                    type: str
                    sample: ExampleExtensionName
                publisher:
                    description:
                        - Name of the extension publisher.
                    returned: always
                    type: str
                    sample: ExampleExtensionPublisher
                version:
                    description:
                        - A string that uniquely identifies the plan version.
                    returned: always
                    type: str
                    sample: 1.0
        properties:
            description:
                - Resource properties.
            returned: always
            type: complex
            sample: {}
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.csm import VisualStudioResourceProviderClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMExtensionsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_resource_name=dict(
                type='str',
                required=True
            ),
            extension_resource_name=dict(
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
        self.account_resource_name = None
        self.extension_resource_name = None
        self.tags = None
        super(AzureRMExtensionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(VisualStudioResourceProviderClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.extension_resource_name is not None:
            self.results['extensions'] = self.get()
        else:
            self.results['extensions'] = self.list_by_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.extensions.get(resource_group_name=self.resource_group,
                                                       account_resource_name=self.account_resource_name,
                                                       extension_resource_name=self.extension_resource_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Extensions.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.extensions.list_by_account(resource_group_name=self.resource_group,
                                                                   account_resource_name=self.account_resource_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Extensions.')

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
            'plan': {
                'name': d.get('plan', {}).get('name', None),
                'product': d.get('plan', {}).get('product', None),
                'publisher': d.get('plan', {}).get('publisher', None),
                'version': d.get('plan', {}).get('version', None)
            },
            'properties': d.get('properties', None)
        }
        return d


def main():
    AzureRMExtensionsFacts()


if __name__ == '__main__':
    main()

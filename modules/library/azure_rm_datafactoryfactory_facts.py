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
module: azure_rm_datafactoryfactory_facts
version_added: "2.8"
short_description: Get Azure Factory facts.
description:
    - Get facts of Azure Factory.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
    if_none_match:
        description:
            - "ETag of the factory entity. Should only be specified for get. If the ETag matches the existing entity tag, or if * was provided, then no
               content will be returned."
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Factory
    azure_rm_datafactoryfactory_facts:
      resource_group: resource_group_name
      factory_name: factory_name
      if_none_match: if_none_match

  - name: List instances of Factory
    azure_rm_datafactoryfactory_facts:
      resource_group: resource_group_name
'''

RETURN = '''
factories:
    description: A list of dictionaries containing facts for Factory.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/example
                    FactoryName"
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: exampleFactoryName
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: East US
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: "{\n  'exampleTag': 'exampleValue'\n}"
        version:
            description:
                - Version of the factory.
            returned: always
            type: str
            sample: 2018-06-01
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMFactoriesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            factory_name=dict(
                type='str'
            ),
            if_none_match=dict(
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
        self.factory_name = None
        self.if_none_match = None
        self.tags = None
        super(AzureRMFactoriesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.factory_name is not None:
            self.results['factories'] = self.get()
        else:
            self.results['factories'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.factories.get(resource_group_name=self.resource_group,
                                                      factory_name=self.factory_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Factories.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.factories.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Factories.')

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
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'version': d.get('version', None)
        }
        return d


def main():
    AzureRMFactoriesFacts()


if __name__ == '__main__':
    main()

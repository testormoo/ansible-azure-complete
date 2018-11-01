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
module: azure_rm_routetable_facts
version_added: "2.8"
short_description: Get Azure Route Table facts.
description:
    - Get facts of Azure Route Table.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    route_table_name:
        description:
            - The name of the route table.
        required: True
    expand:
        description:
            - Expands referenced resources.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Route Table
    azure_rm_routetable_facts:
      resource_group: resource_group_name
      route_table_name: route_table_name
      expand: expand
'''

RETURN = '''
route_tables:
    description: A list of dictionaries containing facts for Route Table.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/routeTables/testrt
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: testrt
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        routes:
            description:
                - Collection of routes contained within a route table.
            returned: always
            type: complex
            sample: routes
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRouteTablesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            route_table_name=dict(
                type='str',
                required=True
            ),
            expand=dict(
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
        self.route_table_name = None
        self.expand = None
        self.tags = None
        super(AzureRMRouteTablesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['route_tables'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.route_tables.get(resource_group_name=self.resource_group,
                                                         route_table_name=self.route_table_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RouteTables.')

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
            'routes': {
            }
        }
        return d


def main():
    AzureRMRouteTablesFacts()


if __name__ == '__main__':
    main()

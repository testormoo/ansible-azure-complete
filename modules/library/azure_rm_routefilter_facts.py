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
module: azure_rm_routefilter_facts
version_added: "2.8"
short_description: Get Azure Route Filter facts.
description:
    - Get facts of Azure Route Filter.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the route filter.
    expand:
        description:
            - Expands referenced express route bgp peering resources.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Route Filter
    azure_rm_routefilter_facts:
      resource_group: resource_group_name
      name: route_filter_name
      expand: expand

  - name: List instances of Route Filter
    azure_rm_routefilter_facts:
      resource_group: resource_group_name
'''

RETURN = '''
route_filters:
    description: A list of dictionaries containing facts for Route Filter.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsofot.Network/routeFilters/filterName
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: filterName
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: "{\n  'key1': 'value1'\n}"
        rules:
            description:
                - Collection of RouteFilterRules contained within a route filter.
            returned: always
            type: complex
            sample: rules
            contains:
        peerings:
            description:
                - A collection of references to express route circuit peerings.
            returned: always
            type: complex
            sample: peerings
            contains:
        etag:
            description:
                - Gets a unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: w/\00000000-0000-0000-0000-000000000000\
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRouteFiltersFacts(AzureRMModuleBase):
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
        self.name = None
        self.expand = None
        self.tags = None
        super(AzureRMRouteFiltersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['route_filters'] = self.get()
        else:
            self.results['route_filters'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.route_filters.get(resource_group_name=self.resource_group,
                                                          route_filter_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RouteFilters.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.route_filters.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RouteFilters.')

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
            'rules': {
            },
            'peerings': {
            },
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMRouteFiltersFacts()


if __name__ == '__main__':
    main()

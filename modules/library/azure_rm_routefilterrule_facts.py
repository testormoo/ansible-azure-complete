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
module: azure_rm_routefilterrule_facts
version_added: "2.8"
short_description: Get Azure Route Filter Rule facts.
description:
    - Get facts of Azure Route Filter Rule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    route_filter_name:
        description:
            - The name of the route filter.
        required: True
    rule_name:
        description:
            - The name of the rule.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Route Filter Rule
    azure_rm_routefilterrule_facts:
      resource_group: resource_group_name
      route_filter_name: route_filter_name
      rule_name: rule_name

  - name: List instances of Route Filter Rule
    azure_rm_routefilterrule_facts:
      resource_group: resource_group_name
      route_filter_name: route_filter_name
'''

RETURN = '''
route_filter_rules:
    description: A list of dictionaries containing facts for Route Filter Rule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsofot.Network/routeFilters/filterName/routeFilterRules/ruleName
        access:
            description:
                - "The access type of the rule. Valid values are: 'Allow', 'Deny'. Possible values include: 'Allow', 'Deny'"
            returned: always
            type: str
            sample: Allow
        communities:
            description:
                - "The collection for bgp community values to filter on. e.g. ['12076:5010','12076:5020']"
            returned: always
            type: str
            sample: "[\n  '12076:5030',\n  '12076:5040'\n]"
        name:
            description:
                - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            returned: always
            type: str
            sample: ruleName
        etag:
            description:
                - A unique read-only string that changes whenever the resource is updated.
            returned: always
            type: str
            sample: w/\00000000-0000-0000-0000-000000000000\
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: "{\n  'key1': 'value1'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRouteFilterRulesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            route_filter_name=dict(
                type='str',
                required=True
            ),
            rule_name=dict(
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
        self.route_filter_name = None
        self.rule_name = None
        self.tags = None
        super(AzureRMRouteFilterRulesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.rule_name is not None:
            self.results['route_filter_rules'] = self.get()
        else:
            self.results['route_filter_rules'] = self.list_by_route_filter()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.route_filter_rules.get(resource_group_name=self.resource_group,
                                                               route_filter_name=self.route_filter_name,
                                                               rule_name=self.rule_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RouteFilterRules.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_route_filter(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.route_filter_rules.list_by_route_filter(resource_group_name=self.resource_group,
                                                                                route_filter_name=self.route_filter_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RouteFilterRules.')

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
            'access': d.get('access', None),
            'communities': d.get('communities', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMRouteFilterRulesFacts()


if __name__ == '__main__':
    main()

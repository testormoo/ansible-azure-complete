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
module: azure_rm_frontdoorroutingrule_facts
version_added: "2.8"
short_description: Get Azure Routing Rule facts.
description:
    - Get facts of Azure Routing Rule.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    routing_rule_name:
        description:
            - Name of the Routing Rule which is unique within the Front Door.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Routing Rule
    azure_rm_frontdoorroutingrule_facts:
      resource_group: resource_group_name
      front_door_name: front_door_name
      routing_rule_name: routing_rule_name

  - name: List instances of Routing Rule
    azure_rm_frontdoorroutingrule_facts:
      resource_group: resource_group_name
      front_door_name: front_door_name
'''

RETURN = '''
routing_rules:
    description: A list of dictionaries containing facts for Routing Rule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/routingRule1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: routingRule1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.frontdoor import FrontDoorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRoutingRulesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            front_door_name=dict(
                type='str',
                required=True
            ),
            routing_rule_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.front_door_name = None
        self.routing_rule_name = None
        super(AzureRMRoutingRulesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.routing_rule_name is not None:
            self.results['routing_rules'] = self.get()
        else:
            self.results['routing_rules'] = self.list_by_front_door()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.routing_rules.get(resource_group_name=self.resource_group,
                                                          front_door_name=self.front_door_name,
                                                          routing_rule_name=self.routing_rule_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RoutingRules.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_front_door(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.routing_rules.list_by_front_door(resource_group_name=self.resource_group,
                                                                         front_door_name=self.front_door_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RoutingRules.')

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
    AzureRMRoutingRulesFacts()


if __name__ == '__main__':
    main()
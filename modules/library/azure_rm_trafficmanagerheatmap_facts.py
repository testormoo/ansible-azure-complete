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
module: azure_rm_trafficmanagerheatmap_facts
version_added: "2.8"
short_description: Get Azure Heat Map facts.
description:
    - Get facts of Azure Heat Map.

options:
    resource_group:
        description:
            - The name of the resource group containing the Traffic Manager endpoint.
        required: True
    name:
        description:
            - The name of the Traffic Manager profile.
        required: True
    heat_map_type:
        description:
            - The type of HeatMap for the Traffic Manager profile.
        required: True
    top_left:
        description:
            - The top left latitude,longitude pair of the rectangular viewport to query for.
    bot_right:
        description:
            - The bottom right latitude,longitude pair of the rectangular viewport to query for.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Heat Map
    azure_rm_trafficmanagerheatmap_facts:
      resource_group: resource_group_name
      name: profile_name
      heat_map_type: heat_map_type
      top_left: top_left
      bot_right: bot_right
'''

RETURN = '''
heat_map:
    description: A list of dictionaries containing facts for Heat Map.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/{subscription-id}/resourceGroups/azuresdkfornetautoresttrafficmanager1323/providers/Microsoft.Network/trafficManagerProfi
                    les/azuresdkfornetautoresttrafficmanager3880/heatMaps/latencyVolumeByLocation"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: default
        endpoints:
            description:
                - The endpoints used in this HeatMap calculation.
            returned: always
            type: complex
            sample: endpoints
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.trafficmanager import TrafficManagerManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMHeatMapFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            heat_map_type=dict(
                type='str',
                required=True
            ),
            top_left=dict(
                type='float'
            ),
            bot_right=dict(
                type='float'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.heat_map_type = None
        self.top_left = None
        self.bot_right = None
        super(AzureRMHeatMapFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(TrafficManagerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['heat_map'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.heat_map.get(resource_group_name=self.resource_group,
                                                     profile_name=self.name,
                                                     heat_map_type=self.heat_map_type)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for HeatMap.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'endpoints': {
            }
        }
        return d


def main():
    AzureRMHeatMapFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_loadbalancer_facts
version_added: "2.8"
short_description: Get Azure Load Balancer facts.
description:
    - Get facts of Azure Load Balancer.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the load balancer.
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
  - name: Get instance of Load Balancer
    azure_rm_loadbalancer_facts:
      resource_group: resource_group_name
      name: load_balancer_name
      expand: expand
'''

RETURN = '''
load_balancers:
    description: A list of dictionaries containing facts for Load Balancer.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/loadBalancers/lb
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: lb
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
        sku:
            description:
                - The load balancer SKU.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "Name of a load balancer SKU. Possible values include: 'Basic', 'Standard'"
                    returned: always
                    type: str
                    sample: Basic
        probes:
            description:
                - Collection of probe objects used in the load balancer
            returned: always
            type: complex
            sample: probes
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


class AzureRMLoadBalancersFacts(AzureRMModuleBase):
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
        super(AzureRMLoadBalancersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['load_balancers'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.load_balancers.get(resource_group_name=self.resource_group,
                                                           load_balancer_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LoadBalancers.')

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
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            },
            'probes': {
            }
        }
        return d


def main():
    AzureRMLoadBalancersFacts()


if __name__ == '__main__':
    main()

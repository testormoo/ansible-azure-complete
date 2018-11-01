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
module: azure_rm_frontdoorbackendpool_facts
version_added: "2.8"
short_description: Get Azure Backend Pool facts.
description:
    - Get facts of Azure Backend Pool.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    backend_pool_name:
        description:
            - Name of the Backend Pool which is unique within the Front Door.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Backend Pool
    azure_rm_frontdoorbackendpool_facts:
      resource_group: resource_group_name
      front_door_name: front_door_name
      backend_pool_name: backend_pool_name

  - name: List instances of Backend Pool
    azure_rm_frontdoorbackendpool_facts:
      resource_group: resource_group_name
      front_door_name: front_door_name
'''

RETURN = '''
backend_pools:
    description: A list of dictionaries containing facts for Backend Pool.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/backendPools/backendPool1
        backends:
            description:
                - The set of backends for this pool
            returned: always
            type: complex
            sample: backends
            contains:
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: backendPool1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.frontdoor import FrontDoorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackendPoolsFacts(AzureRMModuleBase):
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
            backend_pool_name=dict(
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
        self.backend_pool_name = None
        super(AzureRMBackendPoolsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.backend_pool_name is not None:
            self.results['backend_pools'] = self.get()
        else:
            self.results['backend_pools'] = self.list_by_front_door()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.backend_pools.get(resource_group_name=self.resource_group,
                                                          front_door_name=self.front_door_name,
                                                          backend_pool_name=self.backend_pool_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for BackendPools.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_front_door(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.backend_pools.list_by_front_door(resource_group_name=self.resource_group,
                                                                         front_door_name=self.front_door_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for BackendPools.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'backends': {
            },
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMBackendPoolsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_servicefabricmeshnetwork_facts
version_added: "2.8"
short_description: Get Azure Network facts.
description:
    - Get facts of Azure Network.

options:
    resource_group:
        description:
            - Azure resource group name
    name:
        description:
            - The identity of the network.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Network
    azure_rm_servicefabricmeshnetwork_facts:
      resource_group: resource_group_name
      name: network_resource_name

  - name: List instances of Network
    azure_rm_servicefabricmeshnetwork_facts:
      resource_group: resource_group_name

  - name: List instances of Network
    azure_rm_servicefabricmeshnetwork_facts:
'''

RETURN = '''
network:
    description: A list of dictionaries containing facts for Network.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified identifier for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/networks/sampleNetwork
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: sampleNetwork
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - The geo-location where the resource lives
            returned: always
            type: str
            sample: EastUS
        properties:
            description:
                - Describes properties of a network resource.
            returned: always
            type: complex
            sample: properties
            contains:
                kind:
                    description:
                        - Constant filled by server.
                    returned: always
                    type: str
                    sample: Local
                description:
                    description:
                        - User readable description of the network.
                    returned: always
                    type: str
                    sample: Service Fabric Mesh sample network.
                status:
                    description:
                        - "Status of the network. Possible values include: 'Unknown', 'Ready', 'Upgrading', 'Creating', 'Deleting', 'Failed'"
                    returned: always
                    type: str
                    sample: Ready
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.servicefabricmesh import ServiceFabricMeshManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNetworkFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
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
        self.tags = None
        super(AzureRMNetworkFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['network'] = self.get()
        elif self.resource_group is not None:
            self.results['network'] = self.list_by_resource_group()
        else:
            self.results['network'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.network.get(resource_group_name=self.resource_group,
                                                    network_resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Network.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.network.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Network.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.network.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Network.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'properties': {
                'kind': d.get('properties', {}).get('kind', None),
                'description': d.get('properties', {}).get('description', None),
                'status': d.get('properties', {}).get('status', None)
            }
        }
        return d


def main():
    AzureRMNetworkFacts()


if __name__ == '__main__':
    main()

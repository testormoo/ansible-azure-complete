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
module: azure_rm_iothubresource_facts
version_added: "2.8"
short_description: Get Azure Iot Hub Resource facts.
description:
    - Get facts of Azure Iot Hub Resource.

options:
    resource_group:
        description:
            - The name of the resource group that contains the IoT hub.
    name:
        description:
            - The name of the IoT hub.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Iot Hub Resource
    azure_rm_iothubresource_facts:
      resource_group: resource_group_name
      name: resource_name

  - name: List instances of Iot Hub Resource
    azure_rm_iothubresource_facts:
      resource_group: resource_group_name

  - name: List instances of Iot Hub Resource
    azure_rm_iothubresource_facts:
'''

RETURN = '''
iot_hub_resource:
    description: A list of dictionaries containing facts for Iot Hub Resource.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: /subscriptions/91d12660-3dec-467a-be2a-213b5544ddc0/resourceGroups/myResourceGroup/providers/Microsoft.Devices/IotHubs/testHub
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: testHub
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: centraluseuap
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: {}
        etag:
            description:
                - The Etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal ETag convention.
            returned: always
            type: str
            sample: AAAAAAFD6M4=
        properties:
            description:
                - IotHub properties
            returned: always
            type: complex
            sample: properties
            contains:
                state:
                    description:
                        - Thehub state state.
                    returned: always
                    type: str
                    sample: Active
                routing:
                    description:
                        -
                    returned: always
                    type: complex
                    sample: routing
                    contains:
                        endpoints:
                            description:
                                -
                            returned: always
                            type: complex
                            sample: endpoints
                            contains:
                        routes:
                            description:
                                - "The list of user-provided routing rules that the IoT hub uses to route messages to built-in and custom endpoints. A
                                   maximum of 100 routing rules are allowed for paid hubs and a maximum of 5 routing rules are allowed for free hubs."
                            returned: always
                            type: complex
                            sample: routes
                            contains:
                features:
                    description:
                        - "The capabilities and features enabled for the IoT hub. Possible values include: 'None', 'DeviceManagement'"
                    returned: always
                    type: str
                    sample: None
        sku:
            description:
                - IotHub SKU info
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The name of the SKU. Possible values include: 'F1', 'S1', 'S2', 'S3', 'B1', 'B2', 'B3'"
                    returned: always
                    type: str
                    sample: S1
                tier:
                    description:
                        - "The billing tier for the IoT hub. Possible values include: 'Free', 'Standard', 'Basic'"
                    returned: always
                    type: str
                    sample: Standard
                capacity:
                    description:
                        - "The number of provisioned IoT Hub units. See: https://docs.microsoft.com/azure/azure-subscription-service-limits#iot-hub-limits."
                    returned: always
                    type: int
                    sample: 1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.iothub import IotHubClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIotHubResourceFacts(AzureRMModuleBase):
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
        super(AzureRMIotHubResourceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(IotHubClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['iot_hub_resource'] = self.get()
        elif self.resource_group is not None:
            self.results['iot_hub_resource'] = self.list_by_resource_group()
        else:
            self.results['iot_hub_resource'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iot_hub_resource.get(resource_group_name=self.resource_group,
                                                             resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iot Hub Resource.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iot_hub_resource.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iot Hub Resource.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iot_hub_resource.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iot Hub Resource.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'etag': d.get('etag', None),
            'properties': {
                'state': d.get('properties', {}).get('state', None),
                'routing': {
                    'endpoints': {
                    },
                    'routes': {
                    }
                },
                'features': d.get('properties', {}).get('features', None)
            },
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            }
        }
        return d


def main():
    AzureRMIotHubResourceFacts()


if __name__ == '__main__':
    main()

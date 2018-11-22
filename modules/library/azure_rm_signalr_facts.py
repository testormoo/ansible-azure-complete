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
module: azure_rm_signalr_facts
version_added: "2.8"
short_description: Get Azure Signal R facts.
description:
    - Get facts of Azure Signal R.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    name:
        description:
            - The name of the SignalR resource.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Signal R
    azure_rm_signalr_facts:
      resource_group: resource_group_name
      name: resource_name

  - name: List instances of Signal R
    azure_rm_signalr_facts:
      resource_group: resource_group_name

  - name: List instances of Signal R
    azure_rm_signalr_facts:
'''

RETURN = '''
signal_r:
    description: A list of dictionaries containing facts for Signal R.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/myResourceGroup/providers/Microsoft.SignalRService/SignalR/mySignalRS
                    ervice"
        name:
            description:
                - The name of the resouce.
            returned: always
            type: str
            sample: mySignalRService
        location:
            description:
                - The GEO location of the SignalR service. e.g. West US | East US | North Central US | South Central US.
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - Tags of the service which is a list of key value pairs that describe the resource.
            returned: always
            type: complex
            sample: "{\n  'key1': 'value1'\n}"
        sku:
            description:
                - SKU of the service.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - The name of the SKU. This is typically a letter + number code, such as A0 or P3.  Required (if sku is specified)
                    returned: always
                    type: str
                    sample: Standard_S1
                tier:
                    description:
                        - "Optional tier of this particular SKU. `Basic` is deprecated, use `Standard` instead for Basic tier. Possible values include:
                           'Free', 'Basic', 'Standard', 'Premium'"
                    returned: always
                    type: str
                    sample: Standard
                size:
                    description:
                        - Optional, string. When the name field is the combination of tier and some other value, this would be the standalone code.
                    returned: always
                    type: str
                    sample: S1
                capacity:
                    description:
                        - "Optional, integer. If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not
                           \n\npossible for the resource this may be omitted."
                    returned: always
                    type: int
                    sample: 1
        version:
            description:
                - Version of the SignalR resource. Probably you need the same or higher version of client SDKs.
            returned: always
            type: str
            sample: 1.0-preview
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.signalr import SignalRManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSignalRFacts(AzureRMModuleBase):
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
        super(AzureRMSignalRFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SignalRManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['signal_r'] = self.get()
        elif self.resource_group is not None:
            self.results['signal_r'] = self.list_by_resource_group()
        else:
            self.results['signal_r'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.signal_r.get(resource_group_name=self.resource_group,
                                                     resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Signal R.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.signal_r.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Signal R.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.signal_r.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Signal R.')

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
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None),
                'size': d.get('sku', {}).get('size', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            },
            'version': d.get('version', None)
        }
        return d


def main():
    AzureRMSignalRFacts()


if __name__ == '__main__':
    main()

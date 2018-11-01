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
module: azure_rm_windowsiotservicesservice_facts
version_added: "2.8"
short_description: Get Azure Service facts.
description:
    - Get facts of Azure Service.

options:
    resource_group:
        description:
            - The name of the resource group that contains the Windows IoT Device Service.
        required: True
    device_name:
        description:
            - The name of the Windows IoT Device Service.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Service
    azure_rm_windowsiotservicesservice_facts:
      resource_group: resource_group_name
      device_name: device_name

  - name: List instances of Service
    azure_rm_windowsiotservicesservice_facts:
      resource_group: resource_group_name
'''

RETURN = '''
services:
    description: A list of dictionaries containing facts for Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource
            returned: always
            type: str
            sample: /subscriptions/45b60d85-fd72-427a-a708-f994d26e593e/resourceGroups/res9407/providers/Microsoft.WindowsIoT/Services/service8596
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: service8596
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        location:
            description:
                - The Azure Region where the resource lives
            returned: always
            type: str
            sample: westus
        notes:
            description:
                - Windows IoT Device Service notes.
            returned: always
            type: str
            sample: blah
        quantity:
            description:
                - Windows IoT Device Service device allocation,
            returned: always
            type: int
            sample: 1000000
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.windowsiotservices import DeviceServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServicesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            device_name=dict(
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
        self.device_name = None
        self.tags = None
        super(AzureRMServicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DeviceServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.device_name is not None:
            self.results['services'] = self.get()
        else:
            self.results['services'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.services.get(resource_group_name=self.resource_group,
                                                     device_name=self.device_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Services.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.services.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Services.')

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
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'notes': d.get('notes', None),
            'quantity': d.get('quantity', None)
        }
        return d


def main():
    AzureRMServicesFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_iotcentralapp_facts
version_added: "2.8"
short_description: Get Azure App facts.
description:
    - Get facts of Azure App.

options:
    resource_group:
        description:
            - The name of the resource group that contains the IoT Central application.
    name:
        description:
            - The ARM resource name of the IoT Central application.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of App
    azure_rm_iotcentralapp_facts:
      resource_group: resource_group_name
      name: resource_name

  - name: List instances of App
    azure_rm_iotcentralapp_facts:
      resource_group: resource_group_name

  - name: List instances of App
    azure_rm_iotcentralapp_facts:
'''

RETURN = '''
apps:
    description: A list of dictionaries containing facts for App.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The ARM resource identifier.
            returned: always
            type: str
            sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/resRg/providers/Microsoft.IoTCentral/IoTApps/myIoTCentralApp
        name:
            description:
                - The ARM resource name.
            returned: always
            type: str
            sample: myIoTCentralApp
        location:
            description:
                - The resource location.
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: "{\n  'key': 'value'\n}"
        subdomain:
            description:
                - The subdomain of the application.
            returned: always
            type: str
            sample: my-iot-central-app
        template:
            description:
                - "The ID of the application template, which is a blueprint that defines the characteristics and behaviors of an application. Optional; if
                   not specified, defaults to a blank blueprint and allows the application to be defined from scratch."
            returned: always
            type: str
            sample: iotc-default@1.0.0
        sku:
            description:
                - A valid instance SKU.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The name of the SKU. Possible values include: 'F1', 'S1'"
                    returned: always
                    type: str
                    sample: F1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.iotcentral import IotCentralClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAppFacts(AzureRMModuleBase):
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
        super(AzureRMAppFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(IotCentralClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['apps'] = self.get()
        elif self.resource_group is not None:
            self.results['apps'] = self.list_by_resource_group()
        else:
            self.results['apps'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.apps.get(resource_group_name=self.resource_group,
                                                 resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for App.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.apps.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for App.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.apps.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for App.')

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
            'subdomain': d.get('subdomain', None),
            'template': d.get('template', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            }
        }
        return d


def main():
    AzureRMAppFacts()


if __name__ == '__main__':
    main()

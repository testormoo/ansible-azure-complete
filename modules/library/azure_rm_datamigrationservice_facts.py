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
module: azure_rm_datamigrationservice_facts
version_added: "2.8"
short_description: Get Azure Service facts.
description:
    - Get facts of Azure Service.

options:
    group_name:
        description:
            - Name of the resource group
        required: True
    name:
        description:
            - Name of the service
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
    azure_rm_datamigrationservice_facts:
      group_name: group_name
      name: service_name

  - name: List instances of Service
    azure_rm_datamigrationservice_facts:
      group_name: group_name
'''

RETURN = '''
services:
    description: A list of dictionaries containing facts for Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/fc04246f-04c5-437e-ac5e-206a19e7193f/resourceGroups/DmsSdkRg/providers/Microsoft.DataMigration/services/DmsSdkService
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: DmsSdkService
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: southcentralus
        etag:
            description:
                - HTTP strong entity tag value. Ignored if submitted
            returned: always
            type: str
            sample: qt85+bWDN84/6PR8Gllxf63krZcXZX1h3wxAbs6pCjc=
        sku:
            description:
                - Service SKU
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The unique name of the SKU, such as 'P3'"
                    returned: always
                    type: str
                    sample: Basic_1vCore
                tier:
                    description:
                        - "The tier of the SKU, such as 'Basic', 'General Purpose', or 'Business Critical'"
                    returned: always
                    type: str
                    sample: Basic
                size:
                    description:
                        - "The size of the SKU, used when the name alone does not denote a service size or when a SKU has multiple performance classes
                           within a family, e.g. 'A1' for virtual machines"
                    returned: always
                    type: str
                    sample: 1 vCore
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datamigration import DataMigrationServiceClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServiceFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            group_name=dict(
                type='str',
                required=True
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
        self.group_name = None
        self.name = None
        self.tags = None
        super(AzureRMServiceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataMigrationServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['services'] = self.get()
        else:
            self.results['services'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.services.get(group_name=self.group_name,
                                                     service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Service.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.services.list_by_resource_group(group_name=self.group_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Service.')

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
            'etag': d.get('etag', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None),
                'size': d.get('sku', {}).get('size', None)
            }
        }
        return d


def main():
    AzureRMServiceFacts()


if __name__ == '__main__':
    main()

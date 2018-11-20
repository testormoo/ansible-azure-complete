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
module: azure_rm_batchaifileserver_facts
version_added: "2.8"
short_description: Get Azure File Server facts.
description:
    - Get facts of Azure File Server.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - "The name of the file server within the specified resource group. File server names can only contain a combination of alphanumeric characters
               along with dash (-) and underscore (_). The name must be from 1 through 64 characters long."
    file_servers_list_by_resource_group_options:
        description:
            - Additional parameters for the operation
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of File Server
    azure_rm_batchaifileserver_facts:
      resource_group: resource_group_name
      name: file_server_name

  - name: List instances of File Server
    azure_rm_batchaifileserver_facts:
      resource_group: resource_group_name
      file_servers_list_by_resource_group_options: file_servers_list_by_resource_group_options
'''

RETURN = '''
file_servers:
    description: A list of dictionaries containing facts for File Server.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The ID of the resource
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.BatchAI/fileservers/fileserve
                    rcedd134b"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: fileservercedd134b
        location:
            description:
                - The location of the resource
            returned: always
            type: str
            sample: eastus
        tags:
            description:
                - The tags of the resource
            returned: always
            type: complex
            sample: tags
        subnet:
            description:
                -
            returned: always
            type: complex
            sample: subnet
            contains:
                id:
                    description:
                        - The ID of the resource
                    returned: always
                    type: str
                    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.Network/virtualNetwor
                            ks/7feb1976-8c31-4f1f-bea2-86cb1839a7bavnet/subnets/Subnet-1"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.batchai import BatchAIManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMFileServersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            file_servers_list_by_resource_group_options=dict(
                type='dict'
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
        self.file_servers_list_by_resource_group_options = None
        self.tags = None
        super(AzureRMFileServersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(BatchAIManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['file_servers'] = self.get()
        else:
            self.results['file_servers'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.file_servers.get(resource_group_name=self.resource_group,
                                                         file_server_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for FileServers.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.file_servers.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for FileServers.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'subnet': {
                'id': d.get('subnet', {}).get('id', None)
            }
        }
        return d


def main():
    AzureRMFileServersFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_redislinkedserver_facts
version_added: "2.8"
short_description: Get Azure Linked Server facts.
description:
    - Get facts of Azure Linked Server.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the redis cache.
        required: True
    linked_server_name:
        description:
            - The name of the linked server.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Linked Server
    azure_rm_redislinkedserver_facts:
      resource_group: resource_group_name
      name: name
      linked_server_name: linked_server_name
'''

RETURN = '''
linked_server:
    description: A list of dictionaries containing facts for Linked Server.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Cache/Redis/cache1/linkedServers/cache2
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: cache2
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.redis import RedisManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLinkedServerFacts(AzureRMModuleBase):
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
            linked_server_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.linked_server_name = None
        super(AzureRMLinkedServerFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RedisManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['linked_server'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.linked_server.get(resource_group_name=self.resource_group,
                                                          name=self.name,
                                                          linked_server_name=self.linked_server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Linked Server.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMLinkedServerFacts()


if __name__ == '__main__':
    main()

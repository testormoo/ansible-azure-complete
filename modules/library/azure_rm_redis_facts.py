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
module: azure_rm_redis_facts
version_added: "2.8"
short_description: Get Azure Redis facts.
description:
    - Get facts of Azure Redis.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Redis cache.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Redis
    azure_rm_redis_facts:
      resource_group: resource_group_name
      name: name

  - name: List instances of Redis
    azure_rm_redis_facts:
      resource_group: resource_group_name
'''

RETURN = '''
redis:
    description: A list of dictionaries containing facts for Redis.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Cache/Redis/cache1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: cache1
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
            sample: West US
        sku:
            description:
                - The SKU of the Redis cache to deploy.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The type of Redis cache to deploy. Valid values: (Basic, Standard, Premium). Possible values include: 'Basic', 'Standard',
                           'Premium'"
                    returned: always
                    type: str
                    sample: Standard
                family:
                    description:
                        - "The SKU family to use. Valid values: (C, P). (C = Basic/Standard, P = Premium). Possible values include: 'C', 'P'"
                    returned: always
                    type: str
                    sample: C
                capacity:
                    description:
                        - "The size of the Redis cache to deploy. Valid values: for C (Basic/Standard) family (0, 1, 2, 3, 4, 5, 6), for P (Premium) family
                           (1, 2, 3, 4)."
                    returned: always
                    type: int
                    sample: 6
        port:
            description:
                - Redis non-SSL port.
            returned: always
            type: int
            sample: 6379
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.redis import RedisManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRedisFacts(AzureRMModuleBase):
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
        super(AzureRMRedisFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RedisManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['redis'] = self.get()
        else:
            self.results['redis'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.redis.get(resource_group_name=self.resource_group,
                                                  name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Redis.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.redis.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Redis.')

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
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'family': d.get('sku', {}).get('family', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            },
            'port': d.get('port', None)
        }
        return d


def main():
    AzureRMRedisFacts()


if __name__ == '__main__':
    main()

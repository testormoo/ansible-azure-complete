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
module: azure_rm_redis
version_added: "2.8"
short_description: Manage Azure Redis instance.
description:
    - Create, update and delete instance of Azure Redis.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Redis cache.
        required: True
    redis_configuration:
        description:
            - "All Redis Settings. Few possible keys:
               rdb-backup-enabled,rdb-storage-connection-string,rdb-backup-frequency,maxmemory-delta,maxmemory-policy,notify-keyspace-events,maxmemory-sampl
              es,slowlog-log-slower-than,slowlog-max-len,list-max-ziplist-entries,list-max-ziplist-value,hash-max-ziplist-entries,hash-max-ziplist-value,set
              -max-intset-entries,zset-max-ziplist-entries,zset-max-ziplist-value etc."
    enable_non_ssl_port:
        description:
            - Specifies whether the non-ssl Redis server port (6379) is enabled.
    tenant_settings:
        description:
            - A dictionary of tenant settings
    shard_count:
        description:
            - The number of shards to be created on a Premium Cluster Cache.
    minimum_tls_version:
        description:
            - "Optional: requires clients to use a specified TLS version (or higher) to connect (e,g, 'C(1.0)', 'C(1.1)', 'C(1.2)')."
        choices:
            - '1.0'
            - '1.1'
            - '1.2'
    sku:
        description:
            - The SKU of the Redis cache to deploy.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - "The type of Redis cache to deploy. Valid values: (C(c)(basic), C(c)(standard), C(c)(premium))."
                    - Required when C(state) is I(present).
                choices:
                    - 'basic'
                    - 'standard'
                    - 'premium'
            family:
                description:
                    - "The SKU family to use. Valid values: (C(c), C(p)). (C(c) = C(c)(basic)/C(c)(standard), C(p) = C(c)(premium))."
                    - Required when C(state) is I(present).
                choices:
                    - 'c'
                    - 'p'
            capacity:
                description:
                    - "The size of the Redis cache to deploy. Valid values: for C(c) (C(c)(basic)/C(c)(standard)) I(family) (0, 1, 2, 3, 4, 5, 6), for C(p)
                       (C(c)(premium)) I(family) (1, 2, 3, 4)."
                    - Required when C(state) is I(present).
    subnet_id:
        description:
            - "The full resource ID of a subnet in a virtual network to deploy the Redis cache in. Example format:
               /subscriptions/{subid}/resourceGroups/{I(resource_group)}/Microsoft.{Network|ClassicNetwork}/VirtualNetworks/vnet1/subnets/subnet1"
    static_ip:
        description:
            - Static IP address. Required when deploying a Redis cache inside an existing Azure Virtual Network.
    zones:
        description:
            - A list of availability zones denoting where the resource needs to come from.
        type: list
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
      description:
        - Assert the state of the Redis.
        - Use 'present' to create or update an Redis and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Redis
    azure_rm_redis:
      resource_group: rg1
      name: cache1
      redis_configuration: {
  "maxmemory-policy": "allkeys-lru"
}
      enable_non_ssl_port: True
      shard_count: 2
      minimum_tls_version: 1.2
      sku:
        name: Premium
        family: P
        capacity: 1
      subnet_id: /subscriptions/subid/resourceGroups/rg2/providers/Microsoft.Network/virtualNetworks/network1/subnets/subnet1
      static_ip: 192.168.0.5
      zones:
        - [
  "1"
]
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Cache/Redis/cache1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.redis import RedisManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRedis(AzureRMModuleBase):
    """Configuration class for an Azure RM Redis resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            redis_configuration=dict(
                type='dict'
            ),
            enable_non_ssl_port=dict(
                type='str'
            ),
            tenant_settings=dict(
                type='dict'
            ),
            shard_count=dict(
                type='int'
            ),
            minimum_tls_version=dict(
                type='str',
                choices=['1.0',
                         '1.1',
                         '1.2']
            ),
            sku=dict(
                type='dict'
            ),
            subnet_id=dict(
                type='str'
            ),
            static_ip=dict(
                type='str'
            ),
            zones=dict(
                type='list'
            ),
            location=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRedis, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_camelize(self.parameters, ['sku', 'family'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RedisManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_redis()

        if not old_response:
            self.log("Redis instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Redis instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Redis instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_redis()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Redis instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_redis()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_redis():
                time.sleep(20)
        else:
            self.log("Redis instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_redis(self):
        '''
        Creates or updates Redis with the specified configuration.

        :return: deserialized Redis instance state dictionary
        '''
        self.log("Creating / Updating the Redis instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.redis.create(resource_group_name=self.resource_group,
                                                         name=self.name,
                                                         parameters=self.parameters)
            else:
                response = self.mgmt_client.redis.update(resource_group_name=self.resource_group,
                                                         name=self.name,
                                                         parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Redis instance.')
            self.fail("Error creating the Redis instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_redis(self):
        '''
        Deletes specified Redis instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Redis instance {0}".format(self.name))
        try:
            response = self.mgmt_client.redis.delete(resource_group_name=self.resource_group,
                                                     name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Redis instance.')
            self.fail("Error deleting the Redis instance: {0}".format(str(e)))

        return True

    def get_redis(self):
        '''
        Gets the properties of the specified Redis.

        :return: deserialized Redis instance state dictionary
        '''
        self.log("Checking if the Redis instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.redis.get(resource_group_name=self.resource_group,
                                                  name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Redis instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Redis instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMRedis()


if __name__ == '__main__':
    main()

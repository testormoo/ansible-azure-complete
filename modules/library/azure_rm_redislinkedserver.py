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
module: azure_rm_redislinkedserver
version_added: "2.8"
short_description: Manage Azure Linked Server instance.
description:
    - Create, update and delete instance of Azure Linked Server.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Redis cache.
        required: True
    linked_server_name:
        description:
            - The name of the linked server that is being added to the Redis cache.
        required: True
    linked_redis_cache_id:
        description:
            - Fully qualified resourceId of the linked redis cache.
            - Required when C(state) is I(present).
    linked_redis_cache_location:
        description:
            - Location of the linked redis cache.
            - Required when C(state) is I(present).
    server_role:
        description:
            - Role of the linked server.
            - Required when C(state) is I(present).
        choices:
            - 'primary'
            - 'secondary'
    state:
      description:
        - Assert the state of the Linked Server.
        - Use 'present' to create or update an Linked Server and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Linked Server
    azure_rm_redislinkedserver:
      resource_group: rg1
      name: cache1
      linked_server_name: cache2
      linked_redis_cache_id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Cache/Redis/cache2
      linked_redis_cache_location: West US
      server_role: Secondary
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Cache/Redis/cache1/linkedServers/cache2
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMLinkedServer(AzureRMModuleBase):
    """Configuration class for an Azure RM Linked Server resource"""

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
            linked_server_name=dict(
                type='str',
                required=True
            ),
            linked_redis_cache_id=dict(
                type='str'
            ),
            linked_redis_cache_location=dict(
                type='str'
            ),
            server_role=dict(
                type='str',
                choices=['primary',
                         'secondary']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.linked_server_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLinkedServer, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['server_role'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RedisManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_linkedserver()

        if not old_response:
            self.log("Linked Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Linked Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Linked Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_linkedserver()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Linked Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_linkedserver()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Linked Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_linkedserver(self):
        '''
        Creates or updates Linked Server with the specified configuration.

        :return: deserialized Linked Server instance state dictionary
        '''
        self.log("Creating / Updating the Linked Server instance {0}".format(self.linked_server_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.linked_server.create(resource_group_name=self.resource_group,
                                                                 name=self.name,
                                                                 linked_server_name=self.linked_server_name,
                                                                 parameters=self.parameters)
            else:
                response = self.mgmt_client.linked_server.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Linked Server instance.')
            self.fail("Error creating the Linked Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_linkedserver(self):
        '''
        Deletes specified Linked Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Linked Server instance {0}".format(self.linked_server_name))
        try:
            response = self.mgmt_client.linked_server.delete(resource_group_name=self.resource_group,
                                                             name=self.name,
                                                             linked_server_name=self.linked_server_name)
        except CloudError as e:
            self.log('Error attempting to delete the Linked Server instance.')
            self.fail("Error deleting the Linked Server instance: {0}".format(str(e)))

        return True

    def get_linkedserver(self):
        '''
        Gets the properties of the specified Linked Server.

        :return: deserialized Linked Server instance state dictionary
        '''
        self.log("Checking if the Linked Server instance {0} is present".format(self.linked_server_name))
        found = False
        try:
            response = self.mgmt_client.linked_server.get(resource_group_name=self.resource_group,
                                                          name=self.name,
                                                          linked_server_name=self.linked_server_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Linked Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Linked Server instance.')
        if found is True:
            return response.as_dict()

        return False


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


def main():
    """Main execution"""
    AzureRMLinkedServer()


if __name__ == '__main__':
    main()

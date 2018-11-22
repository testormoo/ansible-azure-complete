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
module: azure_rm_sqlsyncgroup
version_added: "2.8"
short_description: Manage Azure Sync Group instance.
description:
    - Create, update and delete instance of Azure Sync Group.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database on which the sync group is hosted.
        required: True
    name:
        description:
            - The name of the sync group.
        required: True
    interval:
        description:
            - Sync interval of the sync group.
    conflict_resolution_policy:
        description:
            - Conflict resolution policy of the sync group.
        choices:
            - 'hub_win'
            - 'member_win'
    sync_database_id:
        description:
            - ARM resource id of the sync database in the sync group.
    hub_database_user_name:
        description:
            - User name for the sync group hub database credential.
    hub_database_password:
        description:
            - Password for the sync group hub database credential.
    schema:
        description:
            - Sync schema of the sync group.
        suboptions:
            tables:
                description:
                    - List of tables in sync group schema.
                type: list
                suboptions:
                    columns:
                        description:
                            - List of columns in sync group schema.
                        type: list
                        suboptions:
                            quoted_name:
                                description:
                                    - Quoted name of sync group table column.
                            data_size:
                                description:
                                    - Data size of the column.
                            data_type:
                                description:
                                    - Data type of the column.
                    quoted_name:
                        description:
                            - Quoted name of sync group schema table.
            master_sync_member_name:
                description:
                    - Name of master sync member where the schema is from.
    state:
      description:
        - Assert the state of the Sync Group.
        - Use 'present' to create or update an Sync Group and 'absent' to delete it.
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
  - name: Create (or update) Sync Group
    azure_rm_sqlsyncgroup:
      resource_group: syncgroupcrud-65440
      server_name: syncgroupcrud-8475
      database_name: syncgroupcrud-4328
      name: syncgroupcrud-3187
      interval: -1
      conflict_resolution_policy: HubWin
      sync_database_id: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/syncgroupcrud-3521/providers/Microsoft.Sql/servers/syncgroupcrud-8475/databases/syncgroupcrud-4328
      hub_database_user_name: hubUser
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/syncgroupcrud-3521/providers/Microsoft.Sql/servers/syncgroupcrud-8475/databas
            es/syncgroupcrud-4328/syncGroups/syncgroupcrud-3187"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSyncGroup(AzureRMModuleBase):
    """Configuration class for an Azure RM Sync Group resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            database_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            interval=dict(
                type='int'
            ),
            conflict_resolution_policy=dict(
                type='str',
                choices=['hub_win',
                         'member_win']
            ),
            sync_database_id=dict(
                type='str'
            ),
            hub_database_user_name=dict(
                type='str'
            ),
            hub_database_password=dict(
                type='str',
                no_log=True
            ),
            schema=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.database_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSyncGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['conflict_resolution_policy'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_syncgroup()

        if not old_response:
            self.log("Sync Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Sync Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Sync Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_syncgroup()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Sync Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_syncgroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_syncgroup():
                time.sleep(20)
        else:
            self.log("Sync Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_syncgroup(self):
        '''
        Creates or updates Sync Group with the specified configuration.

        :return: deserialized Sync Group instance state dictionary
        '''
        self.log("Creating / Updating the Sync Group instance {0}".format(self.name))

        try:
            response = self.mgmt_client.sync_groups.create_or_update(resource_group_name=self.resource_group,
                                                                     server_name=self.server_name,
                                                                     database_name=self.database_name,
                                                                     sync_group_name=self.name,
                                                                     parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Sync Group instance.')
            self.fail("Error creating the Sync Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_syncgroup(self):
        '''
        Deletes specified Sync Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Sync Group instance {0}".format(self.name))
        try:
            response = self.mgmt_client.sync_groups.delete(resource_group_name=self.resource_group,
                                                           server_name=self.server_name,
                                                           database_name=self.database_name,
                                                           sync_group_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Sync Group instance.')
            self.fail("Error deleting the Sync Group instance: {0}".format(str(e)))

        return True

    def get_syncgroup(self):
        '''
        Gets the properties of the specified Sync Group.

        :return: deserialized Sync Group instance state dictionary
        '''
        self.log("Checking if the Sync Group instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.sync_groups.get(resource_group_name=self.resource_group,
                                                        server_name=self.server_name,
                                                        database_name=self.database_name,
                                                        sync_group_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Sync Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Sync Group instance.')
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
    AzureRMSyncGroup()


if __name__ == '__main__':
    main()

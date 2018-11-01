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
module: azure_rm_sqlsyncmember
version_added: "2.8"
short_description: Manage Sync Member instance.
description:
    - Create, update and delete instance of Sync Member.

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
    sync_group_name:
        description:
            - The name of the sync group on which the sync member is hosted.
        required: True
    sync_member_name:
        description:
            - The name of the sync member.
        required: True
    database_type:
        description:
            - Database type of the sync member.
        choices:
            - 'azure_sql_database'
            - 'sql_server_database'
    sync_agent_id:
        description:
            - ARM resource id of the sync agent in the sync member.
    sql_server_database_id:
        description:
            - SQL Server database id of the sync member.
    server_name:
        description:
            - Server name of the member database in the sync member
    database_name:
        description:
            - Database name of the member database in the sync member.
    user_name:
        description:
            - User name of the member database in the sync member.
    password:
        description:
            - Password of the member database in the sync member.
    sync_direction:
        description:
            - Sync direction of the sync member.
        choices:
            - 'bidirectional'
            - 'one_way_member_to_hub'
            - 'one_way_hub_to_member'
    state:
      description:
        - Assert the state of the Sync Member.
        - Use 'present' to create or update an Sync Member and 'absent' to delete it.
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
  - name: Create (or update) Sync Member
    azure_rm_sqlsyncmember:
      resource_group: syncgroupcrud-65440
      server_name: syncgroupcrud-8475
      database_name: syncgroupcrud-4328
      sync_group_name: syncgroupcrud-3187
      sync_member_name: syncgroupcrud-4879
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/syncgroupcrud-65440/providers/Microsoft.Sql/servers/syncgroupcrud-8475/databa
            ses/syncgroupcrud-4328/syncGroups/syncgroupcrud-3187/syncMembers/syncgroupcrud-4879"
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


class AzureRMSyncMembers(AzureRMModuleBase):
    """Configuration class for an Azure RM Sync Member resource"""

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
            sync_group_name=dict(
                type='str',
                required=True
            ),
            sync_member_name=dict(
                type='str',
                required=True
            ),
            database_type=dict(
                type='str',
                choices=['azure_sql_database',
                         'sql_server_database']
            ),
            sync_agent_id=dict(
                type='str'
            ),
            sql_server_database_id=dict(
                type='str'
            ),
            server_name=dict(
                type='str'
            ),
            database_name=dict(
                type='str'
            ),
            user_name=dict(
                type='str'
            ),
            password=dict(
                type='str',
                no_log=True
            ),
            sync_direction=dict(
                type='str',
                choices=['bidirectional',
                         'one_way_member_to_hub',
                         'one_way_hub_to_member']
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
        self.sync_group_name = None
        self.sync_member_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSyncMembers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "database_type":
                    self.parameters["database_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "sync_agent_id":
                    self.parameters["sync_agent_id"] = kwargs[key]
                elif key == "sql_server_database_id":
                    self.parameters["sql_server_database_id"] = kwargs[key]
                elif key == "server_name":
                    self.parameters["server_name"] = kwargs[key]
                elif key == "database_name":
                    self.parameters["database_name"] = kwargs[key]
                elif key == "user_name":
                    self.parameters["user_name"] = kwargs[key]
                elif key == "password":
                    self.parameters["password"] = kwargs[key]
                elif key == "sync_direction":
                    self.parameters["sync_direction"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_syncmember()

        if not old_response:
            self.log("Sync Member instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Sync Member instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Sync Member instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Sync Member instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_syncmember()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Sync Member instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_syncmember()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_syncmember():
                time.sleep(20)
        else:
            self.log("Sync Member instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_syncmember(self):
        '''
        Creates or updates Sync Member with the specified configuration.

        :return: deserialized Sync Member instance state dictionary
        '''
        self.log("Creating / Updating the Sync Member instance {0}".format(self.sync_member_name))

        try:
            response = self.mgmt_client.sync_members.create_or_update(resource_group_name=self.resource_group,
                                                                      server_name=self.server_name,
                                                                      database_name=self.database_name,
                                                                      sync_group_name=self.sync_group_name,
                                                                      sync_member_name=self.sync_member_name,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Sync Member instance.')
            self.fail("Error creating the Sync Member instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_syncmember(self):
        '''
        Deletes specified Sync Member instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Sync Member instance {0}".format(self.sync_member_name))
        try:
            response = self.mgmt_client.sync_members.delete(resource_group_name=self.resource_group,
                                                            server_name=self.server_name,
                                                            database_name=self.database_name,
                                                            sync_group_name=self.sync_group_name,
                                                            sync_member_name=self.sync_member_name)
        except CloudError as e:
            self.log('Error attempting to delete the Sync Member instance.')
            self.fail("Error deleting the Sync Member instance: {0}".format(str(e)))

        return True

    def get_syncmember(self):
        '''
        Gets the properties of the specified Sync Member.

        :return: deserialized Sync Member instance state dictionary
        '''
        self.log("Checking if the Sync Member instance {0} is present".format(self.sync_member_name))
        found = False
        try:
            response = self.mgmt_client.sync_members.get(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         database_name=self.database_name,
                                                         sync_group_name=self.sync_group_name,
                                                         sync_member_name=self.sync_member_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Sync Member instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Sync Member instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMSyncMembers()


if __name__ == '__main__':
    main()

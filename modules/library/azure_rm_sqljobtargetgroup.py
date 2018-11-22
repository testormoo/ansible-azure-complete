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
module: azure_rm_sqljobtargetgroup
version_added: "2.8"
short_description: Manage Azure Job Target Group instance.
description:
    - Create, update and delete instance of Azure Job Target Group.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    job_agent_name:
        description:
            - The name of the job agent.
        required: True
    name:
        description:
            - The name of the target group.
        required: True
    membership_type:
        description:
            - Whether the target is included or excluded from the group.
        choices:
            - 'include'
            - 'exclude'
    type:
        description:
            - The target type.
            - Required when C(state) is I(present).
        choices:
            - 'target_group'
            - 'sql_database'
            - 'sql_elastic_pool'
            - 'sql_shard_map'
            - 'sql_server'
    server_name:
        description:
            - The target server name.
    database_name:
        description:
            - The target database name.
    elastic_pool_name:
        description:
            - The target elastic pool name.
    shard_map_name:
        description:
            - The target shard map.
    refresh_credential:
        description:
            - "The resource ID of the credential that is used during job execution to connect to the target and determine the list of databases inside the
               target."
    state:
      description:
        - Assert the state of the Job Target Group.
        - Use 'present' to create or update an Job Target Group and 'absent' to delete it.
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
  - name: Create (or update) Job Target Group
    azure_rm_sqljobtargetgroup:
      resource_group: group1
      server_name: server1
      job_agent_name: agent1
      name: targetGroup1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/targetGroups/
            targetGroup1"
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


class AzureRMJobTargetGroup(AzureRMModuleBase):
    """Configuration class for an Azure RM Job Target Group resource"""

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
            job_agent_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            membership_type=dict(
                type='str',
                choices=['include',
                         'exclude']
            ),
            type=dict(
                type='str',
                choices=['target_group',
                         'sql_database',
                         'sql_elastic_pool',
                         'sql_shard_map',
                         'sql_server']
            ),
            server_name=dict(
                type='str'
            ),
            database_name=dict(
                type='str'
            ),
            elastic_pool_name=dict(
                type='str'
            ),
            shard_map_name=dict(
                type='str'
            ),
            refresh_credential=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.job_agent_name = None
        self.name = None
        self.members = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobTargetGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.members[key] = kwargs[key]

        dict_camelize(self.members, ['membership_type'], True)
        dict_camelize(self.members, ['type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_jobtargetgroup()

        if not old_response:
            self.log("Job Target Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job Target Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.members, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Target Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobtargetgroup()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job Target Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_jobtargetgroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_jobtargetgroup():
                time.sleep(20)
        else:
            self.log("Job Target Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_jobtargetgroup(self):
        '''
        Creates or updates Job Target Group with the specified configuration.

        :return: deserialized Job Target Group instance state dictionary
        '''
        self.log("Creating / Updating the Job Target Group instance {0}".format(self.name))

        try:
            response = self.mgmt_client.job_target_groups.create_or_update(resource_group_name=self.resource_group,
                                                                           server_name=self.server_name,
                                                                           job_agent_name=self.job_agent_name,
                                                                           target_group_name=self.name,
                                                                           members=self.members)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job Target Group instance.')
            self.fail("Error creating the Job Target Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_jobtargetgroup(self):
        '''
        Deletes specified Job Target Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job Target Group instance {0}".format(self.name))
        try:
            response = self.mgmt_client.job_target_groups.delete(resource_group_name=self.resource_group,
                                                                 server_name=self.server_name,
                                                                 job_agent_name=self.job_agent_name,
                                                                 target_group_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Job Target Group instance.')
            self.fail("Error deleting the Job Target Group instance: {0}".format(str(e)))

        return True

    def get_jobtargetgroup(self):
        '''
        Gets the properties of the specified Job Target Group.

        :return: deserialized Job Target Group instance state dictionary
        '''
        self.log("Checking if the Job Target Group instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.job_target_groups.get(resource_group_name=self.resource_group,
                                                              server_name=self.server_name,
                                                              job_agent_name=self.job_agent_name,
                                                              target_group_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Target Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Target Group instance.')
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
    AzureRMJobTargetGroup()


if __name__ == '__main__':
    main()

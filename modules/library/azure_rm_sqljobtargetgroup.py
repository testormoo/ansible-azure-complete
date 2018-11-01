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
short_description: Manage Job Target Group instance.
description:
    - Create, update and delete instance of Job Target Group.

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
    target_group_name:
        description:
            - The name of the target group.
        required: True
    members:
        description:
            - Members of the target group.
        required: True
        type: list
        suboptions:
            membership_type:
                description:
                    - Whether the target is included or excluded from the group.
                choices:
                    - 'include'
                    - 'exclude'
            type:
                description:
                    - The target type.
                required: True
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
                    - "The resource ID of the credential that is used during job execution to connect to the target and determine the list of databases
                       inside the target."
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
      target_group_name: targetGroup1
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


class AzureRMJobTargetGroups(AzureRMModuleBase):
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
            target_group_name=dict(
                type='str',
                required=True
            ),
            members=dict(
                type='list',
                required=True
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
        self.target_group_name = None
        self.members = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobTargetGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "membership_type":
                    self.members["membership_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "type":
                    self.members["type"] = _snake_to_camel(kwargs[key], True)
                elif key == "server_name":
                    self.members["server_name"] = kwargs[key]
                elif key == "database_name":
                    self.members["database_name"] = kwargs[key]
                elif key == "elastic_pool_name":
                    self.members["elastic_pool_name"] = kwargs[key]
                elif key == "shard_map_name":
                    self.members["shard_map_name"] = kwargs[key]
                elif key == "refresh_credential":
                    self.members["refresh_credential"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Job Target Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Target Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobtargetgroup()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_jobtargetgroup(self):
        '''
        Creates or updates Job Target Group with the specified configuration.

        :return: deserialized Job Target Group instance state dictionary
        '''
        self.log("Creating / Updating the Job Target Group instance {0}".format(self.target_group_name))

        try:
            response = self.mgmt_client.job_target_groups.create_or_update(resource_group_name=self.resource_group,
                                                                           server_name=self.server_name,
                                                                           job_agent_name=self.job_agent_name,
                                                                           target_group_name=self.target_group_name,
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
        self.log("Deleting the Job Target Group instance {0}".format(self.target_group_name))
        try:
            response = self.mgmt_client.job_target_groups.delete(resource_group_name=self.resource_group,
                                                                 server_name=self.server_name,
                                                                 job_agent_name=self.job_agent_name,
                                                                 target_group_name=self.target_group_name)
        except CloudError as e:
            self.log('Error attempting to delete the Job Target Group instance.')
            self.fail("Error deleting the Job Target Group instance: {0}".format(str(e)))

        return True

    def get_jobtargetgroup(self):
        '''
        Gets the properties of the specified Job Target Group.

        :return: deserialized Job Target Group instance state dictionary
        '''
        self.log("Checking if the Job Target Group instance {0} is present".format(self.target_group_name))
        found = False
        try:
            response = self.mgmt_client.job_target_groups.get(resource_group_name=self.resource_group,
                                                              server_name=self.server_name,
                                                              job_agent_name=self.job_agent_name,
                                                              target_group_name=self.target_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Target Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Target Group instance.')
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
    AzureRMJobTargetGroups()


if __name__ == '__main__':
    main()

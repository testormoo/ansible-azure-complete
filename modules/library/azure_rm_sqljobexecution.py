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
module: azure_rm_sqljobexecution
version_added: "2.8"
short_description: Manage Job Execution instance.
description:
    - Create, update and delete instance of Job Execution.

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
    job_name:
        description:
            - The name of the job to get.
        required: True
    job_execution_id:
        description:
            - The job execution id to create the job execution under.
        required: True
    state:
      description:
        - Assert the state of the Job Execution.
        - Use 'present' to create or update an Job Execution and 'absent' to delete it.
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
  - name: Create (or update) Job Execution
    azure_rm_sqljobexecution:
      resource_group: group1
      server_name: server1
      job_agent_name: agent1
      job_name: job1
      job_execution_id: 5555-6666-7777-8888-999999999999
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/jobs/job1/exe
            cutions/5555-6666-7777-8888-999999999999"
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


class AzureRMJobExecutions(AzureRMModuleBase):
    """Configuration class for an Azure RM Job Execution resource"""

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
            job_name=dict(
                type='str',
                required=True
            ),
            job_execution_id=dict(
                type='str',
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
        self.job_name = None
        self.job_execution_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobExecutions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_jobexecution()

        if not old_response:
            self.log("Job Execution instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job Execution instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Job Execution instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Execution instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobexecution()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job Execution instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_jobexecution()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_jobexecution():
                time.sleep(20)
        else:
            self.log("Job Execution instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_jobexecution(self):
        '''
        Creates or updates Job Execution with the specified configuration.

        :return: deserialized Job Execution instance state dictionary
        '''
        self.log("Creating / Updating the Job Execution instance {0}".format(self.job_execution_id))

        try:
            response = self.mgmt_client.job_executions.create_or_update(resource_group_name=self.resource_group,
                                                                        server_name=self.server_name,
                                                                        job_agent_name=self.job_agent_name,
                                                                        job_name=self.job_name,
                                                                        job_execution_id=self.job_execution_id)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job Execution instance.')
            self.fail("Error creating the Job Execution instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_jobexecution(self):
        '''
        Deletes specified Job Execution instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job Execution instance {0}".format(self.job_execution_id))
        try:
            response = self.mgmt_client.job_executions.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Job Execution instance.')
            self.fail("Error deleting the Job Execution instance: {0}".format(str(e)))

        return True

    def get_jobexecution(self):
        '''
        Gets the properties of the specified Job Execution.

        :return: deserialized Job Execution instance state dictionary
        '''
        self.log("Checking if the Job Execution instance {0} is present".format(self.job_execution_id))
        found = False
        try:
            response = self.mgmt_client.job_executions.get(resource_group_name=self.resource_group,
                                                           server_name=self.server_name,
                                                           job_agent_name=self.job_agent_name,
                                                           job_name=self.job_name,
                                                           job_execution_id=self.job_execution_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Execution instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Execution instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMJobExecutions()


if __name__ == '__main__':
    main()

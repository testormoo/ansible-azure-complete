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
module: azure_rm_sqljobstep
version_added: "2.8"
short_description: Manage Job Step instance.
description:
    - Create, update and delete instance of Job Step.

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
            - The name of the job.
        required: True
    step_name:
        description:
            - The name of the job step.
        required: True
    step_id:
        description:
            - "The job step's index within the job. If not specified when creating the job step, it will be created as the last step. If not specified when
               updating the job step, the step id is not modified."
    target_group:
        description:
            - The resource ID of the target group that the job step will be executed on.
        required: True
    credential:
        description:
            - The resource ID of the job credential that will be used to connect to the targets.
        required: True
    action:
        description:
            - The action payload of the job step.
        required: True
        suboptions:
            type:
                description:
                    - Type of action being executed by the job step.
                choices:
                    - 'tsql'
            source:
                description:
                    - The source of the action to execute.
                choices:
                    - 'inline'
            value:
                description:
                    - The action value, for example the text of the T-SQL script to execute.
                required: True
    output:
        description:
            - Output destination properties of the job step.
        suboptions:
            type:
                description:
                    - The output destination type.
                choices:
                    - 'sql_database'
            subscription_id:
                description:
                    - The output destination subscription id.
            resource_group_name:
                description:
                    - The output destination resource group.
            server_name:
                description:
                    - The output destination server name.
                required: True
            database_name:
                description:
                    - The output destination database.
                required: True
            schema_name:
                description:
                    - The output destination schema.
            table_name:
                description:
                    - The output destination table.
                required: True
            credential:
                description:
                    - The resource ID of the credential to use to connect to the output destination.
                required: True
    execution_options:
        description:
            - Execution options for the job step.
        suboptions:
            timeout_seconds:
                description:
                    - Execution timeout for the job step.
            retry_attempts:
                description:
                    - Maximum number of times the job step will be reattempted if the first attempt fails.
            initial_retry_interval_seconds:
                description:
                    - Initial delay between retries for job step execution.
            maximum_retry_interval_seconds:
                description:
                    - The maximum amount of time to wait between retries for job step execution.
            retry_interval_backoff_multiplier:
                description:
                    - The backoff multiplier for the time between retries.
    state:
      description:
        - Assert the state of the Job Step.
        - Use 'present' to create or update an Job Step and 'absent' to delete it.
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
  - name: Create (or update) Job Step
    azure_rm_sqljobstep:
      resource_group: group1
      server_name: server1
      job_agent_name: agent1
      job_name: job1
      step_name: step1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/jobs/job1/ste
            ps/step1"
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


class AzureRMJobSteps(AzureRMModuleBase):
    """Configuration class for an Azure RM Job Step resource"""

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
            step_name=dict(
                type='str',
                required=True
            ),
            step_id=dict(
                type='int'
            ),
            target_group=dict(
                type='str',
                required=True
            ),
            credential=dict(
                type='str',
                required=True
            ),
            action=dict(
                type='dict',
                required=True
            ),
            output=dict(
                type='dict'
            ),
            execution_options=dict(
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
        self.job_agent_name = None
        self.job_name = None
        self.step_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobSteps, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "step_id":
                    self.parameters["step_id"] = kwargs[key]
                elif key == "target_group":
                    self.parameters["target_group"] = kwargs[key]
                elif key == "credential":
                    self.parameters["credential"] = kwargs[key]
                elif key == "action":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'tsql':
                            ev['type'] = 'TSql'
                    if 'source' in ev:
                        if ev['source'] == 'inline':
                            ev['source'] = 'Inline'
                    self.parameters["action"] = ev
                elif key == "output":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'sql_database':
                            ev['type'] = 'SqlDatabase'
                    self.parameters["output"] = ev
                elif key == "execution_options":
                    self.parameters["execution_options"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_jobstep()

        if not old_response:
            self.log("Job Step instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job Step instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Job Step instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Step instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobstep()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job Step instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_jobstep()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_jobstep():
                time.sleep(20)
        else:
            self.log("Job Step instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_jobstep(self):
        '''
        Creates or updates Job Step with the specified configuration.

        :return: deserialized Job Step instance state dictionary
        '''
        self.log("Creating / Updating the Job Step instance {0}".format(self.step_name))

        try:
            response = self.mgmt_client.job_steps.create_or_update(resource_group_name=self.resource_group,
                                                                   server_name=self.server_name,
                                                                   job_agent_name=self.job_agent_name,
                                                                   job_name=self.job_name,
                                                                   step_name=self.step_name,
                                                                   parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job Step instance.')
            self.fail("Error creating the Job Step instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_jobstep(self):
        '''
        Deletes specified Job Step instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job Step instance {0}".format(self.step_name))
        try:
            response = self.mgmt_client.job_steps.delete(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         job_agent_name=self.job_agent_name,
                                                         job_name=self.job_name,
                                                         step_name=self.step_name)
        except CloudError as e:
            self.log('Error attempting to delete the Job Step instance.')
            self.fail("Error deleting the Job Step instance: {0}".format(str(e)))

        return True

    def get_jobstep(self):
        '''
        Gets the properties of the specified Job Step.

        :return: deserialized Job Step instance state dictionary
        '''
        self.log("Checking if the Job Step instance {0} is present".format(self.step_name))
        found = False
        try:
            response = self.mgmt_client.job_steps.get(resource_group_name=self.resource_group,
                                                      server_name=self.server_name,
                                                      job_agent_name=self.job_agent_name,
                                                      job_name=self.job_name,
                                                      step_name=self.step_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Step instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Step instance.')
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
    AzureRMJobSteps()


if __name__ == '__main__':
    main()

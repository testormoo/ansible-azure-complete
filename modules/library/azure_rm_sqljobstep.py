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
short_description: Manage Azure Job Step instance.
description:
    - Create, update and delete instance of Azure Job Step.

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
    name:
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
            - Required when C(state) is I(present).
    credential:
        description:
            - The resource ID of the job credential that will be used to connect to the targets.
            - Required when C(state) is I(present).
    action:
        description:
            - The action payload of the job step.
            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
            database_name:
                description:
                    - The output destination database.
                    - Required when C(state) is I(present).
            schema_name:
                description:
                    - The output destination schema.
            table_name:
                description:
                    - The output destination table.
                    - Required when C(state) is I(present).
            credential:
                description:
                    - The resource ID of the credential to use to connect to the output destination.
                    - Required when C(state) is I(present).
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
      name: step1
      target_group: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/targetGroups/targetGroup0
      credential: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/credentials/cred0
      action:
        value: select 1
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMJobStep(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            step_id=dict(
                type='int'
            ),
            target_group=dict(
                type='str'
            ),
            credential=dict(
                type='str'
            ),
            action=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str',
                        choices=['tsql']
                    ),
                    source=dict(
                        type='str',
                        choices=['inline']
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            output=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str',
                        choices=['sql_database']
                    ),
                    subscription_id=dict(
                        type='str'
                    ),
                    resource_group_name=dict(
                        type='str'
                    ),
                    server_name=dict(
                        type='str'
                    ),
                    database_name=dict(
                        type='str'
                    ),
                    schema_name=dict(
                        type='str'
                    ),
                    table_name=dict(
                        type='str'
                    ),
                    credential=dict(
                        type='str'
                    )
                )
            ),
            execution_options=dict(
                type='dict',
                options=dict(
                    timeout_seconds=dict(
                        type='int'
                    ),
                    retry_attempts=dict(
                        type='int'
                    ),
                    initial_retry_interval_seconds=dict(
                        type='int'
                    ),
                    maximum_retry_interval_seconds=dict(
                        type='int'
                    ),
                    retry_interval_backoff_multiplier=dict(
                        type='float'
                    )
                )
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobStep, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['action', 'type'], True)
        dict_map(self.parameters, ['action', 'type'], {'tsql': 'TSql'})
        dict_camelize(self.parameters, ['action', 'source'], True)
        dict_camelize(self.parameters, ['output', 'type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Step instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobstep()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job Step instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_jobstep()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Job Step instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_jobstep(self):
        '''
        Creates or updates Job Step with the specified configuration.

        :return: deserialized Job Step instance state dictionary
        '''
        self.log("Creating / Updating the Job Step instance {0}".format(self.name))

        try:
            response = self.mgmt_client.job_steps.create_or_update(resource_group_name=self.resource_group,
                                                                   server_name=self.server_name,
                                                                   job_agent_name=self.job_agent_name,
                                                                   job_name=self.job_name,
                                                                   step_name=self.name,
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
        self.log("Deleting the Job Step instance {0}".format(self.name))
        try:
            response = self.mgmt_client.job_steps.delete(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         job_agent_name=self.job_agent_name,
                                                         job_name=self.job_name,
                                                         step_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Job Step instance.')
            self.fail("Error deleting the Job Step instance: {0}".format(str(e)))

        return True

    def get_jobstep(self):
        '''
        Gets the properties of the specified Job Step.

        :return: deserialized Job Step instance state dictionary
        '''
        self.log("Checking if the Job Step instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.job_steps.get(resource_group_name=self.resource_group,
                                                      server_name=self.server_name,
                                                      job_agent_name=self.job_agent_name,
                                                      job_name=self.job_name,
                                                      step_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Step instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Step instance.')
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
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


def main():
    """Main execution"""
    AzureRMJobStep()


if __name__ == '__main__':
    main()

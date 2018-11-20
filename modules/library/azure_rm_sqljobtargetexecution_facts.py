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
module: azure_rm_sqljobtargetexecution_facts
version_added: "2.8"
short_description: Get Azure Job Target Execution facts.
description:
    - Get facts of Azure Job Target Execution.

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
            - The id of the job execution
        required: True
    name:
        description:
            - The name of the step.
    create_time_min:
        description:
            - If specified, only job executions created at or after the specified time are included.
    create_time_max:
        description:
            - If specified, only job executions created before the specified time are included.
    end_time_min:
        description:
            - If specified, only job executions completed at or after the specified time are included.
    end_time_max:
        description:
            - If specified, only job executions completed before the specified time are included.
    is_active:
        description:
            - If specified, only active or only completed job executions are included.
    skip:
        description:
            - The number of elements in the collection to skip.
    top:
        description:
            - The number of elements to return from the collection.
    target_id:
        description:
            - The target id.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Job Target Execution
    azure_rm_sqljobtargetexecution_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      job_name: job_name
      job_execution_id: job_execution_id
      name: step_name
      create_time_min: create_time_min
      create_time_max: create_time_max
      end_time_min: end_time_min
      end_time_max: end_time_max
      is_active: is_active
      skip: skip
      top: top

  - name: List instances of Job Target Execution
    azure_rm_sqljobtargetexecution_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      job_name: job_name
      job_execution_id: job_execution_id
      create_time_min: create_time_min
      create_time_max: create_time_max
      end_time_min: end_time_min
      end_time_max: end_time_max
      is_active: is_active
      skip: skip
      top: top

  - name: Get instance of Job Target Execution
    azure_rm_sqljobtargetexecution_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      job_name: job_name
      job_execution_id: job_execution_id
      name: step_name
      target_id: target_id
'''

RETURN = '''
job_target_executions:
    description: A list of dictionaries containing facts for Job Target Execution.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/jobs/
                    job1/executions/5555-6666-7777-8888-999999999999/steps/step1/targets/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
        lifecycle:
            description:
                - "The detailed state of the job execution. Possible values include: 'Created', 'InProgress', 'WaitingForChildJobExecutions',
                   'WaitingForRetry', 'Succeeded', 'SucceededWithSkipped', 'Failed', 'TimedOut', 'Canceled', 'Skipped'"
            returned: always
            type: str
            sample: Succeeded
        target:
            description:
                - The target that this execution is executed on.
            returned: always
            type: complex
            sample: target
            contains:
                type:
                    description:
                        - "The type of the target. Possible values include: 'TargetGroup', 'SqlDatabase', 'SqlElasticPool', 'SqlShardMap', 'SqlServer'"
                    returned: always
                    type: str
                    sample: SqlDatabase
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobTargetExecutionsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
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
            name=dict(
                type='str'
            ),
            create_time_min=dict(
                type='datetime'
            ),
            create_time_max=dict(
                type='datetime'
            ),
            end_time_min=dict(
                type='datetime'
            ),
            end_time_max=dict(
                type='datetime'
            ),
            is_active=dict(
                type='str'
            ),
            skip=dict(
                type='int'
            ),
            top=dict(
                type='int'
            ),
            target_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.server_name = None
        self.job_agent_name = None
        self.job_name = None
        self.job_execution_id = None
        self.name = None
        self.create_time_min = None
        self.create_time_max = None
        self.end_time_min = None
        self.end_time_max = None
        self.is_active = None
        self.skip = None
        self.top = None
        self.target_id = None
        super(AzureRMJobTargetExecutionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['job_target_executions'] = self.list_by_step()
        else:
            self.results['job_target_executions'] = self.list_by_job_execution()
        elif (self.name is not None and
                self.target_id is not None):
            self.results['job_target_executions'] = self.get()
        return self.results

    def list_by_step(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_target_executions.list_by_step(resource_group_name=self.resource_group,
                                                                           server_name=self.server_name,
                                                                           job_agent_name=self.job_agent_name,
                                                                           job_name=self.job_name,
                                                                           job_execution_id=self.job_execution_id,
                                                                           step_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobTargetExecutions.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_job_execution(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_target_executions.list_by_job_execution(resource_group_name=self.resource_group,
                                                                                    server_name=self.server_name,
                                                                                    job_agent_name=self.job_agent_name,
                                                                                    job_name=self.job_name,
                                                                                    job_execution_id=self.job_execution_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobTargetExecutions.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_target_executions.get(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  job_agent_name=self.job_agent_name,
                                                                  job_name=self.job_name,
                                                                  job_execution_id=self.job_execution_id,
                                                                  step_name=self.name,
                                                                  target_id=self.target_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobTargetExecutions.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'lifecycle': d.get('lifecycle', None),
            'target': {
                'type': d.get('target', {}).get('type', None)
            }
        }
        return d


def main():
    AzureRMJobTargetExecutionsFacts()


if __name__ == '__main__':
    main()

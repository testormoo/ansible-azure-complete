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
module: azure_rm_sqljobstep_facts
version_added: "2.8"
short_description: Get Azure Job Step facts.
description:
    - Get facts of Azure Job Step.

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
    job_version:
        description:
            - The version of the job to get.
    name:
        description:
            - The name of the job step.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Job Step
    azure_rm_sqljobstep_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      job_name: job_name
      job_version: job_version

  - name: Get instance of Job Step
    azure_rm_sqljobstep_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      job_name: job_name
      name: step_name

  - name: List instances of Job Step
    azure_rm_sqljobstep_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      job_name: job_name
'''

RETURN = '''
job_steps:
    description: A list of dictionaries containing facts for Job Step.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/jobs/
                    job1/steps/step1"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: step1
        credential:
            description:
                - The resource ID of the job credential that will be used to connect to the targets.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/crede
                    ntials/cred1"
        action:
            description:
                - The action payload of the job step.
            returned: always
            type: complex
            sample: action
            contains:
                type:
                    description:
                        - "Type of action being executed by the job step. Possible values include: 'TSql'"
                    returned: always
                    type: str
                    sample: TSql
                source:
                    description:
                        - "The source of the action to execute. Possible values include: 'Inline'"
                    returned: always
                    type: str
                    sample: Inline
                value:
                    description:
                        - The action value, for example the text of the T-SQL script to execute.
                    returned: always
                    type: str
                    sample: select 2
        output:
            description:
                - Output destination properties of the job step.
            returned: always
            type: complex
            sample: output
            contains:
                type:
                    description:
                        - "The output destination type. Possible values include: 'SqlDatabase'"
                    returned: always
                    type: str
                    sample: SqlDatabase
                credential:
                    description:
                        - The resource ID of the credential to use to connect to the output destination.
                    returned: always
                    type: str
                    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agen
                            t1/credentials/cred0"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobStepsFacts(AzureRMModuleBase):
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
            job_version=dict(
                type='int'
            ),
            name=dict(
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
        self.job_version = None
        self.name = None
        super(AzureRMJobStepsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.job_version is not None:
            self.results['job_steps'] = self.list_by_version()
        elif self.name is not None:
            self.results['job_steps'] = self.get()
        else:
            self.results['job_steps'] = self.list_by_job()
        return self.results

    def list_by_version(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_steps.list_by_version(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  job_agent_name=self.job_agent_name,
                                                                  job_name=self.job_name,
                                                                  job_version=self.job_version)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobSteps.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_steps.get(resource_group_name=self.resource_group,
                                                      server_name=self.server_name,
                                                      job_agent_name=self.job_agent_name,
                                                      job_name=self.job_name,
                                                      step_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobSteps.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_job(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_steps.list_by_job(resource_group_name=self.resource_group,
                                                              server_name=self.server_name,
                                                              job_agent_name=self.job_agent_name,
                                                              job_name=self.job_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobSteps.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'credential': d.get('credential', None),
            'action': {
                'type': d.get('action', {}).get('type', None),
                'source': d.get('action', {}).get('source', None),
                'value': d.get('action', {}).get('value', None)
            },
            'output': {
                'type': d.get('output', {}).get('type', None),
                'credential': d.get('output', {}).get('credential', None)
            }
        }
        return d


def main():
    AzureRMJobStepsFacts()


if __name__ == '__main__':
    main()

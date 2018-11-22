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
module: azure_rm_sqljobversion_facts
version_added: "2.8"
short_description: Get Azure Job Version facts.
description:
    - Get facts of Azure Job Version.

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
            - The name of the job.
        required: True
    job_version:
        description:
            - The version of the job to get.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Job Version
    azure_rm_sqljobversion_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      name: job_name
      job_version: job_version

  - name: List instances of Job Version
    azure_rm_sqljobversion_facts:
      resource_group: resource_group_name
      server_name: server_name
      job_agent_name: job_agent_name
      name: job_name
'''

RETURN = '''
job_versions:
    description: A list of dictionaries containing facts for Job Version.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1/jobs/
                    job1/versions/1"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobVersionFacts(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            job_version=dict(
                type='int'
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
        self.name = None
        self.job_version = None
        super(AzureRMJobVersionFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.job_version is not None:
            self.results['job_versions'] = self.get()
        else:
            self.results['job_versions'] = self.list_by_job()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_versions.get(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         job_agent_name=self.job_agent_name,
                                                         job_name=self.name,
                                                         job_version=self.job_version)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job Version.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_job(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_versions.list_by_job(resource_group_name=self.resource_group,
                                                                 server_name=self.server_name,
                                                                 job_agent_name=self.job_agent_name,
                                                                 job_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job Version.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMJobVersionFacts()


if __name__ == '__main__':
    main()

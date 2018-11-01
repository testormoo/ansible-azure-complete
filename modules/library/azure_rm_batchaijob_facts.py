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
module: azure_rm_batchaijob_facts
version_added: "2.8"
short_description: Get Azure Job facts.
description:
    - Get facts of Azure Job.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    job_name:
        description:
            - "The name of the job within the specified resource group. Job names can only contain a combination of alphanumeric characters along with dash
               (-) and underscore (_). The name must be from 1 through 64 characters long."
    jobs_list_by_resource_group_options:
        description:
            - Additional parameters for the operation
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Job
    azure_rm_batchaijob_facts:
      resource_group: resource_group_name
      job_name: job_name

  - name: List instances of Job
    azure_rm_batchaijob_facts:
      resource_group: resource_group_name
      jobs_list_by_resource_group_options: jobs_list_by_resource_group_options
'''

RETURN = '''
jobs:
    description: A list of dictionaries containing facts for Job.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The ID of the resource
            returned: always
            type: str
            sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.BatchAI/jobs/job
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: job
        tags:
            description:
                - The tags of the resource
            returned: always
            type: complex
            sample: tags
        priority:
            description:
                - "Priority associated with the job. Priority values can range from -1000 to 1000, with -1000 being the lowest priority and 1000 being the
                   highest priority. The default value is 0."
            returned: always
            type: int
            sample: 0
        cluster:
            description:
                -
            returned: always
            type: complex
            sample: cluster
            contains:
                id:
                    description:
                        - The ID of the resource
                    returned: always
                    type: str
                    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.BatchAI/clusters/demo
                            _cluster"
        constraints:
            description:
                - Constraints associated with the Job.
            returned: always
            type: complex
            sample: constraints
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.batchai import BatchAIManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            job_name=dict(
                type='str'
            ),
            jobs_list_by_resource_group_options=dict(
                type='dict'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.job_name = None
        self.jobs_list_by_resource_group_options = None
        self.tags = None
        super(AzureRMJobsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(BatchAIManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.job_name is not None:
            self.results['jobs'] = self.get()
        else:
            self.results['jobs'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.get(resource_group_name=self.resource_group,
                                                 job_name=self.job_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Jobs.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Jobs.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'priority': d.get('priority', None),
            'cluster': {
                'id': d.get('cluster', {}).get('id', None)
            },
            'constraints': {
            }
        }
        return d


def main():
    AzureRMJobsFacts()


if __name__ == '__main__':
    main()

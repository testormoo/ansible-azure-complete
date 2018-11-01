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
module: azure_rm_mediajob_facts
version_added: "2.8"
short_description: Get Azure Job facts.
description:
    - Get facts of Azure Job.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    transform_name:
        description:
            - The Transform name.
        required: True
    job_name:
        description:
            - The Job name.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Job
    azure_rm_mediajob_facts:
      resource_group: resource_group_name
      account_name: account_name
      transform_name: transform_name
      job_name: job_name
'''

RETURN = '''
jobs:
    description: A list of dictionaries containing facts for Job.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource ID for the resource.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contosoresources/providers/Microsoft.Media/mediaservices/contosomedia
                    /transforms/exampleTransform/jobs/job1"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: job1
        created:
            description:
                - "The UTC date and time when the Job was created, in 'YYYY-MM-DDThh:mm:ssZ' format."
            returned: always
            type: datetime
            sample: "2018-08-08T16:29:58.1798Z"
        state:
            description:
                - "The current state of the job. Possible values include: 'Canceled', 'Canceling', 'Error', 'Finished', 'Processing', 'Queued', 'Scheduled'"
            returned: always
            type: str
            sample: Queued
        input:
            description:
                - The inputs for the Job.
            returned: always
            type: complex
            sample: input
            contains:
        outputs:
            description:
                - The outputs for the Job.
            returned: always
            type: complex
            sample: outputs
            contains:
        priority:
            description:
                - "Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default
                   is normal. Possible values include: 'Low', 'Normal', 'High'"
            returned: always
            type: str
            sample: Low
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.media import AzureMediaServices
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
            account_name=dict(
                type='str',
                required=True
            ),
            transform_name=dict(
                type='str',
                required=True
            ),
            job_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.account_name = None
        self.transform_name = None
        self.job_name = None
        super(AzureRMJobsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['jobs'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.get(resource_group_name=self.resource_group,
                                                 account_name=self.account_name,
                                                 transform_name=self.transform_name,
                                                 job_name=self.job_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Jobs.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'created': d.get('created', None),
            'state': d.get('state', None),
            'input': {
            },
            'outputs': {
            },
            'priority': d.get('priority', None)
        }
        return d


def main():
    AzureRMJobsFacts()


if __name__ == '__main__':
    main()

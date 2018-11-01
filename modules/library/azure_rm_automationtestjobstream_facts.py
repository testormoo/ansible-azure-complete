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
module: azure_rm_automationtestjobstream_facts
version_added: "2.8"
short_description: Get Azure Test Job Stream facts.
description:
    - Get facts of Azure Test Job Stream.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    runbook_name:
        description:
            - The runbook name.
        required: True
    job_stream_id:
        description:
            - The job stream id.
    filter:
        description:
            - The filter to apply on the operation.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Test Job Stream
    azure_rm_automationtestjobstream_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      runbook_name: runbook_name
      job_stream_id: job_stream_id

  - name: List instances of Test Job Stream
    azure_rm_automationtestjobstream_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      runbook_name: runbook_name
      filter: filter
'''

RETURN = '''
test_job_streams:
    description: A list of dictionaries containing facts for Test Job Stream.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Gets or sets the id of the resource.
            returned: always
            type: str
            sample: "/subscriptions/51766542-3ed7-4a72-a187-0c8ab644ddab/resourcegroups/mygroup/providers/Microsoft.Automation/automationAccounts/ContoseAuto
                    mationAccount/runbooks/foo/draft/testJob/streams/851b2101-686f-40e2-8a4b-5b8df08afbd1_00636535684910693884_00000000000000000001"
        time:
            description:
                - Gets or sets the creation time of the job.
            returned: always
            type: datetime
            sample: "2018-02-07T02:48:11.0693884+00:00"
        summary:
            description:
                - Gets or sets the summary.
            returned: always
            type: str
            sample: summary
        value:
            description:
                - Gets or sets the values of the job stream.
            returned: always
            type: complex
            sample: {}
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTestJobStreamsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            runbook_name=dict(
                type='str',
                required=True
            ),
            job_stream_id=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.automation_account_name = None
        self.runbook_name = None
        self.job_stream_id = None
        self.filter = None
        super(AzureRMTestJobStreamsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.job_stream_id is not None:
            self.results['test_job_streams'] = self.get()
        else:
            self.results['test_job_streams'] = self.list_by_test_job()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.test_job_streams.get(resource_group_name=self.resource_group,
                                                             automation_account_name=self.automation_account_name,
                                                             runbook_name=self.runbook_name,
                                                             job_stream_id=self.job_stream_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for TestJobStreams.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_test_job(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.test_job_streams.list_by_test_job(resource_group_name=self.resource_group,
                                                                          automation_account_name=self.automation_account_name,
                                                                          runbook_name=self.runbook_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for TestJobStreams.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'time': d.get('time', None),
            'summary': d.get('summary', None),
            'value': d.get('value', None)
        }
        return d


def main():
    AzureRMTestJobStreamsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_automationjobschedule_facts
version_added: "2.8"
short_description: Get Azure Job Schedule facts.
description:
    - Get facts of Azure Job Schedule.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    name:
        description:
            - The name of the automation account.
        required: True
    job_schedule_id:
        description:
            - The job schedule name.
    filter:
        description:
            - The filter to apply on the operation.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Job Schedule
    azure_rm_automationjobschedule_facts:
      resource_group: resource_group_name
      name: automation_account_name
      job_schedule_id: job_schedule_id

  - name: List instances of Job Schedule
    azure_rm_automationjobschedule_facts:
      resource_group: resource_group_name
      name: automation_account_name
      filter: filter
'''

RETURN = '''
job_schedule:
    description: A list of dictionaries containing facts for Job Schedule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Gets the id of the resource.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/ContoseAutomationAccount/jobSchedules/0fa462ba-
                    3aa2-4138-83ca-9ebc3bc55cdc"
        schedule:
            description:
                - Gets or sets the schedule.
            returned: always
            type: complex
            sample: schedule
            contains:
                name:
                    description:
                        - Gets or sets the name of the Schedule.
                    returned: always
                    type: str
                    sample: ScheduleNameGoesHere332204b5-debe-4348-a5c7-6357457189f2
        runbook:
            description:
                - Gets or sets the runbook.
            returned: always
            type: complex
            sample: runbook
            contains:
                name:
                    description:
                        - Gets or sets the name of the runbook.
                    returned: always
                    type: str
                    sample: TestRunbook
        parameters:
            description:
                - Gets or sets the parameters of the job schedule.
            returned: always
            type: complex
            sample: "{\n  'jobscheduletag01': 'jobschedulevalue01',\n  'jobscheduletag02': 'jobschedulevalue02'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobScheduleFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            job_schedule_id=dict(
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
        self.name = None
        self.job_schedule_id = None
        self.filter = None
        super(AzureRMJobScheduleFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.job_schedule_id is not None:
            self.results['job_schedule'] = self.get()
        else:
            self.results['job_schedule'] = self.list_by_automation_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_schedule.get(resource_group_name=self.resource_group,
                                                         automation_account_name=self.name,
                                                         job_schedule_id=self.job_schedule_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job Schedule.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_schedule.list_by_automation_account(resource_group_name=self.resource_group,
                                                                                automation_account_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job Schedule.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'schedule': {
                'name': d.get('schedule', {}).get('name', None)
            },
            'runbook': {
                'name': d.get('runbook', {}).get('name', None)
            },
            'parameters': d.get('parameters', None)
        }
        return d


def main():
    AzureRMJobScheduleFacts()


if __name__ == '__main__':
    main()

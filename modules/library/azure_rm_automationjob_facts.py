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
module: azure_rm_automationjob_facts
version_added: "2.8"
short_description: Get Azure Job facts.
description:
    - Get facts of Azure Job.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    name:
        description:
            - The job name.
    client_request_id:
        description:
            - Identifies this specific client request.
    filter:
        description:
            - The filter to apply on the operation.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Job
    azure_rm_automationjob_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      name: job_name
      client_request_id: client_request_id

  - name: List instances of Job
    azure_rm_automationjob_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      filter: filter
      client_request_id: client_request_id
'''

RETURN = '''
job:
    description: A list of dictionaries containing facts for Job.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource
            returned: always
            type: str
            sample: "/subscriptions/51766542-3ed7-4a72-a187-0c8ab644ddab/resourceGroups/mygroup/providers/Microsoft.Automation/automationAccounts/ContoseAuto
                    mationAccount/jobs/jobName"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: foo
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
        status:
            description:
                - "Gets or sets the status of the job. Possible values include: 'New', 'Activating', 'Running', 'Completed', 'Failed', 'Stopped', 'Blocked',
                   'Suspended', 'Disconnected', 'Suspending', 'Stopping', 'Resuming', 'Removing'"
            returned: always
            type: str
            sample: New
        exception:
            description:
                - Gets or sets the exception of the job.
            returned: always
            type: str
            sample: exception
        parameters:
            description:
                - Gets or sets the parameters of the job.
            returned: always
            type: complex
            sample: "{\n  'tag01': 'value01',\n  'tag02': 'value02'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobFacts(AzureRMModuleBase):
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
            name=dict(
                type='str'
            ),
            client_request_id=dict(
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
        self.name = None
        self.client_request_id = None
        self.filter = None
        super(AzureRMJobFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['job'] = self.get()
        else:
            self.results['job'] = self.list_by_automation_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job.get(resource_group_name=self.resource_group,
                                                automation_account_name=self.automation_account_name,
                                                job_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job.list_by_automation_account(resource_group_name=self.resource_group,
                                                                       automation_account_name=self.automation_account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job.')

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
            'runbook': {
                'name': d.get('runbook', {}).get('name', None)
            },
            'status': d.get('status', None),
            'exception': d.get('exception', None),
            'parameters': d.get('parameters', None)
        }
        return d


def main():
    AzureRMJobFacts()


if __name__ == '__main__':
    main()

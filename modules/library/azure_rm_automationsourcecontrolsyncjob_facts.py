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
module: azure_rm_automationsourcecontrolsyncjob_facts
version_added: "2.8"
short_description: Get Azure Source Control Sync Job facts.
description:
    - Get facts of Azure Source Control Sync Job.

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
            - The source control name.
        required: True
    source_control_sync_job_id:
        description:
            - The source control sync job id.
    filter:
        description:
            - The filter to apply on the operation.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Source Control Sync Job
    azure_rm_automationsourcecontrolsyncjob_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      name: source_control_name
      source_control_sync_job_id: source_control_sync_job_id

  - name: List instances of Source Control Sync Job
    azure_rm_automationsourcecontrolsyncjob_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      name: source_control_name
      filter: filter
'''

RETURN = '''
source_control_sync_job:
    description: A list of dictionaries containing facts for Source Control Sync Job.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The id of the job.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/sourceControls/MySourceCo
                    ntrol/sourceControlSyncJobs/ce6fe3e3-9db3-4096-a6b4-82bfb4c10a9a"
        exception:
            description:
                - The exceptions that occured while running the sync job.
            returned: always
            type: str
            sample: exception
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSourceControlSyncJobFacts(AzureRMModuleBase):
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
                type='str',
                required=True
            ),
            source_control_sync_job_id=dict(
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
        self.source_control_sync_job_id = None
        self.filter = None
        super(AzureRMSourceControlSyncJobFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.source_control_sync_job_id is not None:
            self.results['source_control_sync_job'] = self.get()
        else:
            self.results['source_control_sync_job'] = self.list_by_automation_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.source_control_sync_job.get(resource_group_name=self.resource_group,
                                                                    automation_account_name=self.automation_account_name,
                                                                    source_control_name=self.name,
                                                                    source_control_sync_job_id=self.source_control_sync_job_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for SourceControlSyncJob.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.source_control_sync_job.list_by_automation_account(resource_group_name=self.resource_group,
                                                                                           automation_account_name=self.automation_account_name,
                                                                                           source_control_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for SourceControlSyncJob.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'exception': d.get('exception', None)
        }
        return d


def main():
    AzureRMSourceControlSyncJobFacts()


if __name__ == '__main__':
    main()

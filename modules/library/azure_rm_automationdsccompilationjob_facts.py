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
module: azure_rm_automationdsccompilationjob_facts
version_added: "2.8"
short_description: Get Azure Dsc Compilation Job facts.
description:
    - Get facts of Azure Dsc Compilation Job.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    compilation_job_name:
        description:
            - The the DSC configuration Id.
    filter:
        description:
            - The filter to apply on the operation.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Dsc Compilation Job
    azure_rm_automationdsccompilationjob_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      compilation_job_name: compilation_job_name

  - name: List instances of Dsc Compilation Job
    azure_rm_automationdsccompilationjob_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      filter: filter
'''

RETURN = '''
dsc_compilation_job:
    description: A list of dictionaries containing facts for Dsc Compilation Job.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/compilationjobs/TestCompi
                    lationJob"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: TestCompilationJob
        configuration:
            description:
                - Gets or sets the configuration.
            returned: always
            type: complex
            sample: configuration
            contains:
                name:
                    description:
                        - Gets or sets the name of the Dsc configuration.
                    returned: always
                    type: str
                    sample: SetupServer
        status:
            description:
                - "Gets or sets the status of the job. Possible values include: 'New', 'Activating', 'Running', 'Completed', 'Failed', 'Stopped', 'Blocked',
                   'Suspended', 'Disconnected', 'Suspending', 'Stopping', 'Resuming', 'Removing'"
            returned: always
            type: str
            sample: New
        exception:
            description:
                - Gets the exception of the job.
            returned: always
            type: str
            sample: exception
        parameters:
            description:
                - Gets or sets the parameters of the job.
            returned: always
            type: complex
            sample: parameters
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDscCompilationJobFacts(AzureRMModuleBase):
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
            compilation_job_name=dict(
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
        self.compilation_job_name = None
        self.filter = None
        super(AzureRMDscCompilationJobFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.compilation_job_name is not None:
            self.results['dsc_compilation_job'] = self.get()
        else:
            self.results['dsc_compilation_job'] = self.list_by_automation_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dsc_compilation_job.get(resource_group_name=self.resource_group,
                                                                automation_account_name=self.automation_account_name,
                                                                compilation_job_name=self.compilation_job_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DscCompilationJob.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dsc_compilation_job.list_by_automation_account(resource_group_name=self.resource_group,
                                                                                       automation_account_name=self.automation_account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DscCompilationJob.')

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
            'configuration': {
                'name': d.get('configuration', {}).get('name', None)
            },
            'status': d.get('status', None),
            'exception': d.get('exception', None),
            'parameters': d.get('parameters', None)
        }
        return d


def main():
    AzureRMDscCompilationJobFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_automationtestjob_facts
version_added: "2.8"
short_description: Get Azure Test Job facts.
description:
    - Get facts of Azure Test Job.

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
            - The runbook name.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Test Job
    azure_rm_automationtestjob_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      name: runbook_name
'''

RETURN = '''
test_job:
    description: A list of dictionaries containing facts for Test Job.
    returned: always
    type: complex
    contains:
        status:
            description:
                - Gets or sets the status of the test job.
            returned: always
            type: str
            sample: Completed
        exception:
            description:
                - Gets or sets the exception of the test job.
            returned: always
            type: str
            sample: exception
        parameters:
            description:
                - Gets or sets the parameters of the test job.
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


class AzureRMTestJobFacts(AzureRMModuleBase):
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
        super(AzureRMTestJobFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['test_job'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.test_job.get(resource_group_name=self.resource_group,
                                                     automation_account_name=self.automation_account_name,
                                                     runbook_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Test Job.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'status': d.get('status', None),
            'exception': d.get('exception', None),
            'parameters': d.get('parameters', None)
        }
        return d


def main():
    AzureRMTestJobFacts()


if __name__ == '__main__':
    main()

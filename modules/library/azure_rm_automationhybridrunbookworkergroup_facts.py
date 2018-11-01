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
module: azure_rm_automationhybridrunbookworkergroup_facts
version_added: "2.8"
short_description: Get Azure Hybrid Runbook Worker Group facts.
description:
    - Get facts of Azure Hybrid Runbook Worker Group.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    hybrid_runbook_worker_group_name:
        description:
            - The hybrid runbook worker group name
    filter:
        description:
            - The filter to apply on the operation.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Hybrid Runbook Worker Group
    azure_rm_automationhybridrunbookworkergroup_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      hybrid_runbook_worker_group_name: hybrid_runbook_worker_group_name

  - name: List instances of Hybrid Runbook Worker Group
    azure_rm_automationhybridrunbookworkergroup_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      filter: filter
'''

RETURN = '''
hybrid_runbook_worker_group:
    description: A list of dictionaries containing facts for Hybrid Runbook Worker Group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Gets or sets the id of the resource.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/testaccount/hybridRunbookWorkerGroups/TestHybri
                    dGroup"
        name:
            description:
                - Gets or sets the name of the group.
            returned: always
            type: str
            sample: TestHybridGroup
        credential:
            description:
                - Sets the credential of a worker group.
            returned: always
            type: complex
            sample: credential
            contains:
                name:
                    description:
                        - Gets or sets the name of the credential.
                    returned: always
                    type: str
                    sample: myRunAsCredentialName
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMHybridRunbookWorkerGroupFacts(AzureRMModuleBase):
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
            hybrid_runbook_worker_group_name=dict(
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
        self.hybrid_runbook_worker_group_name = None
        self.filter = None
        super(AzureRMHybridRunbookWorkerGroupFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.hybrid_runbook_worker_group_name is not None:
            self.results['hybrid_runbook_worker_group'] = self.get()
        else:
            self.results['hybrid_runbook_worker_group'] = self.list_by_automation_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.hybrid_runbook_worker_group.get(resource_group_name=self.resource_group,
                                                                        automation_account_name=self.automation_account_name,
                                                                        hybrid_runbook_worker_group_name=self.hybrid_runbook_worker_group_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for HybridRunbookWorkerGroup.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.hybrid_runbook_worker_group.list_by_automation_account(resource_group_name=self.resource_group,
                                                                                               automation_account_name=self.automation_account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for HybridRunbookWorkerGroup.')

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
            'credential': {
                'name': d.get('credential', {}).get('name', None)
            }
        }
        return d


def main():
    AzureRMHybridRunbookWorkerGroupFacts()


if __name__ == '__main__':
    main()

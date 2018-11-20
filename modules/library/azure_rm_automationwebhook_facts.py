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
module: azure_rm_automationwebhook_facts
version_added: "2.8"
short_description: Get Azure Webhook facts.
description:
    - Get facts of Azure Webhook.

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
            - The webhook name.
    filter:
        description:
            - The filter to apply on the operation.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Webhook
    azure_rm_automationwebhook_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      name: webhook_name

  - name: List instances of Webhook
    azure_rm_automationwebhook_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      filter: filter
'''

RETURN = '''
webhook:
    description: A list of dictionaries containing facts for Webhook.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/webhooks/TestWebhook
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: TestWebhook
        uri:
            description:
                - Gets or sets the webhook uri.
            returned: always
            type: str
            sample: uri
        parameters:
            description:
                - Gets or sets the parameters of the job that is created when the webhook calls the runbook it is associated with.
            returned: always
            type: complex
            sample: parameters
        runbook:
            description:
                - Gets or sets the runbook the webhook is associated with.
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
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWebhookFacts(AzureRMModuleBase):
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
        self.filter = None
        super(AzureRMWebhookFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['webhook'] = self.get()
        else:
            self.results['webhook'] = self.list_by_automation_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.webhook.get(resource_group_name=self.resource_group,
                                                    automation_account_name=self.automation_account_name,
                                                    webhook_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Webhook.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.webhook.list_by_automation_account(resource_group_name=self.resource_group,
                                                                           automation_account_name=self.automation_account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Webhook.')

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
            'uri': d.get('uri', None),
            'parameters': d.get('parameters', None),
            'runbook': {
                'name': d.get('runbook', {}).get('name', None)
            }
        }
        return d


def main():
    AzureRMWebhookFacts()


if __name__ == '__main__':
    main()

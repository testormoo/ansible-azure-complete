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
module: azure_rm_automationagentregistrationinformation_facts
version_added: "2.8"
short_description: Get Azure Agent Registration Information facts.
description:
    - Get facts of Azure Agent Registration Information.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    name:
        description:
            - The name of the automation account.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Agent Registration Information
    azure_rm_automationagentregistrationinformation_facts:
      resource_group: resource_group_name
      name: automation_account_name
'''

RETURN = '''
agent_registration_information:
    description: A list of dictionaries containing facts for Agent Registration Information.
    returned: always
    type: complex
    contains:
        endpoint:
            description:
                - Gets or sets the dsc server endpoint.
            returned: always
            type: str
            sample: "https://eus2-agentservice-prod-1.azure-automation.net/accounts/bd8fac9e-0000-0000-0000-0000f474fbf6"
        keys:
            description:
                - Gets or sets the agent registration keys.
            returned: always
            type: complex
            sample: keys
            contains:
                primary:
                    description:
                        - Gets or sets the primary key.
                    returned: always
                    type: str
                    sample: 5ci0000000000000000000000000000000000000000000000000000000000000000000000000000Y5H/8wFg==
                secondary:
                    description:
                        - Gets or sets the secondary key.
                    returned: always
                    type: str
                    sample: rVp0000000000000000000000000000000000000000000000000000000000000000000000000000f8cbmrOA==
        id:
            description:
                - Gets or sets the id.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount18/agentRegistrationInformat
                    ion/https://eus2-agentservice-prod-1.azure-automation.net/accounts/bd8fac9e-0000-0000-0000-0000f474fbf6"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAgentRegistrationInformationFacts(AzureRMModuleBase):
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
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        super(AzureRMAgentRegistrationInformationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['agent_registration_information'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.agent_registration_information.get(resource_group_name=self.resource_group,
                                                                           automation_account_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Agent Registration Information.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'endpoint': d.get('endpoint', None),
            'keys': {
                'primary': d.get('keys', {}).get('primary', None),
                'secondary': d.get('keys', {}).get('secondary', None)
            },
            'id': d.get('id', None)
        }
        return d


def main():
    AzureRMAgentRegistrationInformationFacts()


if __name__ == '__main__':
    main()

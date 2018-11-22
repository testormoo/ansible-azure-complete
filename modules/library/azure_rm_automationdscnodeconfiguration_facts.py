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
module: azure_rm_automationdscnodeconfiguration_facts
version_added: "2.8"
short_description: Get Azure Dsc Node Configuration facts.
description:
    - Get facts of Azure Dsc Node Configuration.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    filter:
        description:
            - The filter to apply on the operation.
    skip:
        description:
            - The number of rows to skip.
    top:
        description:
            - The the number of rows to take.
    inlinecount:
        description:
            - Return total rows.
    name:
        description:
            - The Dsc node configuration name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Dsc Node Configuration
    azure_rm_automationdscnodeconfiguration_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      filter: filter
      skip: skip
      top: top
      inlinecount: inlinecount

  - name: Get instance of Dsc Node Configuration
    azure_rm_automationdscnodeconfiguration_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      name: node_configuration_name
'''

RETURN = '''
dsc_node_configuration:
    description: A list of dictionaries containing facts for Dsc Node Configuration.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/nodeConfigurations/SetupS
                    erver.localhost"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: SetupServer.localhost
        configuration:
            description:
                - Gets or sets the configuration of the node.
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
        source:
            description:
                - Source of node configuration.
            returned: always
            type: str
            sample: source
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDscNodeConfigurationFacts(AzureRMModuleBase):
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
            filter=dict(
                type='str'
            ),
            skip=dict(
                type='int'
            ),
            top=dict(
                type='int'
            ),
            inlinecount=dict(
                type='str'
            ),
            name=dict(
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
        self.filter = None
        self.skip = None
        self.top = None
        self.inlinecount = None
        self.name = None
        super(AzureRMDscNodeConfigurationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['dsc_node_configuration'] = self.get()
        else:
            self.results['dsc_node_configuration'] = self.list_by_automation_account()
        return self.results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dsc_node_configuration.list_by_automation_account(resource_group_name=self.resource_group,
                                                                                          automation_account_name=self.automation_account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Dsc Node Configuration.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dsc_node_configuration.get(resource_group_name=self.resource_group,
                                                                   automation_account_name=self.automation_account_name,
                                                                   node_configuration_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Dsc Node Configuration.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'configuration': {
                'name': d.get('configuration', {}).get('name', None)
            },
            'source': d.get('source', None)
        }
        return d


def main():
    AzureRMDscNodeConfigurationFacts()


if __name__ == '__main__':
    main()

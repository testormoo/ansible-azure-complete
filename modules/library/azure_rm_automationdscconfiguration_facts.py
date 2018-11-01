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
module: azure_rm_automationdscconfiguration_facts
version_added: "2.8"
short_description: Get Azure Dsc Configuration facts.
description:
    - Get facts of Azure Dsc Configuration.

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
    configuration_name:
        description:
            - The configuration name.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Dsc Configuration
    azure_rm_automationdscconfiguration_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      filter: filter
      skip: skip
      top: top
      inlinecount: inlinecount

  - name: Get instance of Dsc Configuration
    azure_rm_automationdscconfiguration_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      configuration_name: configuration_name
'''

RETURN = '''
dsc_configuration:
    description: A list of dictionaries containing facts for Dsc Configuration.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/configurations/TemplateBasic
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: TemplateBasic
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - The Azure Region where the resource lives
            returned: always
            type: str
            sample: East US 2
        parameters:
            description:
                - Gets or sets the configuration parameters.
            returned: always
            type: complex
            sample: {}
        state:
            description:
                - "Gets or sets the state of the configuration. Possible values include: 'New', 'Edit', 'Published'"
            returned: always
            type: str
            sample: Published
        description:
            description:
                - Gets or sets the description.
            returned: always
            type: str
            sample: sample configuration
        etag:
            description:
                - Gets or sets the etag of the resource.
            returned: always
            type: str
            sample: "'636263396635600000'"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDscConfigurationFacts(AzureRMModuleBase):
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
            configuration_name=dict(
                type='str'
            ),
            tags=dict(
                type='list'
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
        self.configuration_name = None
        self.tags = None
        super(AzureRMDscConfigurationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['dsc_configuration'] = self.list_by_automation_account()
        elif self.configuration_name is not None:
            self.results['dsc_configuration'] = self.get()
        return self.results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dsc_configuration.list_by_automation_account(resource_group_name=self.resource_group,
                                                                                     automation_account_name=self.automation_account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DscConfiguration.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dsc_configuration.get(resource_group_name=self.resource_group,
                                                              automation_account_name=self.automation_account_name,
                                                              configuration_name=self.configuration_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DscConfiguration.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'parameters': d.get('parameters', None),
            'state': d.get('state', None),
            'description': d.get('description', None),
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMDscConfigurationFacts()


if __name__ == '__main__':
    main()

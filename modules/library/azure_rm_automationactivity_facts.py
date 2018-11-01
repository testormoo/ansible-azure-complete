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
module: azure_rm_automationactivity_facts
version_added: "2.8"
short_description: Get Azure Activity facts.
description:
    - Get facts of Azure Activity.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    module_name:
        description:
            - The name of module.
        required: True
    activity_name:
        description:
            - The name of activity.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Activity
    azure_rm_automationactivity_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      module_name: module_name
      activity_name: activity_name

  - name: List instances of Activity
    azure_rm_automationactivity_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      module_name: module_name
'''

RETURN = '''
activity:
    description: A list of dictionaries containing facts for Activity.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Gets or sets the id of the resource.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/modules/AzureRM.Profile/a
                    ctivities/Add-AzureRmAccount"
        name:
            description:
                - Gets the name of the activity.
            returned: always
            type: str
            sample: Add-AzureRmAccount
        definition:
            description:
                - Gets or sets the user name of the activity.
            returned: always
            type: str
            sample: definition
        description:
            description:
                - Gets or sets the description.
            returned: always
            type: str
            sample: "The Add-AzureRmAcccount cmdlet adds an authenticated Azure account to use for Azure Resource Manager cmdlet requests.\n\nYou can use
                     this authenticated account only with Azure Resource Manager cmdlets. To add an authenticated account for use with Service Management
                     cmdlets, use the Add-AzureAccount or the Import-AzurePublishSettingsFile cmdlet."
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMActivityFacts(AzureRMModuleBase):
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
            module_name=dict(
                type='str',
                required=True
            ),
            activity_name=dict(
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
        self.module_name = None
        self.activity_name = None
        super(AzureRMActivityFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.activity_name is not None:
            self.results['activity'] = self.get()
        else:
            self.results['activity'] = self.list_by_module()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.activity.get(resource_group_name=self.resource_group,
                                                     automation_account_name=self.automation_account_name,
                                                     module_name=self.module_name,
                                                     activity_name=self.activity_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Activity.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_module(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.activity.list_by_module(resource_group_name=self.resource_group,
                                                                automation_account_name=self.automation_account_name,
                                                                module_name=self.module_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Activity.')

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
            'definition': d.get('definition', None),
            'description': d.get('description', None)
        }
        return d


def main():
    AzureRMActivityFacts()


if __name__ == '__main__':
    main()

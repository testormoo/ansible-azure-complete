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
module: azure_rm_consumptionbudget_facts
version_added: "2.8"
short_description: Get Azure Budget facts.
description:
    - Get facts of Azure Budget.

options:
    resource_group:
        description:
            - Azure Resource Group Name.
    name:
        description:
            - Budget Name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Budget
    azure_rm_consumptionbudget_facts:
      resource_group: resource_group_name

  - name: Get instance of Budget
    azure_rm_consumptionbudget_facts:
      name: budget_name
'''

RETURN = '''
budgets:
    description: A list of dictionaries containing facts for Budget.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id.
            returned: always
            type: str
            sample: subscriptions/{subscription-id}/providers/Microsoft.Consumption/budgets/TestBudget
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: TestBudget
        category:
            description:
                - "The category of the budget, whether the budget tracks cost or usage. Possible values include: 'Cost', 'Usage'"
            returned: always
            type: str
            sample: Cost
        amount:
            description:
                - The total amount of cost to track with the budget
            returned: always
            type: str
            sample: 100.65
        filters:
            description:
                - May be used to filter budgets by resource group, resource, or meter.
            returned: always
            type: complex
            sample: filters
            contains:
                resources:
                    description:
                        - The list of filters on resources.
                    returned: always
                    type: str
                    sample: "[\n  '/subscriptions/{subscription-id}/resourceGroups/MYDEVTESTRG/providers/Microsoft.Compute/virtualMachines/MSVM2',\n
                             '/subscriptions/{subscription-id}/resourceGroups/MYDEVTESTRG/providers/Microsoft.Compute/virtualMachines/platformcloudplatformG
                            eneric1'\n]"
                meters:
                    description:
                        - The list of filters on meters (GUID), mandatory for budgets of usage category.
                    returned: always
                    type: str
                    sample: "[\n  '00000000-0000-0000-0000-000000000000'\n]"
        notifications:
            description:
                - Dictionary of notifications associated with the budget. Budget can have up to five notifications.
            returned: always
            type: complex
            sample: "{\n  'Actual_GreaterThan_80_Percent': {\n    'enabled': true,\n    'operator': 'GreaterThan',\n    'threshold': '80',\n
                     'contactEmails': [\n      'johndoe@contoso.com',\n      'janesmith@contoso.com'\n    ],\n    'contactRoles': [\n      'Contributor',\n
                          'Reader'\n    ],\n    'contactGroups': [\n
                     '/subscriptions/{subscription-id}/resourceGroups/MYDEVTESTRG/providers/microsoft.insights/actionGroups/SampleActionGroup'\n    ]\n
                     }\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.consumption import ConsumptionManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBudgetsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
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
        self.name = None
        super(AzureRMBudgetsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None:
            self.results['budgets'] = self.list_by_resource_group_name()
        elif self.name is not None:
            self.results['budgets'] = self.get()
        return self.results

    def list_by_resource_group_name(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.budgets.list_by_resource_group_name(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Budgets.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.budgets.get(budget_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Budgets.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'category': d.get('category', None),
            'amount': d.get('amount', None),
            'filters': {
                'resources': d.get('filters', {}).get('resources', None),
                'meters': d.get('filters', {}).get('meters', None)
            },
            'notifications': d.get('notifications', None)
        }
        return d


def main():
    AzureRMBudgetsFacts()


if __name__ == '__main__':
    main()

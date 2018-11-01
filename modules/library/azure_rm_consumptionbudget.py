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
module: azure_rm_consumptionbudget
version_added: "2.8"
short_description: Manage Budget instance.
description:
    - Create, update and delete instance of Budget.

options:
    budget_name:
        description:
            - Budget Name.
        required: True
    e_tag:
        description:
            - "eTag of the resource. To handle concurrent update scenarion, this field will be used to determine whether the user is updating the latest
               version or not."
    category:
        description:
            - The category of the budget, whether the budget tracks C(cost) or C(usage).
        required: True
        choices:
            - 'cost'
            - 'usage'
    amount:
        description:
            - The total amount of C(cost) to track with the budget
        required: True
    time_grain:
        description:
            - The time covered by a budget. Tracking of the I(amount) will be reset based on the time grain.
        required: True
        choices:
            - 'monthly'
            - 'quarterly'
            - 'annually'
    time_period:
        description:
            - "Has start and end date of the budget. The start date must be first of the month and should be less than the end date. Budget start date must
               be on or after June 1, 2017. Future start date should not be more than three months. Past start date should  be selected within the
               I(time_grain) preiod. There are no restrictions on the end date."
        required: True
        suboptions:
            start_date:
                description:
                    - The start date for the budget.
                required: True
            end_date:
                description:
                    - The end date for the budget. If not provided, we default this to 10 years from the start date.
    filters:
        description:
            - May be used to filter budgets by resource group, resource, or meter.
        suboptions:
            resource_groups:
                description:
                    - The list of filters on resource groups, allowed at subscription level only.
                type: list
            resources:
                description:
                    - The list of filters on resources.
                type: list
            meters:
                description:
                    - The list of filters on meters (GUID), mandatory for budgets of usage category.
                type: list
    notifications:
        description:
            - Dictionary of notifications associated with the budget. Budget can have up to five notifications.
    state:
      description:
        - Assert the state of the Budget.
        - Use 'present' to create or update an Budget and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Budget
    azure_rm_consumptionbudget:
      budget_name: TestBudget
      e_tag: "1d34d016a593709"
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: subscriptions/{subscription-id}/providers/Microsoft.Consumption/budgets/TestBudget
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.consumption import ConsumptionManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMBudgets(AzureRMModuleBase):
    """Configuration class for an Azure RM Budget resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            budget_name=dict(
                type='str',
                required=True
            ),
            e_tag=dict(
                type='str'
            ),
            category=dict(
                type='str',
                choices=['cost',
                         'usage'],
                required=True
            ),
            amount=dict(
                type='str',
                required=True
            ),
            time_grain=dict(
                type='str',
                choices=['monthly',
                         'quarterly',
                         'annually'],
                required=True
            ),
            time_period=dict(
                type='dict',
                required=True
            ),
            filters=dict(
                type='dict'
            ),
            notifications=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.budget_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBudgets, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "e_tag":
                    self.parameters["e_tag"] = kwargs[key]
                elif key == "category":
                    self.parameters["category"] = _snake_to_camel(kwargs[key], True)
                elif key == "amount":
                    self.parameters["amount"] = kwargs[key]
                elif key == "time_grain":
                    self.parameters["time_grain"] = _snake_to_camel(kwargs[key], True)
                elif key == "time_period":
                    self.parameters["time_period"] = kwargs[key]
                elif key == "filters":
                    self.parameters["filters"] = kwargs[key]
                elif key == "notifications":
                    self.parameters["notifications"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_budget()

        if not old_response:
            self.log("Budget instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Budget instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Budget instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Budget instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_budget()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Budget instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_budget()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_budget():
                time.sleep(20)
        else:
            self.log("Budget instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_budget(self):
        '''
        Creates or updates Budget with the specified configuration.

        :return: deserialized Budget instance state dictionary
        '''
        self.log("Creating / Updating the Budget instance {0}".format(self.budget_name))

        try:
            response = self.mgmt_client.budgets.create_or_update(budget_name=self.budget_name,
                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Budget instance.')
            self.fail("Error creating the Budget instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_budget(self):
        '''
        Deletes specified Budget instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Budget instance {0}".format(self.budget_name))
        try:
            response = self.mgmt_client.budgets.delete(budget_name=self.budget_name)
        except CloudError as e:
            self.log('Error attempting to delete the Budget instance.')
            self.fail("Error deleting the Budget instance: {0}".format(str(e)))

        return True

    def get_budget(self):
        '''
        Gets the properties of the specified Budget.

        :return: deserialized Budget instance state dictionary
        '''
        self.log("Checking if the Budget instance {0} is present".format(self.budget_name))
        found = False
        try:
            response = self.mgmt_client.budgets.get(budget_name=self.budget_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Budget instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Budget instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMBudgets()


if __name__ == '__main__':
    main()

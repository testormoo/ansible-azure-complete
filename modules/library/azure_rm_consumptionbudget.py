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
short_description: Manage Azure Budget instance.
description:
    - Create, update and delete instance of Azure Budget.

options:
    name:
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
            - Required when C(state) is I(present).
        choices:
            - 'cost'
            - 'usage'
    amount:
        description:
            - The total amount of C(cost) to track with the budget
            - Required when C(state) is I(present).
    time_grain:
        description:
            - The time covered by a budget. Tracking of the I(amount) will be reset based on the time grain.
            - Required when C(state) is I(present).
        choices:
            - 'monthly'
            - 'quarterly'
            - 'annually'
    time_period:
        description:
            - "Has start and end date of the budget. The start date must be first of the month and should be less than the end date. Budget start date must
               be on or after June 1, 2017. Future start date should not be more than three months. Past start date should  be selected within the
               I(time_grain) preiod. There are no restrictions on the end date."
            - Required when C(state) is I(present).
        suboptions:
            start_date:
                description:
                    - The start date for the budget.
                    - Required when C(state) is I(present).
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
      name: TestBudget
      e_tag: "1d34d016a593709"
      category: Cost
      amount: 100.65
      time_grain: Monthly
      time_period:
        start_date: 2017-10-01T00:00:00Z
        end_date: 2018-10-31T00:00:00Z
      filters:
        resource_groups:
          - [
  "MYDEVTESTRG"
]
        resources:
          - [
  "/subscriptions/{subscription-id}/resourceGroups/MYDEVTESTRG/providers/Microsoft.Compute/virtualMachines/MYVM2",
  "/subscriptions/{subscription-id}/resourceGroups/MYDEVTESTRG/providers/Microsoft.Compute/virtualMachines/platformcloudplatformGeneric1"
]
        meters:
          - [
  "00000000-0000-0000-0000-000000000000"
]
      notifications: {
  "Actual_GreaterThan_80_Percent": {
    "enabled": true,
    "operator": "GreaterThan",
    "threshold": "80",
    "contactEmails": [
      "johndoe@contoso.com",
      "janesmith@contoso.com"
    ],
    "contactRoles": [
      "Contributor",
      "Reader"
    ],
    "contactGroups": [
      "/subscriptions/{subscription-id}/resourceGroups/MYDEVTESTRG/providers/microsoft.insights/actionGroups/SampleActionGroup"
    ]
  }
}
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMBudget(AzureRMModuleBase):
    """Configuration class for an Azure RM Budget resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            e_tag=dict(
                type='str'
            ),
            category=dict(
                type='str',
                choices=['cost',
                         'usage']
            ),
            amount=dict(
                type='str'
            ),
            time_grain=dict(
                type='str',
                choices=['monthly',
                         'quarterly',
                         'annually']
            ),
            time_period=dict(
                type='dict',
                options=dict(
                    start_date=dict(
                        type='datetime'
                    ),
                    end_date=dict(
                        type='datetime'
                    )
                )
            ),
            filters=dict(
                type='dict',
                options=dict(
                    resource_groups=dict(
                        type='list'
                    ),
                    resources=dict(
                        type='list'
                    ),
                    meters=dict(
                        type='list'
                    )
                )
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

        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBudget, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['category'], True)
        dict_camelize(self.parameters, ['time_grain'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Budget instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_budget()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Budget instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_budget()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Budget instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_budget(self):
        '''
        Creates or updates Budget with the specified configuration.

        :return: deserialized Budget instance state dictionary
        '''
        self.log("Creating / Updating the Budget instance {0}".format(self.name))

        try:
            response = self.mgmt_client.budgets.create_or_update(budget_name=self.name,
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
        self.log("Deleting the Budget instance {0}".format(self.name))
        try:
            response = self.mgmt_client.budgets.delete(budget_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Budget instance.')
            self.fail("Error deleting the Budget instance: {0}".format(str(e)))

        return True

    def get_budget(self):
        '''
        Gets the properties of the specified Budget.

        :return: deserialized Budget instance state dictionary
        '''
        self.log("Checking if the Budget instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.budgets.get(budget_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Budget instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Budget instance.')
        if found is True:
            return response.as_dict()

        return False


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def main():
    """Main execution"""
    AzureRMBudget()


if __name__ == '__main__':
    main()

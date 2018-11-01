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
module: azure_rm_costmanagementreportconfig
version_added: "2.8"
short_description: Manage Report Config instance.
description:
    - Create, update and delete instance of Report Config.

options:
    report_config_name:
        description:
            - Report Config Name.
        required: True
    schedule:
        description:
            - Has schedule information for the report config.
        suboptions:
            status:
                description:
                    - "The status of the schedule. Whether C(active) or not. If C(inactive), the report's scheduled execution is paused."
                choices:
                    - 'active'
                    - 'inactive'
            recurrence:
                description:
                    - The schedule recurrence.
                required: True
                choices:
                    - 'daily'
                    - 'weekly'
                    - 'monthly'
                    - 'annually'
            recurrence_period:
                description:
                    - Has start and end date of the I(recurrence). The start date must be in future. If present, the end date must be greater than start date.
                required: True
                suboptions:
                    from_property:
                        description:
                            - The start date of recurrence.
                        required: True
                    to:
                        description:
                            - The end date of recurrence. If not provided, we default this to 10 years from the start date.
    format:
        description:
            - The format of the report being delivered.
        choices:
            - 'csv'
    delivery_info:
        description:
            - Has delivery information for the report config.
        required: True
        suboptions:
            destination:
                description:
                    - Has destination for the report being delivered.
                required: True
                suboptions:
                    resource_id:
                        description:
                            - The resource id of the storage account where reports will be delivered.
                        required: True
                    container:
                        description:
                            - The name of the container where reports will be uploaded.
                        required: True
                    root_folder_path:
                        description:
                            - The name of the directory where reports will be uploaded.
    definition:
        description:
            - Has definition for the report config.
        required: True
        suboptions:
            type:
                description:
                    - The type of the report.
                required: True
            timeframe:
                description:
                    - The time frame for pulling data for the report. If C(custom), then a specific time period must be provided.
                required: True
                choices:
                    - 'week_to_date'
                    - 'month_to_date'
                    - 'year_to_date'
                    - 'custom'
            time_period:
                description:
                    - Has time period for pulling data for the report.
                suboptions:
                    from_property:
                        description:
                            - The start date I(to) pull data from.
                        required: True
                    to:
                        description:
                            - The end date to pull data to.
                        required: True
            dataset:
                description:
                    - Has definition for data in this report config.
                suboptions:
                    granularity:
                        description:
                            - The granularity of rows in the report.
                        choices:
                            - 'daily'
                    configuration:
                        description:
                            - "Has configuration information for the data in the report. The configuration will be ignored if I(aggregation) and I(grouping)
                               are provided."
                        suboptions:
                            columns:
                                description:
                                    - "Array of column names to be included in the report. Any valid report column name is allowed. If not provided, then
                                       report includes all columns."
                                type: list
                    aggregation:
                        description:
                            - "Dictionary of aggregation expression to use in the report. The key of each item in the dictionary is the alias for the
                               aggregated column. Report can have upto 2 aggregation clauses."
                    grouping:
                        description:
                            - Array of group by expression to use in the report. Report can have upto 2 group by clauses.
                        type: list
                        suboptions:
                            column_type:
                                description:
                                    - Has type of the column to group.
                                required: True
                                choices:
                                    - 'tag'
                                    - 'dimension'
                            name:
                                description:
                                    - The name of the column to group.
                                required: True
                    filter:
                        description:
                            - Has filter expression to use in the report.
                        suboptions:
                            and_property:
                                description:
                                    - "The logical 'AND' expression. Must have atleast 2 items."
                                type: list
                                suboptions:
                                    and_property:
                                        description:
                                            - "The logical 'AND' expression. Must have atleast 2 items."
                                        type: list
                                    or_property:
                                        description:
                                            - "The logical 'OR' expression. Must have atleast 2 items."
                                        type: list
                                    not_property:
                                        description:
                                            - "The logical 'NOT' expression."
                                    dimension:
                                        description:
                                            - Has comparison expression for a dimension
                                    tag:
                                        description:
                                            - Has comparison expression for a tag
                            or_property:
                                description:
                                    - "The logical 'OR' expression. Must have atleast 2 items."
                                type: list
                                suboptions:
                                    and_property:
                                        description:
                                            - "The logical 'AND' expression. Must have atleast 2 items."
                                        type: list
                                    or_property:
                                        description:
                                            - "The logical 'OR' expression. Must have atleast 2 items."
                                        type: list
                                    not_property:
                                        description:
                                            - "The logical 'NOT' expression."
                                    dimension:
                                        description:
                                            - Has comparison expression for a dimension
                                    tag:
                                        description:
                                            - Has comparison expression for a tag
                            not_property:
                                description:
                                    - "The logical 'NOT' expression."
                                suboptions:
                                    and_property:
                                        description:
                                            - "The logical 'AND' expression. Must have atleast 2 items."
                                        type: list
                                    or_property:
                                        description:
                                            - "The logical 'OR' expression. Must have atleast 2 items."
                                        type: list
                                    not_property:
                                        description:
                                            - "The logical 'NOT' expression."
                                    dimension:
                                        description:
                                            - Has comparison expression for a dimension
                                    tag:
                                        description:
                                            - Has comparison expression for a tag
                            dimension:
                                description:
                                    - Has comparison expression for a dimension
                                suboptions:
                                    name:
                                        description:
                                            - The name of the column to use in comaprison.
                                        required: True
                                    operator:
                                        description:
                                            - The operator to use for comparison.
                                        required: True
                                    values:
                                        description:
                                            - Array of values to use for comparison
                                        required: True
                                        type: list
                            tag:
                                description:
                                    - Has comparison expression for a tag
                                suboptions:
                                    name:
                                        description:
                                            - The name of the column to use in comaprison.
                                        required: True
                                    operator:
                                        description:
                                            - The operator to use for comparison.
                                        required: True
                                    values:
                                        description:
                                            - Array of values to use for comparison
                                        required: True
                                        type: list
    state:
      description:
        - Assert the state of the Report Config.
        - Use 'present' to create or update an Report Config and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Report Config
    azure_rm_costmanagementreportconfig:
      report_config_name: TestReportConfig
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: subscriptions/{subscription-id}/providers/Microsoft.Consumption/reportconfigs/TestReportConfig
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.costmanagement import CostManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMReportConfig(AzureRMModuleBase):
    """Configuration class for an Azure RM Report Config resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            report_config_name=dict(
                type='str',
                required=True
            ),
            schedule=dict(
                type='dict'
            ),
            format=dict(
                type='str',
                choices=['csv']
            ),
            delivery_info=dict(
                type='dict',
                required=True
            ),
            definition=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.report_config_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMReportConfig, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "schedule":
                    ev = kwargs[key]
                    if 'status' in ev:
                        if ev['status'] == 'active':
                            ev['status'] = 'Active'
                        elif ev['status'] == 'inactive':
                            ev['status'] = 'Inactive'
                    if 'recurrence' in ev:
                        if ev['recurrence'] == 'daily':
                            ev['recurrence'] = 'Daily'
                        elif ev['recurrence'] == 'weekly':
                            ev['recurrence'] = 'Weekly'
                        elif ev['recurrence'] == 'monthly':
                            ev['recurrence'] = 'Monthly'
                        elif ev['recurrence'] == 'annually':
                            ev['recurrence'] = 'Annually'
                    self.parameters["schedule"] = ev
                elif key == "format":
                    self.parameters["format"] = _snake_to_camel(kwargs[key], True)
                elif key == "delivery_info":
                    self.parameters["delivery_info"] = kwargs[key]
                elif key == "definition":
                    ev = kwargs[key]
                    if 'timeframe' in ev:
                        if ev['timeframe'] == 'week_to_date':
                            ev['timeframe'] = 'WeekToDate'
                        elif ev['timeframe'] == 'month_to_date':
                            ev['timeframe'] = 'MonthToDate'
                        elif ev['timeframe'] == 'year_to_date':
                            ev['timeframe'] = 'YearToDate'
                        elif ev['timeframe'] == 'custom':
                            ev['timeframe'] = 'Custom'
                    self.parameters["definition"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CostManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_reportconfig()

        if not old_response:
            self.log("Report Config instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Report Config instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Report Config instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Report Config instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_reportconfig()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Report Config instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_reportconfig()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_reportconfig():
                time.sleep(20)
        else:
            self.log("Report Config instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_reportconfig(self):
        '''
        Creates or updates Report Config with the specified configuration.

        :return: deserialized Report Config instance state dictionary
        '''
        self.log("Creating / Updating the Report Config instance {0}".format(self.report_config_name))

        try:
            response = self.mgmt_client.report_config.create_or_update(report_config_name=self.report_config_name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Report Config instance.')
            self.fail("Error creating the Report Config instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_reportconfig(self):
        '''
        Deletes specified Report Config instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Report Config instance {0}".format(self.report_config_name))
        try:
            response = self.mgmt_client.report_config.delete(report_config_name=self.report_config_name)
        except CloudError as e:
            self.log('Error attempting to delete the Report Config instance.')
            self.fail("Error deleting the Report Config instance: {0}".format(str(e)))

        return True

    def get_reportconfig(self):
        '''
        Gets the properties of the specified Report Config.

        :return: deserialized Report Config instance state dictionary
        '''
        self.log("Checking if the Report Config instance {0} is present".format(self.report_config_name))
        found = False
        try:
            response = self.mgmt_client.report_config.get(report_config_name=self.report_config_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Report Config instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Report Config instance.')
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
    AzureRMReportConfig()


if __name__ == '__main__':
    main()

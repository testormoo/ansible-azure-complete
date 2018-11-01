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
module: azure_rm_automationschedule
version_added: "2.8"
short_description: Manage Schedule instance.
description:
    - Create, update and delete instance of Schedule.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    schedule_name:
        description:
            - The schedule name.
        required: True
    name:
        description:
            - Gets or sets the name of the Schedule.
        required: True
    description:
        description:
            - Gets or sets the description of the schedule.
    start_time:
        description:
            - Gets or sets the start time of the schedule.
        required: True
    expiry_time:
        description:
            - Gets or sets the end time of the schedule.
    interval:
        description:
            - Gets or sets the interval of the schedule.
    frequency:
        description:
            - "Possible values include: 'C(one_time)', 'C(day)', 'C(hour)', 'C(week)', 'C(month)'"
        required: True
        choices:
            - 'one_time'
            - 'day'
            - 'hour'
            - 'week'
            - 'month'
    time_zone:
        description:
            - Gets or sets the time zone of the schedule.
    advanced_schedule:
        description:
            - Gets or sets the AdvancedSchedule.
        suboptions:
            week_days:
                description:
                    - Days of the week that the job should execute on.
                type: list
            month_days:
                description:
                    - Days of the month that the job should execute on. Must be between 1 and 31.
                type: list
            monthly_occurrences:
                description:
                    - Occurrences of days within a month.
                type: list
                suboptions:
                    occurrence:
                        description:
                            - Occurrence of the week within the month. Must be between 1 and 5
                    day:
                        description:
                            - Day of the I(occurrence). Must be one of C(monday), C(tuesday), C(wednesday), C(thursday), C(friday), C(saturday), C(sunday).
                        choices:
                            - 'monday'
                            - 'tuesday'
                            - 'wednesday'
                            - 'thursday'
                            - 'friday'
                            - 'saturday'
                            - 'sunday'
    state:
      description:
        - Assert the state of the Schedule.
        - Use 'present' to create or update an Schedule and 'absent' to delete it.
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
  - name: Create (or update) Schedule
    azure_rm_automationschedule:
      resource_group: rg
      automation_account_name: myAutomationAccount33
      schedule_name: mySchedule
      name: mySchedule
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/schedules/mySchedule
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSchedule(AzureRMModuleBase):
    """Configuration class for an Azure RM Schedule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            schedule_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            start_time=dict(
                type='datetime',
                required=True
            ),
            expiry_time=dict(
                type='datetime'
            ),
            interval=dict(
                type='str'
            ),
            frequency=dict(
                type='str',
                choices=['one_time',
                         'day',
                         'hour',
                         'week',
                         'month'],
                required=True
            ),
            time_zone=dict(
                type='str'
            ),
            advanced_schedule=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.schedule_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSchedule, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "start_time":
                    self.parameters["start_time"] = kwargs[key]
                elif key == "expiry_time":
                    self.parameters["expiry_time"] = kwargs[key]
                elif key == "interval":
                    self.parameters["interval"] = kwargs[key]
                elif key == "frequency":
                    self.parameters["frequency"] = _snake_to_camel(kwargs[key], True)
                elif key == "time_zone":
                    self.parameters["time_zone"] = kwargs[key]
                elif key == "advanced_schedule":
                    self.parameters["advanced_schedule"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_schedule()

        if not old_response:
            self.log("Schedule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Schedule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Schedule instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Schedule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_schedule()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Schedule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_schedule()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_schedule():
                time.sleep(20)
        else:
            self.log("Schedule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_schedule(self):
        '''
        Creates or updates Schedule with the specified configuration.

        :return: deserialized Schedule instance state dictionary
        '''
        self.log("Creating / Updating the Schedule instance {0}".format(self.schedule_name))

        try:
            response = self.mgmt_client.schedule.create_or_update(resource_group_name=self.resource_group,
                                                                  automation_account_name=self.automation_account_name,
                                                                  schedule_name=self.schedule_name,
                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Schedule instance.')
            self.fail("Error creating the Schedule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_schedule(self):
        '''
        Deletes specified Schedule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Schedule instance {0}".format(self.schedule_name))
        try:
            response = self.mgmt_client.schedule.delete(resource_group_name=self.resource_group,
                                                        automation_account_name=self.automation_account_name,
                                                        schedule_name=self.schedule_name)
        except CloudError as e:
            self.log('Error attempting to delete the Schedule instance.')
            self.fail("Error deleting the Schedule instance: {0}".format(str(e)))

        return True

    def get_schedule(self):
        '''
        Gets the properties of the specified Schedule.

        :return: deserialized Schedule instance state dictionary
        '''
        self.log("Checking if the Schedule instance {0} is present".format(self.schedule_name))
        found = False
        try:
            response = self.mgmt_client.schedule.get(resource_group_name=self.resource_group,
                                                     automation_account_name=self.automation_account_name,
                                                     schedule_name=self.schedule_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Schedule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Schedule instance.')
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
    AzureRMSchedule()


if __name__ == '__main__':
    main()

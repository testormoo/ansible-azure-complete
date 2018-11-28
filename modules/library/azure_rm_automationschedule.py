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
short_description: Manage Azure Schedule instance.
description:
    - Create, update and delete instance of Azure Schedule.

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
            - The schedule name.
        required: True
    name:
        description:
            - Gets or sets the name of the Schedule.
            - Required when C(state) is I(present).
    description:
        description:
            - Gets or sets the description of the schedule.
    start_time:
        description:
            - Gets or sets the start time of the schedule.
            - Required when C(state) is I(present).
    expiry_time:
        description:
            - Gets or sets the end time of the schedule.
    interval:
        description:
            - Gets or sets the interval of the schedule.
    frequency:
        description:
            - "Possible values include: 'C(one_time)', 'C(day)', 'C(hour)', 'C(week)', 'C(month)'"
            - Required when C(state) is I(present).
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
      name: mySchedule
      name: mySchedule
      description: my description of schedule goes here
      start_time: 2017-03-27T17:28:57.2494819Z
      expiry_time: 2017-04-01T17:28:57.2494819Z
      interval: 1
      frequency: Hour
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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
            name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            start_time=dict(
                type='datetime'
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
                         'month']
            ),
            time_zone=dict(
                type='str'
            ),
            advanced_schedule=dict(
                type='dict'
                options=dict(
                    week_days=dict(
                        type='list'
                    ),
                    month_days=dict(
                        type='list'
                    ),
                    monthly_occurrences=dict(
                        type='list'
                        options=dict(
                            occurrence=dict(
                                type='int'
                            ),
                            day=dict(
                                type='str',
                                choices=['monday',
                                         'tuesday',
                                         'wednesday',
                                         'thursday',
                                         'friday',
                                         'saturday',
                                         'sunday']
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.name = None
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

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['frequency'], True)
        dict_camelize(self.parameters, ['advanced_schedule', 'monthly_occurrences', 'day'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Schedule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_schedule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Schedule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_schedule()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Schedule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_schedule(self):
        '''
        Creates or updates Schedule with the specified configuration.

        :return: deserialized Schedule instance state dictionary
        '''
        self.log("Creating / Updating the Schedule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.schedule.create_or_update(resource_group_name=self.resource_group,
                                                                  automation_account_name=self.automation_account_name,
                                                                  schedule_name=self.name,
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
        self.log("Deleting the Schedule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.schedule.delete(resource_group_name=self.resource_group,
                                                        automation_account_name=self.automation_account_name,
                                                        schedule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Schedule instance.')
            self.fail("Error deleting the Schedule instance: {0}".format(str(e)))

        return True

    def get_schedule(self):
        '''
        Gets the properties of the specified Schedule.

        :return: deserialized Schedule instance state dictionary
        '''
        self.log("Checking if the Schedule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.schedule.get(resource_group_name=self.resource_group,
                                                     automation_account_name=self.automation_account_name,
                                                     schedule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Schedule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Schedule instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
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
    AzureRMSchedule()


if __name__ == '__main__':
    main()

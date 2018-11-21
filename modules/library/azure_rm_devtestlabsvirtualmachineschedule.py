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
module: azure_rm_devtestlabsvirtualmachineschedule
version_added: "2.8"
short_description: Manage Azure Virtual Machine Schedule instance.
description:
    - Create, update and delete instance of Azure Virtual Machine Schedule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    lab_name:
        description:
            - The name of the lab.
        required: True
    virtual_machine_name:
        description:
            - The name of the virtual machine.
        required: True
    name:
        description:
            - The name of the schedule.
        required: True
    location:
        description:
            - The location of the resource.
    status:
        description:
            - "The status of the schedule (i.e. Enabled, Disabled). Possible values include: 'Enabled', 'Disabled'"
        type: bool
    task_type:
        description:
            - The task type of the schedule (e.g. LabVmsShutdownTask, LabVmAutoStart).
    weekly_recurrence:
        description:
            - If the schedule will occur only some days of the week, specify the weekly recurrence.
        suboptions:
            weekdays:
                description:
                    - The days of the week for which the schedule is set (e.g. Sunday, Monday, Tuesday, etc.).
                type: list
            time:
                description:
                    - The time of the day the schedule will occur.
    daily_recurrence:
        description:
            - If the schedule will occur once each day of the week, specify the daily recurrence.
        suboptions:
            time:
                description:
                    - The time of day the schedule will occur.
    hourly_recurrence:
        description:
            - If the schedule will occur multiple times a day, specify the hourly recurrence.
        suboptions:
            minute:
                description:
                    - Minutes of the hour the schedule will run.
    time_zone_id:
        description:
            - The time zone ID (e.g. Pacific Standard time).
    notification_settings:
        description:
            - Notification settings.
        suboptions:
            status:
                description:
                    - "If notifications are enabled for this schedule (i.e. Enabled, Disabled). Possible values include: 'Disabled', 'Enabled'"
                type: bool
            time_in_minutes:
                description:
                    - Time in minutes before event at which notification will be sent.
            webhook_url:
                description:
                    - The webhook URL to which the notification will be sent.
    target_resource_id:
        description:
            - The resource ID to which the schedule belongs
    state:
      description:
        - Assert the state of the Virtual Machine Schedule.
        - Use 'present' to create or update an Virtual Machine Schedule and 'absent' to delete it.
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
  - name: Create (or update) Virtual Machine Schedule
    azure_rm_devtestlabsvirtualmachineschedule:
      resource_group: NOT FOUND
      lab_name: NOT FOUND
      virtual_machine_name: NOT FOUND
      name: NOT FOUND
      status: status
      notification_settings:
        status: status
'''

RETURN = '''
id:
    description:
        - The identifier of the resource.
    returned: always
    type: str
    sample: id
status:
    description:
        - "The status of the schedule (i.e. Enabled, Disabled). Possible values include: 'Enabled', 'Disabled'"
    returned: always
    type: str
    sample: status
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.devtestlabs import DevTestLabsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualMachineSchedules(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Machine Schedule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            lab_name=dict(
                type='str',
                required=True
            ),
            virtual_machine_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            status=dict(
                type='bool'
            ),
            task_type=dict(
                type='str'
            ),
            weekly_recurrence=dict(
                type='dict'
            ),
            daily_recurrence=dict(
                type='dict'
            ),
            hourly_recurrence=dict(
                type='dict'
            ),
            time_zone_id=dict(
                type='str'
            ),
            notification_settings=dict(
                type='dict'
            ),
            target_resource_id=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.lab_name = None
        self.virtual_machine_name = None
        self.name = None
        self.schedule = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualMachineSchedules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.schedule[key] = kwargs[key]

        expand(self.schedule, ['status'], map={True: 'Enabled', False: 'Disabled'})
        expand(self.schedule, ['notification_settings', 'status'], map={True: 'Enabled', False: 'Disabled'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_virtualmachineschedule()

        if not old_response:
            self.log("Virtual Machine Schedule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Machine Schedule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.schedule, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Machine Schedule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualmachineschedule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Machine Schedule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualmachineschedule()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_virtualmachineschedule():
                time.sleep(20)
        else:
            self.log("Virtual Machine Schedule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_virtualmachineschedule(self):
        '''
        Creates or updates Virtual Machine Schedule with the specified configuration.

        :return: deserialized Virtual Machine Schedule instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Machine Schedule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_machine_schedules.create_or_update(resource_group_name=self.resource_group,
                                                                                   lab_name=self.lab_name,
                                                                                   virtual_machine_name=self.virtual_machine_name,
                                                                                   name=self.name,
                                                                                   schedule=self.schedule)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Machine Schedule instance.')
            self.fail("Error creating the Virtual Machine Schedule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualmachineschedule(self):
        '''
        Deletes specified Virtual Machine Schedule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Machine Schedule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_machine_schedules.delete(resource_group_name=self.resource_group,
                                                                         lab_name=self.lab_name,
                                                                         virtual_machine_name=self.virtual_machine_name,
                                                                         name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Machine Schedule instance.')
            self.fail("Error deleting the Virtual Machine Schedule instance: {0}".format(str(e)))

        return True

    def get_virtualmachineschedule(self):
        '''
        Gets the properties of the specified Virtual Machine Schedule.

        :return: deserialized Virtual Machine Schedule instance state dictionary
        '''
        self.log("Checking if the Virtual Machine Schedule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_machine_schedules.get(resource_group_name=self.resource_group,
                                                                      lab_name=self.lab_name,
                                                                      virtual_machine_name=self.virtual_machine_name,
                                                                      name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Machine Schedule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Machine Schedule instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def expand(d, path, **kwargs):
    expand = kwargs.get('expand', None)
    rename = kwargs.get('rename', None)
    camelize = kwargs.get('camelize', False)
    camelize_lower = kwargs.get('camelize_lower', False)
    upper = kwargs.get('upper', False)
    map = kwargs.get('map', None)
    if isinstance(d, list):
        for i in range(len(d)):
            expand(d[i], path, **kwargs)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_name = path[0]
            new_name = old_name if rename is None else rename
            old_value = d.get(old_name, None)
            new_value = None
            if map is not None:
                new_value = map.get(old_value, None)
            if new_value is None:
                if camelize:
                    new_value = _snake_to_camel(old_value, True)
                elif camelize_lower:
                    new_value = _snake_to_camel(old_value, False)
                elif upper:
                    new_value = old_value.upper()
            if expand is None:
                # just rename
                if new_name != old_name:
                    d.pop(old_name, None)
            else:
                # expand and rename
                d[expand] = d.get(expand, {})
                d.pop(old_name, None)
                d = d[expand]
            d[new_name] = new_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                expand(sd, path[1:], **kwargs)


def main():
    """Main execution"""
    AzureRMVirtualMachineSchedules()


if __name__ == '__main__':
    main()

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
module: azure_rm_automationjobschedule
version_added: "2.8"
short_description: Manage Azure Job Schedule instance.
description:
    - Create, update and delete instance of Azure Job Schedule.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    name:
        description:
            - The name of the automation account.
        required: True
    job_schedule_id:
        description:
            - The job I(schedule) name.
        required: True
    schedule:
        description:
            - Gets or sets the schedule.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - Gets or sets the name of the Schedule.
    runbook:
        description:
            - Gets or sets the runbook.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - Gets or sets the name of the runbook.
    run_on:
        description:
            - Gets or sets the hybrid worker group that the scheduled job should run on.
    parameters:
        description:
            - Gets or sets a list of job properties.
    state:
      description:
        - Assert the state of the Job Schedule.
        - Use 'present' to create or update an Job Schedule and 'absent' to delete it.
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
  - name: Create (or update) Job Schedule
    azure_rm_automationjobschedule:
      resource_group: rg
      name: ContoseAutomationAccount
      job_schedule_id: 0fa462ba-3aa2-4138-83ca-9ebc3bc55cdc
      schedule:
        name: ScheduleNameGoesHere332204b5-debe-4348-a5c7-6357457189f2
      runbook:
        name: TestRunbook
      parameters: {
  "jobscheduletag01": "jobschedulevalue01",
  "jobscheduletag02": "jobschedulevalue02"
}
'''

RETURN = '''
id:
    description:
        - Gets the id of the resource.
    returned: always
    type: str
    sample: id
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


class AzureRMJobSchedule(AzureRMModuleBase):
    """Configuration class for an Azure RM Job Schedule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            job_schedule_id=dict(
                type='str',
                required=True
            ),
            schedule=dict(
                type='dict'
            ),
            runbook=dict(
                type='dict'
            ),
            run_on=dict(
                type='str'
            ),
            parameters=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.job_schedule_id = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobSchedule, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_jobschedule()

        if not old_response:
            self.log("Job Schedule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job Schedule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Schedule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobschedule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job Schedule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_jobschedule()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_jobschedule():
                time.sleep(20)
        else:
            self.log("Job Schedule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_jobschedule(self):
        '''
        Creates or updates Job Schedule with the specified configuration.

        :return: deserialized Job Schedule instance state dictionary
        '''
        self.log("Creating / Updating the Job Schedule instance {0}".format(self.job_schedule_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.job_schedule.create(resource_group_name=self.resource_group,
                                                                automation_account_name=self.name,
                                                                job_schedule_id=self.job_schedule_id,
                                                                parameters=self.parameters)
            else:
                response = self.mgmt_client.job_schedule.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job Schedule instance.')
            self.fail("Error creating the Job Schedule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_jobschedule(self):
        '''
        Deletes specified Job Schedule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job Schedule instance {0}".format(self.job_schedule_id))
        try:
            response = self.mgmt_client.job_schedule.delete(resource_group_name=self.resource_group,
                                                            automation_account_name=self.name,
                                                            job_schedule_id=self.job_schedule_id)
        except CloudError as e:
            self.log('Error attempting to delete the Job Schedule instance.')
            self.fail("Error deleting the Job Schedule instance: {0}".format(str(e)))

        return True

    def get_jobschedule(self):
        '''
        Gets the properties of the specified Job Schedule.

        :return: deserialized Job Schedule instance state dictionary
        '''
        self.log("Checking if the Job Schedule instance {0} is present".format(self.job_schedule_id))
        found = False
        try:
            response = self.mgmt_client.job_schedule.get(resource_group_name=self.resource_group,
                                                         automation_account_name=self.name,
                                                         job_schedule_id=self.job_schedule_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Schedule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Schedule instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMJobSchedule()


if __name__ == '__main__':
    main()

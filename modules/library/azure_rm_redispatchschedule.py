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
module: azure_rm_redispatchschedule
version_added: "2.8"
short_description: Manage Patch Schedule instance.
description:
    - Create, update and delete instance of Patch Schedule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Redis cache.
        required: True
    default:
        description:
            - Default string modeled as parameter for auto generation to work correctly.
        required: True
    schedule_entries:
        description:
            - List of patch schedules for a Redis cache.
        required: True
        type: list
        suboptions:
            day_of_week:
                description:
                    - Day of the week when a cache can be patched.
                    - Required when C(state) is I(present).
                choices:
                    - 'monday'
                    - 'tuesday'
                    - 'wednesday'
                    - 'thursday'
                    - 'friday'
                    - 'saturday'
                    - 'sunday'
                    - 'everyday'
                    - 'weekend'
            start_hour_utc:
                description:
                    - Start hour after which cache patching can start.
                    - Required when C(state) is I(present).
            maintenance_window:
                description:
                    - ISO8601 timespan specifying how much time cache patching can take.
    state:
      description:
        - Assert the state of the Patch Schedule.
        - Use 'present' to create or update an Patch Schedule and 'absent' to delete it.
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
  - name: Create (or update) Patch Schedule
    azure_rm_redispatchschedule:
      resource_group: rg1
      name: cache1
      default: default
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Cache/Redis/cache1/patchSchedules/default
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.redis import RedisManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPatchSchedules(AzureRMModuleBase):
    """Configuration class for an Azure RM Patch Schedule resource"""

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
            default=dict(
                type='str',
                required=True
            ),
            schedule_entries=dict(
                type='list',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.default = None
        self.schedule_entries = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPatchSchedules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "day_of_week":
                    self.schedule_entries["day_of_week"] = _snake_to_camel(kwargs[key], True)
                elif key == "start_hour_utc":
                    self.schedule_entries["start_hour_utc"] = kwargs[key]
                elif key == "maintenance_window":
                    self.schedule_entries["maintenance_window"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RedisManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_patchschedule()

        if not old_response:
            self.log("Patch Schedule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Patch Schedule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Patch Schedule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_patchschedule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Patch Schedule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_patchschedule()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_patchschedule():
                time.sleep(20)
        else:
            self.log("Patch Schedule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_patchschedule(self):
        '''
        Creates or updates Patch Schedule with the specified configuration.

        :return: deserialized Patch Schedule instance state dictionary
        '''
        self.log("Creating / Updating the Patch Schedule instance {0}".format(self.default))

        try:
            response = self.mgmt_client.patch_schedules.create_or_update(resource_group_name=self.resource_group,
                                                                         name=self.name,
                                                                         default=self.default,
                                                                         schedule_entries=self.schedule_entries)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Patch Schedule instance.')
            self.fail("Error creating the Patch Schedule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_patchschedule(self):
        '''
        Deletes specified Patch Schedule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Patch Schedule instance {0}".format(self.default))
        try:
            response = self.mgmt_client.patch_schedules.delete(resource_group_name=self.resource_group,
                                                               name=self.name,
                                                               default=self.default)
        except CloudError as e:
            self.log('Error attempting to delete the Patch Schedule instance.')
            self.fail("Error deleting the Patch Schedule instance: {0}".format(str(e)))

        return True

    def get_patchschedule(self):
        '''
        Gets the properties of the specified Patch Schedule.

        :return: deserialized Patch Schedule instance state dictionary
        '''
        self.log("Checking if the Patch Schedule instance {0} is present".format(self.default))
        found = False
        try:
            response = self.mgmt_client.patch_schedules.get(resource_group_name=self.resource_group,
                                                            name=self.name,
                                                            default=self.default)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Patch Schedule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Patch Schedule instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMPatchSchedules()


if __name__ == '__main__':
    main()

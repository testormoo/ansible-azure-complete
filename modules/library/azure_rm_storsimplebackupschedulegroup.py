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
module: azure_rm_storsimplebackupschedulegroup
version_added: "2.8"
short_description: Manage Azure Backup Schedule Group instance.
description:
    - Create, update and delete instance of Azure Backup Schedule Group.

options:
    device_name:
        description:
            - The name of the device.
        required: True
    schedule_group_name:
        description:
            - The name of the schedule group.
        required: True
    start_time:
        description:
            - The start time. When this field is specified we will generate Default GrandFather Father Son Backup Schedules.
            - Required when C(state) is I(present).
        suboptions:
            hour:
                description:
                    - The hour.
                    - Required when C(state) is I(present).
            minute:
                description:
                    - The minute.
                    - Required when C(state) is I(present).
    resource_group:
        description:
            - The resource group name
        required: True
    name:
        description:
            - The manager name
        required: True
    state:
      description:
        - Assert the state of the Backup Schedule Group.
        - Use 'present' to create or update an Backup Schedule Group and 'absent' to delete it.
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
  - name: Create (or update) Backup Schedule Group
    azure_rm_storsimplebackupschedulegroup:
      device_name: HSDK-4XY4FI2IVG
      schedule_group_name: BackupSchGroupForSDKTest
      start_time:
        hour: 17
        minute: 38
      resource_group: ResourceGroupForSDKTest
      name: hAzureSDKOperations
'''

RETURN = '''
id:
    description:
        - The identifier.
    returned: always
    type: str
    sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzureSDKOper
            ations/devices/hsdk-4xy4fi2ivg/backupScheduleGroups/BackupSchGroupForSDKTest"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMBackupScheduleGroup(AzureRMModuleBase):
    """Configuration class for an Azure RM Backup Schedule Group resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            device_name=dict(
                type='str',
                required=True
            ),
            schedule_group_name=dict(
                type='str',
                required=True
            ),
            start_time=dict(
                type='dict',
                options=dict(
                    hour=dict(
                        type='int'
                    ),
                    minute=dict(
                        type='int'
                    )
                )
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.device_name = None
        self.schedule_group_name = None
        self.schedule_group = dict()
        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBackupScheduleGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.schedule_group[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_backupschedulegroup()

        if not old_response:
            self.log("Backup Schedule Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Backup Schedule Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.schedule_group, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Backup Schedule Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_backupschedulegroup()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Backup Schedule Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_backupschedulegroup()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Backup Schedule Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_backupschedulegroup(self):
        '''
        Creates or updates Backup Schedule Group with the specified configuration.

        :return: deserialized Backup Schedule Group instance state dictionary
        '''
        self.log("Creating / Updating the Backup Schedule Group instance {0}".format(self.name))

        try:
            response = self.mgmt_client.backup_schedule_groups.create_or_update(device_name=self.device_name,
                                                                                schedule_group_name=self.schedule_group_name,
                                                                                schedule_group=self.schedule_group,
                                                                                resource_group_name=self.resource_group,
                                                                                manager_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Backup Schedule Group instance.')
            self.fail("Error creating the Backup Schedule Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_backupschedulegroup(self):
        '''
        Deletes specified Backup Schedule Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Backup Schedule Group instance {0}".format(self.name))
        try:
            response = self.mgmt_client.backup_schedule_groups.delete(device_name=self.device_name,
                                                                      schedule_group_name=self.schedule_group_name,
                                                                      resource_group_name=self.resource_group,
                                                                      manager_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Backup Schedule Group instance.')
            self.fail("Error deleting the Backup Schedule Group instance: {0}".format(str(e)))

        return True

    def get_backupschedulegroup(self):
        '''
        Gets the properties of the specified Backup Schedule Group.

        :return: deserialized Backup Schedule Group instance state dictionary
        '''
        self.log("Checking if the Backup Schedule Group instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.backup_schedule_groups.get(device_name=self.device_name,
                                                                   schedule_group_name=self.schedule_group_name,
                                                                   resource_group_name=self.resource_group,
                                                                   manager_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Backup Schedule Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Backup Schedule Group instance.')
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
            else:
                key = list(old[0])[0]
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


def main():
    """Main execution"""
    AzureRMBackupScheduleGroup()


if __name__ == '__main__':
    main()

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
module: azure_rm_storsimpleiscsidisk
version_added: "2.8"
short_description: Manage Azure Iscsi Disk instance.
description:
    - Create, update and delete instance of Azure Iscsi Disk.

options:
    device_name:
        description:
            - The device name.
        required: True
    iscsi_server_name:
        description:
            - The iscsi server name.
        required: True
    disk_name:
        description:
            - The disk name.
        required: True
    description:
        description:
            - The description.
    disk_status:
        description:
            - The disk status.
            - Required when C(state) is I(present).
        choices:
            - 'online'
            - 'offline'
    access_control_records:
        description:
            - The access control records.
            - Required when C(state) is I(present).
        type: list
    data_policy:
        description:
            - The data policy.
            - Required when C(state) is I(present).
        choices:
            - 'invalid'
            - 'local'
            - 'tiered'
            - 'cloud'
    provisioned_capacity_in_bytes:
        description:
            - The provisioned capacity in bytes.
            - Required when C(state) is I(present).
    monitoring_status:
        description:
            - "The monitoring. Possible values include: 'Enabled', 'Disabled'"
            - Required when C(state) is I(present).
        type: bool
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
        - Assert the state of the Iscsi Disk.
        - Use 'present' to create or update an Iscsi Disk and 'absent' to delete it.
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
  - name: Create (or update) Iscsi Disk
    azure_rm_storsimpleiscsidisk:
      device_name: HSDK-0NZI14MDTF
      iscsi_server_name: HSDK-0NZI14MDTF
      disk_name: Auto-TestIscsiDisk1
      description: Demo IscsiDisk for SDK Test Tiered
      disk_status: Online
      access_control_records:
        - []
      data_policy: Tiered
      provisioned_capacity_in_bytes: 536870912000
      monitoring_status: monitoring_status
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
            ations/devices/HSDK-0NZI14MDTF/iscsiServers/HSDK-0NZI14MDTF/disks/Auto-TestIscsiDisk1"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

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


class AzureRMIscsiDisk(AzureRMModuleBase):
    """Configuration class for an Azure RM Iscsi Disk resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            device_name=dict(
                type='str',
                required=True
            ),
            iscsi_server_name=dict(
                type='str',
                required=True
            ),
            disk_name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            disk_status=dict(
                type='str',
                choices=['online',
                         'offline']
            ),
            access_control_records=dict(
                type='list'
            ),
            data_policy=dict(
                type='str',
                choices=['invalid',
                         'local',
                         'tiered',
                         'cloud']
            ),
            provisioned_capacity_in_bytes=dict(
                type='int'
            ),
            monitoring_status=dict(
                type='bool'
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
        self.iscsi_server_name = None
        self.disk_name = None
        self.iscsi_disk = dict()
        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIscsiDisk, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.iscsi_disk[key] = kwargs[key]

        dict_camelize(self.iscsi_disk, ['disk_status'], True)
        dict_camelize(self.iscsi_disk, ['data_policy'], True)
        dict_map(self.iscsi_disk, ['monitoring_status'], '{True: 'Enabled', False: 'Disabled'}')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_iscsidisk()

        if not old_response:
            self.log("Iscsi Disk instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Iscsi Disk instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.iscsi_disk, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Iscsi Disk instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_iscsidisk()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Iscsi Disk instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_iscsidisk()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_iscsidisk():
                time.sleep(20)
        else:
            self.log("Iscsi Disk instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_iscsidisk(self):
        '''
        Creates or updates Iscsi Disk with the specified configuration.

        :return: deserialized Iscsi Disk instance state dictionary
        '''
        self.log("Creating / Updating the Iscsi Disk instance {0}".format(self.name))

        try:
            response = self.mgmt_client.iscsi_disks.create_or_update(device_name=self.device_name,
                                                                     iscsi_server_name=self.iscsi_server_name,
                                                                     disk_name=self.disk_name,
                                                                     iscsi_disk=self.iscsi_disk,
                                                                     resource_group_name=self.resource_group,
                                                                     manager_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Iscsi Disk instance.')
            self.fail("Error creating the Iscsi Disk instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_iscsidisk(self):
        '''
        Deletes specified Iscsi Disk instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Iscsi Disk instance {0}".format(self.name))
        try:
            response = self.mgmt_client.iscsi_disks.delete(device_name=self.device_name,
                                                           iscsi_server_name=self.iscsi_server_name,
                                                           disk_name=self.disk_name,
                                                           resource_group_name=self.resource_group,
                                                           manager_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Iscsi Disk instance.')
            self.fail("Error deleting the Iscsi Disk instance: {0}".format(str(e)))

        return True

    def get_iscsidisk(self):
        '''
        Gets the properties of the specified Iscsi Disk.

        :return: deserialized Iscsi Disk instance state dictionary
        '''
        self.log("Checking if the Iscsi Disk instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.iscsi_disks.get(device_name=self.device_name,
                                                        iscsi_server_name=self.iscsi_server_name,
                                                        disk_name=self.disk_name,
                                                        resource_group_name=self.resource_group,
                                                        manager_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Iscsi Disk instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Iscsi Disk instance.')
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
    AzureRMIscsiDisk()


if __name__ == '__main__':
    main()

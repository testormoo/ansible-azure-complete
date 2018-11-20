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
module: azure_rm_storsimplefileshare
version_added: "2.8"
short_description: Manage File Share instance.
description:
    - Create, update and delete instance of File Share.

options:
    device_name:
        description:
            - The device name.
        required: True
    file_server_name:
        description:
            - The file server name.
        required: True
    share_name:
        description:
            - The file share name.
        required: True
    file_share:
        description:
            - The file share.
        required: True
        suboptions:
            description:
                description:
                    - Description for file share
            share_status:
                description:
                    - The Share Status.
                    - Required when C(state) is I(present).
                choices:
                    - 'online'
                    - 'offline'
            data_policy:
                description:
                    - The data policy.
                    - Required when C(state) is I(present).
                choices:
                    - 'invalid'
                    - 'local'
                    - 'tiered'
                    - 'cloud'
            admin_user:
                description:
                    - "The user/group who will have full permission in this share. Active directory email address. Example: xyz@contoso.com or Contoso\xyz."
                    - Required when C(state) is I(present).
            provisioned_capacity_in_bytes:
                description:
                    - The total provisioned capacity in Bytes
                    - Required when C(state) is I(present).
            monitoring_status:
                description:
                    - The monitoring status.
                    - Required when C(state) is I(present).
                choices:
                    - 'enabled'
                    - 'disabled'
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
        - Assert the state of the File Share.
        - Use 'present' to create or update an File Share and 'absent' to delete it.
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
  - name: Create (or update) File Share
    azure_rm_storsimplefileshare:
      device_name: HSDK-4XY4FI2IVG
      file_server_name: HSDK-4XY4FI2IVG
      share_name: Auto-TestFileShare1
      file_share:
        description: Demo FileShare for SDK Test Tiered
        share_status: Online
        data_policy: Tiered
        admin_user: fareast\idcdlslb
        provisioned_capacity_in_bytes: 536870912000
        monitoring_status: Enabled
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
            ations/devices/hsdk-4xy4fi2ivg/fileServers/HSDK-4XY4FI2IVG/shares/Auto-TestFileShare1"
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


class AzureRMFileShares(AzureRMModuleBase):
    """Configuration class for an Azure RM File Share resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            device_name=dict(
                type='str',
                required=True
            ),
            file_server_name=dict(
                type='str',
                required=True
            ),
            share_name=dict(
                type='str',
                required=True
            ),
            file_share=dict(
                type='dict',
                required=True
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
        self.file_server_name = None
        self.share_name = None
        self.file_share = dict()
        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFileShares, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "description":
                    self.file_share["description"] = kwargs[key]
                elif key == "share_status":
                    self.file_share["share_status"] = _snake_to_camel(kwargs[key], True)
                elif key == "data_policy":
                    self.file_share["data_policy"] = _snake_to_camel(kwargs[key], True)
                elif key == "admin_user":
                    self.file_share["admin_user"] = kwargs[key]
                elif key == "provisioned_capacity_in_bytes":
                    self.file_share["provisioned_capacity_in_bytes"] = kwargs[key]
                elif key == "monitoring_status":
                    self.file_share["monitoring_status"] = _snake_to_camel(kwargs[key], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_fileshare()

        if not old_response:
            self.log("File Share instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("File Share instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the File Share instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_fileshare()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("File Share instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_fileshare()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_fileshare():
                time.sleep(20)
        else:
            self.log("File Share instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_fileshare(self):
        '''
        Creates or updates File Share with the specified configuration.

        :return: deserialized File Share instance state dictionary
        '''
        self.log("Creating / Updating the File Share instance {0}".format(self.name))

        try:
            response = self.mgmt_client.file_shares.create_or_update(device_name=self.device_name,
                                                                     file_server_name=self.file_server_name,
                                                                     share_name=self.share_name,
                                                                     file_share=self.file_share,
                                                                     resource_group_name=self.resource_group,
                                                                     manager_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the File Share instance.')
            self.fail("Error creating the File Share instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_fileshare(self):
        '''
        Deletes specified File Share instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the File Share instance {0}".format(self.name))
        try:
            response = self.mgmt_client.file_shares.delete(device_name=self.device_name,
                                                           file_server_name=self.file_server_name,
                                                           share_name=self.share_name,
                                                           resource_group_name=self.resource_group,
                                                           manager_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the File Share instance.')
            self.fail("Error deleting the File Share instance: {0}".format(str(e)))

        return True

    def get_fileshare(self):
        '''
        Gets the properties of the specified File Share.

        :return: deserialized File Share instance state dictionary
        '''
        self.log("Checking if the File Share instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.file_shares.get(device_name=self.device_name,
                                                        file_server_name=self.file_server_name,
                                                        share_name=self.share_name,
                                                        resource_group_name=self.resource_group,
                                                        manager_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("File Share instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the File Share instance.')
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
    AzureRMFileShares()


if __name__ == '__main__':
    main()

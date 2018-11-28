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
module: azure_rm_storsimpleiscsiserver
version_added: "2.8"
short_description: Manage Azure Iscsi Server instance.
description:
    - Create, update and delete instance of Azure Iscsi Server.

options:
    device_name:
        description:
            - The device name.
        required: True
    iscsi_server_name:
        description:
            - The iscsi server name.
        required: True
    storage_domain_id:
        description:
            - The storage domain id.
            - Required when C(state) is I(present).
    backup_schedule_group_id:
        description:
            - The backup policy id.
            - Required when C(state) is I(present).
    description:
        description:
            - The description.
    chap_id:
        description:
            - The chap id.
    reverse_chap_id:
        description:
            - The reverse chap id.
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
        - Assert the state of the Iscsi Server.
        - Use 'present' to create or update an Iscsi Server and 'absent' to delete it.
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
  - name: Create (or update) Iscsi Server
    azure_rm_storsimpleiscsiserver:
      device_name: HSDK-WSJQERQW3F
      iscsi_server_name: HSDK-WSJQERQW3F
      storage_domain_id: /subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzureSDKOperations/storageDomains/Default-HSDK-WSJQERQW3F-StorageDomain
      backup_schedule_group_id: /subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzureSDKOperations/devices/HSDK-WSJQERQW3F/backupScheduleGroups/Default-HSDK-WSJQERQW3F-BackupScheduleGroup
      chap_id: /subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzureSDKOperations/devices/HSDK-WSJQERQW3F/chapSettings/ChapSettingForSDK
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
            ations/devices/HSDK-WSJQERQW3F/iscsiServers/HSDK-WSJQERQW3F"
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


class AzureRMIscsiServer(AzureRMModuleBase):
    """Configuration class for an Azure RM Iscsi Server resource"""

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
            storage_domain_id=dict(
                type='str'
            ),
            backup_schedule_group_id=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            chap_id=dict(
                type='str'
            ),
            reverse_chap_id=dict(
                type='str'
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
        self.iscsi_server = dict()
        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIscsiServer, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.iscsi_server[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_iscsiserver()

        if not old_response:
            self.log("Iscsi Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Iscsi Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.iscsi_server, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Iscsi Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_iscsiserver()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Iscsi Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_iscsiserver()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Iscsi Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_iscsiserver(self):
        '''
        Creates or updates Iscsi Server with the specified configuration.

        :return: deserialized Iscsi Server instance state dictionary
        '''
        self.log("Creating / Updating the Iscsi Server instance {0}".format(self.name))

        try:
            response = self.mgmt_client.iscsi_servers.create_or_update(device_name=self.device_name,
                                                                       iscsi_server_name=self.iscsi_server_name,
                                                                       iscsi_server=self.iscsi_server,
                                                                       resource_group_name=self.resource_group,
                                                                       manager_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Iscsi Server instance.')
            self.fail("Error creating the Iscsi Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_iscsiserver(self):
        '''
        Deletes specified Iscsi Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Iscsi Server instance {0}".format(self.name))
        try:
            response = self.mgmt_client.iscsi_servers.delete(device_name=self.device_name,
                                                             iscsi_server_name=self.iscsi_server_name,
                                                             resource_group_name=self.resource_group,
                                                             manager_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Iscsi Server instance.')
            self.fail("Error deleting the Iscsi Server instance: {0}".format(str(e)))

        return True

    def get_iscsiserver(self):
        '''
        Gets the properties of the specified Iscsi Server.

        :return: deserialized Iscsi Server instance state dictionary
        '''
        self.log("Checking if the Iscsi Server instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.iscsi_servers.get(device_name=self.device_name,
                                                          iscsi_server_name=self.iscsi_server_name,
                                                          resource_group_name=self.resource_group,
                                                          manager_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Iscsi Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Iscsi Server instance.')
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


def main():
    """Main execution"""
    AzureRMIscsiServer()


if __name__ == '__main__':
    main()

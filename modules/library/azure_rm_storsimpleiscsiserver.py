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
short_description: Manage Iscsi Server instance.
description:
    - Create, update and delete instance of Iscsi Server.

options:
    device_name:
        description:
            - The device name.
        required: True
    iscsi_server_name:
        description:
            - The iscsi server name.
        required: True
    iscsi_server:
        description:
            - The iscsi server.
        required: True
        suboptions:
            storage_domain_id:
                description:
                    - The storage domain id.
                required: True
            backup_schedule_group_id:
                description:
                    - The backup policy id.
                required: True
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
    manager_name:
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
      resource_group: ResourceGroupForSDKTest
      manager_name: hAzureSDKOperations
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


class AzureRMIscsiServers(AzureRMModuleBase):
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
            iscsi_server=dict(
                type='dict',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            manager_name=dict(
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
        self.manager_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIscsiServers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "storage_domain_id":
                    self.iscsi_server["storage_domain_id"] = kwargs[key]
                elif key == "backup_schedule_group_id":
                    self.iscsi_server["backup_schedule_group_id"] = kwargs[key]
                elif key == "description":
                    self.iscsi_server["description"] = kwargs[key]
                elif key == "chap_id":
                    self.iscsi_server["chap_id"] = kwargs[key]
                elif key == "reverse_chap_id":
                    self.iscsi_server["reverse_chap_id"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Iscsi Server instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Iscsi Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_iscsiserver()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Iscsi Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_iscsiserver()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_iscsiserver():
                time.sleep(20)
        else:
            self.log("Iscsi Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_iscsiserver(self):
        '''
        Creates or updates Iscsi Server with the specified configuration.

        :return: deserialized Iscsi Server instance state dictionary
        '''
        self.log("Creating / Updating the Iscsi Server instance {0}".format(self.manager_name))

        try:
            response = self.mgmt_client.iscsi_servers.create_or_update(device_name=self.device_name,
                                                                       iscsi_server_name=self.iscsi_server_name,
                                                                       iscsi_server=self.iscsi_server,
                                                                       resource_group_name=self.resource_group,
                                                                       manager_name=self.manager_name)
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
        self.log("Deleting the Iscsi Server instance {0}".format(self.manager_name))
        try:
            response = self.mgmt_client.iscsi_servers.delete(device_name=self.device_name,
                                                             iscsi_server_name=self.iscsi_server_name,
                                                             resource_group_name=self.resource_group,
                                                             manager_name=self.manager_name)
        except CloudError as e:
            self.log('Error attempting to delete the Iscsi Server instance.')
            self.fail("Error deleting the Iscsi Server instance: {0}".format(str(e)))

        return True

    def get_iscsiserver(self):
        '''
        Gets the properties of the specified Iscsi Server.

        :return: deserialized Iscsi Server instance state dictionary
        '''
        self.log("Checking if the Iscsi Server instance {0} is present".format(self.manager_name))
        found = False
        try:
            response = self.mgmt_client.iscsi_servers.get(device_name=self.device_name,
                                                          iscsi_server_name=self.iscsi_server_name,
                                                          resource_group_name=self.resource_group,
                                                          manager_name=self.manager_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Iscsi Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Iscsi Server instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMIscsiServers()


if __name__ == '__main__':
    main()

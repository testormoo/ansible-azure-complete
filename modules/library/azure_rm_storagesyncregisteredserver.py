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
module: azure_rm_storagesyncregisteredserver
version_added: "2.8"
short_description: Manage Registered Server instance.
description:
    - Create, update and delete instance of Registered Server.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    storage_sync_service_name:
        description:
            - Name of Storage Sync Service resource.
        required: True
    server_id:
        description:
            - GUID identifying the on-premises server.
        required: True
    server_certificate:
        description:
            - Registered Server Certificate
    agent_version:
        description:
            - Registered Server Agent Version
    server_os_version:
        description:
            - Registered Server OS Version
    last_heart_beat:
        description:
            - Registered Server last heart beat
    server_role:
        description:
            - Registered Server serverRole
    cluster_id:
        description:
            - Registered Server clusterId
    cluster_name:
        description:
            - Registered Server clusterName
    server_id:
        description:
            - Registered Server serverId
    friendly_name:
        description:
            - Friendly Name
    state:
      description:
        - Assert the state of the Registered Server.
        - Use 'present' to create or update an Registered Server and 'absent' to delete it.
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
  - name: Create (or update) Registered Server
    azure_rm_storagesyncregisteredserver:
      resource_group: SampleResourceGroup_1
      storage_sync_service_name: SampleStorageSyncService_1
      server_id: "080d4133-bdb5-40a0-96a0-71a6057bfe9a"
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/52b8da2f-61e0-4a1f-8dde-336911f367fb/resourceGroups/SampleResourceGroup_1/providers/10.91.86.47/storageSyncServices/SampleStorage
            SyncService_1/registeredServers/530a0384-50ac-456d-8240-9d6621404151"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storagesync import StorageSyncManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRegisteredServers(AzureRMModuleBase):
    """Configuration class for an Azure RM Registered Server resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            storage_sync_service_name=dict(
                type='str',
                required=True
            ),
            server_id=dict(
                type='str',
                required=True
            ),
            server_certificate=dict(
                type='str'
            ),
            agent_version=dict(
                type='str'
            ),
            server_os_version=dict(
                type='str'
            ),
            last_heart_beat=dict(
                type='str'
            ),
            server_role=dict(
                type='str'
            ),
            cluster_id=dict(
                type='str'
            ),
            cluster_name=dict(
                type='str'
            ),
            server_id=dict(
                type='str'
            ),
            friendly_name=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.storage_sync_service_name = None
        self.server_id = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRegisteredServers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "server_certificate":
                    self.parameters["server_certificate"] = kwargs[key]
                elif key == "agent_version":
                    self.parameters["agent_version"] = kwargs[key]
                elif key == "server_os_version":
                    self.parameters["server_os_version"] = kwargs[key]
                elif key == "last_heart_beat":
                    self.parameters["last_heart_beat"] = kwargs[key]
                elif key == "server_role":
                    self.parameters["server_role"] = kwargs[key]
                elif key == "cluster_id":
                    self.parameters["cluster_id"] = kwargs[key]
                elif key == "cluster_name":
                    self.parameters["cluster_name"] = kwargs[key]
                elif key == "server_id":
                    self.parameters["server_id"] = kwargs[key]
                elif key == "friendly_name":
                    self.parameters["friendly_name"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_registeredserver()

        if not old_response:
            self.log("Registered Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Registered Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Registered Server instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Registered Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_registeredserver()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Registered Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_registeredserver()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_registeredserver():
                time.sleep(20)
        else:
            self.log("Registered Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_registeredserver(self):
        '''
        Creates or updates Registered Server with the specified configuration.

        :return: deserialized Registered Server instance state dictionary
        '''
        self.log("Creating / Updating the Registered Server instance {0}".format(self.server_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.registered_servers.create(resource_group_name=self.resource_group,
                                                                      storage_sync_service_name=self.storage_sync_service_name,
                                                                      server_id=self.server_id,
                                                                      parameters=self.parameters)
            else:
                response = self.mgmt_client.registered_servers.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Registered Server instance.')
            self.fail("Error creating the Registered Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_registeredserver(self):
        '''
        Deletes specified Registered Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Registered Server instance {0}".format(self.server_id))
        try:
            response = self.mgmt_client.registered_servers.delete(resource_group_name=self.resource_group,
                                                                  storage_sync_service_name=self.storage_sync_service_name,
                                                                  server_id=self.server_id)
        except CloudError as e:
            self.log('Error attempting to delete the Registered Server instance.')
            self.fail("Error deleting the Registered Server instance: {0}".format(str(e)))

        return True

    def get_registeredserver(self):
        '''
        Gets the properties of the specified Registered Server.

        :return: deserialized Registered Server instance state dictionary
        '''
        self.log("Checking if the Registered Server instance {0} is present".format(self.server_id))
        found = False
        try:
            response = self.mgmt_client.registered_servers.get(resource_group_name=self.resource_group,
                                                               storage_sync_service_name=self.storage_sync_service_name,
                                                               server_id=self.server_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Registered Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Registered Server instance.')
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
    AzureRMRegisteredServers()


if __name__ == '__main__':
    main()
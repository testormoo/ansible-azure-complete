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
module: azure_rm_storagesyncserverendpoint
version_added: "2.8"
short_description: Manage Server Endpoint instance.
description:
    - Create, update and delete instance of Server Endpoint.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    storage_sync_service_name:
        description:
            - Name of Storage Sync Service resource.
        required: True
    sync_group_name:
        description:
            - Name of Sync Group resource.
        required: True
    name:
        description:
            - Name of Server Endpoint object.
        required: True
    server_local_path:
        description:
            - Server Local path.
    cloud_tiering:
        description:
            - Cloud Tiering.
        choices:
            - 'on'
            - 'off'
    volume_free_space_percent:
        description:
            - Level of free space to be maintained by Cloud Tiering if it is enabled.
    tier_files_older_than_days:
        description:
            - Tier files older than days.
    friendly_name:
        description:
            - Friendly Name
    server_resource_id:
        description:
            - Server Resource Id.
    state:
      description:
        - Assert the state of the Server Endpoint.
        - Use 'present' to create or update an Server Endpoint and 'absent' to delete it.
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
  - name: Create (or update) Server Endpoint
    azure_rm_storagesyncserverendpoint:
      resource_group: SampleResourceGroup_1
      storage_sync_service_name: SampleStorageSyncService_1
      sync_group_name: SampleSyncGroup_1
      name: SampleServerEndpoint_1
      server_local_path: D:\SampleServerEndpoint_1
      cloud_tiering: off
      volume_free_space_percent: 100
      tier_files_older_than_days: 0
      server_resource_id: /subscriptions/3a048283-338f-4002-a9dd-a50fdadcb392/resourceGroups/SampleResourceGroup_1/providers/Microsoft.StorageSync/storageSyncServices/SampleStorageSyncServer_1/registeredServers/080d4133-bdb5-40a0-96a0-71a6057bfe9a
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/52b8da2f-61e0-4a1f-8dde-336911f367fb/resourceGroups/SampleResourceGroup_1/providers/10.91.86.47/storageSyncServices/SampleStorage
            SyncService_1/syncGroups/SampleSyncGroup_1/serverEndpoints/SampleServerEndpoint_1"
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


class AzureRMServerEndpoints(AzureRMModuleBase):
    """Configuration class for an Azure RM Server Endpoint resource"""

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
            sync_group_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            server_local_path=dict(
                type='str'
            ),
            cloud_tiering=dict(
                type='str',
                choices=['on',
                         'off']
            ),
            volume_free_space_percent=dict(
                type='int'
            ),
            tier_files_older_than_days=dict(
                type='int'
            ),
            friendly_name=dict(
                type='str'
            ),
            server_resource_id=dict(
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
        self.sync_group_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServerEndpoints, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "server_local_path":
                    self.parameters["server_local_path"] = kwargs[key]
                elif key == "cloud_tiering":
                    self.parameters["cloud_tiering"] = kwargs[key]
                elif key == "volume_free_space_percent":
                    self.parameters["volume_free_space_percent"] = kwargs[key]
                elif key == "tier_files_older_than_days":
                    self.parameters["tier_files_older_than_days"] = kwargs[key]
                elif key == "friendly_name":
                    self.parameters["friendly_name"] = kwargs[key]
                elif key == "server_resource_id":
                    self.parameters["server_resource_id"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_serverendpoint()

        if not old_response:
            self.log("Server Endpoint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Server Endpoint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Server Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_serverendpoint()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Server Endpoint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_serverendpoint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_serverendpoint():
                time.sleep(20)
        else:
            self.log("Server Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_serverendpoint(self):
        '''
        Creates or updates Server Endpoint with the specified configuration.

        :return: deserialized Server Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Server Endpoint instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.server_endpoints.create(resource_group_name=self.resource_group,
                                                                    storage_sync_service_name=self.storage_sync_service_name,
                                                                    sync_group_name=self.sync_group_name,
                                                                    server_endpoint_name=self.name,
                                                                    parameters=self.parameters)
            else:
                response = self.mgmt_client.server_endpoints.update(resource_group_name=self.resource_group,
                                                                    storage_sync_service_name=self.storage_sync_service_name,
                                                                    sync_group_name=self.sync_group_name,
                                                                    server_endpoint_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Server Endpoint instance.')
            self.fail("Error creating the Server Endpoint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serverendpoint(self):
        '''
        Deletes specified Server Endpoint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Server Endpoint instance {0}".format(self.name))
        try:
            response = self.mgmt_client.server_endpoints.delete(resource_group_name=self.resource_group,
                                                                storage_sync_service_name=self.storage_sync_service_name,
                                                                sync_group_name=self.sync_group_name,
                                                                server_endpoint_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Server Endpoint instance.')
            self.fail("Error deleting the Server Endpoint instance: {0}".format(str(e)))

        return True

    def get_serverendpoint(self):
        '''
        Gets the properties of the specified Server Endpoint.

        :return: deserialized Server Endpoint instance state dictionary
        '''
        self.log("Checking if the Server Endpoint instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.server_endpoints.get(resource_group_name=self.resource_group,
                                                             storage_sync_service_name=self.storage_sync_service_name,
                                                             sync_group_name=self.sync_group_name,
                                                             server_endpoint_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Server Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Server Endpoint instance.')
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


def main():
    """Main execution"""
    AzureRMServerEndpoints()


if __name__ == '__main__':
    main()

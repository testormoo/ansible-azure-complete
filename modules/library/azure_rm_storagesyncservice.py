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
module: azure_rm_storagesyncservice
version_added: "2.8"
short_description: Manage Storage Sync Service instance.
description:
    - Create, update and delete instance of Storage Sync Service.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    storage_sync_service_name:
        description:
            - Name of Storage Sync Service resource.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
      description:
        - Assert the state of the Storage Sync Service.
        - Use 'present' to create or update an Storage Sync Service and 'absent' to delete it.
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
  - name: Create (or update) Storage Sync Service
    azure_rm_storagesyncservice:
      resource_group: SampleResourceGroup_1
      storage_sync_service_name: SampleStorageSyncService_1
      location: eastus
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/3a048283-338f-4002-a9dd-a50fdadcb392/resourceGroups/SampleResourceGroup_1/providers/Microsoft.StorageSync/storageSyncServices/Sam
            pleStorageSyncService_1"
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


class AzureRMStorageSyncServices(AzureRMModuleBase):
    """Configuration class for an Azure RM Storage Sync Service resource"""

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
            location=dict(
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
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStorageSyncServices, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_storagesyncservice()

        if not old_response:
            self.log("Storage Sync Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Storage Sync Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Storage Sync Service instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Storage Sync Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_storagesyncservice()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Storage Sync Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_storagesyncservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_storagesyncservice():
                time.sleep(20)
        else:
            self.log("Storage Sync Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_storagesyncservice(self):
        '''
        Creates or updates Storage Sync Service with the specified configuration.

        :return: deserialized Storage Sync Service instance state dictionary
        '''
        self.log("Creating / Updating the Storage Sync Service instance {0}".format(self.storage_sync_service_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.storage_sync_services.create(resource_group_name=self.resource_group,
                                                                         storage_sync_service_name=self.storage_sync_service_name,
                                                                         parameters=self.parameters)
            else:
                response = self.mgmt_client.storage_sync_services.update(resource_group_name=self.resource_group,
                                                                         storage_sync_service_name=self.storage_sync_service_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Storage Sync Service instance.')
            self.fail("Error creating the Storage Sync Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_storagesyncservice(self):
        '''
        Deletes specified Storage Sync Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Storage Sync Service instance {0}".format(self.storage_sync_service_name))
        try:
            response = self.mgmt_client.storage_sync_services.delete(resource_group_name=self.resource_group,
                                                                     storage_sync_service_name=self.storage_sync_service_name)
        except CloudError as e:
            self.log('Error attempting to delete the Storage Sync Service instance.')
            self.fail("Error deleting the Storage Sync Service instance: {0}".format(str(e)))

        return True

    def get_storagesyncservice(self):
        '''
        Gets the properties of the specified Storage Sync Service.

        :return: deserialized Storage Sync Service instance state dictionary
        '''
        self.log("Checking if the Storage Sync Service instance {0} is present".format(self.storage_sync_service_name))
        found = False
        try:
            response = self.mgmt_client.storage_sync_services.get(resource_group_name=self.resource_group,
                                                                  storage_sync_service_name=self.storage_sync_service_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Storage Sync Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Storage Sync Service instance.')
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
    AzureRMStorageSyncServices()


if __name__ == '__main__':
    main()

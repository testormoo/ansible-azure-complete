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
module: azure_rm_storagesyncsyncgroup
version_added: "2.8"
short_description: Manage Sync Group instance.
description:
    - Create, update and delete instance of Sync Group.

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
    properties:
        description:
            - The parameters used to create the sync group
    state:
      description:
        - Assert the state of the Sync Group.
        - Use 'present' to create or update an Sync Group and 'absent' to delete it.
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
  - name: Create (or update) Sync Group
    azure_rm_storagesyncsyncgroup:
      resource_group: SampleResourceGroup_1
      storage_sync_service_name: SampleStorageSyncService_1
      sync_group_name: SampleSyncGroup_1
      properties: NOT FOUND
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/3a048283-338f-4002-a9dd-a50fdadcb392/resourceGroups/SampleResourceGroup_1/providers/Microsoft.StorageSync/storageSyncServices/Sam
            pleStorageSyncService_1/syncGroups/SampleSyncGroup_1"
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


class AzureRMSyncGroups(AzureRMModuleBase):
    """Configuration class for an Azure RM Sync Group resource"""

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
            properties=dict(
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
        self.properties = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSyncGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_syncgroup()

        if not old_response:
            self.log("Sync Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Sync Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Sync Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Sync Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_syncgroup()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Sync Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_syncgroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_syncgroup():
                time.sleep(20)
        else:
            self.log("Sync Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_syncgroup(self):
        '''
        Creates or updates Sync Group with the specified configuration.

        :return: deserialized Sync Group instance state dictionary
        '''
        self.log("Creating / Updating the Sync Group instance {0}".format(self.sync_group_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.sync_groups.create(resource_group_name=self.resource_group,
                                                               storage_sync_service_name=self.storage_sync_service_name,
                                                               sync_group_name=self.sync_group_name)
            else:
                response = self.mgmt_client.sync_groups.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Sync Group instance.')
            self.fail("Error creating the Sync Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_syncgroup(self):
        '''
        Deletes specified Sync Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Sync Group instance {0}".format(self.sync_group_name))
        try:
            response = self.mgmt_client.sync_groups.delete(resource_group_name=self.resource_group,
                                                           storage_sync_service_name=self.storage_sync_service_name,
                                                           sync_group_name=self.sync_group_name)
        except CloudError as e:
            self.log('Error attempting to delete the Sync Group instance.')
            self.fail("Error deleting the Sync Group instance: {0}".format(str(e)))

        return True

    def get_syncgroup(self):
        '''
        Gets the properties of the specified Sync Group.

        :return: deserialized Sync Group instance state dictionary
        '''
        self.log("Checking if the Sync Group instance {0} is present".format(self.sync_group_name))
        found = False
        try:
            response = self.mgmt_client.sync_groups.get(resource_group_name=self.resource_group,
                                                        storage_sync_service_name=self.storage_sync_service_name,
                                                        sync_group_name=self.sync_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Sync Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Sync Group instance.')
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
    AzureRMSyncGroups()


if __name__ == '__main__':
    main()

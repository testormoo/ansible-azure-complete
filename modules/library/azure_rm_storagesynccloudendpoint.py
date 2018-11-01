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
module: azure_rm_storagesynccloudendpoint
version_added: "2.8"
short_description: Manage Cloud Endpoint instance.
description:
    - Create, update and delete instance of Cloud Endpoint.

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
    cloud_endpoint_name:
        description:
            - Name of Cloud Endpoint object.
        required: True
    storage_account_resource_id:
        description:
            - Storage Account Resource Id
    storage_account_share_name:
        description:
            - Storage Account Share name
    storage_account_tenant_id:
        description:
            - Storage Account Tenant Id
    state:
      description:
        - Assert the state of the Cloud Endpoint.
        - Use 'present' to create or update an Cloud Endpoint and 'absent' to delete it.
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
  - name: Create (or update) Cloud Endpoint
    azure_rm_storagesynccloudendpoint:
      resource_group: SampleResourceGroup_1
      storage_sync_service_name: SampleStorageSyncService_1
      sync_group_name: SampleSyncGroup_1
      cloud_endpoint_name: SampleCloudEndpoint_1
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/52b8da2f-61e0-4a1f-8dde-336911f367fb/resourceGroups/SampleResourceGroup_1/providers/10.91.86.47/storageSyncServices/SampleStorage
            SyncService_1/syncGroups/SampleSyncGroup_1/cloudEndpoints/SampleCloudEndpoint_1"
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


class AzureRMCloudEndpoints(AzureRMModuleBase):
    """Configuration class for an Azure RM Cloud Endpoint resource"""

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
            cloud_endpoint_name=dict(
                type='str',
                required=True
            ),
            storage_account_resource_id=dict(
                type='str'
            ),
            storage_account_share_name=dict(
                type='str'
            ),
            storage_account_tenant_id=dict(
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
        self.cloud_endpoint_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCloudEndpoints, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "storage_account_resource_id":
                    self.parameters["storage_account_resource_id"] = kwargs[key]
                elif key == "storage_account_share_name":
                    self.parameters["storage_account_share_name"] = kwargs[key]
                elif key == "storage_account_tenant_id":
                    self.parameters["storage_account_tenant_id"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_cloudendpoint()

        if not old_response:
            self.log("Cloud Endpoint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Cloud Endpoint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Cloud Endpoint instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Cloud Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_cloudendpoint()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Cloud Endpoint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_cloudendpoint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_cloudendpoint():
                time.sleep(20)
        else:
            self.log("Cloud Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_cloudendpoint(self):
        '''
        Creates or updates Cloud Endpoint with the specified configuration.

        :return: deserialized Cloud Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Cloud Endpoint instance {0}".format(self.cloud_endpoint_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.cloud_endpoints.create(resource_group_name=self.resource_group,
                                                                   storage_sync_service_name=self.storage_sync_service_name,
                                                                   sync_group_name=self.sync_group_name,
                                                                   cloud_endpoint_name=self.cloud_endpoint_name,
                                                                   parameters=self.parameters)
            else:
                response = self.mgmt_client.cloud_endpoints.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Cloud Endpoint instance.')
            self.fail("Error creating the Cloud Endpoint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_cloudendpoint(self):
        '''
        Deletes specified Cloud Endpoint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Cloud Endpoint instance {0}".format(self.cloud_endpoint_name))
        try:
            response = self.mgmt_client.cloud_endpoints.delete(resource_group_name=self.resource_group,
                                                               storage_sync_service_name=self.storage_sync_service_name,
                                                               sync_group_name=self.sync_group_name,
                                                               cloud_endpoint_name=self.cloud_endpoint_name)
        except CloudError as e:
            self.log('Error attempting to delete the Cloud Endpoint instance.')
            self.fail("Error deleting the Cloud Endpoint instance: {0}".format(str(e)))

        return True

    def get_cloudendpoint(self):
        '''
        Gets the properties of the specified Cloud Endpoint.

        :return: deserialized Cloud Endpoint instance state dictionary
        '''
        self.log("Checking if the Cloud Endpoint instance {0} is present".format(self.cloud_endpoint_name))
        found = False
        try:
            response = self.mgmt_client.cloud_endpoints.get(resource_group_name=self.resource_group,
                                                            storage_sync_service_name=self.storage_sync_service_name,
                                                            sync_group_name=self.sync_group_name,
                                                            cloud_endpoint_name=self.cloud_endpoint_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Cloud Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Cloud Endpoint instance.')
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
    AzureRMCloudEndpoints()


if __name__ == '__main__':
    main()

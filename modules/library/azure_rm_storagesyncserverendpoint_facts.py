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
module: azure_rm_storagesyncserverendpoint_facts
version_added: "2.8"
short_description: Get Azure Server Endpoint facts.
description:
    - Get facts of Azure Server Endpoint.

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

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Server Endpoint
    azure_rm_storagesyncserverendpoint_facts:
      resource_group: resource_group_name
      storage_sync_service_name: storage_sync_service_name
      sync_group_name: sync_group_name
      name: server_endpoint_name

  - name: List instances of Server Endpoint
    azure_rm_storagesyncserverendpoint_facts:
      resource_group: resource_group_name
      storage_sync_service_name: storage_sync_service_name
      sync_group_name: sync_group_name
'''

RETURN = '''
server_endpoints:
    description: A list of dictionaries containing facts for Server Endpoint.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/3a048283-338f-4002-a9dd-a50fdadcb392/resourceGroups/SampleResourceGroup_1/providers/Microsoft.StorageSync/storageSyncServ
                    ices/SampleStorageSyncService_1/syncGroups/SyncGroup_Restore_08-08_Test112/serverEndpoints/SampleServerEndpoint_1"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: SampleServerEndpoint_1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storagesync import StorageSyncManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServerEndpointsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
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
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.storage_sync_service_name = None
        self.sync_group_name = None
        self.name = None
        super(AzureRMServerEndpointsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorageSyncManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['server_endpoints'] = self.get()
        else:
            self.results['server_endpoints'] = self.list_by_sync_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.server_endpoints.get(resource_group_name=self.resource_group,
                                                             storage_sync_service_name=self.storage_sync_service_name,
                                                             sync_group_name=self.sync_group_name,
                                                             server_endpoint_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ServerEndpoints.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_sync_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.server_endpoints.list_by_sync_group(resource_group_name=self.resource_group,
                                                                            storage_sync_service_name=self.storage_sync_service_name,
                                                                            sync_group_name=self.sync_group_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ServerEndpoints.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMServerEndpointsFacts()


if __name__ == '__main__':
    main()

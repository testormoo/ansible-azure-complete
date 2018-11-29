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
short_description: Manage Azure Storage Sync Service instance.
description:
    - Create, update and delete instance of Azure Storage Sync Service.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    name:
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
      name: SampleStorageSyncService_1
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMStorageSyncService(AzureRMModuleBase):
    """Configuration class for an Azure RM Storage Sync Service resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStorageSyncService, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Storage Sync Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_storagesyncservice()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Storage Sync Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_storagesyncservice()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Storage Sync Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_storagesyncservice(self):
        '''
        Creates or updates Storage Sync Service with the specified configuration.

        :return: deserialized Storage Sync Service instance state dictionary
        '''
        self.log("Creating / Updating the Storage Sync Service instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.storage_sync_services.create(resource_group_name=self.resource_group,
                                                                         storage_sync_service_name=self.name,
                                                                         parameters=self.parameters)
            else:
                response = self.mgmt_client.storage_sync_services.update(resource_group_name=self.resource_group,
                                                                         storage_sync_service_name=self.name)
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
        self.log("Deleting the Storage Sync Service instance {0}".format(self.name))
        try:
            response = self.mgmt_client.storage_sync_services.delete(resource_group_name=self.resource_group,
                                                                     storage_sync_service_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Storage Sync Service instance.')
            self.fail("Error deleting the Storage Sync Service instance: {0}".format(str(e)))

        return True

    def get_storagesyncservice(self):
        '''
        Gets the properties of the specified Storage Sync Service.

        :return: deserialized Storage Sync Service instance state dictionary
        '''
        self.log("Checking if the Storage Sync Service instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.storage_sync_services.get(resource_group_name=self.resource_group,
                                                                  storage_sync_service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Storage Sync Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Storage Sync Service instance.')
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
            else:
                key = list(old[0])[0]
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def main():
    """Main execution"""
    AzureRMStorageSyncService()


if __name__ == '__main__':
    main()

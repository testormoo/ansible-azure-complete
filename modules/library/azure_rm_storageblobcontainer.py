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
module: azure_rm_storageblobcontainer
version_added: "2.8"
short_description: Manage Blob Container instance.
description:
    - Create, update and delete instance of Blob Container.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    account_name:
        description:
            - "The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and
               use numbers and lower-case letters only."
        required: True
    container_name:
        description:
            - "The name of the C(blob) C(container) within the specified storage account. C(blob) C(container) names must be between 3 and 63 characters in
               length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter
               or number."
        required: True
    public_access:
        description:
            - Specifies whether data in the C(container) may be accessed publicly and the level of access.
        choices:
            - 'container'
            - 'blob'
            - 'none'
    metadata:
        description:
            - A name-value pair to associate with the C(container) as metadata.
    state:
      description:
        - Assert the state of the Blob Container.
        - Use 'present' to create or update an Blob Container and 'absent' to delete it.
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
  - name: Create (or update) Blob Container
    azure_rm_storageblobcontainer:
      resource_group: res3376
      account_name: sto328
      container_name: container6185
      public_access: NOT FOUND
      metadata: metadata
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/{subscription-id}/resourceGroups/res3376/providers/Microsoft.Storage/storageAccounts/sto328/blobServices/default/containers/conta
            iner6185"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storage import StorageManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMBlobContainers(AzureRMModuleBase):
    """Configuration class for an Azure RM Blob Container resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            container_name=dict(
                type='str',
                required=True
            ),
            public_access=dict(
                type='str',
                choices=['container',
                         'blob',
                         'none']
            ),
            metadata=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.container_name = None
        self.public_access = None
        self.metadata = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBlobContainers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorageManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_blobcontainer()

        if not old_response:
            self.log("Blob Container instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Blob Container instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Blob Container instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Blob Container instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_blobcontainer()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Blob Container instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_blobcontainer()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_blobcontainer():
                time.sleep(20)
        else:
            self.log("Blob Container instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_blobcontainer(self):
        '''
        Creates or updates Blob Container with the specified configuration.

        :return: deserialized Blob Container instance state dictionary
        '''
        self.log("Creating / Updating the Blob Container instance {0}".format(self.container_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.blob_containers.create(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   container_name=self.container_name)
            else:
                response = self.mgmt_client.blob_containers.update(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   container_name=self.container_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Blob Container instance.')
            self.fail("Error creating the Blob Container instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_blobcontainer(self):
        '''
        Deletes specified Blob Container instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Blob Container instance {0}".format(self.container_name))
        try:
            response = self.mgmt_client.blob_containers.delete(resource_group_name=self.resource_group,
                                                               account_name=self.account_name,
                                                               container_name=self.container_name)
        except CloudError as e:
            self.log('Error attempting to delete the Blob Container instance.')
            self.fail("Error deleting the Blob Container instance: {0}".format(str(e)))

        return True

    def get_blobcontainer(self):
        '''
        Gets the properties of the specified Blob Container.

        :return: deserialized Blob Container instance state dictionary
        '''
        self.log("Checking if the Blob Container instance {0} is present".format(self.container_name))
        found = False
        try:
            response = self.mgmt_client.blob_containers.get(resource_group_name=self.resource_group,
                                                            account_name=self.account_name,
                                                            container_name=self.container_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Blob Container instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Blob Container instance.')
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
    AzureRMBlobContainers()


if __name__ == '__main__':
    main()

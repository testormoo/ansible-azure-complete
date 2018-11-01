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
module: azure_rm_netappvolume
version_added: "2.8"
short_description: Manage Volume instance.
description:
    - Create, update and delete instance of Volume.

options:
    body:
        description:
            - Volume object supplied in the body of the operation.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                required: True
            name1:
                description:
                    - FileSystem name
            creation_token:
                description:
                    - A unique file path for the volume. Used when creating mount targets
                required: True
            service_level:
                description:
                    - The service level of the file system.
                required: True
                choices:
                    - 'basic'
                    - 'standard'
                    - 'premium'
            usage_threshold:
                description:
                    - Maximum storage quota allowed for a file system in bytes. This is a soft quota used for alerting only. Upper limit is 100TB.
            subnet_id:
                description:
                    - The Azure Resource URI for a delegated subnet. Must have the delegation Microsoft.NetApp/volumes
    resource_group:
        description:
            - The name of the resource group.
        required: True
    account_name:
        description:
            - The name of the NetApp account
        required: True
    pool_name:
        description:
            - The name of the capacity pool
        required: True
    volume_name:
        description:
            - The name of the volume
        required: True
    state:
      description:
        - Assert the state of the Volume.
        - Use 'present' to create or update an Volume and 'absent' to delete it.
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
  - name: Create (or update) Volume
    azure_rm_netappvolume:
      resource_group: resourceGroup
      account_name: accountName
      pool_name: poolName
      volume_name: volumeName
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.netapp import AzureNetAppFilesManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVolumes(AzureRMModuleBase):
    """Configuration class for an Azure RM Volume resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            body=dict(
                type='dict',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            pool_name=dict(
                type='str',
                required=True
            ),
            volume_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.body = dict()
        self.resource_group = None
        self.account_name = None
        self.pool_name = None
        self.volume_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVolumes, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.body["location"] = kwargs[key]
                elif key == "name1":
                    self.body["name1"] = kwargs[key]
                elif key == "creation_token":
                    self.body["creation_token"] = kwargs[key]
                elif key == "service_level":
                    self.body["service_level"] = _snake_to_camel(kwargs[key], True)
                elif key == "usage_threshold":
                    self.body["usage_threshold"] = kwargs[key]
                elif key == "subnet_id":
                    self.body["subnet_id"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureNetAppFilesManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_volume()

        if not old_response:
            self.log("Volume instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Volume instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Volume instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Volume instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_volume()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Volume instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_volume()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_volume():
                time.sleep(20)
        else:
            self.log("Volume instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_volume(self):
        '''
        Creates or updates Volume with the specified configuration.

        :return: deserialized Volume instance state dictionary
        '''
        self.log("Creating / Updating the Volume instance {0}".format(self.volume_name))

        try:
            response = self.mgmt_client.volumes.create_or_update(body=self.body,
                                                                 resource_group=self.resource_group,
                                                                 account_name=self.account_name,
                                                                 pool_name=self.pool_name,
                                                                 volume_name=self.volume_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Volume instance.')
            self.fail("Error creating the Volume instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_volume(self):
        '''
        Deletes specified Volume instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Volume instance {0}".format(self.volume_name))
        try:
            response = self.mgmt_client.volumes.delete(resource_group=self.resource_group,
                                                       account_name=self.account_name,
                                                       pool_name=self.pool_name,
                                                       volume_name=self.volume_name)
        except CloudError as e:
            self.log('Error attempting to delete the Volume instance.')
            self.fail("Error deleting the Volume instance: {0}".format(str(e)))

        return True

    def get_volume(self):
        '''
        Gets the properties of the specified Volume.

        :return: deserialized Volume instance state dictionary
        '''
        self.log("Checking if the Volume instance {0} is present".format(self.volume_name))
        found = False
        try:
            response = self.mgmt_client.volumes.get(resource_group=self.resource_group,
                                                    account_name=self.account_name,
                                                    pool_name=self.pool_name,
                                                    volume_name=self.volume_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Volume instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Volume instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMVolumes()


if __name__ == '__main__':
    main()

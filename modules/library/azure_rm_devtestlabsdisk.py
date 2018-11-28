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
module: azure_rm_devtestlabsdisk
version_added: "2.8"
short_description: Manage Azure Disk instance.
description:
    - Create, update and delete instance of Azure Disk.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    lab_name:
        description:
            - The name of the lab.
        required: True
    user_name:
        description:
            - The name of the user profile.
        required: True
    name:
        description:
            - The name of the disk.
        required: True
    location:
        description:
            - The location of the resource.
    disk_type:
        description:
            - The storage type for the disk (i.e. C(standard), C(premium)).
        choices:
            - 'standard'
            - 'premium'
    disk_size_gi_b:
        description:
            - The size of the disk in GibiBytes.
    leased_by_lab_vm_id:
        description:
            - The resource ID of the VM to which this disk is leased.
    disk_blob_name:
        description:
            - When backed by a blob, the name of the VHD blob without extension.
    disk_uri:
        description:
            - When backed by a blob, the URI of underlying blob.
    host_caching:
        description:
            - The host caching policy of the disk (i.e. None, ReadOnly, ReadWrite).
    managed_disk_id:
        description:
            - When backed by managed disk, this is the ID of the compute disk resource.
    state:
      description:
        - Assert the state of the Disk.
        - Use 'present' to create or update an Disk and 'absent' to delete it.
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
  - name: Create (or update) Disk
    azure_rm_devtestlabsdisk:
      resource_group: NOT FOUND
      lab_name: NOT FOUND
      user_name: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The identifier of the resource.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.devtestlabs import DevTestLabsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDisk(AzureRMModuleBase):
    """Configuration class for an Azure RM Disk resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            lab_name=dict(
                type='str',
                required=True
            ),
            user_name=dict(
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
            disk_type=dict(
                type='str',
                choices=['standard',
                         'premium']
            ),
            disk_size_gi_b=dict(
                type='int'
            ),
            leased_by_lab_vm_id=dict(
                type='str'
            ),
            disk_blob_name=dict(
                type='str'
            ),
            disk_uri=dict(
                type='str'
            ),
            host_caching=dict(
                type='str'
            ),
            managed_disk_id=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.lab_name = None
        self.user_name = None
        self.name = None
        self.disk = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDisk, self).__init__(derived_arg_spec=self.module_arg_spec,
                                          supports_check_mode=True,
                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.disk[key] = kwargs[key]

        dict_camelize(self.disk, ['disk_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_disk()

        if not old_response:
            self.log("Disk instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Disk instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.disk, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Disk instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_disk()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Disk instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_disk()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Disk instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_disk(self):
        '''
        Creates or updates Disk with the specified configuration.

        :return: deserialized Disk instance state dictionary
        '''
        self.log("Creating / Updating the Disk instance {0}".format(self.name))

        try:
            response = self.mgmt_client.disks.create_or_update(resource_group_name=self.resource_group,
                                                               lab_name=self.lab_name,
                                                               user_name=self.user_name,
                                                               name=self.name,
                                                               disk=self.disk)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Disk instance.')
            self.fail("Error creating the Disk instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_disk(self):
        '''
        Deletes specified Disk instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Disk instance {0}".format(self.name))
        try:
            response = self.mgmt_client.disks.delete(resource_group_name=self.resource_group,
                                                     lab_name=self.lab_name,
                                                     user_name=self.user_name,
                                                     name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Disk instance.')
            self.fail("Error deleting the Disk instance: {0}".format(str(e)))

        return True

    def get_disk(self):
        '''
        Gets the properties of the specified Disk.

        :return: deserialized Disk instance state dictionary
        '''
        self.log("Checking if the Disk instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.disks.get(resource_group_name=self.resource_group,
                                                  lab_name=self.lab_name,
                                                  user_name=self.user_name,
                                                  name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Disk instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Disk instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMDisk()


if __name__ == '__main__':
    main()

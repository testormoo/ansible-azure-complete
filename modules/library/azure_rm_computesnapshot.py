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
module: azure_rm_computesnapshot
version_added: "2.8"
short_description: Manage Azure Snapshot instance.
description:
    - Create, update and delete instance of Azure Snapshot.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - "The name of the snapshot that is being created. The name can't be changed after the snapshot is created. Supported characters for the name
               are a-z, A-Z, 0-9 and _. The max name length is 80 characters."
        required: True
    location:
        description:
            - Resource location
            - Required when C(state) is I(present).
    sku:
        description:
        suboptions:
            name:
                description:
                    - The sku name.
                choices:
                    - 'standard_lrs'
                    - 'premium_lrs'
                    - 'standard_zrs'
    os_type:
        description:
            - The Operating System type.
        choices:
            - 'windows'
            - 'linux'
    creation_data:
        description:
            - Disk source information. CreationData information cannot be changed after the disk has been created.
            - Required when C(state) is I(present).
        suboptions:
            create_option:
                description:
                    - "This enumerates the possible sources of a disk's creation."
                    - Required when C(state) is I(present).
                choices:
                    - 'empty'
                    - 'attach'
                    - 'from_image'
                    - 'import'
                    - 'copy'
                    - 'restore'
            storage_account_id:
                description:
                    - "If I(create_option) is C(import), the Azure Resource Manager identifier of the storage account containing the blob to C(import) as a
                       disk. Required only if the blob is in a different subscription"
            image_reference:
                description:
                    - Disk source information.
                suboptions:
                    id:
                        description:
                            - A relative uri containing either a Platform Image Repository or user image reference.
                            - Required when C(state) is I(present).
                    lun:
                        description:
                            - "If the disk is created from an image's data disk, this is an index that indicates which of the data disks in the image to
                               use. For OS disks, this field is null."
            source_uri:
                description:
                    - If I(create_option) is C(import), this is the URI of a blob to be imported into a managed disk.
            source_resource_id:
                description:
                    - If I(create_option) is C(copy), this is the ARM id of the source snapshot or disk.
    disk_size_gb:
        description:
            - "If I(creation_data).createOption is Empty, this field is mandatory and it indicates the size of the VHD to create. If this field is present
               for updates or creation with other options, it indicates a resize. Resizes are only allowed if the disk is not attached to a running VM, and
               can only increase the disk's size."
    encryption_settings:
        description:
            - Encryption settings for disk or snapshot
        suboptions:
            enabled:
                description:
                    - "Set this flag to true and provide I(disk_encryption_key) and optional I(key_encryption_key) to enable encryption. Set this flag to
                       false and remove I(disk_encryption_key) and I(key_encryption_key) to disable encryption. If EncryptionSettings is null in the
                       request object, the existing settings remain unchanged."
            disk_encryption_key:
                description:
                    - Key Vault Secret Url and vault id of the disk encryption key
                suboptions:
                    source_vault:
                        description:
                            - Resource id of the KeyVault containing the key or secret
                            - Required when C(state) is I(present).
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                    secret_url:
                        description:
                            - Url pointing to a key or secret in KeyVault
                            - Required when C(state) is I(present).
            key_encryption_key:
                description:
                    - Key Vault Key Url and vault id of the key encryption key
                suboptions:
                    source_vault:
                        description:
                            - Resource id of the KeyVault containing the key or secret
                            - Required when C(state) is I(present).
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                    key_url:
                        description:
                            - Url pointing to a key or secret in KeyVault
                            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Snapshot.
        - Use 'present' to create or update an Snapshot and 'absent' to delete it.
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
  - name: Create (or update) Snapshot
    azure_rm_computesnapshot:
      resource_group: myResourceGroup
      name: mySnapshot2
      location: West US
      creation_data:
        create_option: Copy
        source_resource_id: subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Compute/snapshots/mySnapshot1
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
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSnapshot(AzureRMModuleBase):
    """Configuration class for an Azure RM Snapshot resource"""

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
            sku=dict(
                type='dict'
            ),
            os_type=dict(
                type='str',
                choices=['windows',
                         'linux']
            ),
            creation_data=dict(
                type='dict'
            ),
            disk_size_gb=dict(
                type='int'
            ),
            encryption_settings=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.snapshot = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSnapshot, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.snapshot[key] = kwargs[key]

        dict_camelize(self.snapshot, ['sku', 'name'], True)
        dict_map(self.snapshot, ['sku', 'name'], {'standard_lrs': 'Standard_LRS', 'premium_lrs': 'Premium_LRS', 'standard_zrs': 'Standard_ZRS'})
        dict_camelize(self.snapshot, ['os_type'], True)
        dict_camelize(self.snapshot, ['creation_data', 'create_option'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_snapshot()

        if not old_response:
            self.log("Snapshot instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Snapshot instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.snapshot, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Snapshot instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_snapshot()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Snapshot instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_snapshot()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_snapshot():
                time.sleep(20)
        else:
            self.log("Snapshot instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_snapshot(self):
        '''
        Creates or updates Snapshot with the specified configuration.

        :return: deserialized Snapshot instance state dictionary
        '''
        self.log("Creating / Updating the Snapshot instance {0}".format(self.name))

        try:
            response = self.mgmt_client.snapshots.create_or_update(resource_group_name=self.resource_group,
                                                                   snapshot_name=self.name,
                                                                   snapshot=self.snapshot)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Snapshot instance.')
            self.fail("Error creating the Snapshot instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_snapshot(self):
        '''
        Deletes specified Snapshot instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Snapshot instance {0}".format(self.name))
        try:
            response = self.mgmt_client.snapshots.delete(resource_group_name=self.resource_group,
                                                         snapshot_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Snapshot instance.')
            self.fail("Error deleting the Snapshot instance: {0}".format(str(e)))

        return True

    def get_snapshot(self):
        '''
        Gets the properties of the specified Snapshot.

        :return: deserialized Snapshot instance state dictionary
        '''
        self.log("Checking if the Snapshot instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.snapshots.get(resource_group_name=self.resource_group,
                                                      snapshot_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Snapshot instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Snapshot instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


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


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMSnapshot()


if __name__ == '__main__':
    main()

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
module: azure_rm_computedisk
version_added: "2.8"
short_description: Manage Azure Disk instance.
description:
    - Create, update and delete instance of Azure Disk.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - "The name of the managed disk that is being created. The name can't be changed after the disk is created. Supported characters for the name
               are a-z, A-Z, 0-9 and _. The maximum name length is 80 characters."
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
                    - 'standard_ssd_lrs'
                    - 'ultra_ssd_lrs'
    zones:
        description:
            - The Logical zone list for Disk.
        type: list
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
    disk_iops_read_write:
        description:
            - The number of IOPS allowed for this disk; only settable for UltraSSD disks. One operation can transfer between 4k and 256k bytes.
    disk_mbps_read_write:
        description:
            - "The bandwidth allowed for this disk; only settable for UltraSSD disks. MBps means millions of bytes per second - MB here uses the ISO
               notation, of powers of 10."
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
    azure_rm_computedisk:
      resource_group: myResourceGroup
      name: myDisk
      location: West US
      creation_data:
        create_option: Empty
      disk_size_gb: 200
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMDisk(AzureRMModuleBase):
    """Configuration class for an Azure RM Disk resource"""

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
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['standard_lrs',
                                 'premium_lrs',
                                 'standard_ssd_lrs',
                                 'ultra_ssd_lrs']
                    )
                )
            ),
            zones=dict(
                type='list'
            ),
            os_type=dict(
                type='str',
                choices=['windows',
                         'linux']
            ),
            creation_data=dict(
                type='dict',
                options=dict(
                    create_option=dict(
                        type='str',
                        choices=['empty',
                                 'attach',
                                 'from_image',
                                 'import',
                                 'copy',
                                 'restore']
                    ),
                    storage_account_id=dict(
                        type='str'
                    ),
                    image_reference=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            lun=dict(
                                type='int'
                            )
                        )
                    ),
                    source_uri=dict(
                        type='str'
                    ),
                    source_resource_id=dict(
                        type='str'
                    )
                )
            ),
            disk_size_gb=dict(
                type='int'
            ),
            encryption_settings=dict(
                type='dict',
                options=dict(
                    enabled=dict(
                        type='str'
                    ),
                    disk_encryption_key=dict(
                        type='dict',
                        options=dict(
                            source_vault=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            secret_url=dict(
                                type='str'
                            )
                        )
                    ),
                    key_encryption_key=dict(
                        type='dict',
                        options=dict(
                            source_vault=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            key_url=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            disk_iops_read_write=dict(
                type='int'
            ),
            disk_mbps_read_write=dict(
                type='int'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
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

        dict_camelize(self.disk, ['sku', 'name'], True)
        dict_map(self.disk, ['sku', 'name'], {'standard_lrs': 'Standard_LRS', 'premium_lrs': 'Premium_LRS', 'standard_ssd_lrs': 'StandardSSD_LRS', 'ultra_ssd_lrs': 'UltraSSD_LRS'})
        dict_camelize(self.disk, ['os_type'], True)
        dict_camelize(self.disk, ['creation_data', 'create_option'], True)
        dict_resource_id(self.disk, ['creation_data', 'image_reference', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.disk, ['encryption_settings', 'disk_encryption_key', 'source_vault', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.disk, ['encryption_settings', 'key_encryption_key', 'source_vault', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
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
                                                               disk_name=self.name,
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
                                                     disk_name=self.name)
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
                                                  disk_name=self.name)
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMDisk()


if __name__ == '__main__':
    main()

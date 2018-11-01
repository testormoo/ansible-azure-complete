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
short_description: Manage Disk instance.
description:
    - Create, update and delete instance of Disk.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    disk_name:
        description:
            - "The name of the managed I(disk) that is being created. The name can't be changed after the I(disk) is created. Supported characters for the
               name are a-z, A-Z, 0-9 and _. The maximum name length is 80 characters."
        required: True
    disk:
        description:
            - Disk object supplied in the body of the Put disk operation.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                required: True
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
                required: True
                suboptions:
                    create_option:
                        description:
                            - "This enumerates the possible sources of a disk's creation."
                        required: True
                        choices:
                            - 'empty'
                            - 'attach'
                            - 'from_image'
                            - 'import'
                            - 'copy'
                            - 'restore'
                    storage_account_id:
                        description:
                            - "If I(create_option) is C(import), the Azure Resource Manager identifier of the storage account containing the blob to
                               C(import) as a disk. Required only if the blob is in a different subscription"
                    image_reference:
                        description:
                            - Disk source information.
                        suboptions:
                            id:
                                description:
                                    - A relative uri containing either a Platform Image Repository or user image reference.
                                required: True
                            lun:
                                description:
                                    - "If the disk is created from an image's data disk, this is an index that indicates which of the data disks in the
                                       image to use. For OS disks, this field is null."
                    source_uri:
                        description:
                            - If I(create_option) is C(import), this is the URI of a blob to be imported into a managed disk.
                    source_resource_id:
                        description:
                            - If I(create_option) is C(copy), this is the ARM id of the source snapshot or disk.
            disk_size_gb:
                description:
                    - "If I(creation_data).createOption is Empty, this field is mandatory and it indicates the size of the VHD to create. If this field is
                       present for updates or creation with other options, it indicates a resize. Resizes are only allowed if the disk is not attached to a
                       running VM, and can only increase the disk's size."
            encryption_settings:
                description:
                    - Encryption settings for disk or snapshot
                suboptions:
                    enabled:
                        description:
                            - "Set this flag to true and provide I(disk_encryption_key) and optional I(key_encryption_key) to enable encryption. Set this
                               flag to false and remove I(disk_encryption_key) and I(key_encryption_key) to disable encryption. If EncryptionSettings is
                               null in the request object, the existing settings remain unchanged."
                    disk_encryption_key:
                        description:
                            - Key Vault Secret Url and vault id of the disk encryption key
                        suboptions:
                            source_vault:
                                description:
                                    - Resource id of the KeyVault containing the key or secret
                                required: True
                                suboptions:
                                    id:
                                        description:
                                            - Resource Id
                            secret_url:
                                description:
                                    - Url pointing to a key or secret in KeyVault
                                required: True
                    key_encryption_key:
                        description:
                            - Key Vault Key Url and vault id of the key encryption key
                        suboptions:
                            source_vault:
                                description:
                                    - Resource id of the KeyVault containing the key or secret
                                required: True
                                suboptions:
                                    id:
                                        description:
                                            - Resource Id
                            key_url:
                                description:
                                    - Url pointing to a key or secret in KeyVault
                                required: True
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
      disk_name: myDisk
      disk:
        location: West US
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


class AzureRMDisks(AzureRMModuleBase):
    """Configuration class for an Azure RM Disk resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            disk_name=dict(
                type='str',
                required=True
            ),
            disk=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.disk_name = None
        self.disk = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDisks, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.disk["location"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'standard_lrs':
                            ev['name'] = 'Standard_LRS'
                        elif ev['name'] == 'premium_lrs':
                            ev['name'] = 'Premium_LRS'
                        elif ev['name'] == 'standard_ssd_lrs':
                            ev['name'] = 'StandardSSD_LRS'
                        elif ev['name'] == 'ultra_ssd_lrs':
                            ev['name'] = 'UltraSSD_LRS'
                    self.disk["sku"] = ev
                elif key == "zones":
                    self.disk["zones"] = kwargs[key]
                elif key == "os_type":
                    self.disk["os_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "creation_data":
                    ev = kwargs[key]
                    if 'create_option' in ev:
                        if ev['create_option'] == 'empty':
                            ev['create_option'] = 'Empty'
                        elif ev['create_option'] == 'attach':
                            ev['create_option'] = 'Attach'
                        elif ev['create_option'] == 'from_image':
                            ev['create_option'] = 'FromImage'
                        elif ev['create_option'] == 'import':
                            ev['create_option'] = 'Import'
                        elif ev['create_option'] == 'copy':
                            ev['create_option'] = 'Copy'
                        elif ev['create_option'] == 'restore':
                            ev['create_option'] = 'Restore'
                    self.disk["creation_data"] = ev
                elif key == "disk_size_gb":
                    self.disk["disk_size_gb"] = kwargs[key]
                elif key == "encryption_settings":
                    self.disk["encryption_settings"] = kwargs[key]
                elif key == "disk_iops_read_write":
                    self.disk["disk_iops_read_write"] = kwargs[key]
                elif key == "disk_mbps_read_write":
                    self.disk["disk_mbps_read_write"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Disk instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Disk instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_disk()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Disk instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_disk()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_disk():
                time.sleep(20)
        else:
            self.log("Disk instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_disk(self):
        '''
        Creates or updates Disk with the specified configuration.

        :return: deserialized Disk instance state dictionary
        '''
        self.log("Creating / Updating the Disk instance {0}".format(self.disk_name))

        try:
            response = self.mgmt_client.disks.create_or_update(resource_group_name=self.resource_group,
                                                               disk_name=self.disk_name,
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
        self.log("Deleting the Disk instance {0}".format(self.disk_name))
        try:
            response = self.mgmt_client.disks.delete(resource_group_name=self.resource_group,
                                                     disk_name=self.disk_name)
        except CloudError as e:
            self.log('Error attempting to delete the Disk instance.')
            self.fail("Error deleting the Disk instance: {0}".format(str(e)))

        return True

    def get_disk(self):
        '''
        Gets the properties of the specified Disk.

        :return: deserialized Disk instance state dictionary
        '''
        self.log("Checking if the Disk instance {0} is present".format(self.disk_name))
        found = False
        try:
            response = self.mgmt_client.disks.get(resource_group_name=self.resource_group,
                                                  disk_name=self.disk_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Disk instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Disk instance.')
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
    AzureRMDisks()


if __name__ == '__main__':
    main()

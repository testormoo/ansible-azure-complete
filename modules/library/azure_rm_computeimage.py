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
module: azure_rm_computeimage
version_added: "2.8"
short_description: Manage Azure Image instance.
description:
    - Create, update and delete instance of Azure Image.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the image.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    source_virtual_machine:
        description:
            - The source virtual machine from which Image is created.
        suboptions:
            id:
                description:
                    - Resource Id
    storage_profile:
        description:
            - Specifies the storage settings for the virtual machine disks.
        suboptions:
            os_disk:
                description:
                    - "Specifies information about the operating system disk used by the virtual machine. <br><br> For more information about disks, see
                       [About disks and VHDs for Azure virtual
                       machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-about-disks-vhds?toc=%2fazure%2fvirtual-machines
                      %2fwindows%2ftoc.json)."
                suboptions:
                    os_type:
                        description:
                            - "This property allows you to specify the type of the OS that is included in the disk if creating a VM from a custom image.
                               <br><br> Possible values are: <br><br> **C(windows)** <br><br> **C(linux)**."
                            - Required when C(state) is I(present).
                        choices:
                            - 'windows'
                            - 'linux'
                    os_state:
                        description:
                            - The OS State.
                            - Required when C(state) is I(present).
                        choices:
                            - 'generalized'
                            - 'specialized'
                    snapshot:
                        description:
                            - The snapshot.
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                    managed_disk:
                        description:
                            - The managedDisk.
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                    blob_uri:
                        description:
                            - The Virtual Hard Disk.
                    caching:
                        description:
                            - "Specifies the caching requirements. <br><br> Possible values are: <br><br> **C(none)** <br><br> **C(read_only)** <br><br>
                               **C(read_write)** <br><br> Default: **C(none) for Standard storage. C(read_only) for Premium storage**."
                        choices:
                            - 'none'
                            - 'read_only'
                            - 'read_write'
                    disk_size_gb:
                        description:
                            - "Specifies the size of empty data disks in gigabytes. This element can be used to overwrite the name of the disk in a virtual
                               machine image. <br><br> This value cannot be larger than 1023 GB"
                    storage_account_type:
                        description:
                            - Specifies the storage account type for the managed disk. C(ultra_ssd_lrs) cannot be used with OS Disk.
                        choices:
                            - 'standard_lrs'
                            - 'premium_lrs'
                            - 'standard_ssd_lrs'
                            - 'ultra_ssd_lrs'
            data_disks:
                description:
                    - "Specifies the parameters that are used to add a data disk to a virtual machine. <br><br> For more information about disks, see [About
                       disks and VHDs for Azure virtual
                       machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-about-disks-vhds?toc=%2fazure%2fvirtual-machines
                      %2fwindows%2ftoc.json)."
                type: list
                suboptions:
                    lun:
                        description:
                            - "Specifies the logical unit number of the data disk. This value is used to identify data disks within the VM and therefore
                               must be unique for each data disk attached to a VM."
                            - Required when C(state) is I(present).
                    snapshot:
                        description:
                            - The snapshot.
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                    managed_disk:
                        description:
                            - The managedDisk.
                        suboptions:
                            id:
                                description:
                                    - Resource Id
                    blob_uri:
                        description:
                            - The Virtual Hard Disk.
                    caching:
                        description:
                            - "Specifies the caching requirements. <br><br> Possible values are: <br><br> **C(none)** <br><br> **C(read_only)** <br><br>
                               **C(read_write)** <br><br> Default: **C(none) for Standard storage. C(read_only) for Premium storage**."
                        choices:
                            - 'none'
                            - 'read_only'
                            - 'read_write'
                    disk_size_gb:
                        description:
                            - "Specifies the size of empty data disks in gigabytes. This element can be used to overwrite the name of the disk in a virtual
                               machine image. <br><br> This value cannot be larger than 1023 GB"
                    storage_account_type:
                        description:
                            - "Specifies the storage account type for the managed disk. NOTE: C(ultra_ssd_lrs) can only be used with data disks, it cannot
                               be used with OS Disk."
                        choices:
                            - 'standard_lrs'
                            - 'premium_lrs'
                            - 'standard_ssd_lrs'
                            - 'ultra_ssd_lrs'
            zone_resilient:
                description:
                    - "Specifies whether an image is zone resilient or not. Default is false. Zone resilient images can be created only in regions that
                       provide Zone Redundant Storage (ZRS)."
    state:
      description:
        - Assert the state of the Image.
        - Use 'present' to create or update an Image and 'absent' to delete it.
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
  - name: Create (or update) Image
    azure_rm_computeimage:
      resource_group: myResourceGroup
      name: myImage
      location: eastus
      storage_profile:
        os_disk:
          os_type: Linux
          os_state: Generalized
          blob_uri: https://mystorageaccount.blob.core.windows.net/osimages/osimage.vhd
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


class AzureRMImage(AzureRMModuleBase):
    """Configuration class for an Azure RM Image resource"""

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
            source_virtual_machine=dict(
                type='dict'
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            storage_profile=dict(
                type='dict'
                options=dict(
                    os_disk=dict(
                        type='dict'
                        options=dict(
                            os_type=dict(
                                type='str',
                                choices=['windows',
                                         'linux']
                            ),
                            os_state=dict(
                                type='str',
                                choices=['generalized',
                                         'specialized']
                            ),
                            snapshot=dict(
                                type='dict'
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            managed_disk=dict(
                                type='dict'
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            blob_uri=dict(
                                type='str'
                            ),
                            caching=dict(
                                type='str',
                                choices=['none',
                                         'read_only',
                                         'read_write']
                            ),
                            disk_size_gb=dict(
                                type='int'
                            ),
                            storage_account_type=dict(
                                type='str',
                                choices=['standard_lrs',
                                         'premium_lrs',
                                         'standard_ssd_lrs',
                                         'ultra_ssd_lrs']
                            )
                        )
                    ),
                    data_disks=dict(
                        type='list'
                        options=dict(
                            lun=dict(
                                type='int'
                            ),
                            snapshot=dict(
                                type='dict'
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            managed_disk=dict(
                                type='dict'
                                options=dict(
                                    id=dict(
                                        type='str'
                                    )
                                )
                            ),
                            blob_uri=dict(
                                type='str'
                            ),
                            caching=dict(
                                type='str',
                                choices=['none',
                                         'read_only',
                                         'read_write']
                            ),
                            disk_size_gb=dict(
                                type='int'
                            ),
                            storage_account_type=dict(
                                type='str',
                                choices=['standard_lrs',
                                         'premium_lrs',
                                         'standard_ssd_lrs',
                                         'ultra_ssd_lrs']
                            )
                        )
                    ),
                    zone_resilient=dict(
                        type='str'
                    )
                )
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

        super(AzureRMImage, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['source_virtual_machine', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'os_type'], True)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'os_state'], True)
        dict_resource_id(self.parameters, ['storage_profile', 'os_disk', 'snapshot', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['storage_profile', 'os_disk', 'managed_disk', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'caching'], True)
        dict_camelize(self.parameters, ['storage_profile', 'os_disk', 'storage_account_type'], True)
        dict_map(self.parameters, ['storage_profile', 'os_disk', 'storage_account_type'], {'standard_lrs': 'Standard_LRS', 'premium_lrs': 'Premium_LRS', 'standard_ssd_lrs': 'StandardSSD_LRS', 'ultra_ssd_lrs': 'UltraSSD_LRS'})
        dict_resource_id(self.parameters, ['storage_profile', 'data_disks', 'snapshot', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['storage_profile', 'data_disks', 'managed_disk', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['storage_profile', 'data_disks', 'caching'], True)
        dict_camelize(self.parameters, ['storage_profile', 'data_disks', 'storage_account_type'], True)
        dict_map(self.parameters, ['storage_profile', 'data_disks', 'storage_account_type'], {'standard_lrs': 'Standard_LRS', 'premium_lrs': 'Premium_LRS', 'standard_ssd_lrs': 'StandardSSD_LRS', 'ultra_ssd_lrs': 'UltraSSD_LRS'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_image()

        if not old_response:
            self.log("Image instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Image instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Image instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_image()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Image instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_image()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Image instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_image(self):
        '''
        Creates or updates Image with the specified configuration.

        :return: deserialized Image instance state dictionary
        '''
        self.log("Creating / Updating the Image instance {0}".format(self.name))

        try:
            response = self.mgmt_client.images.create_or_update(resource_group_name=self.resource_group,
                                                                image_name=self.name,
                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Image instance.')
            self.fail("Error creating the Image instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_image(self):
        '''
        Deletes specified Image instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Image instance {0}".format(self.name))
        try:
            response = self.mgmt_client.images.delete(resource_group_name=self.resource_group,
                                                      image_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Image instance.')
            self.fail("Error deleting the Image instance: {0}".format(str(e)))

        return True

    def get_image(self):
        '''
        Gets the properties of the specified Image.

        :return: deserialized Image instance state dictionary
        '''
        self.log("Checking if the Image instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.images.get(resource_group_name=self.resource_group,
                                                   image_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Image instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Image instance.')
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
    AzureRMImage()


if __name__ == '__main__':
    main()

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
module: azure_rm_devtestlabscustomimage
version_added: "2.8"
short_description: Manage Azure Custom Image instance.
description:
    - Create, update and delete instance of Azure Custom Image.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    lab_name:
        description:
            - The name of the lab.
        required: True
    name:
        description:
            - The name of the custom image.
        required: True
    location:
        description:
            - The location of the resource.
    vm:
        description:
            - The virtual machine from which the image is to be created.
        suboptions:
            source_vm_id:
                description:
                    - The source vm identifier.
            windows_os_info:
                description:
                    - The Windows OS information of the VM.
                suboptions:
                    windows_os_state:
                        description:
                            - The state of the Windows OS (i.e. C(non_sysprepped), C(sysprep_requested), C(sysprep_applied)).
                        choices:
                            - 'non_sysprepped'
                            - 'sysprep_requested'
                            - 'sysprep_applied'
            linux_os_info:
                description:
                    - The Linux OS information of the VM.
                suboptions:
                    linux_os_state:
                        description:
                            - The state of the Linux OS (i.e. C(non_deprovisioned), C(deprovision_requested), C(deprovision_applied)).
                        choices:
                            - 'non_deprovisioned'
                            - 'deprovision_requested'
                            - 'deprovision_applied'
    vhd:
        description:
            - The VHD from which the image is to be created.
        suboptions:
            image_name:
                description:
                    - The image name.
            sys_prep:
                description:
                    - Indicates whether sysprep has been run on the VHD.
            os_type:
                description:
                    - The OS type of the custom image (i.e. C(windows), C(linux)).
                    - Required when C(state) is I(present).
                choices:
                    - 'windows'
                    - 'linux'
                    - 'none'
    description:
        description:
            - The description of the custom image.
    author:
        description:
            - The author of the custom image.
    managed_image_id:
        description:
            - The Managed Image Id backing the custom image.
    state:
      description:
        - Assert the state of the Custom Image.
        - Use 'present' to create or update an Custom Image and 'absent' to delete it.
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
  - name: Create (or update) Custom Image
    azure_rm_devtestlabscustomimage:
      resource_group: NOT FOUND
      lab_name: NOT FOUND
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


class AzureRMCustomImages(AzureRMModuleBase):
    """Configuration class for an Azure RM Custom Image resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            vm=dict(
                type='dict'
            ),
            vhd=dict(
                type='dict'
            ),
            description=dict(
                type='str'
            ),
            author=dict(
                type='str'
            ),
            managed_image_id=dict(
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
        self.name = None
        self.custom_image = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCustomImages, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.custom_image[key] = kwargs[key]

        expand(self.custom_image, ['vm', 'windows_os_info', 'windows_os_state'], camelize=True)
        expand(self.custom_image, ['vm', 'linux_os_info', 'linux_os_state'], camelize=True)
        expand(self.custom_image, ['vhd', 'os_type'], camelize=True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DevTestLabsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_customimage()

        if not old_response:
            self.log("Custom Image instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Custom Image instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.custom_image, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Custom Image instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_customimage()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Custom Image instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_customimage()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_customimage():
                time.sleep(20)
        else:
            self.log("Custom Image instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_customimage(self):
        '''
        Creates or updates Custom Image with the specified configuration.

        :return: deserialized Custom Image instance state dictionary
        '''
        self.log("Creating / Updating the Custom Image instance {0}".format(self.name))

        try:
            response = self.mgmt_client.custom_images.create_or_update(resource_group_name=self.resource_group,
                                                                       lab_name=self.lab_name,
                                                                       name=self.name,
                                                                       custom_image=self.custom_image)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Custom Image instance.')
            self.fail("Error creating the Custom Image instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_customimage(self):
        '''
        Deletes specified Custom Image instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Custom Image instance {0}".format(self.name))
        try:
            response = self.mgmt_client.custom_images.delete(resource_group_name=self.resource_group,
                                                             lab_name=self.lab_name,
                                                             name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Custom Image instance.')
            self.fail("Error deleting the Custom Image instance: {0}".format(str(e)))

        return True

    def get_customimage(self):
        '''
        Gets the properties of the specified Custom Image.

        :return: deserialized Custom Image instance state dictionary
        '''
        self.log("Checking if the Custom Image instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.custom_images.get(resource_group_name=self.resource_group,
                                                          lab_name=self.lab_name,
                                                          name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Custom Image instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Custom Image instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def expand(d, path, **kwargs):
    expand = kwargs.get('expand', None)
    rename = kwargs.get('rename', None)
    camelize = kwargs.get('camelize', False)
    camelize_lower = kwargs.get('camelize_lower', False)
    upper = kwargs.get('upper', False)
    map = kwargs.get('map', None)
    if isinstance(d, list):
        for i in range(len(d)):
            expand(d[i], path, **kwargs)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_name = path[0]
            new_name = old_name if rename is None else rename
            old_value = d.get(old_name, None)
            new_value = None
            if map is not None:
                new_value = map.get(old_value, None)
            if new_value is None:
                if camelize:
                    new_value = _snake_to_camel(old_value, True)
                elif camelize_lower:
                    new_value = _snake_to_camel(old_value, False)
                elif upper:
                    new_value = old_value.upper()
            if expand is None:
                # just rename
                if new_name != old_name:
                    d.pop(old_name, None)
            else:
                # expand and rename
                d[expand] = d.get(expand, {})
                d.pop(old_name, None)
                d = d[expand]
            d[new_name] = new_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                expand(sd, path[1:], **kwargs)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMCustomImages()


if __name__ == '__main__':
    main()

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
module: azure_rm_computevirtualmachinescalesetextension
version_added: "2.8"
short_description: Manage Azure Virtual Machine Scale Set Extension instance.
description:
    - Create, update and delete instance of Azure Virtual Machine Scale Set Extension.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    vm_scale_set_name:
        description:
            - The name of the VM scale set where the extension should be create or updated.
        required: True
    name:
        description:
            - The name of the VM scale set extension.
        required: True
    name:
        description:
            - The name of the extension.
    force_update_tag:
        description:
            - "If a value is provided and is different from the previous value, the extension handler will be forced to update even if the extension
               configuration has not changed."
    publisher:
        description:
            - The name of the extension handler publisher.
    type:
        description:
            - "Specifies the type of the extension; an example is 'CustomScriptExtension'."
    type_handler_version:
        description:
            - Specifies the version of the script handler.
    auto_upgrade_minor_version:
        description:
            - "Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the
               extension will not upgrade minor versions unless redeployed, even with this property set to true."
    settings:
        description:
            - Json formatted public settings for the extension.
    protected_settings:
        description:
            - The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected I(settings) at all.
    state:
      description:
        - Assert the state of the Virtual Machine Scale Set Extension.
        - Use 'present' to create or update an Virtual Machine Scale Set Extension and 'absent' to delete it.
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
  - name: Create (or update) Virtual Machine Scale Set Extension
    azure_rm_computevirtualmachinescalesetextension:
      resource_group: NOT FOUND
      vm_scale_set_name: NOT FOUND
      name: NOT FOUND
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


class AzureRMVirtualMachineScaleSetExtension(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Machine Scale Set Extension resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vm_scale_set_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            force_update_tag=dict(
                type='str'
            ),
            publisher=dict(
                type='str'
            ),
            type=dict(
                type='str'
            ),
            type_handler_version=dict(
                type='str'
            ),
            auto_upgrade_minor_version=dict(
                type='str'
            ),
            settings=dict(
                type='str'
            ),
            protected_settings=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.vm_scale_set_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualMachineScaleSetExtension, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                         supports_check_mode=True,
                                                                         supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.extension_parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_virtualmachinescalesetextension()

        if not old_response:
            self.log("Virtual Machine Scale Set Extension instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Machine Scale Set Extension instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.extension_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Machine Scale Set Extension instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualmachinescalesetextension()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Machine Scale Set Extension instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualmachinescalesetextension()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Machine Scale Set Extension instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_virtualmachinescalesetextension(self):
        '''
        Creates or updates Virtual Machine Scale Set Extension with the specified configuration.

        :return: deserialized Virtual Machine Scale Set Extension instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Machine Scale Set Extension instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_machine_scale_set_extensions.create_or_update(resource_group_name=self.resource_group,
                                                                                              vm_scale_set_name=self.vm_scale_set_name,
                                                                                              vmss_extension_name=self.name,
                                                                                              extension_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Machine Scale Set Extension instance.')
            self.fail("Error creating the Virtual Machine Scale Set Extension instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualmachinescalesetextension(self):
        '''
        Deletes specified Virtual Machine Scale Set Extension instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Machine Scale Set Extension instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_machine_scale_set_extensions.delete(resource_group_name=self.resource_group,
                                                                                    vm_scale_set_name=self.vm_scale_set_name,
                                                                                    vmss_extension_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Machine Scale Set Extension instance.')
            self.fail("Error deleting the Virtual Machine Scale Set Extension instance: {0}".format(str(e)))

        return True

    def get_virtualmachinescalesetextension(self):
        '''
        Gets the properties of the specified Virtual Machine Scale Set Extension.

        :return: deserialized Virtual Machine Scale Set Extension instance state dictionary
        '''
        self.log("Checking if the Virtual Machine Scale Set Extension instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_machine_scale_set_extensions.get(resource_group_name=self.resource_group,
                                                                                 vm_scale_set_name=self.vm_scale_set_name,
                                                                                 vmss_extension_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Machine Scale Set Extension instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Machine Scale Set Extension instance.')
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def main():
    """Main execution"""
    AzureRMVirtualMachineScaleSetExtension()


if __name__ == '__main__':
    main()

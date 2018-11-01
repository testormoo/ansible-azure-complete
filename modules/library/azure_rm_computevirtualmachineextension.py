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
module: azure_rm_computevirtualmachineextension
version_added: "2.8"
short_description: Manage Virtual Machine Extension instance.
description:
    - Create, update and delete instance of Virtual Machine Extension.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    vm_name:
        description:
            - The name of the virtual machine where the extension should be created or updated.
        required: True
    vm_extension_name:
        description:
            - The name of the virtual machine extension.
        required: True
    location:
        description:
            - Resource location
        required: True
    force_update_tag:
        description:
            - How the extension handler should be forced to update even if the extension configuration has not changed.
    publisher:
        description:
            - The name of the extension handler publisher.
    virtual_machine_extension_type:
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
    instance_view:
        description:
            - The virtual machine extension instance view.
        suboptions:
            name:
                description:
                    - The virtual machine extension name.
            type:
                description:
                    - "Specifies the type of the extension; an example is 'CustomScriptExtension'."
            type_handler_version:
                description:
                    - Specifies the version of the script handler.
            substatuses:
                description:
                    - The resource status information.
                type: list
                suboptions:
                    code:
                        description:
                            - The status code.
                    level:
                        description:
                            - The level I(code).
                        choices:
                            - 'info'
                            - 'warning'
                            - 'error'
                    display_status:
                        description:
                            - The short localizable label for the status.
                    message:
                        description:
                            - The detailed status message, including for alerts and C(error) messages.
                    time:
                        description:
                            - The time of the status.
            statuses:
                description:
                    - The resource status information.
                type: list
                suboptions:
                    code:
                        description:
                            - The status code.
                    level:
                        description:
                            - The level I(code).
                        choices:
                            - 'info'
                            - 'warning'
                            - 'error'
                    display_status:
                        description:
                            - The short localizable label for the status.
                    message:
                        description:
                            - The detailed status message, including for alerts and C(error) messages.
                    time:
                        description:
                            - The time of the status.
    state:
      description:
        - Assert the state of the Virtual Machine Extension.
        - Use 'present' to create or update an Virtual Machine Extension and 'absent' to delete it.
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
  - name: Create (or update) Virtual Machine Extension
    azure_rm_computevirtualmachineextension:
      resource_group: NOT FOUND
      vm_name: NOT FOUND
      vm_extension_name: NOT FOUND
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


class AzureRMVirtualMachineExtensions(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Machine Extension resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vm_name=dict(
                type='str',
                required=True
            ),
            vm_extension_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            force_update_tag=dict(
                type='str'
            ),
            publisher=dict(
                type='str'
            ),
            virtual_machine_extension_type=dict(
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
            instance_view=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.vm_name = None
        self.vm_extension_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualMachineExtensions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "force_update_tag":
                    self.parameters["force_update_tag"] = kwargs[key]
                elif key == "publisher":
                    self.parameters["publisher"] = kwargs[key]
                elif key == "virtual_machine_extension_type":
                    self.parameters["virtual_machine_extension_type"] = kwargs[key]
                elif key == "type_handler_version":
                    self.parameters["type_handler_version"] = kwargs[key]
                elif key == "auto_upgrade_minor_version":
                    self.parameters["auto_upgrade_minor_version"] = kwargs[key]
                elif key == "settings":
                    self.parameters["settings"] = kwargs[key]
                elif key == "protected_settings":
                    self.parameters["protected_settings"] = kwargs[key]
                elif key == "instance_view":
                    self.parameters["instance_view"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_virtualmachineextension()

        if not old_response:
            self.log("Virtual Machine Extension instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Machine Extension instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Virtual Machine Extension instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Machine Extension instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualmachineextension()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Machine Extension instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualmachineextension()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_virtualmachineextension():
                time.sleep(20)
        else:
            self.log("Virtual Machine Extension instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_virtualmachineextension(self):
        '''
        Creates or updates Virtual Machine Extension with the specified configuration.

        :return: deserialized Virtual Machine Extension instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Machine Extension instance {0}".format(self.vm_extension_name))

        try:
            response = self.mgmt_client.virtual_machine_extensions.create_or_update(resource_group_name=self.resource_group,
                                                                                    vm_name=self.vm_name,
                                                                                    vm_extension_name=self.vm_extension_name,
                                                                                    extension_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Machine Extension instance.')
            self.fail("Error creating the Virtual Machine Extension instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualmachineextension(self):
        '''
        Deletes specified Virtual Machine Extension instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Machine Extension instance {0}".format(self.vm_extension_name))
        try:
            response = self.mgmt_client.virtual_machine_extensions.delete(resource_group_name=self.resource_group,
                                                                          vm_name=self.vm_name,
                                                                          vm_extension_name=self.vm_extension_name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Machine Extension instance.')
            self.fail("Error deleting the Virtual Machine Extension instance: {0}".format(str(e)))

        return True

    def get_virtualmachineextension(self):
        '''
        Gets the properties of the specified Virtual Machine Extension.

        :return: deserialized Virtual Machine Extension instance state dictionary
        '''
        self.log("Checking if the Virtual Machine Extension instance {0} is present".format(self.vm_extension_name))
        found = False
        try:
            response = self.mgmt_client.virtual_machine_extensions.get(resource_group_name=self.resource_group,
                                                                       vm_name=self.vm_name,
                                                                       vm_extension_name=self.vm_extension_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Machine Extension instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Machine Extension instance.')
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
    AzureRMVirtualMachineExtensions()


if __name__ == '__main__':
    main()
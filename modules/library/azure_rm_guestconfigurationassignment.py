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
module: azure_rm_guestconfigurationassignment
version_added: "2.8"
short_description: Manage Guest Configuration Assignment instance.
description:
    - Create, update and delete instance of Guest Configuration Assignment.

options:
    guest_configuration_assignment_name:
        description:
            - Name of the guest configuration assignment.
        required: True
    guest_configuration:
        description:
            - The guest configuration to assign.
        suboptions:
            kind:
                description:
                    - "Kind of the guest configuration. For example:C(dsc)."
                choices:
                    - 'dsc'
            name:
                description:
                    - Name of the guest configuration.
            version:
                description:
                    - Version of the guest configuration.
            configuration_parameter:
                description:
                    - The configuration parameters for the guest configuration.
                type: list
            configuration_setting:
                description:
                    - The configuration setting for the guest configuration.
                suboptions:
                    allow_module_overwrite:
                        description:
                            - "If C(true) - new configurations downloaded from the pull service are allowed to overwrite the old ones on the target node.
                               Otherwise, C(false)."
                        choices:
                            - 'true'
                            - 'false'
    context:
        description:
            - "The source which initiated the guest configuration assignment. Ex: Azure Policy"
    resource_group:
        description:
            - The resource group name.
        required: True
    vm_name:
        description:
            - The name of the virtual machine.
        required: True
    state:
      description:
        - Assert the state of the Guest Configuration Assignment.
        - Use 'present' to create or update an Guest Configuration Assignment and 'absent' to delete it.
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
  - name: Create (or update) Guest Configuration Assignment
    azure_rm_guestconfigurationassignment:
      guest_configuration_assignment_name: SecureProtocol
      guest_configuration:
        name: AuditSecureProtocol
        version: 1.0.0.3
      context: Azure policy
      resource_group: myResourceGroupName
      vm_name: myVMName
'''

RETURN = '''
id:
    description:
        - ARM resource id of the guest configuration assignment.
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
    from azure.mgmt.guestconfiguration import GuestConfigurationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGuestConfigurationAssignments(AzureRMModuleBase):
    """Configuration class for an Azure RM Guest Configuration Assignment resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            guest_configuration_assignment_name=dict(
                type='str',
                required=True
            ),
            guest_configuration=dict(
                type='dict'
            ),
            context=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            vm_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.guest_configuration_assignment_name = None
        self.parameters = dict()
        self.resource_group = None
        self.vm_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGuestConfigurationAssignments, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                   supports_check_mode=True,
                                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "guest_configuration":
                    ev = kwargs[key]
                    if 'kind' in ev:
                        if ev['kind'] == 'dsc':
                            ev['kind'] = 'DSC'
                    self.parameters.setdefault("properties", {})["guest_configuration"] = ev
                elif key == "context":
                    self.parameters.setdefault("properties", {})["context"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GuestConfigurationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_guestconfigurationassignment()

        if not old_response:
            self.log("Guest Configuration Assignment instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Guest Configuration Assignment instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Guest Configuration Assignment instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Guest Configuration Assignment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_guestconfigurationassignment()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Guest Configuration Assignment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_guestconfigurationassignment()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_guestconfigurationassignment():
                time.sleep(20)
        else:
            self.log("Guest Configuration Assignment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_guestconfigurationassignment(self):
        '''
        Creates or updates Guest Configuration Assignment with the specified configuration.

        :return: deserialized Guest Configuration Assignment instance state dictionary
        '''
        self.log("Creating / Updating the Guest Configuration Assignment instance {0}".format(self.vm_name))

        try:
            response = self.mgmt_client.guest_configuration_assignments.create_or_update(guest_configuration_assignment_name=self.guest_configuration_assignment_name,
                                                                                         parameters=self.parameters,
                                                                                         resource_group_name=self.resource_group,
                                                                                         vm_name=self.vm_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Guest Configuration Assignment instance.')
            self.fail("Error creating the Guest Configuration Assignment instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_guestconfigurationassignment(self):
        '''
        Deletes specified Guest Configuration Assignment instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Guest Configuration Assignment instance {0}".format(self.vm_name))
        try:
            response = self.mgmt_client.guest_configuration_assignments.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Guest Configuration Assignment instance.')
            self.fail("Error deleting the Guest Configuration Assignment instance: {0}".format(str(e)))

        return True

    def get_guestconfigurationassignment(self):
        '''
        Gets the properties of the specified Guest Configuration Assignment.

        :return: deserialized Guest Configuration Assignment instance state dictionary
        '''
        self.log("Checking if the Guest Configuration Assignment instance {0} is present".format(self.vm_name))
        found = False
        try:
            response = self.mgmt_client.guest_configuration_assignments.get(resource_group_name=self.resource_group,
                                                                            guest_configuration_assignment_name=self.guest_configuration_assignment_name,
                                                                            vm_name=self.vm_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Guest Configuration Assignment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Guest Configuration Assignment instance.')
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
    AzureRMGuestConfigurationAssignments()


if __name__ == '__main__':
    main()

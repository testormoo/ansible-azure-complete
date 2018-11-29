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
short_description: Manage Azure Guest Configuration Assignment instance.
description:
    - Create, update and delete instance of Azure Guest Configuration Assignment.

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
    name:
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
      name: myVMName
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMGuestConfigurationAssignment(AzureRMModuleBase):
    """Configuration class for an Azure RM Guest Configuration Assignment resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            guest_configuration_assignment_name=dict(
                type='str',
                required=True
            ),
            guest_configuration=dict(
                type='dict',
                options=dict(
                    kind=dict(
                        type='str',
                        choices=['dsc']
                    ),
                    name=dict(
                        type='str'
                    ),
                    version=dict(
                        type='str'
                    ),
                    configuration_parameter=dict(
                        type='list'
                    ),
                    configuration_setting=dict(
                        type='dict',
                        options=dict(
                            allow_module_overwrite=dict(
                                type='str',
                                choices=['true',
                                         'false']
                            )
                        )
                    )
                )
            ),
            context=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGuestConfigurationAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                    supports_check_mode=True,
                                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_upper(self.parameters, ['guest_configuration', 'kind'])
        dict_camelize(self.parameters, ['guest_configuration', 'configuration_setting', 'allow_module_overwrite'], True)
        dict_expand(self.parameters, ['guest_configuration'])
        dict_expand(self.parameters, ['context'])

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Guest Configuration Assignment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_guestconfigurationassignment()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Guest Configuration Assignment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_guestconfigurationassignment()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Guest Configuration Assignment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_guestconfigurationassignment(self):
        '''
        Creates or updates Guest Configuration Assignment with the specified configuration.

        :return: deserialized Guest Configuration Assignment instance state dictionary
        '''
        self.log("Creating / Updating the Guest Configuration Assignment instance {0}".format(self.name))

        try:
            response = self.mgmt_client.guest_configuration_assignments.create_or_update(guest_configuration_assignment_name=self.guest_configuration_assignment_name,
                                                                                         parameters=self.parameters,
                                                                                         resource_group_name=self.resource_group,
                                                                                         vm_name=self.name)
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
        self.log("Deleting the Guest Configuration Assignment instance {0}".format(self.name))
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
        self.log("Checking if the Guest Configuration Assignment instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.guest_configuration_assignments.get(resource_group_name=self.resource_group,
                                                                            guest_configuration_assignment_name=self.guest_configuration_assignment_name,
                                                                            vm_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Guest Configuration Assignment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Guest Configuration Assignment instance.')
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


def main():
    """Main execution"""
    AzureRMGuestConfigurationAssignment()


if __name__ == '__main__':
    main()

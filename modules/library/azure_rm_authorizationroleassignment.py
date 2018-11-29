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
module: azure_rm_authorizationroleassignment
version_added: "2.8"
short_description: Manage Azure Role Assignment instance.
description:
    - Create, update and delete instance of Azure Role Assignment.

options:
    scope:
        description:
            - "The scope of the role assignment to create. The scope can be any REST resource instance. For example, use '/subscriptions/{subscription-id}/'
               for a subscription, '/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}' for a resource group, and
               '/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/{resource-provider}/{resource-type}/{resource-name}' for a
               resource."
        required: True
    name:
        description:
            - The name of the role assignment to create. It can be any valid GUID.
        required: True
    role_definition_id:
        description:
            - The role definition ID used in the role assignment.
            - Required when C(state) is I(present).
    principal_id:
        description:
            - "The principal ID assigned to the role. This maps to the ID inside the Active Directory. It can point to a user, service principal, or
               security group."
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Role Assignment.
        - Use 'present' to create or update an Role Assignment and 'absent' to delete it.
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
  - name: Create (or update) Role Assignment
    azure_rm_authorizationroleassignment:
      scope: scope
      name: roleAssignmentName
'''

RETURN = '''
id:
    description:
        - The role assignment ID.
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
    from azure.mgmt.authorization import AuthorizationManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRoleAssignment(AzureRMModuleBase):
    """Configuration class for an Azure RM Role Assignment resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            role_definition_id=dict(
                type='str'
            ),
            principal_id=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.scope = None
        self.name = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRoleAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.properties[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AuthorizationManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_roleassignment()

        if not old_response:
            self.log("Role Assignment instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Role Assignment instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Role Assignment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_roleassignment()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Role Assignment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_roleassignment()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Role Assignment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_roleassignment(self):
        '''
        Creates or updates Role Assignment with the specified configuration.

        :return: deserialized Role Assignment instance state dictionary
        '''
        self.log("Creating / Updating the Role Assignment instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.role_assignments.create(scope=self.scope,
                                                                    role_assignment_name=self.name,
                                                                    properties=self.properties)
            else:
                response = self.mgmt_client.role_assignments.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Role Assignment instance.')
            self.fail("Error creating the Role Assignment instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_roleassignment(self):
        '''
        Deletes specified Role Assignment instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Role Assignment instance {0}".format(self.name))
        try:
            response = self.mgmt_client.role_assignments.delete(scope=self.scope,
                                                                role_assignment_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Role Assignment instance.')
            self.fail("Error deleting the Role Assignment instance: {0}".format(str(e)))

        return True

    def get_roleassignment(self):
        '''
        Gets the properties of the specified Role Assignment.

        :return: deserialized Role Assignment instance state dictionary
        '''
        self.log("Checking if the Role Assignment instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.role_assignments.get(scope=self.scope,
                                                             role_assignment_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Role Assignment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Role Assignment instance.')
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


def main():
    """Main execution"""
    AzureRMRoleAssignment()


if __name__ == '__main__':
    main()

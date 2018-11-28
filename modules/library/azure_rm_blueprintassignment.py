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
module: azure_rm_blueprintassignment
version_added: "2.8"
short_description: Manage Azure Assignment instance.
description:
    - Create, update and delete instance of Azure Assignment.

options:
    subscription_id:
        description:
            - azure subscriptionId, which we assign the blueprint to.
        required: True
    name:
        description:
            - name of the assignment.
        required: True
    location:
        description:
            - The location of this Blueprint assignment.
            - Required when C(state) is I(present).
    identity:
        description:
            - Managed Service Identity for this Blueprint assignment
            - Required when C(state) is I(present).
        suboptions:
            type:
                description:
                    - Type of the Managed Service Identity.
                    - Required when C(state) is I(present).
                choices:
                    - 'none'
                    - 'system_assigned'
                    - 'user_assigned'
            principal_id:
                description:
                    - Azure Active Directory principal ID associated with this Identity.
            tenant_id:
                description:
                    - ID of the Azure Active Directory.
    display_name:
        description:
            - One-liner string explain this resource.
    description:
        description:
            - Multi-line explain this resource.
    blueprint_id:
        description:
            - ID of the Blueprint definition resource.
    parameters:
        description:
            - Blueprint parameter values.
            - Required when C(state) is I(present).
    resource_groups:
        description:
            - Names and locations of resource group placeholders.
            - Required when C(state) is I(present).
    locks:
        description:
            - Defines how Blueprint-managed resources will be locked.
        suboptions:
            mode:
                description:
                    - Lock mode.
                choices:
                    - 'none'
                    - 'all_resources'
    state:
      description:
        - Assert the state of the Assignment.
        - Use 'present' to create or update an Assignment and 'absent' to delete it.
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
  - name: Create (or update) Assignment
    azure_rm_blueprintassignment:
      subscription_id: f8df94f2-2f5a-4f4a-bcaf-1bb992fb564b
      name: assignSimpleBlueprint
      location: eastus
      identity:
        type: SystemAssigned
      description: enforce pre-defined simpleBlueprint to this XXXXXXXX subscription.
      blueprint_id: /providers/Microsoft.Management/managementGroups/ContosoOnlineGroup/providers/Microsoft.Blueprint/blueprints/simpleBlueprint
      parameters: {
  "storageAccountType": {
    "value": "Standard_LRS"
  },
  "costCenter": {
    "value": "Contoso/Online/Shopping/Production"
  },
  "owners": {
    "value": [
      "johnDoe@contoso.com",
      "johnsteam@contoso.com"
    ]
  }
}
      resource_groups: {
  "storageRG": {
    "name": "defaultRG",
    "location": "eastus"
  }
}
'''

RETURN = '''
id:
    description:
        - String Id used to locate any resource on Azure.
    returned: always
    type: str
    sample: id
status:
    description:
        - Status of Blueprint assignment. This field is readonly.
    returned: always
    type: complex
    sample: status
    contains:
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.blueprint import BlueprintManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAssignment(AzureRMModuleBase):
    """Configuration class for an Azure RM Assignment resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            subscription_id=dict(
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
            identity=dict(
                type='dict'
                options=dict(
                    type=dict(
                        type='str',
                        choices=['none',
                                 'system_assigned',
                                 'user_assigned']
                    ),
                    principal_id=dict(
                        type='str'
                    ),
                    tenant_id=dict(
                        type='str'
                    )
                )
            ),
            display_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            blueprint_id=dict(
                type='str'
            ),
            parameters=dict(
                type='dict'
            ),
            resource_groups=dict(
                type='dict'
            ),
            locks=dict(
                type='dict'
                options=dict(
                    mode=dict(
                        type='str',
                        choices=['none',
                                 'all_resources']
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.subscription_id = None
        self.name = None
        self.assignment = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.assignment[key] = kwargs[key]

        dict_camelize(self.assignment, ['identity', 'type'], True)
        dict_camelize(self.assignment, ['locks', 'mode'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BlueprintManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_assignment()

        if not old_response:
            self.log("Assignment instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Assignment instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.assignment, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Assignment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_assignment()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Assignment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_assignment()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Assignment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': {
                }
                })
        return self.results

    def create_update_assignment(self):
        '''
        Creates or updates Assignment with the specified configuration.

        :return: deserialized Assignment instance state dictionary
        '''
        self.log("Creating / Updating the Assignment instance {0}".format(self.name))

        try:
            response = self.mgmt_client.assignments.create_or_update(subscription_id=self.subscription_id,
                                                                     assignment_name=self.name,
                                                                     assignment=self.assignment)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Assignment instance.')
            self.fail("Error creating the Assignment instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_assignment(self):
        '''
        Deletes specified Assignment instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Assignment instance {0}".format(self.name))
        try:
            response = self.mgmt_client.assignments.delete(subscription_id=self.subscription_id,
                                                           assignment_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Assignment instance.')
            self.fail("Error deleting the Assignment instance: {0}".format(str(e)))

        return True

    def get_assignment(self):
        '''
        Gets the properties of the specified Assignment.

        :return: deserialized Assignment instance state dictionary
        '''
        self.log("Checking if the Assignment instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.assignments.get(subscription_id=self.subscription_id,
                                                        assignment_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Assignment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Assignment instance.')
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


def main():
    """Main execution"""
    AzureRMAssignment()


if __name__ == '__main__':
    main()

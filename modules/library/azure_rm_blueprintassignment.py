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
short_description: Manage Assignment instance.
description:
    - Create, update and delete instance of Assignment.

options:
    subscription_id:
        description:
            - azure subscriptionId, which we assign the blueprint to.
        required: True
    assignment_name:
        description:
            - name of the I(assignment).
        required: True
    assignment:
        description:
            - assignment object to save.
        required: True
        suboptions:
            location:
                description:
                    - The location of this Blueprint assignment.
                required: True
            identity:
                description:
                    - Managed Service Identity for this Blueprint assignment
                required: True
                suboptions:
                    type:
                        description:
                            - Type of the Managed Service Identity.
                        required: True
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
                required: True
            resource_groups:
                description:
                    - Names and locations of resource group placeholders.
                required: True
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
      assignment_name: assignSimpleBlueprint
      assignment:
        location: eastus
        identity:
          type: SystemAssigned
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


class AzureRMAssignments(AzureRMModuleBase):
    """Configuration class for an Azure RM Assignment resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            subscription_id=dict(
                type='str',
                required=True
            ),
            assignment_name=dict(
                type='str',
                required=True
            ),
            assignment=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.subscription_id = None
        self.assignment_name = None
        self.assignment = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAssignments, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.assignment["location"] = kwargs[key]
                elif key == "identity":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'none':
                            ev['type'] = 'None'
                        elif ev['type'] == 'system_assigned':
                            ev['type'] = 'SystemAssigned'
                        elif ev['type'] == 'user_assigned':
                            ev['type'] = 'UserAssigned'
                    self.assignment["identity"] = ev
                elif key == "display_name":
                    self.assignment["display_name"] = kwargs[key]
                elif key == "description":
                    self.assignment["description"] = kwargs[key]
                elif key == "blueprint_id":
                    self.assignment["blueprint_id"] = kwargs[key]
                elif key == "parameters":
                    self.assignment["parameters"] = kwargs[key]
                elif key == "resource_groups":
                    self.assignment["resource_groups"] = kwargs[key]
                elif key == "locks":
                    ev = kwargs[key]
                    if 'mode' in ev:
                        if ev['mode'] == 'none':
                            ev['mode'] = 'None'
                        elif ev['mode'] == 'all_resources':
                            ev['mode'] = 'AllResources'
                    self.assignment["locks"] = ev

        old_response = None
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
                self.log("Need to check if Assignment instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Assignment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_assignment()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Assignment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_assignment()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_assignment():
                time.sleep(20)
        else:
            self.log("Assignment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_assignment(self):
        '''
        Creates or updates Assignment with the specified configuration.

        :return: deserialized Assignment instance state dictionary
        '''
        self.log("Creating / Updating the Assignment instance {0}".format(self.assignment_name))

        try:
            response = self.mgmt_client.assignments.create_or_update(subscription_id=self.subscription_id,
                                                                     assignment_name=self.assignment_name,
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
        self.log("Deleting the Assignment instance {0}".format(self.assignment_name))
        try:
            response = self.mgmt_client.assignments.delete(subscription_id=self.subscription_id,
                                                           assignment_name=self.assignment_name)
        except CloudError as e:
            self.log('Error attempting to delete the Assignment instance.')
            self.fail("Error deleting the Assignment instance: {0}".format(str(e)))

        return True

    def get_assignment(self):
        '''
        Gets the properties of the specified Assignment.

        :return: deserialized Assignment instance state dictionary
        '''
        self.log("Checking if the Assignment instance {0} is present".format(self.assignment_name))
        found = False
        try:
            response = self.mgmt_client.assignments.get(subscription_id=self.subscription_id,
                                                        assignment_name=self.assignment_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Assignment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Assignment instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': {
            }
        }
        return d


def main():
    """Main execution"""
    AzureRMAssignments()


if __name__ == '__main__':
    main()

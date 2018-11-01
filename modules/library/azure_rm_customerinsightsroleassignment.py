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
module: azure_rm_customerinsightsroleassignment
version_added: "2.8"
short_description: Manage Role Assignment instance.
description:
    - Create, update and delete instance of Role Assignment.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    assignment_name:
        description:
            - The assignment name
        required: True
    display_name:
        description:
            - Localized display names for the metadata.
    description:
        description:
            - Localized description for the metadata.
    role:
        description:
            - Type of roles.
        required: True
        choices:
            - 'admin'
            - 'reader'
            - 'manage_admin'
            - 'manage_reader'
            - 'data_admin'
            - 'data_reader'
    principals:
        description:
            - The principals being assigned to.
        required: True
        type: list
        suboptions:
            principal_id:
                description:
                    - The principal id being assigned to.
                required: True
            principal_type:
                description:
                    - The Type of the principal ID.
                required: True
            principal_metadata:
                description:
                    - Other metadata for the principal.
    profiles:
        description:
            - Profiles set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    interactions:
        description:
            - Interactions set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    links:
        description:
            - Links set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    kpis:
        description:
            - Kpis set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    sas_policies:
        description:
            - Sas Policies set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    connectors:
        description:
            - Connectors set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    views:
        description:
            - Views set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    relationship_links:
        description:
            - The I(role) assignments set for the relationship I(links).
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    relationships:
        description:
            - The I(role) assignments set for the relationships.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    widget_types:
        description:
            - Widget types set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    role_assignments:
        description:
            - The I(role) assignments set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    conflation_policies:
        description:
            - Widget types set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
    segments:
        description:
            - The I(role) assignments set for the assignment.
        suboptions:
            elements:
                description:
                    - The elements included in the set.
                type: list
            exceptions:
                description:
                    - "The I(elements) that are not included in the set, in case I(elements) contains '*' indicating 'all'."
                type: list
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
    azure_rm_customerinsightsroleassignment:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      assignment_name: assignmentName8976
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/azSdkTestHub/RoleAssignme
            nts/assignmentName8976"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRoleAssignments(AzureRMModuleBase):
    """Configuration class for an Azure RM Role Assignment resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            assignment_name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='dict'
            ),
            description=dict(
                type='dict'
            ),
            role=dict(
                type='str',
                choices=['admin',
                         'reader',
                         'manage_admin',
                         'manage_reader',
                         'data_admin',
                         'data_reader'],
                required=True
            ),
            principals=dict(
                type='list',
                required=True
            ),
            profiles=dict(
                type='dict'
            ),
            interactions=dict(
                type='dict'
            ),
            links=dict(
                type='dict'
            ),
            kpis=dict(
                type='dict'
            ),
            sas_policies=dict(
                type='dict'
            ),
            connectors=dict(
                type='dict'
            ),
            views=dict(
                type='dict'
            ),
            relationship_links=dict(
                type='dict'
            ),
            relationships=dict(
                type='dict'
            ),
            widget_types=dict(
                type='dict'
            ),
            role_assignments=dict(
                type='dict'
            ),
            conflation_policies=dict(
                type='dict'
            ),
            segments=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.assignment_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRoleAssignments, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "role":
                    self.parameters["role"] = _snake_to_camel(kwargs[key], True)
                elif key == "principals":
                    self.parameters["principals"] = kwargs[key]
                elif key == "profiles":
                    self.parameters["profiles"] = kwargs[key]
                elif key == "interactions":
                    self.parameters["interactions"] = kwargs[key]
                elif key == "links":
                    self.parameters["links"] = kwargs[key]
                elif key == "kpis":
                    self.parameters["kpis"] = kwargs[key]
                elif key == "sas_policies":
                    self.parameters["sas_policies"] = kwargs[key]
                elif key == "connectors":
                    self.parameters["connectors"] = kwargs[key]
                elif key == "views":
                    self.parameters["views"] = kwargs[key]
                elif key == "relationship_links":
                    self.parameters["relationship_links"] = kwargs[key]
                elif key == "relationships":
                    self.parameters["relationships"] = kwargs[key]
                elif key == "widget_types":
                    self.parameters["widget_types"] = kwargs[key]
                elif key == "role_assignments":
                    self.parameters["role_assignments"] = kwargs[key]
                elif key == "conflation_policies":
                    self.parameters["conflation_policies"] = kwargs[key]
                elif key == "segments":
                    self.parameters["segments"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

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
                self.log("Need to check if Role Assignment instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Role Assignment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_roleassignment()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Role Assignment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_roleassignment()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_roleassignment():
                time.sleep(20)
        else:
            self.log("Role Assignment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_roleassignment(self):
        '''
        Creates or updates Role Assignment with the specified configuration.

        :return: deserialized Role Assignment instance state dictionary
        '''
        self.log("Creating / Updating the Role Assignment instance {0}".format(self.assignment_name))

        try:
            response = self.mgmt_client.role_assignments.create_or_update(resource_group_name=self.resource_group,
                                                                          hub_name=self.hub_name,
                                                                          assignment_name=self.assignment_name,
                                                                          parameters=self.parameters)
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
        self.log("Deleting the Role Assignment instance {0}".format(self.assignment_name))
        try:
            response = self.mgmt_client.role_assignments.delete(resource_group_name=self.resource_group,
                                                                hub_name=self.hub_name,
                                                                assignment_name=self.assignment_name)
        except CloudError as e:
            self.log('Error attempting to delete the Role Assignment instance.')
            self.fail("Error deleting the Role Assignment instance: {0}".format(str(e)))

        return True

    def get_roleassignment(self):
        '''
        Gets the properties of the specified Role Assignment.

        :return: deserialized Role Assignment instance state dictionary
        '''
        self.log("Checking if the Role Assignment instance {0} is present".format(self.assignment_name))
        found = False
        try:
            response = self.mgmt_client.role_assignments.get(resource_group_name=self.resource_group,
                                                             hub_name=self.hub_name,
                                                             assignment_name=self.assignment_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Role Assignment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Role Assignment instance.')
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
    AzureRMRoleAssignments()


if __name__ == '__main__':
    main()

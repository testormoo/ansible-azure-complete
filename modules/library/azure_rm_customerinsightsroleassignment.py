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
short_description: Manage Azure Role Assignment instance.
description:
    - Create, update and delete instance of Azure Role Assignment.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    name:
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
            - Required when C(state) is I(present).
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
            - Required when C(state) is I(present).
        type: list
        suboptions:
            principal_id:
                description:
                    - The principal id being assigned to.
                    - Required when C(state) is I(present).
            principal_type:
                description:
                    - The Type of the principal ID.
                    - Required when C(state) is I(present).
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
      name: assignmentName8976
      role: Admin
      principals:
        - principal_id: 4c54c38ffa9b416ba5a6d6c8a20cbe7e
          principal_type: User
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMRoleAssignment(AzureRMModuleBase):
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
            name=dict(
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
                         'data_reader']
            ),
            principals=dict(
                type='list'
                options=dict(
                    principal_id=dict(
                        type='str'
                    ),
                    principal_type=dict(
                        type='str'
                    ),
                    principal_metadata=dict(
                        type='dict'
                    )
                )
            ),
            profiles=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            interactions=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            links=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            kpis=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            sas_policies=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            connectors=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            views=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            relationship_links=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            relationships=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            widget_types=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            role_assignments=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            conflation_policies=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
                    )
                )
            ),
            segments=dict(
                type='dict'
                options=dict(
                    elements=dict(
                        type='list'
                    ),
                    exceptions=dict(
                        type='list'
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
        self.hub_name = None
        self.name = None
        self.parameters = dict()

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
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['role'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            response = self.mgmt_client.role_assignments.create_or_update(resource_group_name=self.resource_group,
                                                                          hub_name=self.hub_name,
                                                                          assignment_name=self.name,
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
        self.log("Deleting the Role Assignment instance {0}".format(self.name))
        try:
            response = self.mgmt_client.role_assignments.delete(resource_group_name=self.resource_group,
                                                                hub_name=self.hub_name,
                                                                assignment_name=self.name)
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
            response = self.mgmt_client.role_assignments.get(resource_group_name=self.resource_group,
                                                             hub_name=self.hub_name,
                                                             assignment_name=self.name)
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
    AzureRMRoleAssignment()


if __name__ == '__main__':
    main()

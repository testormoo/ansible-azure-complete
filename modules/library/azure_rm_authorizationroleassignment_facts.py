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
module: azure_rm_authorizationroleassignment_facts
version_added: "2.8"
short_description: Get Azure Role Assignment facts.
description:
    - Get facts of Azure Role Assignment.

options:
    scope:
        description:
            - The scope of the role assignment.
        required: True
    role_assignment_name:
        description:
            - The name of the role assignment to get.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Role Assignment
    azure_rm_authorizationroleassignment_facts:
      scope: scope
      role_assignment_name: role_assignment_name
'''

RETURN = '''
role_assignments:
    description: A list of dictionaries containing facts for Role Assignment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The role assignment ID.
            returned: always
            type: str
            sample: /subscriptions/subId/resourcegroups/rgname/providers/Microsoft.Authorization/roleAssignments/roleassignmentId
        name:
            description:
                - The role assignment name.
            returned: always
            type: str
            sample: raId
        properties:
            description:
                - Role assignment properties.
            returned: always
            type: complex
            sample: properties
            contains:
                scope:
                    description:
                        - The role assignment scope.
                    returned: always
                    type: str
                    sample: /subscriptions/subId/resourcegroups/rgname
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.authorization import AuthorizationManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRoleAssignmentsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            role_assignment_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.scope = None
        self.role_assignment_name = None
        super(AzureRMRoleAssignmentsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AuthorizationManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['role_assignments'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.role_assignments.get(scope=self.scope,
                                                             role_assignment_name=self.role_assignment_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RoleAssignments.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'properties': {
                'scope': d.get('properties', {}).get('scope', None)
            }
        }
        return d


def main():
    AzureRMRoleAssignmentsFacts()


if __name__ == '__main__':
    main()

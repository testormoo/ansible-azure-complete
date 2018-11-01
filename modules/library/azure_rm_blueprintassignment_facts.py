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
module: azure_rm_blueprintassignment_facts
version_added: "2.8"
short_description: Get Azure Assignment facts.
description:
    - Get facts of Azure Assignment.

options:
    subscription_id:
        description:
            - azure subscriptionId, which we assign the blueprint to.
        required: True
    assignment_name:
        description:
            - name of the assignment.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Assignment
    azure_rm_blueprintassignment_facts:
      subscription_id: subscription_id
      assignment_name: assignment_name
'''

RETURN = '''
assignments:
    description: A list of dictionaries containing facts for Assignment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - String Id used to locate any resource on Azure.
            returned: always
            type: str
            sample: /subscriptions/f8df94f2-2f5a-4f4a-bcaf-1bb992fb564b/providers/Microsoft.Blueprint/blueprintAssignments/assignSimpleBlueprint
        name:
            description:
                - Name of this resource.
            returned: always
            type: str
            sample: assignSimpleBlueprint
        location:
            description:
                - The location of this Blueprint assignment.
            returned: always
            type: str
            sample: eastus
        identity:
            description:
                - Managed Service Identity for this Blueprint assignment
            returned: always
            type: complex
            sample: identity
            contains:
                type:
                    description:
                        - "Type of the Managed Service Identity. Possible values include: 'None', 'SystemAssigned', 'UserAssigned'"
                    returned: always
                    type: str
                    sample: SystemAssigned
        description:
            description:
                - Multi-line explain this resource.
            returned: always
            type: str
            sample: enforce pre-defined simpleBlueprint to this XXXXXXXX subscription.
        parameters:
            description:
                - Blueprint parameter values.
            returned: always
            type: complex
            sample: "{\n  'storageAccountType': {\n    'value': 'Standard_LRS'\n  },\n  'costCenter': {\n    'value': 'Contoso/Online/Shopping/Production'\n
                      },\n  'owners': {\n    'value': [\n      'johnDoe@contoso.com',\n      'johnsteam@contoso.com'\n    ]\n  }\n}"
        status:
            description:
                - Status of Blueprint assignment. This field is readonly.
            returned: always
            type: complex
            sample: status
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.blueprint import BlueprintManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAssignmentsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            subscription_id=dict(
                type='str',
                required=True
            ),
            assignment_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.subscription_id = None
        self.assignment_name = None
        super(AzureRMAssignmentsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(BlueprintManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['assignments'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assignments.get(subscription_id=self.subscription_id,
                                                        assignment_name=self.assignment_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Assignments.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'identity': {
                'type': d.get('identity', {}).get('type', None)
            },
            'description': d.get('description', None),
            'parameters': d.get('parameters', None),
            'status': {
            }
        }
        return d


def main():
    AzureRMAssignmentsFacts()


if __name__ == '__main__':
    main()

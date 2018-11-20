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
module: azure_rm_guestconfigurationassignment_facts
version_added: "2.8"
short_description: Get Azure Guest Configuration Assignment facts.
description:
    - Get facts of Azure Guest Configuration Assignment.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    guest_configuration_assignment_name:
        description:
            - The guest configuration assingment name.
        required: True
    name:
        description:
            - The name of the virtual machine.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Guest Configuration Assignment
    azure_rm_guestconfigurationassignment_facts:
      resource_group: resource_group_name
      guest_configuration_assignment_name: guest_configuration_assignment_name
      name: vm_name
'''

RETURN = '''
guest_configuration_assignments:
    description: A list of dictionaries containing facts for Guest Configuration Assignment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ARM resource id of the guest configuration assignment.
            returned: always
            type: str
            sample: "/subscriptions/subscriptionId/resourceGroups/myResourceGroupName/providers/Microsoft.Compute/virtualMachines/myvm/providers/Microsoft.Gu
                    estConfiguration/guestConfigurationAssignments/AuditSecureProtocol"
        name:
            description:
                - Name of the guest configuration assignment.
            returned: always
            type: str
            sample: AuditSecureProtocol
        location:
            description:
                - Region where the VM is located.
            returned: always
            type: str
            sample: centraluseuap
        properties:
            description:
                - Properties of the Guest configuration assignment.
            returned: always
            type: complex
            sample: properties
            contains:
                context:
                    description:
                        - "The source which initiated the guest configuration assignment. Ex: Azure Policy"
                    returned: always
                    type: str
                    sample: context
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.guestconfiguration import GuestConfigurationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMGuestConfigurationAssignmentsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            guest_configuration_assignment_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.guest_configuration_assignment_name = None
        self.name = None
        super(AzureRMGuestConfigurationAssignmentsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(GuestConfigurationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['guest_configuration_assignments'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.guest_configuration_assignments.get(resource_group_name=self.resource_group,
                                                                            guest_configuration_assignment_name=self.guest_configuration_assignment_name,
                                                                            vm_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for GuestConfigurationAssignments.')

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
            'properties': {
                'context': d.get('properties', {}).get('context', None)
            }
        }
        return d


def main():
    AzureRMGuestConfigurationAssignmentsFacts()


if __name__ == '__main__':
    main()

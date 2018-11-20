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
module: azure_rm_guestconfigurationassignmentreport_facts
version_added: "2.8"
short_description: Get Azure Guest Configuration Assignment Report facts.
description:
    - Get facts of Azure Guest Configuration Assignment Report.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    guest_configuration_assignment_name:
        description:
            - The guest configuration assignment name.
        required: True
    report_id:
        description:
            - The GUID for the guest configuration assignment report.
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
  - name: Get instance of Guest Configuration Assignment Report
    azure_rm_guestconfigurationassignmentreport_facts:
      resource_group: resource_group_name
      guest_configuration_assignment_name: guest_configuration_assignment_name
      report_id: report_id
      name: vm_name
'''

RETURN = '''
guest_configuration_assignment_reports:
    description: A list of dictionaries containing facts for Guest Configuration Assignment Report.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ARM resource id of the report for the guest configuration assignment.
            returned: always
            type: str
            sample: "/subscriptions/mysubscriptionid/resourceGroups/myResourceGroupName/providers/Microsoft.Compute/virtualMachines/myvm/providers/Microsoft.
                    GuestConfiguration/guestConfigurationAssignments/AuditSecureProtocol/reports/7367cbb8-ae99-47d0-a33b-a283564d2cb1"
        name:
            description:
                - GUID that identifies the guest configuration assignment report under a subscription, resource group.
            returned: always
            type: str
            sample: 7367cbb8-ae99-47d0-a33b-a283564d2cb1
        properties:
            description:
                - Properties of the guest configuration report.
            returned: always
            type: complex
            sample: properties
            contains:
                assignment:
                    description:
                        - Configuration details of the guest configuration assignment.
                    returned: always
                    type: complex
                    sample: assignment
                    contains:
                        name:
                            description:
                                - Name of the guest configuration assignment.
                            returned: always
                            type: str
                            sample: AuditSecureProtocol
                        configuration:
                            description:
                                - Information about the configuration.
                            returned: always
                            type: complex
                            sample: configuration
                            contains:
                                name:
                                    description:
                                        - Name of the configuration.
                                    returned: always
                                    type: str
                                    sample: AuditSecureProtocol
                vm:
                    description:
                        - Information about the VM.
                    returned: always
                    type: complex
                    sample: vm
                    contains:
                        id:
                            description:
                                - Azure resource Id of the VM.
                            returned: always
                            type: str
                            sample: /subscriptions/mysubscriptionid/resourceGroups/myResourceGroupName/providers/Microsoft.Compute/virtualMachines/myvm
                        uuid:
                            description:
                                - UUID(Universally Unique Identifier) of the VM.
                            returned: always
                            type: str
                            sample: vmuuid
                details:
                    description:
                        - Details of the assignment report.
                    returned: always
                    type: complex
                    sample: details
                    contains:
                        resources:
                            description:
                                - The list of resources for which guest configuration assignment compliance is checked.
                            returned: always
                            type: complex
                            sample: resources
                            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.guestconfiguration import GuestConfigurationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMGuestConfigurationAssignmentReportsFacts(AzureRMModuleBase):
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
            report_id=dict(
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
        self.report_id = None
        self.name = None
        super(AzureRMGuestConfigurationAssignmentReportsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(GuestConfigurationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['guest_configuration_assignment_reports'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.guest_configuration_assignment_reports.get(resource_group_name=self.resource_group,
                                                                                   guest_configuration_assignment_name=self.guest_configuration_assignment_name,
                                                                                   report_id=self.report_id,
                                                                                   vm_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for GuestConfigurationAssignmentReports.')

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
                'assignment': {
                    'name': d.get('properties', {}).get('assignment', {}).get('name', None),
                    'configuration': {
                        'name': d.get('properties', {}).get('assignment', {}).get('configuration', {}).get('name', None)
                    }
                },
                'vm': {
                    'id': d.get('properties', {}).get('vm', {}).get('id', None),
                    'uuid': d.get('properties', {}).get('vm', {}).get('uuid', None)
                },
                'details': {
                    'resources': {
                    }
                }
            }
        }
        return d


def main():
    AzureRMGuestConfigurationAssignmentReportsFacts()


if __name__ == '__main__':
    main()

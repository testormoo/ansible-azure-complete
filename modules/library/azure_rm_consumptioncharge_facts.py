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
module: azure_rm_consumptioncharge_facts
version_added: "2.8"
short_description: Get Azure Charge facts.
description:
    - Get facts of Azure Charge.

options:
    billing_account_id:
        description:
            - BillingAccount ID
        required: True
    enrollment_account_id:
        description:
            - EnrollmentAccount ID
    filter:
        description:
            - "May be used to filter charges by properties/usageEnd (Utc time), properties/usageStart (Utc time). The filter supports 'eq', 'lt', 'gt',
               'le', 'ge', and 'and'. It does not currently support 'ne', 'or', or 'not'. Tag filter is a key value pair string where key and value is
               separated by a colon (:)."
    department_id:
        description:
            - Department ID

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Charge
    azure_rm_consumptioncharge_facts:
      billing_account_id: billing_account_id
      enrollment_account_id: enrollment_account_id
      filter: filter

  - name: List instances of Charge
    azure_rm_consumptioncharge_facts:
      billing_account_id: billing_account_id
      department_id: department_id
      filter: filter
'''

RETURN = '''
charges:
    description: A list of dictionaries containing facts for Charge.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.consumption import ConsumptionManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMChargesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            billing_account_id=dict(
                type='str',
                required=True
            ),
            enrollment_account_id=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
            department_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.billing_account_id = None
        self.enrollment_account_id = None
        self.filter = None
        self.department_id = None
        super(AzureRMChargesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.enrollment_account_id is not None:
            self.results['charges'] = self.list_by_enrollment_account()
        elif self.department_id is not None:
            self.results['charges'] = self.list_by_department()
        return self.results

    def list_by_enrollment_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.charges.list_by_enrollment_account(billing_account_id=self.billing_account_id,
                                                                           enrollment_account_id=self.enrollment_account_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Charges.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_department(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.charges.list_by_department(billing_account_id=self.billing_account_id,
                                                                   department_id=self.department_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Charges.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMChargesFacts()


if __name__ == '__main__':
    main()

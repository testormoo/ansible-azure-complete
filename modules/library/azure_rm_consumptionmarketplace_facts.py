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
module: azure_rm_consumptionmarketplace_facts
version_added: "2.8"
short_description: Get Azure Marketplace facts.
description:
    - Get facts of Azure Marketplace.

options:
    filter:
        description:
            - "May be used to filter marketplaces by properties/usageEnd (Utc time), properties/usageStart (Utc time), properties/resourceGroup,
               properties/instanceName or properties/instanceId. The filter supports 'eq', 'lt', 'gt', 'le', 'ge', and 'and'. It does not currently support
               'ne', 'or', or 'not'."
    top:
        description:
            - May be used to limit the number of results to the most recent N marketplaces.
    skiptoken:
        description:
            - "Skiptoken is only used if a previous operation returned a partial result. If a previous response contains a nextLink element, the value of
               the nextLink element will include a skiptoken parameter that specifies a starting point to use for subsequent calls."
    name:
        description:
            - Billing Period Name.
    billing_account_id:
        description:
            - BillingAccount ID
    department_id:
        description:
            - Department ID
    enrollment_account_id:
        description:
            - EnrollmentAccount ID

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Marketplace
    azure_rm_consumptionmarketplace_facts:
      filter: filter
      top: top
      skiptoken: skiptoken
      name: billing_period_name

  - name: List instances of Marketplace
    azure_rm_consumptionmarketplace_facts:
      filter: filter
      top: top
      skiptoken: skiptoken
      billing_account_id: billing_account_id

  - name: List instances of Marketplace
    azure_rm_consumptionmarketplace_facts:
      filter: filter
      top: top
      skiptoken: skiptoken
      department_id: department_id

  - name: List instances of Marketplace
    azure_rm_consumptionmarketplace_facts:
      filter: filter
      top: top
      skiptoken: skiptoken
      enrollment_account_id: enrollment_account_id
'''

RETURN = '''
marketplaces:
    description: A list of dictionaries containing facts for Marketplace.
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


class AzureRMMarketplacesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skiptoken=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            billing_account_id=dict(
                type='str'
            ),
            department_id=dict(
                type='str'
            ),
            enrollment_account_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.filter = None
        self.top = None
        self.skiptoken = None
        self.name = None
        self.billing_account_id = None
        self.department_id = None
        self.enrollment_account_id = None
        super(AzureRMMarketplacesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['marketplaces'] = self.list_by_billing_period()
        elif self.billing_account_id is not None:
            self.results['marketplaces'] = self.list_by_billing_account()
        elif self.department_id is not None:
            self.results['marketplaces'] = self.list_by_department()
        elif self.enrollment_account_id is not None:
            self.results['marketplaces'] = self.list_by_enrollment_account()
        return self.results

    def list_by_billing_period(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.marketplaces.list_by_billing_period(billing_period_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Marketplaces.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_billing_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.marketplaces.list_by_billing_account(billing_account_id=self.billing_account_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Marketplaces.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_department(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.marketplaces.list_by_department(department_id=self.department_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Marketplaces.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_enrollment_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.marketplaces.list_by_enrollment_account(enrollment_account_id=self.enrollment_account_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Marketplaces.')

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
    AzureRMMarketplacesFacts()


if __name__ == '__main__':
    main()

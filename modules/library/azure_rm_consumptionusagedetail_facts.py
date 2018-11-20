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
module: azure_rm_consumptionusagedetail_facts
version_added: "2.8"
short_description: Get Azure Usage Detail facts.
description:
    - Get facts of Azure Usage Detail.

options:
    name:
        description:
            - Billing Period Name.
    expand:
        description:
            - "May be used to expand the properties/additionalProperties or properties/meterDetails within a list of usage details. By default, these fields
               are not included when listing usage details."
    filter:
        description:
            - "May be used to filter usageDetails by properties/usageEnd (Utc time), properties/usageStart (Utc time), properties/resourceGroup,
               properties/instanceName or properties/instanceId. The filter supports 'eq', 'lt', 'gt', 'le', 'ge', and 'and'. It does not currently support
               'ne', 'or', or 'not'. Tag filter is a key value pair string where key and value is separated by a colon (:)."
    skiptoken:
        description:
            - "Skiptoken is only used if a previous operation returned a partial result. If a previous response contains a nextLink element, the value of
               the nextLink element will include a skiptoken parameter that specifies a starting point to use for subsequent calls."
    top:
        description:
            - May be used to limit the number of results to the most recent N usageDetails.
    query_options:
        description:
            - Additional parameters for the operation
    billing_account_id:
        description:
            - BillingAccount ID
    department_id:
        description:
            - Department ID
    enrollment_account_id:
        description:
            - EnrollmentAccount ID
    management_group_id:
        description:
            - Azure Management Group ID.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Usage Detail
    azure_rm_consumptionusagedetail_facts:
      name: billing_period_name
      expand: expand
      filter: filter
      skiptoken: skiptoken
      top: top
      query_options: query_options

  - name: List instances of Usage Detail
    azure_rm_consumptionusagedetail_facts:
      billing_account_id: billing_account_id
      expand: expand
      filter: filter
      skiptoken: skiptoken
      top: top
      query_options: query_options

  - name: List instances of Usage Detail
    azure_rm_consumptionusagedetail_facts:
      department_id: department_id
      expand: expand
      filter: filter
      skiptoken: skiptoken
      top: top
      query_options: query_options

  - name: List instances of Usage Detail
    azure_rm_consumptionusagedetail_facts:
      enrollment_account_id: enrollment_account_id
      expand: expand
      filter: filter
      skiptoken: skiptoken
      top: top
      query_options: query_options

  - name: List instances of Usage Detail
    azure_rm_consumptionusagedetail_facts:
      management_group_id: management_group_id
      expand: expand
      filter: filter
      skiptoken: skiptoken
      top: top
      query_options: query_options
'''

RETURN = '''
usage_details:
    description: A list of dictionaries containing facts for Usage Detail.
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


class AzureRMUsageDetailsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            name=dict(
                type='str'
            ),
            expand=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
            skiptoken=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            query_options=dict(
                type='dict'
            ),
            billing_account_id=dict(
                type='str'
            ),
            department_id=dict(
                type='str'
            ),
            enrollment_account_id=dict(
                type='str'
            ),
            management_group_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.name = None
        self.expand = None
        self.filter = None
        self.skiptoken = None
        self.top = None
        self.query_options = None
        self.billing_account_id = None
        self.department_id = None
        self.enrollment_account_id = None
        self.management_group_id = None
        super(AzureRMUsageDetailsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['usage_details'] = self.list_by_billing_period()
        elif self.billing_account_id is not None:
            self.results['usage_details'] = self.list_by_billing_account()
        elif self.department_id is not None:
            self.results['usage_details'] = self.list_by_department()
        elif self.enrollment_account_id is not None:
            self.results['usage_details'] = self.list_by_enrollment_account()
        elif self.management_group_id is not None:
            self.results['usage_details'] = self.list_by_management_group()
        return self.results

    def list_by_billing_period(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.usage_details.list_by_billing_period(billing_period_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UsageDetails.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_billing_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.usage_details.list_by_billing_account(billing_account_id=self.billing_account_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UsageDetails.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_department(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.usage_details.list_by_department(department_id=self.department_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UsageDetails.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_enrollment_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.usage_details.list_by_enrollment_account(enrollment_account_id=self.enrollment_account_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UsageDetails.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_management_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.usage_details.list_by_management_group(management_group_id=self.management_group_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for UsageDetails.')

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
    AzureRMUsageDetailsFacts()


if __name__ == '__main__':
    main()

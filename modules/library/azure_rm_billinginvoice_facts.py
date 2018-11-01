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
module: azure_rm_billinginvoice_facts
version_added: "2.8"
short_description: Get Azure Invoice facts.
description:
    - Get facts of Azure Invoice.

options:
    invoice_name:
        description:
            - The name of an invoice resource.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Invoice
    azure_rm_billinginvoice_facts:
      invoice_name: invoice_name
'''

RETURN = '''
invoices:
    description: A list of dictionaries containing facts for Invoice.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id.
            returned: always
            type: str
            sample: /subscriptions/subid/providers/Microsoft.Billing/invoices/2017-02-05-123456789
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 2017-02-05-123456789
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.billing import BillingManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMInvoicesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            invoice_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.invoice_name = None
        super(AzureRMInvoicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(BillingManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['invoices'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.invoices.get(invoice_name=self.invoice_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Invoices.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMInvoicesFacts()


if __name__ == '__main__':
    main()
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
module: azure_rm_consumptionpricesheet_facts
version_added: "2.8"
short_description: Get Azure Price Sheet facts.
description:
    - Get facts of Azure Price Sheet.

options:
    expand:
        description:
            - May be used to expand the properties/meterDetails within a price sheet. By default, these fields are not included when returning price sheet.
    skiptoken:
        description:
            - "Skiptoken is only used if a previous operation returned a partial result. If a previous response contains a nextLink element, the value of
               the nextLink element will include a skiptoken parameter that specifies a starting point to use for subsequent calls."
    top:
        description:
            - May be used to limit the number of results to the top N results.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Price Sheet
    azure_rm_consumptionpricesheet_facts:
      expand: expand
      skiptoken: skiptoken
      top: top
'''

RETURN = '''
price_sheet:
    description: A list of dictionaries containing facts for Price Sheet.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Billing/billingPeriods/201702/providers/Microsoft.Consumption/pr
                    icesheets/default"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: default
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        pricesheets:
            description:
                - Price sheet
            returned: always
            type: complex
            sample: pricesheets
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


class AzureRMPriceSheetFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            expand=dict(
                type='str'
            ),
            skiptoken=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.expand = None
        self.skiptoken = None
        self.top = None
        self.tags = None
        super(AzureRMPriceSheetFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['price_sheet'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.price_sheet.get()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for PriceSheet.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'pricesheets': {
            }
        }
        return d


def main():
    AzureRMPriceSheetFacts()


if __name__ == '__main__':
    main()

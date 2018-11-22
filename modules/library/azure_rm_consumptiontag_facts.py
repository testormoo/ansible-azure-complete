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
module: azure_rm_consumptiontag_facts
version_added: "2.8"
short_description: Get Azure Tag facts.
description:
    - Get facts of Azure Tag.

options:
    billing_account_id:
        description:
            - BillingAccount ID
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Tag
    azure_rm_consumptiontag_facts:
      billing_account_id: billing_account_id
'''

RETURN = '''
tags:
    description: A list of dictionaries containing facts for Tag.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id.
            returned: always
            type: str
            sample: providers/Microsoft.CostManagement/billingAccounts/{billingaccount-id}/providers/Microsoft.Consumption/tags/tags1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: tags1
        tags:
            description:
                - A list of Tag.
            returned: always
            type: complex
            sample: tags
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


class AzureRMTagFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            billing_account_id=dict(
                type='str',
                required=True
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
        self.billing_account_id = None
        self.tags = None
        super(AzureRMTagFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ConsumptionManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['tags'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tags.get(billing_account_id=self.billing_account_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tag.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': {
            }
        }
        return d


def main():
    AzureRMTagFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_apimanagementquotabycounterkey_facts
version_added: "2.8"
short_description: Get Azure Quota By Counter Key facts.
description:
    - Get facts of Azure Quota By Counter Key.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    quota_counter_key:
        description:
            - "Quota counter key identifier.This is the result of expression defined in counter-key attribute of the quota-by-key policy.For Example, if you
               specify counter-key='boo' in the policy, then it's accessible by 'boo' counter key. But if it's defined as counter-key='@('b'+'a')' then it
               will be accessible by 'ba' key"
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Quota By Counter Key
    azure_rm_apimanagementquotabycounterkey_facts:
      resource_group: resource_group_name
      service_name: service_name
      quota_counter_key: quota_counter_key
'''

RETURN = '''
quota_by_counter_keys:
    description: A list of dictionaries containing facts for Quota By Counter Key.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMQuotaByCounterKeysFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            quota_counter_key=dict(
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
        self.service_name = None
        self.quota_counter_key = None
        super(AzureRMQuotaByCounterKeysFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['quota_by_counter_keys'] = self.list_by_service()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.quota_by_counter_keys.list_by_service(resource_group_name=self.resource_group,
                                                                              service_name=self.service_name,
                                                                              quota_counter_key=self.quota_counter_key)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for QuotaByCounterKeys.')

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
    AzureRMQuotaByCounterKeysFacts()


if __name__ == '__main__':
    main()

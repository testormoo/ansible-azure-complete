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
module: azure_rm_dedicatedhsm_facts
version_added: "2.8"
short_description: Get Azure Dedicated Hsm facts.
description:
    - Get facts of Azure Dedicated Hsm.

options:
    resource_group:
        description:
            - The name of the Resource Group to which the dedicated hsm belongs.
    name:
        description:
            - The name of the dedicated HSM.
    top:
        description:
            - Maximum number of results to return.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Dedicated Hsm
    azure_rm_dedicatedhsm_facts:
      resource_group: resource_group_name
      name: name

  - name: List instances of Dedicated Hsm
    azure_rm_dedicatedhsm_facts:
      resource_group: resource_group_name
      top: top

  - name: List instances of Dedicated Hsm
    azure_rm_dedicatedhsm_facts:
      top: top
'''

RETURN = '''
dedicated_hsm:
    description: A list of dictionaries containing facts for Dedicated Hsm.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The Azure Resource Manager resource ID for the dedicated HSM.
            returned: always
            type: str
            sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/hsm-group/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/hsm1
        name:
            description:
                - The name of the dedicated HSM.
            returned: always
            type: str
            sample: hsm1
        location:
            description:
                - The supported Azure location where the dedicated HSM should be created.
            returned: always
            type: str
            sample: westus
        sku:
            description:
                - SKU details
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "SKU of the dedicated HSM. Possible values include: 'SafeNet Luna Network HSM A790'"
                    returned: always
                    type: str
                    sample: SafeNet Luna Network HSM A790
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'Dept': 'hsm',\n  'Environment': 'dogfood',\n  'Slice': 'A'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.dedicatedhsm import AzureDedicatedHSMResourceProvider
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDedicatedHsmFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
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
        self.resource_group = None
        self.name = None
        self.top = None
        self.tags = None
        super(AzureRMDedicatedHsmFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureDedicatedHSMResourceProvider,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['dedicated_hsm'] = self.get()
        elif self.resource_group is not None:
            self.results['dedicated_hsm'] = self.list_by_resource_group()
        else:
            self.results['dedicated_hsm'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dedicated_hsm.get(resource_group_name=self.resource_group,
                                                          name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Dedicated Hsm.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dedicated_hsm.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Dedicated Hsm.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.dedicated_hsm.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Dedicated Hsm.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            },
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMDedicatedHsmFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_searchadminkey_facts
version_added: "2.8"
short_description: Get Azure Admin Key facts.
description:
    - Get facts of Azure Admin Key.

options:
    resource_group:
        description:
            - The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the Azure Search service associated with the specified resource group.
        required: True
    search_management_request_options:
        description:
            - Additional parameters for the operation

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Admin Key
    azure_rm_searchadminkey_facts:
      resource_group: resource_group_name
      name: search_service_name
      search_management_request_options: search_management_request_options
'''

RETURN = '''
admin_keys:
    description: A list of dictionaries containing facts for Admin Key.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.search import SearchManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAdminKeysFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            search_management_request_options=dict(
                type='dict'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.search_management_request_options = None
        super(AzureRMAdminKeysFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SearchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['admin_keys'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.admin_keys.get(resource_group_name=self.resource_group,
                                                       search_service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AdminKeys.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMAdminKeysFacts()


if __name__ == '__main__':
    main()

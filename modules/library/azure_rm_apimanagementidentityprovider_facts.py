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
module: azure_rm_apimanagementidentityprovider_facts
version_added: "2.8"
short_description: Get Azure Identity Provider facts.
description:
    - Get facts of Azure Identity Provider.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    identity_provider_name:
        description:
            - Identity Provider Type identifier.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Identity Provider
    azure_rm_apimanagementidentityprovider_facts:
      resource_group: resource_group_name
      service_name: service_name
      identity_provider_name: identity_provider_name

  - name: List instances of Identity Provider
    azure_rm_apimanagementidentityprovider_facts:
      resource_group: resource_group_name
      service_name: service_name
'''

RETURN = '''
identity_provider:
    description: A list of dictionaries containing facts for Identity Provider.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/identityProviders/aadB2C
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: aadB2C
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIdentityProviderFacts(AzureRMModuleBase):
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
            identity_provider_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.service_name = None
        self.identity_provider_name = None
        super(AzureRMIdentityProviderFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.identity_provider_name is not None:
            self.results['identity_provider'] = self.get()
        else:
            self.results['identity_provider'] = self.list_by_service()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.identity_provider.get(resource_group_name=self.resource_group,
                                                              service_name=self.service_name,
                                                              identity_provider_name=self.identity_provider_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IdentityProvider.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.identity_provider.list_by_service(resource_group_name=self.resource_group,
                                                                          service_name=self.service_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IdentityProvider.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

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
    AzureRMIdentityProviderFacts()


if __name__ == '__main__':
    main()

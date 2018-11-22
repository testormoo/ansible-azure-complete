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
module: azure_rm_apimanagementopenidconnectprovider_facts
version_added: "2.8"
short_description: Get Azure Open Id Connect Provider facts.
description:
    - Get facts of Azure Open Id Connect Provider.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    filter:
        description:
            - | Field | Supported operators    | Supported functions                         |
            - |-------|------------------------|---------------------------------------------|
            - | id    | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | name  | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    opid:
        description:
            - Identifier of the OpenID Connect Provider.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Open Id Connect Provider
    azure_rm_apimanagementopenidconnectprovider_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Open Id Connect Provider
    azure_rm_apimanagementopenidconnectprovider_facts:
      resource_group: resource_group_name
      name: service_name
      opid: opid
'''

RETURN = '''
open_id_connect_provider:
    description: A list of dictionaries containing facts for Open Id Connect Provider.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/openidConnectProviders/templateOpenIdConnect2
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: templateOpenIdConnect2
        description:
            description:
                - User-friendly description of OpenID Connect Provider.
            returned: always
            type: str
            sample: open id provider template2
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMOpenIdConnectProviderFacts(AzureRMModuleBase):
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
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            ),
            opid=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.filter = None
        self.top = None
        self.skip = None
        self.opid = None
        super(AzureRMOpenIdConnectProviderFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.opid is not None:
            self.results['open_id_connect_provider'] = self.get()
        else:
            self.results['open_id_connect_provider'] = self.list_by_service()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.open_id_connect_provider.list_by_service(resource_group_name=self.resource_group,
                                                                                 service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Open Id Connect Provider.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.open_id_connect_provider.get(resource_group_name=self.resource_group,
                                                                     service_name=self.name,
                                                                     opid=self.opid)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Open Id Connect Provider.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None)
        }
        return d


def main():
    AzureRMOpenIdConnectProviderFacts()


if __name__ == '__main__':
    main()

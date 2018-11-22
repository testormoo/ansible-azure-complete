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
module: azure_rm_apimanagementauthorizationserver_facts
version_added: "2.8"
short_description: Get Azure Authorization Server facts.
description:
    - Get facts of Azure Authorization Server.

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
    authsid:
        description:
            - Identifier of the authorization server.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Authorization Server
    azure_rm_apimanagementauthorizationserver_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Authorization Server
    azure_rm_apimanagementauthorizationserver_facts:
      resource_group: resource_group_name
      name: service_name
      authsid: authsid
'''

RETURN = '''
authorization_server:
    description: A list of dictionaries containing facts for Authorization Server.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/authorizationServers/newauthServer2
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: newauthServer2
        description:
            description:
                - Description of the authorization server. Can contain HTML formatting tags.
            returned: always
            type: str
            sample: test server
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAuthorizationServerFacts(AzureRMModuleBase):
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
            authsid=dict(
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
        self.authsid = None
        super(AzureRMAuthorizationServerFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.authsid is not None:
            self.results['authorization_server'] = self.get()
        else:
            self.results['authorization_server'] = self.list_by_service()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.authorization_server.list_by_service(resource_group_name=self.resource_group,
                                                                             service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Authorization Server.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.authorization_server.get(resource_group_name=self.resource_group,
                                                                 service_name=self.name,
                                                                 authsid=self.authsid)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Authorization Server.')

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
    AzureRMAuthorizationServerFacts()


if __name__ == '__main__':
    main()

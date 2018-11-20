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
module: azure_rm_apimanagementapi_facts
version_added: "2.8"
short_description: Get Azure Api facts.
description:
    - Get facts of Azure Api.

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
            - | Field       | Supported operators    | Supported functions               |
            - |-------------|------------------------|-----------------------------------|
            - | id          | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | name        | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | description | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | serviceUrl  | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | path        | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    expand_api_version_set:
        description:
            - Include full ApiVersionSet resource in response
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Api
    azure_rm_apimanagementapi_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip
      expand_api_version_set: expand_api_version_set

  - name: List instances of Api
    azure_rm_apimanagementapi_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Api
    azure_rm_apimanagementapi_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
'''

RETURN = '''
api:
    description: A list of dictionaries containing facts for Api.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/57d1f7558aa04f15146d9d8a
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 57d1f7558aa04f15146d9d8a
        path:
            description:
                - "Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to
                   the API endpoint base URL specified during the service instance creation to form a public URL for this API."
            returned: always
            type: str
            sample: schulte
        protocols:
            description:
                - Describes on which protocols the operations in this API can be invoked.
            returned: always
            type: str
            sample: "[\n  'https'\n]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiFacts(AzureRMModuleBase):
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
            expand_api_version_set=dict(
                type='str'
            ),
            api_id=dict(
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
        self.expand_api_version_set = None
        self.api_id = None
        super(AzureRMApiFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['api'] = self.list_by_service()
        else:
            self.results['api'] = self.list_by_tags()
        elif self.api_id is not None:
            self.results['api'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api.list_by_service(resource_group_name=self.resource_group,
                                                            service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_tags(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api.list_by_tags(resource_group_name=self.resource_group,
                                                         service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api.get(resource_group_name=self.resource_group,
                                                service_name=self.name,
                                                api_id=self.api_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'path': d.get('path', None),
            'protocols': d.get('protocols', None)
        }
        return d


def main():
    AzureRMApiFacts()


if __name__ == '__main__':
    main()

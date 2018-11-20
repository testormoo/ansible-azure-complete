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
module: azure_rm_apimanagementapioperation_facts
version_added: "2.8"
short_description: Get Azure Api Operation facts.
description:
    - Get facts of Azure Api Operation.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."
        required: True
    filter:
        description:
            - | Field       | Supported operators    | Supported functions               |
            - |-------------|------------------------|-----------------------------------|
            - | name        | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | method      | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | description | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | urlTemplate | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    operation_id:
        description:
            - Operation identifier within an API. Must be unique in the current API Management service instance.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Api Operation
    azure_rm_apimanagementapioperation_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Api Operation
    azure_rm_apimanagementapioperation_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      operation_id: operation_id
'''

RETURN = '''
api_operation:
    description: A list of dictionaries containing facts for Api Operation.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/57d2ef278aa04f0888cba3f3/operations/
                    57d2ef278aa04f0ad01d6cdc"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 57d2ef278aa04f0ad01d6cdc
        request:
            description:
                - An entity containing request details.
            returned: always
            type: complex
            sample: request
            contains:
                description:
                    description:
                        - Operation request description.
                    returned: always
                    type: str
                    sample: IFazioService_CancelOrder_InputMessage
                headers:
                    description:
                        - Collection of operation request headers.
                    returned: always
                    type: complex
                    sample: headers
                    contains:
                representations:
                    description:
                        - Collection of operation request representations.
                    returned: always
                    type: complex
                    sample: representations
                    contains:
        responses:
            description:
                - Array of Operation responses.
            returned: always
            type: complex
            sample: responses
            contains:
        method:
            description:
                - A Valid HTTP Operation Method. Typical Http Methods like GET, PUT, POST but not limited by only them.
            returned: always
            type: str
            sample: POST
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiOperationFacts(AzureRMModuleBase):
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
            api_id=dict(
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
            operation_id=dict(
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
        self.api_id = None
        self.filter = None
        self.top = None
        self.skip = None
        self.operation_id = None
        super(AzureRMApiOperationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['api_operation'] = self.list_by_api()
        elif self.operation_id is not None:
            self.results['api_operation'] = self.get()
        return self.results

    def list_by_api(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_operation.list_by_api(resource_group_name=self.resource_group,
                                                                  service_name=self.name,
                                                                  api_id=self.api_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ApiOperation.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_operation.get(resource_group_name=self.resource_group,
                                                          service_name=self.name,
                                                          api_id=self.api_id,
                                                          operation_id=self.operation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ApiOperation.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'request': {
                'description': d.get('request', {}).get('description', None),
                'headers': {
                },
                'representations': {
                }
            },
            'responses': {
            },
            'method': d.get('method', None)
        }
        return d


def main():
    AzureRMApiOperationFacts()


if __name__ == '__main__':
    main()

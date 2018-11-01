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
module: azure_rm_apimanagementtag_facts
version_added: "2.8"
short_description: Get Azure Tag facts.
description:
    - Get facts of Azure Tag.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."
    operation_id:
        description:
            - Operation identifier within an API. Must be unique in the current API Management service instance.
    filter:
        description:
            - | Field       | Supported operators    | Supported functions                         |
            - |-------------|------------------------|---------------------------------------------|
            - | id          | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | name        | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | method     | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | description | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | urlTemplate | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    product_id:
        description:
            - Product identifier. Must be unique in the current API Management service instance.
    tag_id:
        description:
            - Tag identifier. Must be unique in the current API Management service instance.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Tag
    azure_rm_apimanagementtag_facts:
      resource_group: resource_group_name
      service_name: service_name
      api_id: api_id
      operation_id: operation_id
      filter: filter
      top: top
      skip: skip

  - name: List instances of Tag
    azure_rm_apimanagementtag_facts:
      resource_group: resource_group_name
      service_name: service_name
      api_id: api_id
      filter: filter
      top: top
      skip: skip

  - name: List instances of Tag
    azure_rm_apimanagementtag_facts:
      resource_group: resource_group_name
      service_name: service_name
      product_id: product_id
      filter: filter
      top: top
      skip: skip

  - name: List instances of Tag
    azure_rm_apimanagementtag_facts:
      resource_group: resource_group_name
      service_name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Tag
    azure_rm_apimanagementtag_facts:
      resource_group: resource_group_name
      service_name: service_name
      tag_id: tag_id
'''

RETURN = '''
tag:
    description: A list of dictionaries containing facts for Tag.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/tags/59306a29e4bbd510dc24e5f9
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 59306a29e4bbd510dc24e5f9
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTagFacts(AzureRMModuleBase):
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
            api_id=dict(
                type='str'
            ),
            operation_id=dict(
                type='str'
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
            product_id=dict(
                type='str'
            ),
            tag_id=dict(
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
        self.api_id = None
        self.operation_id = None
        self.filter = None
        self.top = None
        self.skip = None
        self.product_id = None
        self.tag_id = None
        super(AzureRMTagFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.api_id is not None and
                self.operation_id is not None):
            self.results['tag'] = self.list_by_operation()
        elif self.api_id is not None:
            self.results['tag'] = self.list_by_api()
        elif self.product_id is not None:
            self.results['tag'] = self.list_by_product()
        else:
            self.results['tag'] = self.list_by_service()
        elif self.tag_id is not None:
            self.results['tag'] = self.get()
        return self.results

    def list_by_operation(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tag.list_by_operation(resource_group_name=self.resource_group,
                                                              service_name=self.service_name,
                                                              api_id=self.api_id,
                                                              operation_id=self.operation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tag.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_api(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tag.list_by_api(resource_group_name=self.resource_group,
                                                        service_name=self.service_name,
                                                        api_id=self.api_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tag.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_product(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tag.list_by_product(resource_group_name=self.resource_group,
                                                            service_name=self.service_name,
                                                            product_id=self.product_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tag.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tag.list_by_service(resource_group_name=self.resource_group,
                                                            service_name=self.service_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tag.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tag.get(resource_group_name=self.resource_group,
                                                service_name=self.service_name,
                                                tag_id=self.tag_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tag.')

        if response is not None:
            results.append(self.format_item(response))

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
    AzureRMTagFacts()


if __name__ == '__main__':
    main()

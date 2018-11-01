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
module: azure_rm_apimanagementproperty_facts
version_added: "2.8"
short_description: Get Azure Property facts.
description:
    - Get facts of Azure Property.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    filter:
        description:
            - | Field | Supported operators    | Supported functions                                   |
            - |-------|------------------------|-------------------------------------------------------|
            - | tags  | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith, any, all |
            - | name  | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith           |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    prop_id:
        description:
            - Identifier of the property.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Property
    azure_rm_apimanagementproperty_facts:
      resource_group: resource_group_name
      service_name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Property
    azure_rm_apimanagementproperty_facts:
      resource_group: resource_group_name
      service_name: service_name
      prop_id: prop_id
'''

RETURN = '''
property:
    description: A list of dictionaries containing facts for Property.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/properties/testarmTemplateproperties2
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: testarmTemplateproperties2
        tags:
            description:
                - Optional tags that when provided can be used to filter the property list.
            returned: always
            type: str
            sample: "[\n  'foo',\n  'bar'\n]"
        secret:
            description:
                - Determines whether the value is a secret and should be encrypted or not. Default value is false.
            returned: always
            type: str
            sample: False
        value:
            description:
                - Value of the property. Can contain policy expressions. It may not be empty or consist only of whitespace.
            returned: always
            type: str
            sample: propValue
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPropertyFacts(AzureRMModuleBase):
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
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            ),
            prop_id=dict(
                type='str'
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
        self.service_name = None
        self.filter = None
        self.top = None
        self.skip = None
        self.prop_id = None
        self.tags = None
        super(AzureRMPropertyFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['property'] = self.list_by_service()
        elif self.prop_id is not None:
            self.results['property'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.property.list_by_service(resource_group_name=self.resource_group,
                                                                 service_name=self.service_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Property.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.property.get(resource_group_name=self.resource_group,
                                                     service_name=self.service_name,
                                                     prop_id=self.prop_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Property.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'secret': d.get('secret', None),
            'value': d.get('value', None)
        }
        return d


def main():
    AzureRMPropertyFacts()


if __name__ == '__main__':
    main()

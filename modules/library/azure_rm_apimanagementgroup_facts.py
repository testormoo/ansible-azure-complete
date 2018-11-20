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
module: azure_rm_apimanagementgroup_facts
version_added: "2.8"
short_description: Get Azure Group facts.
description:
    - Get facts of Azure Group.

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
            - | Field       | Supported operators    | Supported functions                         |
            - |-------------|------------------------|---------------------------------------------|
            - | id          | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | name        | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | description | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | type        | eq, ne                 | N/A                                         |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    group_id:
        description:
            - Group identifier. Must be unique in the current API Management service instance.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Group
    azure_rm_apimanagementgroup_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Group
    azure_rm_apimanagementgroup_facts:
      resource_group: resource_group_name
      name: service_name
      group_id: group_id
'''

RETURN = '''
group:
    description: A list of dictionaries containing facts for Group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/groups/59306a29e4bbd510dc24e5f9
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 59306a29e4bbd510dc24e5f9
        description:
            description:
                - Group description. Can contain HTML formatting tags.
            returned: always
            type: str
            sample: awesome group of people
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMGroupFacts(AzureRMModuleBase):
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
            group_id=dict(
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
        self.group_id = None
        super(AzureRMGroupFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['group'] = self.list_by_service()
        elif self.group_id is not None:
            self.results['group'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.group.list_by_service(resource_group_name=self.resource_group,
                                                              service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Group.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.group.get(resource_group_name=self.resource_group,
                                                  service_name=self.name,
                                                  group_id=self.group_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Group.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None)
        }
        return d


def main():
    AzureRMGroupFacts()


if __name__ == '__main__':
    main()

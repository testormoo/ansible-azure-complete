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
module: azure_rm_apimanagementtagresource_facts
version_added: "2.8"
short_description: Get Azure Tag Resource facts.
description:
    - Get facts of Azure Tag Resource.

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
            - | aid         | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | apiName     | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | apiRevision | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | path        | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | description | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | serviceUrl  | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | method      | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | urlTemplate | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | terms       | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | state       | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | isCurrent   | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Tag Resource
    azure_rm_apimanagementtagresource_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip
'''

RETURN = '''
tag_resource:
    description: A list of dictionaries containing facts for Tag Resource.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTagResourceFacts(AzureRMModuleBase):
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
        super(AzureRMTagResourceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['tag_resource'] = self.list_by_service()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.tag_resource.list_by_service(resource_group_name=self.resource_group,
                                                                     service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Tag Resource.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMTagResourceFacts()


if __name__ == '__main__':
    main()

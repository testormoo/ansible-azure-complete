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
module: azure_rm_apimanagementapiversionset_facts
version_added: "2.8"
short_description: Get Azure Api Version Set facts.
description:
    - Get facts of Azure Api Version Set.

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
            - | Field            | Supported operators    | Supported functions               |
            - |------------------|------------------------|-----------------------------------|
            - | id               | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | firstName        | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | lastName         | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | email            | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
            - | state            | eq                     | N/A                               |
            - | registrationDate | ge, le, eq, ne, gt, lt | N/A                               |
            - | note             | ge, le, eq, ne, gt, lt | substringof, contains, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    version_set_id:
        description:
            - Api Version Set identifier. Must be unique in the current API Management service instance.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Api Version Set
    azure_rm_apimanagementapiversionset_facts:
      resource_group: resource_group_name
      name: service_name
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Api Version Set
    azure_rm_apimanagementapiversionset_facts:
      resource_group: resource_group_name
      name: service_name
      version_set_id: version_set_id
'''

RETURN = '''
api_version_set:
    description: A list of dictionaries containing facts for Api Version Set.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/api-version-sets/vs1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: vs1
        description:
            description:
                - Description of API Version Set.
            returned: always
            type: str
            sample: Version configuration
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiVersionSetFacts(AzureRMModuleBase):
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
            version_set_id=dict(
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
        self.version_set_id = None
        super(AzureRMApiVersionSetFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.version_set_id is not None:
            self.results['api_version_set'] = self.get()
        else:
            self.results['api_version_set'] = self.list_by_service()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_version_set.list_by_service(resource_group_name=self.resource_group,
                                                                        service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api Version Set.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_version_set.get(resource_group_name=self.resource_group,
                                                            service_name=self.name,
                                                            version_set_id=self.version_set_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api Version Set.')

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
    AzureRMApiVersionSetFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_cdnendpoint_facts
version_added: "2.8"
short_description: Get Azure Endpoint facts.
description:
    - Get facts of Azure Endpoint.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    profile_name:
        description:
            - Name of the CDN profile which is unique within the resource group.
        required: True
    name:
        description:
            - Name of the endpoint under the profile which is unique globally.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Endpoint
    azure_rm_cdnendpoint_facts:
      resource_group: resource_group_name
      profile_name: profile_name
      name: endpoint_name

  - name: List instances of Endpoint
    azure_rm_cdnendpoint_facts:
      resource_group: resource_group_name
      profile_name: profile_name
'''

RETURN = '''
endpoints:
    description: A list of dictionaries containing facts for Endpoint.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourcegroups/RG/providers/Microsoft.Cdn/profiles/profile1/endpoints/endpoint1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: endpoint1
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: CentralUs
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        origins:
            description:
                - The source of the content being delivered via CDN.
            returned: always
            type: complex
            sample: origins
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.cdn import CdnManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEndpointsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.profile_name = None
        self.name = None
        self.tags = None
        super(AzureRMEndpointsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(CdnManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['endpoints'] = self.get()
        else:
            self.results['endpoints'] = self.list_by_profile()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.endpoints.get(resource_group_name=self.resource_group,
                                                      profile_name=self.profile_name,
                                                      endpoint_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Endpoints.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_profile(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.endpoints.list_by_profile(resource_group_name=self.resource_group,
                                                                  profile_name=self.profile_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Endpoints.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'origins': {
            }
        }
        return d


def main():
    AzureRMEndpointsFacts()


if __name__ == '__main__':
    main()

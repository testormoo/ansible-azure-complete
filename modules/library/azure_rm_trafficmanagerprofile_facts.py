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
module: azure_rm_trafficmanagerprofile_facts
version_added: "2.8"
short_description: Get Azure Profile facts.
description:
    - Get facts of Azure Profile.

options:
    resource_group:
        description:
            - The name of the resource group containing the Traffic Manager profile.
    name:
        description:
            - The name of the Traffic Manager profile.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Profile
    azure_rm_trafficmanagerprofile_facts:
      resource_group: resource_group_name
      name: profile_name

  - name: List instances of Profile
    azure_rm_trafficmanagerprofile_facts:
      resource_group: resource_group_name

  - name: List instances of Profile
    azure_rm_trafficmanagerprofile_facts:
'''

RETURN = '''
profiles:
    description: A list of dictionaries containing facts for Profile.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/{subscription-id}/resourceGroups/azuresdkfornetautoresttrafficmanager1323/providers/Microsoft.Network/trafficManagerProfi
                    les/azuresdkfornetautoresttrafficmanager3880"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: azuresdkfornetautoresttrafficmanager3880
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - The Azure Region where the resource lives
            returned: always
            type: str
            sample: global
        endpoints:
            description:
                - The list of endpoints in the Traffic Manager profile.
            returned: always
            type: complex
            sample: endpoints
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.trafficmanager import TrafficManagerManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProfilesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
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
        self.name = None
        self.tags = None
        super(AzureRMProfilesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(TrafficManagerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['profiles'] = self.get()
        elif self.resource_group is not None:
            self.results['profiles'] = self.list_by_resource_group()
        else:
            self.results['profiles'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.profiles.get(resource_group_name=self.resource_group,
                                                     profile_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Profiles.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.profiles.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Profiles.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.profiles.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Profiles.')

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
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'endpoints': {
            }
        }
        return d


def main():
    AzureRMProfilesFacts()


if __name__ == '__main__':
    main()

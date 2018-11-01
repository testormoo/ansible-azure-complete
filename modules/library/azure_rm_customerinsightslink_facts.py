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
module: azure_rm_customerinsightslink_facts
version_added: "2.8"
short_description: Get Azure Link facts.
description:
    - Get facts of Azure Link.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    link_name:
        description:
            - The name of the link.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Link
    azure_rm_customerinsightslink_facts:
      resource_group: resource_group_name
      hub_name: hub_name
      link_name: link_name

  - name: List instances of Link
    azure_rm_customerinsightslink_facts:
      resource_group: resource_group_name
      hub_name: hub_name
'''

RETURN = '''
links:
    description: A list of dictionaries containing facts for Link.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/azSdkTestHub/link
                    s/linkTest4806"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: azSdkTestHub/linkTest4806
        description:
            description:
                - Localized descriptions for the Link.
            returned: always
            type: complex
            sample: "{\n  'en-us': 'Link Description'\n}"
        mappings:
            description:
                - The set of properties mappings between the source and target Types.
            returned: always
            type: complex
            sample: mappings
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLinksFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            link_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.hub_name = None
        self.link_name = None
        super(AzureRMLinksFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.link_name is not None:
            self.results['links'] = self.get()
        else:
            self.results['links'] = self.list_by_hub()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.links.get(resource_group_name=self.resource_group,
                                                  hub_name=self.hub_name,
                                                  link_name=self.link_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Links.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_hub(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.links.list_by_hub(resource_group_name=self.resource_group,
                                                          hub_name=self.hub_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Links.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None),
            'mappings': {
            }
        }
        return d


def main():
    AzureRMLinksFacts()


if __name__ == '__main__':
    main()
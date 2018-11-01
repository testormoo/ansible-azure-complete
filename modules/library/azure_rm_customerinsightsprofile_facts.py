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
module: azure_rm_customerinsightsprofile_facts
version_added: "2.8"
short_description: Get Azure Profile facts.
description:
    - Get facts of Azure Profile.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    profile_name:
        description:
            - The name of the profile.
    locale_code:
        description:
            - Locale of profile to retrieve, default is en-us.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Profile
    azure_rm_customerinsightsprofile_facts:
      resource_group: resource_group_name
      hub_name: hub_name
      profile_name: profile_name
      locale_code: locale_code

  - name: List instances of Profile
    azure_rm_customerinsightsprofile_facts:
      resource_group: resource_group_name
      hub_name: hub_name
      locale_code: locale_code
'''

RETURN = '''
profiles:
    description: A list of dictionaries containing facts for Profile.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/azSdkTestHub/prof
                    iles/TestProfileType396"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: azSdkTestHub/TestProfileType396
        fields:
            description:
                - The properties of the Profile.
            returned: always
            type: complex
            sample: fields
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


class AzureRMProfilesFacts(AzureRMModuleBase):
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
            profile_name=dict(
                type='str'
            ),
            locale_code=dict(
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
        self.profile_name = None
        self.locale_code = None
        super(AzureRMProfilesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.profile_name is not None:
            self.results['profiles'] = self.get()
        else:
            self.results['profiles'] = self.list_by_hub()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.profiles.get(resource_group_name=self.resource_group,
                                                     hub_name=self.hub_name,
                                                     profile_name=self.profile_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Profiles.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_hub(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.profiles.list_by_hub(resource_group_name=self.resource_group,
                                                             hub_name=self.hub_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Profiles.')

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
            'fields': {
            }
        }
        return d


def main():
    AzureRMProfilesFacts()


if __name__ == '__main__':
    main()

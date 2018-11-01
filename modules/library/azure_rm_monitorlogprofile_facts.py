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
module: azure_rm_monitorlogprofile_facts
version_added: "2.8"
short_description: Get Azure Log Profile facts.
description:
    - Get facts of Azure Log Profile.

options:
    log_profile_name:
        description:
            - The name of the log profile.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Log Profile
    azure_rm_monitorlogprofile_facts:
      log_profile_name: log_profile_name
'''

RETURN = '''
log_profiles:
    description: A list of dictionaries containing facts for Log Profile.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Azure resource Id
            returned: always
            type: str
            sample: /subscriptions/df602c9c-7aa0-407d-a6fb-eb20c8bd1192/providers/microsoft.insights/logprofiles/default
        name:
            description:
                - Azure resource name
            returned: always
            type: str
            sample: default
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: location
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: tags
        locations:
            description:
                - "List of regions for which Activity Log events should be stored or streamed. It is a comma separated list of valid ARM locations including
                   the 'global' location."
            returned: always
            type: str
            sample: "[\n  'global'\n]"
        categories:
            description:
                - "the categories of the logs. These categories are created as is convenient to the user. Some values are: 'Write', 'Delete', and/or
                   'Action.'"
            returned: always
            type: str
            sample: "[\n  'Delete',\n  'Write',\n  'Action'\n]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLogProfilesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            log_profile_name=dict(
                type='str',
                required=True
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
        self.log_profile_name = None
        self.tags = None
        super(AzureRMLogProfilesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['log_profiles'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.log_profiles.get(log_profile_name=self.log_profile_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LogProfiles.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'locations': d.get('locations', None),
            'categories': d.get('categories', None)
        }
        return d


def main():
    AzureRMLogProfilesFacts()


if __name__ == '__main__':
    main()

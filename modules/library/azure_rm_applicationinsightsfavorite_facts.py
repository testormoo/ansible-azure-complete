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
module: azure_rm_applicationinsightsfavorite_facts
version_added: "2.8"
short_description: Get Azure Favorite facts.
description:
    - Get facts of Azure Favorite.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    resource_name:
        description:
            - The name of the Application Insights component resource.
        required: True
    favorite_id:
        description:
            - The Id of a specific favorite defined in the Application Insights component
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
  - name: Get instance of Favorite
    azure_rm_applicationinsightsfavorite_facts:
      resource_group: resource_group_name
      resource_name: resource_name
      favorite_id: favorite_id
'''

RETURN = '''
favorites:
    description: A list of dictionaries containing facts for Favorite.
    returned: always
    type: complex
    contains:
        version:
            description:
                - "This instance's version of the data model. This can change as new features are added that can be marked favorite. Current examples
                   include MetricsExplorer (ME) and Search."
            returned: always
            type: str
            sample: version
        tags:
            description:
                - A list of 0 or more tags that are associated with this favorite definition
            returned: always
            type: str
            sample: tags
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMFavoritesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            favorite_id=dict(
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
        self.resource_group = None
        self.resource_name = None
        self.favorite_id = None
        self.tags = None
        super(AzureRMFavoritesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['favorites'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.favorites.get(resource_group_name=self.resource_group,
                                                      resource_name=self.resource_name,
                                                      favorite_id=self.favorite_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Favorites.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'version': d.get('version', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMFavoritesFacts()


if __name__ == '__main__':
    main()

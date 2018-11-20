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
module: azure_rm_applicationinsightsanalyticsitem_facts
version_added: "2.8"
short_description: Get Azure Analytics Item facts.
description:
    - Get facts of Azure Analytics Item.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Application Insights component resource.
        required: True
    scope_path:
        description:
            - "Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights
               component."
        required: True
    id:
        description:
            - The Id of a specific item defined in the Application Insights component
    name:
        description:
            - The name of a specific item defined in the Application Insights component

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Analytics Item
    azure_rm_applicationinsightsanalyticsitem_facts:
      resource_group: resource_group_name
      name: resource_name
      scope_path: scope_path
      id: id
      name: name
'''

RETURN = '''
analytics_items:
    description: A list of dictionaries containing facts for Analytics Item.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Internally assigned unique id of the item definition.
            returned: always
            type: str
            sample: id
        version:
            description:
                - "This instance's version of the data model. This can change as new features are added."
            returned: always
            type: str
            sample: version
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAnalyticsItemsFacts(AzureRMModuleBase):
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
            scope_path=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            name=dict(
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
        self.scope_path = None
        self.id = None
        self.name = None
        super(AzureRMAnalyticsItemsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['analytics_items'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.analytics_items.get(resource_group_name=self.resource_group,
                                                            resource_name=self.name,
                                                            scope_path=self.scope_path)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AnalyticsItems.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'version': d.get('version', None)
        }
        return d


def main():
    AzureRMAnalyticsItemsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_timeseriesinsightsenvironment_facts
version_added: "2.8"
short_description: Get Azure Environment facts.
description:
    - Get facts of Azure Environment.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
    name:
        description:
            - The name of the Time Series Insights environment associated with the specified resource group.
    expand:
        description:
            - Setting $expand=status will include the status of the internal services of the environment in the Time Series Insights service.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Environment
    azure_rm_timeseriesinsightsenvironment_facts:
      resource_group: resource_group_name
      name: environment_name
      expand: expand

  - name: List instances of Environment
    azure_rm_timeseriesinsightsenvironment_facts:
      resource_group: resource_group_name

  - name: List instances of Environment
    azure_rm_timeseriesinsightsenvironment_facts:
'''

RETURN = '''
environments:
    description: A list of dictionaries containing facts for Environment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.TimeSeriesInsights/Environments/env1
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: env1
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: {}
        sku:
            description:
                - The sku determines the capacity of the environment, the SLA (in queries-per-minute and total capacity), and the billing rate.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The name of this SKU. Possible values include: 'S1', 'S2'"
                    returned: always
                    type: str
                    sample: S1
                capacity:
                    description:
                        - The capacity of the sku. This value can be changed to support scale out of environments after they have been created.
                    returned: always
                    type: int
                    sample: 1
        status:
            description:
                - An object that represents the status of the environment, and its internal state in the Time Series Insights service.
            returned: always
            type: complex
            sample: status
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.timeseriesinsights import TimeSeriesInsightsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEnvironmentsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            expand=dict(
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
        self.expand = None
        self.tags = None
        super(AzureRMEnvironmentsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(TimeSeriesInsightsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['environments'] = self.get()
        elif self.resource_group is not None:
            self.results['environments'] = self.list_by_resource_group()
        else:
            self.results['environments'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.environments.get(resource_group_name=self.resource_group,
                                                         environment_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Environments.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.environments.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Environments.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.environments.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Environments.')

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
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            },
            'status': {
            }
        }
        return d


def main():
    AzureRMEnvironmentsFacts()


if __name__ == '__main__':
    main()

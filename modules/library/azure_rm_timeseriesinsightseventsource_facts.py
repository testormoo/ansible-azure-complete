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
module: azure_rm_timeseriesinsightseventsource_facts
version_added: "2.8"
short_description: Get Azure Event Source facts.
description:
    - Get facts of Azure Event Source.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    environment_name:
        description:
            - The name of the Time Series Insights environment associated with the specified resource group.
        required: True
    name:
        description:
            - The name of the Time Series Insights event source associated with the specified environment.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Event Source
    azure_rm_timeseriesinsightseventsource_facts:
      resource_group: resource_group_name
      environment_name: environment_name
      name: event_source_name

  - name: List instances of Event Source
    azure_rm_timeseriesinsightseventsource_facts:
      resource_group: resource_group_name
      environment_name: environment_name
'''

RETURN = '''
event_sources:
    description: A list of dictionaries containing facts for Event Source.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.TimeSeriesInsights/Environments/env1/eventSources/es1
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: es1
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
        kind:
            description:
                - Constant filled by server.
            returned: always
            type: str
            sample: Microsoft.EventHub
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.timeseriesinsights import TimeSeriesInsightsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEventSourcesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            environment_name=dict(
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
        self.environment_name = None
        self.name = None
        self.tags = None
        super(AzureRMEventSourcesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(TimeSeriesInsightsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['event_sources'] = self.get()
        else:
            self.results['event_sources'] = self.list_by_environment()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_sources.get(resource_group_name=self.resource_group,
                                                          environment_name=self.environment_name,
                                                          event_source_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for EventSources.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_environment(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_sources.list_by_environment(resource_group_name=self.resource_group,
                                                                          environment_name=self.environment_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for EventSources.')

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
            'kind': d.get('kind', None)
        }
        return d


def main():
    AzureRMEventSourcesFacts()


if __name__ == '__main__':
    main()

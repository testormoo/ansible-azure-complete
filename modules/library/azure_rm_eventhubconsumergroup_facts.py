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
module: azure_rm_eventhubconsumergroup_facts
version_added: "2.8"
short_description: Get Azure Consumer Group facts.
description:
    - Get facts of Azure Consumer Group.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    namespace_name:
        description:
            - The Namespace name
        required: True
    event_hub_name:
        description:
            - The Event Hub name
        required: True
    skip:
        description:
            - "Skip is only used if a previous operation returned a partial result. If a previous response contains a nextLink element, the value of the
               nextLink element will include a skip parameter that specifies a starting point to use for subsequent calls."
    top:
        description:
            - May be used to limit the number of results to the most recent N usageDetails.
    name:
        description:
            - The consumer group name

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Consumer Group
    azure_rm_eventhubconsumergroup_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
      event_hub_name: event_hub_name
      skip: skip
      top: top

  - name: Get instance of Consumer Group
    azure_rm_eventhubconsumergroup_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
      event_hub_name: event_hub_name
      name: consumer_group_name
'''

RETURN = '''
consumer_groups:
    description: A list of dictionaries containing facts for Consumer Group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: "/subscriptions/5f750a97-50d9-4e36-8081-c9ee4c0210d4/resourceGroups/ArunMonocle/providers/Microsoft.EventHub/namespaces/sdk-Namespace-266
                    1/eventhubs/sdk-EventHub-6681/consumergroups/sdk-ConsumerGroup-5563"
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: sdk-ConsumerGroup-5563
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventhub import EventHubManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMConsumerGroupFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            namespace_name=dict(
                type='str',
                required=True
            ),
            event_hub_name=dict(
                type='str',
                required=True
            ),
            skip=dict(
                type='int'
            ),
            top=dict(
                type='int'
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
        self.namespace_name = None
        self.event_hub_name = None
        self.skip = None
        self.top = None
        self.name = None
        super(AzureRMConsumerGroupFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['consumer_groups'] = self.get()
        else:
            self.results['consumer_groups'] = self.list_by_event_hub()
        return self.results

    def list_by_event_hub(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.consumer_groups.list_by_event_hub(resource_group_name=self.resource_group,
                                                                          namespace_name=self.namespace_name,
                                                                          event_hub_name=self.event_hub_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Consumer Group.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.consumer_groups.get(resource_group_name=self.resource_group,
                                                            namespace_name=self.namespace_name,
                                                            event_hub_name=self.event_hub_name,
                                                            consumer_group_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Consumer Group.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMConsumerGroupFacts()


if __name__ == '__main__':
    main()

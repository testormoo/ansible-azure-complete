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
module: azure_rm_eventgrideventsubscription_facts
version_added: "2.8"
short_description: Get Azure Event Subscription facts.
description:
    - Get facts of Azure Event Subscription.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription."
    provider_namespace:
        description:
            - Namespace of the provider of the topic
    resource_type_name:
        description:
            - Name of the resource type
    resource_name:
        description:
            - Name of the resource
    domain_name:
        description:
            - Name of the top level domain
    topic_name:
        description:
            - Name of the domain topic
    scope:
        description:
            - "The scope of the event subscription. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource
               provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription,
               '/subscriptions/{subscriptionId}/resourceGroups/{I(resource_group)}' for a resource group, and
               '/subscriptions/{subscriptionId}/resourceGroups/{I(resource_group)}/providers/{resourceProviderNamespace}/{resourceType}/{I(resource_name)}'
               for a resource, and
               '/subscriptions/{subscriptionId}/resourceGroups/{I(resource_group)}/providers/Microsoft.EventGrid/topics/{I(topic_name)}' for an EventGrid
               topic."
    event_subscription_name:
        description:
            - Name of the event subscription

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Event Subscription
    azure_rm_eventgrideventsubscription_facts:
      resource_group: resource_group_name
      provider_namespace: provider_namespace
      resource_type_name: resource_type_name
      resource_name: resource_name

  - name: List instances of Event Subscription
    azure_rm_eventgrideventsubscription_facts:
      resource_group: resource_group_name
      domain_name: domain_name
      topic_name: topic_name

  - name: Get instance of Event Subscription
    azure_rm_eventgrideventsubscription_facts:
      scope: scope
      event_subscription_name: event_subscription_name
'''

RETURN = '''
event_subscriptions:
    description: A list of dictionaries containing facts for Event Subscription.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified identifier of the resource
            returned: always
            type: str
            sample: /subscriptions/5b4b650e-28b9-4790-b3ab-ddbd88d727c4/providers/Microsoft.EventGrid/eventSubscriptions/examplesubscription3
        name:
            description:
                - Name of the resource
            returned: always
            type: str
            sample: examplesubscription3
        topic:
            description:
                - Name of the topic of the event subscription.
            returned: always
            type: str
            sample: /subscriptions/5b4b650e-28b9-4790-b3ab-ddbd88d727c4
        destination:
            description:
                - Information about the destination where events have to be delivered for the event subscription.
            returned: always
            type: complex
            sample: destination
            contains:
        filter:
            description:
                - Information about the filter for the event subscription.
            returned: always
            type: complex
            sample: filter
            contains:
        labels:
            description:
                - List of user defined labels.
            returned: always
            type: str
            sample: "[\n  'label1',\n  'label2'\n]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventgrid import EventGridManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEventSubscriptionsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            provider_namespace=dict(
                type='str'
            ),
            resource_type_name=dict(
                type='str'
            ),
            resource_name=dict(
                type='str'
            ),
            domain_name=dict(
                type='str'
            ),
            topic_name=dict(
                type='str'
            ),
            scope=dict(
                type='str'
            ),
            event_subscription_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.provider_namespace = None
        self.resource_type_name = None
        self.resource_name = None
        self.domain_name = None
        self.topic_name = None
        self.scope = None
        self.event_subscription_name = None
        super(AzureRMEventSubscriptionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.provider_namespace is not None and
                self.resource_type_name is not None and
                self.resource_name is not None):
            self.results['event_subscriptions'] = self.list_by_resource()
        elif (self.resource_group is not None and
                self.domain_name is not None and
                self.topic_name is not None):
            self.results['event_subscriptions'] = self.list_by_domain_topic()
        elif (self.scope is not None and
                self.event_subscription_name is not None):
            self.results['event_subscriptions'] = self.get()
        return self.results

    def list_by_resource(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_subscriptions.list_by_resource(resource_group_name=self.resource_group,
                                                                             provider_namespace=self.provider_namespace,
                                                                             resource_type_name=self.resource_type_name,
                                                                             resource_name=self.resource_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for EventSubscriptions.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_domain_topic(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_subscriptions.list_by_domain_topic(resource_group_name=self.resource_group,
                                                                                 domain_name=self.domain_name,
                                                                                 topic_name=self.topic_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for EventSubscriptions.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_subscriptions.get(scope=self.scope,
                                                                event_subscription_name=self.event_subscription_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for EventSubscriptions.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'topic': d.get('topic', None),
            'destination': {
            },
            'filter': {
            },
            'labels': d.get('labels', None)
        }
        return d


def main():
    AzureRMEventSubscriptionsFacts()


if __name__ == '__main__':
    main()

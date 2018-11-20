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
module: azure_rm_servicebussubscription_facts
version_added: "2.8"
short_description: Get Azure Subscription facts.
description:
    - Get facts of Azure Subscription.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    namespace_name:
        description:
            - The namespace name
        required: True
    topic_name:
        description:
            - The topic name.
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
            - The subscription name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Subscription
    azure_rm_servicebussubscription_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
      topic_name: topic_name
      skip: skip
      top: top

  - name: Get instance of Subscription
    azure_rm_servicebussubscription_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
      topic_name: topic_name
      name: subscription_name
'''

RETURN = '''
subscriptions:
    description: A list of dictionaries containing facts for Subscription.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: "/subscriptions/Subscriptionid/resourceGroups/ResourceGroup/providers/Microsoft.ServiceBus/namespaces/sdk-Namespace-1349/topics/sdk-Topic
                    s-8740/subscriptions/sdk-Subscriptions-2178"
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: sdk-Subscriptions-2178
        status:
            description:
                - "Enumerates the possible values for the status of a messaging entity. Possible values include: 'Active', 'Disabled', 'Restoring',
                   'SendDisabled', 'ReceiveDisabled', 'Creating', 'Deleting', 'Renaming', 'Unknown'"
            returned: always
            type: str
            sample: Active
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.servicebus import ServiceBusManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSubscriptionsFacts(AzureRMModuleBase):
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
            topic_name=dict(
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
        self.topic_name = None
        self.skip = None
        self.top = None
        self.name = None
        super(AzureRMSubscriptionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceBusManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['subscriptions'] = self.list_by_topic()
        elif self.name is not None:
            self.results['subscriptions'] = self.get()
        return self.results

    def list_by_topic(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.subscriptions.list_by_topic(resource_group_name=self.resource_group,
                                                                    namespace_name=self.namespace_name,
                                                                    topic_name=self.topic_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Subscriptions.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.subscriptions.get(resource_group_name=self.resource_group,
                                                          namespace_name=self.namespace_name,
                                                          topic_name=self.topic_name,
                                                          subscription_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Subscriptions.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMSubscriptionsFacts()


if __name__ == '__main__':
    main()

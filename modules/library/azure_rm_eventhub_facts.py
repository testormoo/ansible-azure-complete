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
module: azure_rm_eventhub_facts
version_added: "2.8"
short_description: Get Azure Event Hub facts.
description:
    - Get facts of Azure Event Hub.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    namespace_name:
        description:
            - The Namespace name
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
            - The Event Hub name

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Event Hub
    azure_rm_eventhub_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
      skip: skip
      top: top

  - name: Get instance of Event Hub
    azure_rm_eventhub_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
      name: event_hub_name
'''

RETURN = '''
event_hubs:
    description: A list of dictionaries containing facts for Event Hub.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: "/subscriptions/e2f361f0-3b27-4503-a9cc-21cfba380093/resourceGroups/Default-NotificationHubs-AustraliaEast/providers/Microsoft.EventHub/n
                    amespaces/sdk-Namespace-716/eventhubs/sdk-EventHub-10"
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: sdk-EventHub-10
        status:
            description:
                - "Enumerates the possible values for the status of the Event Hub. Possible values include: 'Active', 'Disabled', 'Restoring',
                   'SendDisabled', 'ReceiveDisabled', 'Creating', 'Deleting', 'Renaming', 'Unknown'"
            returned: always
            type: str
            sample: Active
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventhub import EventHubManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEventHubFacts(AzureRMModuleBase):
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
        self.skip = None
        self.top = None
        self.name = None
        super(AzureRMEventHubFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['event_hubs'] = self.get()
        else:
            self.results['event_hubs'] = self.list_by_namespace()
        return self.results

    def list_by_namespace(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_hubs.list_by_namespace(resource_group_name=self.resource_group,
                                                                     namespace_name=self.namespace_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Event Hub.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_hubs.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.namespace_name,
                                                       event_hub_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Event Hub.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMEventHubFacts()


if __name__ == '__main__':
    main()

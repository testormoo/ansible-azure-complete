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
module: azure_rm_medialiveevent_facts
version_added: "2.8"
short_description: Get Azure Live Event facts.
description:
    - Get facts of Azure Live Event.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    name:
        description:
            - The name of the Live Event.
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
  - name: Get instance of Live Event
    azure_rm_medialiveevent_facts:
      resource_group: resource_group_name
      account_name: account_name
      name: live_event_name
'''

RETURN = '''
live_events:
    description: A list of dictionaries containing facts for Live Event.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource ID for the resource.
            returned: always
            type: str
            sample: "/subscriptions/0a6ec948-5a62-437d-b9df-934dc7c1b722/resourceGroups/mediaresources/providers/Microsoft.Media/mediaservices/slitestmedia10
                    /liveevents/myLiveEvent1"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: myLiveEvent1
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - The Azure Region of the resource.
            returned: always
            type: str
            sample: West US
        description:
            description:
                - The Live Event description.
            returned: always
            type: str
            sample: description
        input:
            description:
                - The Live Event input.
            returned: always
            type: complex
            sample: input
            contains:
                endpoints:
                    description:
                        - The input endpoints for the Live Event.
                    returned: always
                    type: complex
                    sample: endpoints
                    contains:
        preview:
            description:
                - The Live Event preview.
            returned: always
            type: complex
            sample: preview
            contains:
                endpoints:
                    description:
                        - The endpoints for preview.
                    returned: always
                    type: complex
                    sample: endpoints
                    contains:
        encoding:
            description:
                - The Live Event encoding.
            returned: always
            type: complex
            sample: encoding
            contains:
        created:
            description:
                - The exact time the Live Event was created.
            returned: always
            type: datetime
            sample: "2018-03-03T02:25:08.3474032Z"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLiveEventFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.account_name = None
        self.name = None
        self.tags = None
        super(AzureRMLiveEventFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['live_events'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.live_events.get(resource_group_name=self.resource_group,
                                                        account_name=self.account_name,
                                                        live_event_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Live Event.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'description': d.get('description', None),
            'input': {
                'endpoints': {
                }
            },
            'preview': {
                'endpoints': {
                }
            },
            'encoding': {
            },
            'created': d.get('created', None)
        }
        return d


def main():
    AzureRMLiveEventFacts()


if __name__ == '__main__':
    main()

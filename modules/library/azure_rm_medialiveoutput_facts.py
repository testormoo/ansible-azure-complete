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
module: azure_rm_medialiveoutput_facts
version_added: "2.8"
short_description: Get Azure Live Output facts.
description:
    - Get facts of Azure Live Output.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    live_event_name:
        description:
            - The name of the Live Event.
        required: True
    live_output_name:
        description:
            - The name of the Live Output.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Live Output
    azure_rm_medialiveoutput_facts:
      resource_group: resource_group_name
      account_name: account_name
      live_event_name: live_event_name
      live_output_name: live_output_name
'''

RETURN = '''
live_outputs:
    description: A list of dictionaries containing facts for Live Output.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource ID for the resource.
            returned: always
            type: str
            sample: "/subscriptions/0a6ec948-5a62-437d-b9df-934dc7c1b722/resourceGroups/mediaresources/providers/Microsoft.Media/mediaservices/slitestmedia10
                    /liveevents/myLiveEvent1/liveoutputs/myLiveOutput1"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: myLiveOutput1
        description:
            description:
                - The description of the Live Output.
            returned: always
            type: str
            sample: description
        hls:
            description:
                - The HLS configuration.
            returned: always
            type: complex
            sample: hls
            contains:
        created:
            description:
                - The exact time the Live Output was created.
            returned: always
            type: datetime
            sample: "0001-01-01T08:00:00+00:00"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLiveOutputsFacts(AzureRMModuleBase):
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
            live_event_name=dict(
                type='str',
                required=True
            ),
            live_output_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.account_name = None
        self.live_event_name = None
        self.live_output_name = None
        super(AzureRMLiveOutputsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['live_outputs'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.live_outputs.get(resource_group_name=self.resource_group,
                                                         account_name=self.account_name,
                                                         live_event_name=self.live_event_name,
                                                         live_output_name=self.live_output_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LiveOutputs.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None),
            'hls': {
            },
            'created': d.get('created', None)
        }
        return d


def main():
    AzureRMLiveOutputsFacts()


if __name__ == '__main__':
    main()

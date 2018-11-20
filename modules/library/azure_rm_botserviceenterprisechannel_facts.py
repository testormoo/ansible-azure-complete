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
module: azure_rm_botserviceenterprisechannel_facts
version_added: "2.8"
short_description: Get Azure Enterprise Channel facts.
description:
    - Get facts of Azure Enterprise Channel.

options:
    resource_group:
        description:
            - The name of the Bot resource group in the user subscription.
        required: True
    name:
        description:
            - The name of the Bot resource.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Enterprise Channel
    azure_rm_botserviceenterprisechannel_facts:
      resource_group: resource_group_name
      name: resource_name

  - name: List instances of Enterprise Channel
    azure_rm_botserviceenterprisechannel_facts:
      resource_group: resource_group_name
'''

RETURN = '''
enterprise_channels:
    description: A list of dictionaries containing facts for Enterprise Channel.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Specifies the resource ID.
            returned: always
            type: str
            sample: contoso-dl
        location:
            description:
                - Specifies the location of the resource.
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Contains resource tags defined as key/value pairs.
            returned: always
            type: complex
            sample: "{\n  'tag1': 'value1',\n  'tag2': 'value2'\n}"
        etag:
            description:
                - Entity Tag
            returned: always
            type: str
            sample: etag1
        properties:
            description:
                - The set of properties specific to an Enterprise Channel resource.
            returned: always
            type: complex
            sample: properties
            contains:
                state:
                    description:
                        - "The current state of the Enterprise Channel. Possible values include: 'Creating', 'CreateFailed', 'Started', 'Starting',
                           'StartFailed', 'Stopped', 'Stopping', 'StopFailed', 'Deleting', 'DeleteFailed'"
                    returned: always
                    type: str
                    sample: Started
                nodes:
                    description:
                        - The nodes associated with the Enterprise Channel.
                    returned: always
                    type: complex
                    sample: nodes
                    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.botservice import AzureBotService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEnterpriseChannelsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
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
        self.name = None
        self.tags = None
        super(AzureRMEnterpriseChannelsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureBotService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['enterprise_channels'] = self.get()
        else:
            self.results['enterprise_channels'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.enterprise_channels.get(resource_group_name=self.resource_group,
                                                                resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for EnterpriseChannels.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.enterprise_channels.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for EnterpriseChannels.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'etag': d.get('etag', None),
            'properties': {
                'state': d.get('properties', {}).get('state', None),
                'nodes': {
                }
            }
        }
        return d


def main():
    AzureRMEnterpriseChannelsFacts()


if __name__ == '__main__':
    main()

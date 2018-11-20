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
module: azure_rm_botservicebot_facts
version_added: "2.8"
short_description: Get Azure Bot facts.
description:
    - Get facts of Azure Bot.

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
  - name: Get instance of Bot
    azure_rm_botservicebot_facts:
      resource_group: resource_group_name
      name: resource_name

  - name: List instances of Bot
    azure_rm_botservicebot_facts:
      resource_group: resource_group_name
'''

RETURN = '''
bots:
    description: A list of dictionaries containing facts for Bot.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Specifies the resource ID.
            returned: always
            type: str
            sample: someid
        name:
            description:
                - Specifies the name of the resource.
            returned: always
            type: str
            sample: samplename
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
        kind:
            description:
                - "Required. Gets or sets the Kind of the resource. Possible values include: 'sdk', 'designer', 'bot', 'function'"
            returned: always
            type: str
            sample: sdk
        etag:
            description:
                - Entity Tag
            returned: always
            type: str
            sample: etag1
        properties:
            description:
                - The set of properties specific to bot resource
            returned: always
            type: complex
            sample: properties
            contains:
                description:
                    description:
                        - The description of the bot
                    returned: always
                    type: str
                    sample: The description of the bot
                endpoint:
                    description:
                        - "The bot's endpoint"
                    returned: always
                    type: str
                    sample: "http://mybot.coffee"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.botservice import AzureBotService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBotsFacts(AzureRMModuleBase):
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
        super(AzureRMBotsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureBotService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['bots'] = self.get()
        else:
            self.results['bots'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.bots.get(resource_group_name=self.resource_group,
                                                 resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Bots.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.bots.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Bots.')

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
            'kind': d.get('kind', None),
            'etag': d.get('etag', None),
            'properties': {
                'description': d.get('properties', {}).get('description', None),
                'endpoint': d.get('properties', {}).get('endpoint', None)
            }
        }
        return d


def main():
    AzureRMBotsFacts()


if __name__ == '__main__':
    main()

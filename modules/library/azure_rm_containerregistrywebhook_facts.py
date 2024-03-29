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
module: azure_rm_containerregistrywebhook_facts
version_added: "2.8"
short_description: Get Azure Webhook facts.
description:
    - Get facts of Azure Webhook.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        required: True
    registry_name:
        description:
            - The name of the container registry.
        required: True
    name:
        description:
            - The name of the webhook.
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
  - name: Get instance of Webhook
    azure_rm_containerregistrywebhook_facts:
      resource_group: resource_group_name
      registry_name: registry_name
      name: webhook_name
'''

RETURN = '''
webhooks:
    description: A list of dictionaries containing facts for Webhook.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.ContainerRegistry/registries/myRe
                    gistry/webhooks/myWebhook"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: myWebhook
        location:
            description:
                - The location of the resource. This cannot be changed after the resource is created.
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - The tags of the resource.
            returned: always
            type: complex
            sample: "{\n  'key': 'value'\n}"
        status:
            description:
                - "The status of the webhook at the time the operation was called. Possible values include: 'enabled', 'disabled'"
            returned: always
            type: str
            sample: enabled
        scope:
            description:
                - "The scope of repositories where the event can be triggered. For example, 'foo:*' means events for all tags under repository 'foo'.
                   'foo:bar' means events for 'foo:bar' only. 'foo' is equivalent to 'foo:latest'. Empty means all events."
            returned:
            type: str
            sample: myRepository
        actions:
            description:
                - The list of actions that trigger the webhook to post notifications.
            returned: always
            type: str
            sample: "[\n  'push'\n]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.containerregistry import ContainerRegistryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWebhookFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registry_name=dict(
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
        self.registry_name = None
        self.name = None
        self.tags = None
        super(AzureRMWebhookFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ContainerRegistryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['webhooks'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.webhooks.get(resource_group_name=self.resource_group,
                                                     registry_name=self.registry_name,
                                                     webhook_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Webhook.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'status': d.get('status', None),
            'scope': d.get('scope', None),
            'actions': d.get('actions', None)
        }
        return d


def main():
    AzureRMWebhookFacts()


if __name__ == '__main__':
    main()

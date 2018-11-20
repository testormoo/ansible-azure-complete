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
module: azure_rm_relaywcfrelay_facts
version_added: "2.8"
short_description: Get Azure W C F Relay facts.
description:
    - Get facts of Azure W C F Relay.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    namespace_name:
        description:
            - The namespace name
        required: True
    name:
        description:
            - The relay name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of W C F Relay
    azure_rm_relaywcfrelay_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
      name: relay_name

  - name: List instances of W C F Relay
    azure_rm_relaywcfrelay_facts:
      resource_group: resource_group_name
      namespace_name: namespace_name
'''

RETURN = '''
wcf_relays:
    description: A list of dictionaries containing facts for W C F Relay.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/e2f361f0-3b27-4503-a9cc-21cfba380093/resourceGroups/Default-ServiceBus-WestUS/providers/Microsoft.Relay/namespaces/sdk-Re
                    layNamespace-9953/WcfRelays/sdk-Relay-Wcf-1194"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: sdk-Relay-Wcf-1194
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.relay import RelayManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWCFRelaysFacts(AzureRMModuleBase):
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
        self.name = None
        super(AzureRMWCFRelaysFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RelayManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['wcf_relays'] = self.get()
        else:
            self.results['wcf_relays'] = self.list_by_namespace()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.wcf_relays.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.namespace_name,
                                                       relay_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WCFRelays.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_namespace(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.wcf_relays.list_by_namespace(resource_group_name=self.resource_group,
                                                                     namespace_name=self.namespace_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WCFRelays.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMWCFRelaysFacts()


if __name__ == '__main__':
    main()

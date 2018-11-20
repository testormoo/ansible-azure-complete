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
module: azure_rm_sqlserverkey_facts
version_added: "2.8"
short_description: Get Azure Server Key facts.
description:
    - Get facts of Azure Server Key.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the server key to be retrieved.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Server Key
    azure_rm_sqlserverkey_facts:
      resource_group: resource_group_name
      server_name: server_name
      name: key_name

  - name: List instances of Server Key
    azure_rm_sqlserverkey_facts:
      resource_group: resource_group_name
      server_name: server_name
'''

RETURN = '''
server_keys:
    description: A list of dictionaries containing facts for Server Key.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-7398/providers/Microsoft.Sql/servers/sqlcrudtest-4645/key
                    s/someVault_someKey_01234567890123456789012345678901"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: sqlcrudtest-4645
        kind:
            description:
                - Kind of encryption protector. This is metadata used for the Azure portal experience.
            returned: always
            type: str
            sample: azurekeyvault
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: Japan East
        uri:
            description:
                - The URI of the server key.
            returned: always
            type: str
            sample: "https://someVault.vault.azure.net/keys/someKey/01234567890123456789012345678901"
        thumbprint:
            description:
                - Thumbprint of the server key.
            returned: always
            type: str
            sample: 00112233445566778899AABBCCDDEEFFAABBCCDD
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServerKeysFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
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
        self.server_name = None
        self.name = None
        super(AzureRMServerKeysFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['server_keys'] = self.get()
        else:
            self.results['server_keys'] = self.list_by_server()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.server_keys.get(resource_group_name=self.resource_group,
                                                        server_name=self.server_name,
                                                        key_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ServerKeys.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.server_keys.list_by_server(resource_group_name=self.resource_group,
                                                                   server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ServerKeys.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'kind': d.get('kind', None),
            'location': d.get('location', None),
            'uri': d.get('uri', None),
            'thumbprint': d.get('thumbprint', None)
        }
        return d


def main():
    AzureRMServerKeysFacts()


if __name__ == '__main__':
    main()

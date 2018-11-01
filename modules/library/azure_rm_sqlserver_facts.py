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
module: azure_rm_sqlserver_facts
version_added: "2.8"
short_description: Get Azure SQL Server facts.
description:
    - Get facts of Azure SQL Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of SQL Server
    azure_rm_sqlserver_facts:
      resource_group: resource_group_name
      server_name: server_name

  - name: List instances of SQL Server
    azure_rm_sqlserver_facts:
      resource_group: resource_group_name
'''

RETURN = '''
servers:
    description: A list of dictionaries containing facts for SQL Server.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-7398/providers/Microsoft.Sql/servers/sqlcrudtest-4645
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: sqlcrudtest-4645
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: japaneast
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: "{\n  'tagKey1': 'TagValue1'\n}"
        kind:
            description:
                - Kind of sql server. This is metadata used for the Azure portal experience.
            returned: always
            type: str
            sample: v12.0
        version:
            description:
                - The version of the server.
            returned: always
            type: str
            sample: 12.0
        state:
            description:
                - The state of the server.
            returned: always
            type: str
            sample: Ready
        fully_qualified_domain_name:
            description:
                - The fully qualified domain name of the server.
            returned: always
            type: str
            sample: fully_qualified_domain_name
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
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
        self.server_name = None
        self.tags = None
        super(AzureRMServersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.server_name is not None:
            self.results['servers'] = self.get()
        else:
            self.results['servers'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.servers.get(resource_group_name=self.resource_group,
                                                    server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Servers.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.servers.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Servers.')

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
            'version': d.get('version', None),
            'state': d.get('state', None),
            'fully_qualified_domain_name': d.get('fully_qualified_domain_name', None)
        }
        return d


def main():
    AzureRMServersFacts()


if __name__ == '__main__':
    main()

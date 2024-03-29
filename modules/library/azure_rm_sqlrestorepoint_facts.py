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
module: azure_rm_sqlrestorepoint_facts
version_added: "2.8"
short_description: Get Azure Restore Point facts.
description:
    - Get facts of Azure Restore Point.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database.
        required: True
    name:
        description:
            - The name of the restore point.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Restore Point
    azure_rm_sqlrestorepoint_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name
      name: restore_point_name

  - name: List instances of Restore Point
    azure_rm_sqlrestorepoint_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name
'''

RETURN = '''
restore_points:
    description: A list of dictionaries containing facts for Restore Point.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/providers/Microsoft.Sql/servers/testserver/databases/testDatabase/restorePoints/1315
                    46477590000000"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 131546477590000000
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: japaneast
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRestorePointFacts(AzureRMModuleBase):
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
            database_name=dict(
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
        self.database_name = None
        self.name = None
        super(AzureRMRestorePointFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['restore_points'] = self.get()
        else:
            self.results['restore_points'] = self.list_by_database()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.restore_points.get(resource_group_name=self.resource_group,
                                                           server_name=self.server_name,
                                                           database_name=self.database_name,
                                                           restore_point_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Restore Point.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_database(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.restore_points.list_by_database(resource_group_name=self.resource_group,
                                                                        server_name=self.server_name,
                                                                        database_name=self.database_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Restore Point.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None)
        }
        return d


def main():
    AzureRMRestorePointFacts()


if __name__ == '__main__':
    main()

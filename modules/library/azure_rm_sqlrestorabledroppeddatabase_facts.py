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
module: azure_rm_sqlrestorabledroppeddatabase_facts
version_added: "2.8"
short_description: Get Azure Restorable Dropped Database facts.
description:
    - Get facts of Azure Restorable Dropped Database.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the server.
        required: True
    restorable_droppeded_database_id:
        description:
            - The id of the deleted database in the form of databaseName,deletionTimeInFileTimeFormat

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Restorable Dropped Database
    azure_rm_sqlrestorabledroppeddatabase_facts:
      resource_group: resource_group_name
      name: server_name
      restorable_droppeded_database_id: restorable_droppeded_database_id

  - name: List instances of Restorable Dropped Database
    azure_rm_sqlrestorabledroppeddatabase_facts:
      resource_group: resource_group_name
      name: server_name
'''

RETURN = '''
restorable_dropped_databases:
    description: A list of dictionaries containing facts for Restorable Dropped Database.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/restorabledroppeddatabasetest-1257/providers/Microsoft.Sql/servers/re
                    storabledroppeddatabasetest-2389/restorableDroppedDatabases/restorabledroppeddatabasetest-7654,131403269876900000"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: restorabledroppeddatabasetest-7654,131403269876900000
        location:
            description:
                - The geo-location where the resource lives
            returned: always
            type: str
            sample: Japan East
        edition:
            description:
                - The edition of the database
            returned: always
            type: str
            sample: Basic
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRestorableDroppedDatabasesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            restorable_droppeded_database_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.restorable_droppeded_database_id = None
        super(AzureRMRestorableDroppedDatabasesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.restorable_droppeded_database_id is not None:
            self.results['restorable_dropped_databases'] = self.get()
        else:
            self.results['restorable_dropped_databases'] = self.list_by_server()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.restorable_dropped_databases.get(resource_group_name=self.resource_group,
                                                                         server_name=self.name,
                                                                         restorable_droppeded_database_id=self.restorable_droppeded_database_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RestorableDroppedDatabases.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.restorable_dropped_databases.list_by_server(resource_group_name=self.resource_group,
                                                                                    server_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for RestorableDroppedDatabases.')

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
            'location': d.get('location', None),
            'edition': d.get('edition', None)
        }
        return d


def main():
    AzureRMRestorableDroppedDatabasesFacts()


if __name__ == '__main__':
    main()

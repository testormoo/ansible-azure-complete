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
module: azure_rm_sqllongtermretentionbackup_facts
version_added: "2.8"
short_description: Get Azure Long Term Retention Backup facts.
description:
    - Get facts of Azure Long Term Retention Backup.

options:
    location_name:
        description:
            - The location of the database
        required: True
    long_term_retention_server_name:
        description:
    long_term_retention_database_name:
        description:
    only_latest_per_database:
        description:
            - Whether or not to only get the latest backup for each database.
    database_state:
        description:
            - Whether to query against just live databases, just deleted databases, or all databases.
    name:
        description:
            - The backup name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Long Term Retention Backup
    azure_rm_sqllongtermretentionbackup_facts:
      location_name: location_name
      long_term_retention_server_name: long_term_retention_server_name
      long_term_retention_database_name: long_term_retention_database_name
      only_latest_per_database: only_latest_per_database
      database_state: database_state

  - name: Get instance of Long Term Retention Backup
    azure_rm_sqllongtermretentionbackup_facts:
      location_name: location_name
      long_term_retention_server_name: long_term_retention_server_name
      long_term_retention_database_name: long_term_retention_database_name
      name: backup_name

  - name: List instances of Long Term Retention Backup
    azure_rm_sqllongtermretentionbackup_facts:
      location_name: location_name
      long_term_retention_server_name: long_term_retention_server_name
      only_latest_per_database: only_latest_per_database
      database_state: database_state

  - name: List instances of Long Term Retention Backup
    azure_rm_sqllongtermretentionbackup_facts:
      location_name: location_name
      only_latest_per_database: only_latest_per_database
      database_state: database_state
'''

RETURN = '''
long_term_retention_backups:
    description: A list of dictionaries containing facts for Long Term Retention Backup.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/providers/Microsoft.Sql/locations/japaneast/longTermRetentionServers/testserver/long
                    TermRetentionDatabases/testDatabase/longTermRetentionBackups/2017-03-10T08:00:00.000Z;55555555-6666-7777-8888-999999999999;2017-09-06T08
                    :00:00.000Z"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: "2017-03-10T08:00:00.000Z;55555555-6666-7777-8888-999999999999;131637960820000000"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLongTermRetentionBackupsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            location_name=dict(
                type='str',
                required=True
            ),
            long_term_retention_server_name=dict(
                type='str'
            ),
            long_term_retention_database_name=dict(
                type='str'
            ),
            only_latest_per_database=dict(
                type='str'
            ),
            database_state=dict(
                type='str'
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
        self.location_name = None
        self.long_term_retention_server_name = None
        self.long_term_retention_database_name = None
        self.only_latest_per_database = None
        self.database_state = None
        self.name = None
        super(AzureRMLongTermRetentionBackupsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.long_term_retention_server_name is not None and
                self.long_term_retention_database_name is not None):
            self.results['long_term_retention_backups'] = self.list_by_database()
        elif (self.long_term_retention_server_name is not None and
                self.long_term_retention_database_name is not None and
                self.name is not None):
            self.results['long_term_retention_backups'] = self.get()
        elif self.long_term_retention_server_name is not None:
            self.results['long_term_retention_backups'] = self.list_by_server()
        else:
            self.results['long_term_retention_backups'] = self.list_by_location()
        return self.results

    def list_by_database(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.long_term_retention_backups.list_by_database(location_name=self.location_name,
                                                                                     long_term_retention_server_name=self.long_term_retention_server_name,
                                                                                     long_term_retention_database_name=self.long_term_retention_database_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LongTermRetentionBackups.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.long_term_retention_backups.get(location_name=self.location_name,
                                                                        long_term_retention_server_name=self.long_term_retention_server_name,
                                                                        long_term_retention_database_name=self.long_term_retention_database_name,
                                                                        backup_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LongTermRetentionBackups.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.long_term_retention_backups.list_by_server(location_name=self.location_name,
                                                                                   long_term_retention_server_name=self.long_term_retention_server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LongTermRetentionBackups.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_location(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.long_term_retention_backups.list_by_location(location_name=self.location_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LongTermRetentionBackups.')

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
    AzureRMLongTermRetentionBackupsFacts()


if __name__ == '__main__':
    main()

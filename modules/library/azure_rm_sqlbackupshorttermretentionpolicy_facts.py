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
module: azure_rm_sqlbackupshorttermretentionpolicy_facts
version_added: "2.8"
short_description: Get Azure Backup Short Term Retention Policy facts.
description:
    - Get facts of Azure Backup Short Term Retention Policy.

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
    policy_name:
        description:
            - "The policy name. Should always be 'default'."

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Backup Short Term Retention Policy
    azure_rm_sqlbackupshorttermretentionpolicy_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name
      policy_name: policy_name

  - name: List instances of Backup Short Term Retention Policy
    azure_rm_sqlbackupshorttermretentionpolicy_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name
'''

RETURN = '''
backup_short_term_retention_policies:
    description: A list of dictionaries containing facts for Backup Short Term Retention Policy.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default-SQL-SouthEastAsia/providers/Microsoft.Sql/servers/testsvr/dat
                    abases/testdb/backupShortTermRetentionPolicies/default"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: default
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupShortTermRetentionPoliciesFacts(AzureRMModuleBase):
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
            policy_name=dict(
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
        self.policy_name = None
        super(AzureRMBackupShortTermRetentionPoliciesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.policy_name is not None:
            self.results['backup_short_term_retention_policies'] = self.get()
        else:
            self.results['backup_short_term_retention_policies'] = self.list_by_database()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.backup_short_term_retention_policies.get(resource_group_name=self.resource_group,
                                                                                 server_name=self.server_name,
                                                                                 database_name=self.database_name,
                                                                                 policy_name=self.policy_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for BackupShortTermRetentionPolicies.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_database(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.backup_short_term_retention_policies.list_by_database(resource_group_name=self.resource_group,
                                                                                              server_name=self.server_name,
                                                                                              database_name=self.database_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for BackupShortTermRetentionPolicies.')

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
    AzureRMBackupShortTermRetentionPoliciesFacts()


if __name__ == '__main__':
    main()

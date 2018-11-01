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
module: azure_rm_sqldatabaseautomatictuning_facts
version_added: "2.8"
short_description: Get Azure Database Automatic Tuning facts.
description:
    - Get facts of Azure Database Automatic Tuning.

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

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Database Automatic Tuning
    azure_rm_sqldatabaseautomatictuning_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name
'''

RETURN = '''
database_automatic_tuning:
    description: A list of dictionaries containing facts for Database Automatic Tuning.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/c3aa9078-0000-0000-0000-e36f151182d7/resourceGroups/default-sql-onebox/providers/Microsoft.Sql/servers/testsvr11/database
                    s/db1/automaticTuning/current"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: current
        options:
            description:
                - Automatic tuning options definition.
            returned: always
            type: complex
            sample: "{\n  'forceLastGoodPlan': {\n    'desiredState': 'Default',\n    'actualState': 'On',\n    'reasonCode': '2',\n    'reasonDesc':
                     'AutoConfigured'\n  },\n  'createIndex': {\n    'desiredState': 'Default',\n    'actualState': 'On',\n    'reasonCode': '2',\n
                     'reasonDesc': 'AutoConfigured'\n  },\n  'dropIndex': {\n    'desiredState': 'Default',\n    'actualState': 'Off',\n    'reasonCode':
                     '2',\n    'reasonDesc': 'AutoConfigured'\n  },\n  'maintainIndex': {\n    'desiredState': 'Default',\n    'actualState': 'Off',\n
                     'reasonCode': '2',\n    'reasonDesc': 'AutoConfigured'\n  }\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDatabaseAutomaticTuningFacts(AzureRMModuleBase):
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
        super(AzureRMDatabaseAutomaticTuningFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['database_automatic_tuning'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.database_automatic_tuning.get(resource_group_name=self.resource_group,
                                                                      server_name=self.server_name,
                                                                      database_name=self.database_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DatabaseAutomaticTuning.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'options': d.get('options', None)
        }
        return d


def main():
    AzureRMDatabaseAutomaticTuningFacts()


if __name__ == '__main__':
    main()

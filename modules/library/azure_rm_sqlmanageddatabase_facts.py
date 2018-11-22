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
module: azure_rm_sqlmanageddatabase_facts
version_added: "2.8"
short_description: Get Azure Managed Database facts.
description:
    - Get facts of Azure Managed Database.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    managed_instance_name:
        description:
            - The name of the managed instance.
        required: True
    name:
        description:
            - The name of the database.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Managed Database
    azure_rm_sqlmanageddatabase_facts:
      resource_group: resource_group_name
      managed_instance_name: managed_instance_name
      name: database_name

  - name: List instances of Managed Database
    azure_rm_sqlmanageddatabase_facts:
      resource_group: resource_group_name
      managed_instance_name: managed_instance_name
'''

RETURN = '''
managed_databases:
    description: A list of dictionaries containing facts for Managed Database.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/testrg/providers/Microsoft.Sql/managedInstances/testcl/databases/testdb1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: testdb1
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: southeastasia
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        collation:
            description:
                - Collation of the managed database.
            returned: always
            type: str
            sample: SQL_Latin1_General_CP1_CI_AS
        status:
            description:
                - "Status for the database. Possible values include: 'Online', 'Offline', 'Shutdown', 'Creating', 'Inaccessible'"
            returned: always
            type: str
            sample: Online
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagedDatabaseFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            managed_instance_name=dict(
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
        self.managed_instance_name = None
        self.name = None
        self.tags = None
        super(AzureRMManagedDatabaseFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['managed_databases'] = self.get()
        else:
            self.results['managed_databases'] = self.list_by_instance()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managed_databases.get(resource_group_name=self.resource_group,
                                                              managed_instance_name=self.managed_instance_name,
                                                              database_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Managed Database.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_instance(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managed_databases.list_by_instance(resource_group_name=self.resource_group,
                                                                           managed_instance_name=self.managed_instance_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Managed Database.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'collation': d.get('collation', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMManagedDatabaseFacts()


if __name__ == '__main__':
    main()

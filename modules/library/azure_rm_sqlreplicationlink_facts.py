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
module: azure_rm_sqlreplicationlink_facts
version_added: "2.8"
short_description: Get Azure Replication Link facts.
description:
    - Get facts of Azure Replication Link.

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
            - The name of the database to get the link for.
        required: True
    link_id:
        description:
            - The replication link ID to be retrieved.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Replication Link
    azure_rm_sqlreplicationlink_facts:
      resource_group: resource_group_name
      server_name: server_name
      name: database_name
      link_id: link_id

  - name: List instances of Replication Link
    azure_rm_sqlreplicationlink_facts:
      resource_group: resource_group_name
      server_name: server_name
      name: database_name
'''

RETURN = '''
replication_links:
    description: A list of dictionaries containing facts for Replication Link.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-8931/providers/Microsoft.Sql/servers/sqlcrudtest-2137/dat
                    abases/testdb/replicationLinks/f0550bf5-07ce-4270-8e4b-71737975973a"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: f0550bf5-07ce-4270-8e4b-71737975973a
        location:
            description:
                - Location of the server that contains this firewall rule.
            returned: always
            type: str
            sample: Japan East
        role:
            description:
                - "The role of the database in the replication link. Possible values include: 'Primary', 'Secondary', 'NonReadableSecondary', 'Source',
                   'Copy'"
            returned: always
            type: str
            sample: Secondary
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMReplicationLinkFacts(AzureRMModuleBase):
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
                type='str',
                required=True
            ),
            link_id=dict(
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
        self.link_id = None
        super(AzureRMReplicationLinkFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.link_id is not None:
            self.results['replication_links'] = self.get()
        else:
            self.results['replication_links'] = self.list_by_database()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.replication_links.get(resource_group_name=self.resource_group,
                                                              server_name=self.server_name,
                                                              database_name=self.name,
                                                              link_id=self.link_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Replication Link.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_database(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.replication_links.list_by_database(resource_group_name=self.resource_group,
                                                                           server_name=self.server_name,
                                                                           database_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Replication Link.')

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
            'location': d.get('location', None),
            'role': d.get('role', None)
        }
        return d


def main():
    AzureRMReplicationLinkFacts()


if __name__ == '__main__':
    main()

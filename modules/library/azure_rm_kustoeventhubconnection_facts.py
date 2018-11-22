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
module: azure_rm_kustoeventhubconnection_facts
version_added: "2.8"
short_description: Get Azure Event Hub Connection facts.
description:
    - Get facts of Azure Event Hub Connection.

options:
    resource_group:
        description:
            - The name of the resource group containing the Kusto cluster.
        required: True
    cluster_name:
        description:
            - The name of the Kusto cluster.
        required: True
    database_name:
        description:
            - The name of the database in the Kusto cluster.
        required: True
    name:
        description:
            - The name of the event hub connection.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Event Hub Connection
    azure_rm_kustoeventhubconnection_facts:
      resource_group: resource_group_name
      cluster_name: cluster_name
      database_name: database_name
      name: event_hub_connection_name

  - name: List instances of Event Hub Connection
    azure_rm_kustoeventhubconnection_facts:
      resource_group: resource_group_name
      cluster_name: cluster_name
      database_name: database_name
'''

RETURN = '''
event_hub_connections:
    description: A list of dictionaries containing facts for Event Hub Connection.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/12345678-1234-1234-1234-123456789098/resourceGroups/kustorptest/providers/Microsoft.Kusto/Clusters/KustoClusterRPTest4/Da
                    tabases/KustoDatabase8"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: KustoClusterRPTest4/KustoDatabase8
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: westus
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.kusto import KustoManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEventHubConnectionFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
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
        self.cluster_name = None
        self.database_name = None
        self.name = None
        super(AzureRMEventHubConnectionFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(KustoManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['event_hub_connections'] = self.get()
        else:
            self.results['event_hub_connections'] = self.list_by_database()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_hub_connections.get(resource_group_name=self.resource_group,
                                                                  cluster_name=self.cluster_name,
                                                                  database_name=self.database_name,
                                                                  event_hub_connection_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Event Hub Connection.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_database(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.event_hub_connections.list_by_database(resource_group_name=self.resource_group,
                                                                               cluster_name=self.cluster_name,
                                                                               database_name=self.database_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Event Hub Connection.')

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
    AzureRMEventHubConnectionFacts()


if __name__ == '__main__':
    main()

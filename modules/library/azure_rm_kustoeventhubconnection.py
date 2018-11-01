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
module: azure_rm_kustoeventhubconnection
version_added: "2.8"
short_description: Manage Event Hub Connection instance.
description:
    - Create, update and delete instance of Event Hub Connection.

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
    event_hub_connection_name:
        description:
            - The name of the event hub connection.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    event_hub_resource_id:
        description:
            - The resource ID of the event hub to be used to create a data connection.
        required: True
    consumer_group:
        description:
            - The event hub consumer group.
        required: True
    table_name:
        description:
            - The table where the data should be ingested. Optionally the table information can be added to each message.
    mapping_rule_name:
        description:
            - The mapping rule to be used to ingest the data. Optionally the mapping information can be added to each message.
    data_format:
        description:
            - The data format of the message. Optionally the data format can be added to each message.
        choices:
            - 'multijson'
            - 'json'
            - 'csv'
    state:
      description:
        - Assert the state of the Event Hub Connection.
        - Use 'present' to create or update an Event Hub Connection and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Event Hub Connection
    azure_rm_kustoeventhubconnection:
      resource_group: kustorptest
      cluster_name: KustoClusterRPTest4
      database_name: KustoDatabase8
      event_hub_connection_name: kustoeventhubconnection1
      location: eastus
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/12345678-1234-1234-1234-123456789098/resourceGroups/kustorptest/providers/Microsoft.Kusto/Clusters/KustoClusterRPTest4/Databases/
            KustoDatabase8"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.kusto import KustoManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMEventHubConnections(AzureRMModuleBase):
    """Configuration class for an Azure RM Event Hub Connection resource"""

    def __init__(self):
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
            event_hub_connection_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            event_hub_resource_id=dict(
                type='str',
                required=True
            ),
            consumer_group=dict(
                type='str',
                required=True
            ),
            table_name=dict(
                type='str'
            ),
            mapping_rule_name=dict(
                type='str'
            ),
            data_format=dict(
                type='str',
                choices=['multijson',
                         'json',
                         'csv']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.cluster_name = None
        self.database_name = None
        self.event_hub_connection_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEventHubConnections, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "event_hub_resource_id":
                    self.parameters["event_hub_resource_id"] = kwargs[key]
                elif key == "consumer_group":
                    self.parameters["consumer_group"] = kwargs[key]
                elif key == "table_name":
                    self.parameters["table_name"] = kwargs[key]
                elif key == "mapping_rule_name":
                    self.parameters["mapping_rule_name"] = kwargs[key]
                elif key == "data_format":
                    ev = kwargs[key]
                    if ev == 'multijson':
                        ev = 'MULTIJSON'
                    elif ev == 'json':
                        ev = 'JSON'
                    elif ev == 'csv':
                        ev = 'CSV'
                    self.parameters["data_format"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(KustoManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_eventhubconnection()

        if not old_response:
            self.log("Event Hub Connection instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Event Hub Connection instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Event Hub Connection instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Event Hub Connection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_eventhubconnection()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Event Hub Connection instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_eventhubconnection()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_eventhubconnection():
                time.sleep(20)
        else:
            self.log("Event Hub Connection instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_eventhubconnection(self):
        '''
        Creates or updates Event Hub Connection with the specified configuration.

        :return: deserialized Event Hub Connection instance state dictionary
        '''
        self.log("Creating / Updating the Event Hub Connection instance {0}".format(self.event_hub_connection_name))

        try:
            response = self.mgmt_client.event_hub_connections.create_or_update(resource_group_name=self.resource_group,
                                                                               cluster_name=self.cluster_name,
                                                                               database_name=self.database_name,
                                                                               event_hub_connection_name=self.event_hub_connection_name,
                                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Event Hub Connection instance.')
            self.fail("Error creating the Event Hub Connection instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_eventhubconnection(self):
        '''
        Deletes specified Event Hub Connection instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Event Hub Connection instance {0}".format(self.event_hub_connection_name))
        try:
            response = self.mgmt_client.event_hub_connections.delete(resource_group_name=self.resource_group,
                                                                     cluster_name=self.cluster_name,
                                                                     database_name=self.database_name,
                                                                     event_hub_connection_name=self.event_hub_connection_name)
        except CloudError as e:
            self.log('Error attempting to delete the Event Hub Connection instance.')
            self.fail("Error deleting the Event Hub Connection instance: {0}".format(str(e)))

        return True

    def get_eventhubconnection(self):
        '''
        Gets the properties of the specified Event Hub Connection.

        :return: deserialized Event Hub Connection instance state dictionary
        '''
        self.log("Checking if the Event Hub Connection instance {0} is present".format(self.event_hub_connection_name))
        found = False
        try:
            response = self.mgmt_client.event_hub_connections.get(resource_group_name=self.resource_group,
                                                                  cluster_name=self.cluster_name,
                                                                  database_name=self.database_name,
                                                                  event_hub_connection_name=self.event_hub_connection_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Event Hub Connection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Event Hub Connection instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMEventHubConnections()


if __name__ == '__main__':
    main()

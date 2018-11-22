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
short_description: Manage Azure Event Hub Connection instance.
description:
    - Create, update and delete instance of Azure Event Hub Connection.

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
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    event_hub_resource_id:
        description:
            - The resource ID of the event hub to be used to create a data connection.
            - Required when C(state) is I(present).
    consumer_group:
        description:
            - The event hub consumer group.
            - Required when C(state) is I(present).
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
      name: kustoeventhubconnection1
      location: eastus
      event_hub_resource_id: /subscriptions/12345678-1234-1234-1234-123456789098/resourceGroups/kustorptest/providers/Microsoft.EventHub/namespaces/eventhubTestns1/eventhubs/eventhubTest1
      consumer_group: testConsumerGroup1
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


class AzureRMEventHubConnection(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            event_hub_resource_id=dict(
                type='str'
            ),
            consumer_group=dict(
                type='str'
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEventHubConnection, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_upper(self.parameters, ['data_format'])

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Event Hub Connection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_eventhubconnection()

            self.results['changed'] = True
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
            self.results.update(self.format_response(response))
        return self.results

    def create_update_eventhubconnection(self):
        '''
        Creates or updates Event Hub Connection with the specified configuration.

        :return: deserialized Event Hub Connection instance state dictionary
        '''
        self.log("Creating / Updating the Event Hub Connection instance {0}".format(self.name))

        try:
            response = self.mgmt_client.event_hub_connections.create_or_update(resource_group_name=self.resource_group,
                                                                               cluster_name=self.cluster_name,
                                                                               database_name=self.database_name,
                                                                               event_hub_connection_name=self.name,
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
        self.log("Deleting the Event Hub Connection instance {0}".format(self.name))
        try:
            response = self.mgmt_client.event_hub_connections.delete(resource_group_name=self.resource_group,
                                                                     cluster_name=self.cluster_name,
                                                                     database_name=self.database_name,
                                                                     event_hub_connection_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Event Hub Connection instance.')
            self.fail("Error deleting the Event Hub Connection instance: {0}".format(str(e)))

        return True

    def get_eventhubconnection(self):
        '''
        Gets the properties of the specified Event Hub Connection.

        :return: deserialized Event Hub Connection instance state dictionary
        '''
        self.log("Checking if the Event Hub Connection instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.event_hub_connections.get(resource_group_name=self.resource_group,
                                                                  cluster_name=self.cluster_name,
                                                                  database_name=self.database_name,
                                                                  event_hub_connection_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Event Hub Connection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Event Hub Connection instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMEventHubConnection()


if __name__ == '__main__':
    main()

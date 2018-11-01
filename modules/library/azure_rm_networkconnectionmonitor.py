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
module: azure_rm_networkconnectionmonitor
version_added: "2.8"
short_description: Manage Connection Monitor instance.
description:
    - Create, update and delete instance of Connection Monitor.

options:
    resource_group:
        description:
            - The name of the resource group containing Network Watcher.
        required: True
    network_watcher_name:
        description:
            - The name of the Network Watcher resource.
        required: True
    connection_monitor_name:
        description:
            - The name of the connection monitor.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    source:
        description:
        required: True
        suboptions:
            resource_id:
                description:
                    - The ID of the resource used as the source by connection monitor.
                required: True
            port:
                description:
                    - The source port used by connection monitor.
    destination:
        description:
        required: True
        suboptions:
            resource_id:
                description:
                    - The ID of the resource used as the destination by connection monitor.
            address:
                description:
                    - Address of the connection monitor destination (IP or domain name).
            port:
                description:
                    - The destination port used by connection monitor.
    auto_start:
        description:
            - Determines if the connection monitor will start automatically once created.
    monitoring_interval_in_seconds:
        description:
            - Monitoring interval in seconds.
    state:
      description:
        - Assert the state of the Connection Monitor.
        - Use 'present' to create or update an Connection Monitor and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Connection Monitor
    azure_rm_networkconnectionmonitor:
      resource_group: NOT FOUND
      network_watcher_name: NOT FOUND
      connection_monitor_name: NOT FOUND
      location: eastus
'''

RETURN = '''
id:
    description:
        - ID of the connection monitor.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMConnectionMonitors(AzureRMModuleBase):
    """Configuration class for an Azure RM Connection Monitor resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            network_watcher_name=dict(
                type='str',
                required=True
            ),
            connection_monitor_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            source=dict(
                type='dict',
                required=True
            ),
            destination=dict(
                type='dict',
                required=True
            ),
            auto_start=dict(
                type='str'
            ),
            monitoring_interval_in_seconds=dict(
                type='int'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.network_watcher_name = None
        self.connection_monitor_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConnectionMonitors, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "source":
                    self.parameters["source"] = kwargs[key]
                elif key == "destination":
                    self.parameters["destination"] = kwargs[key]
                elif key == "auto_start":
                    self.parameters["auto_start"] = kwargs[key]
                elif key == "monitoring_interval_in_seconds":
                    self.parameters["monitoring_interval_in_seconds"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_connectionmonitor()

        if not old_response:
            self.log("Connection Monitor instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Connection Monitor instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Connection Monitor instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Connection Monitor instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_connectionmonitor()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Connection Monitor instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_connectionmonitor()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_connectionmonitor():
                time.sleep(20)
        else:
            self.log("Connection Monitor instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_connectionmonitor(self):
        '''
        Creates or updates Connection Monitor with the specified configuration.

        :return: deserialized Connection Monitor instance state dictionary
        '''
        self.log("Creating / Updating the Connection Monitor instance {0}".format(self.connection_monitor_name))

        try:
            response = self.mgmt_client.connection_monitors.create_or_update(resource_group_name=self.resource_group,
                                                                             network_watcher_name=self.network_watcher_name,
                                                                             connection_monitor_name=self.connection_monitor_name,
                                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Connection Monitor instance.')
            self.fail("Error creating the Connection Monitor instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_connectionmonitor(self):
        '''
        Deletes specified Connection Monitor instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Connection Monitor instance {0}".format(self.connection_monitor_name))
        try:
            response = self.mgmt_client.connection_monitors.delete(resource_group_name=self.resource_group,
                                                                   network_watcher_name=self.network_watcher_name,
                                                                   connection_monitor_name=self.connection_monitor_name)
        except CloudError as e:
            self.log('Error attempting to delete the Connection Monitor instance.')
            self.fail("Error deleting the Connection Monitor instance: {0}".format(str(e)))

        return True

    def get_connectionmonitor(self):
        '''
        Gets the properties of the specified Connection Monitor.

        :return: deserialized Connection Monitor instance state dictionary
        '''
        self.log("Checking if the Connection Monitor instance {0} is present".format(self.connection_monitor_name))
        found = False
        try:
            response = self.mgmt_client.connection_monitors.get(resource_group_name=self.resource_group,
                                                                network_watcher_name=self.network_watcher_name,
                                                                connection_monitor_name=self.connection_monitor_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Connection Monitor instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Connection Monitor instance.')
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
    AzureRMConnectionMonitors()


if __name__ == '__main__':
    main()

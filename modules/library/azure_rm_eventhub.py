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
module: azure_rm_eventhub
version_added: "2.8"
short_description: Manage Event Hub instance.
description:
    - Create, update and delete instance of Event Hub.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    namespace_name:
        description:
            - The Namespace name
        required: True
    event_hub_name:
        description:
            - The Event Hub name
        required: True
    message_retention_in_days:
        description:
            - Number of days to retain the events for this Event Hub, value should be 1 to 7 days
    partition_count:
        description:
            - Number of partitions created for the Event Hub, allowed values are from 1 to 32 partitions.
    status:
        description:
            - Enumerates the possible values for the status of the Event Hub.
        choices:
            - 'active'
            - 'disabled'
            - 'restoring'
            - 'send_disabled'
            - 'receive_disabled'
            - 'creating'
            - 'deleting'
            - 'renaming'
            - 'unknown'
    capture_description:
        description:
            - Properties of capture description
        suboptions:
            enabled:
                description:
                    - A value that indicates whether capture description is enabled.
            encoding:
                description:
                    - "Enumerates the possible values for the encoding format of capture description. Note: 'C(avro_deflate)' will be deprecated in New API
                       Version."
                choices:
                    - 'avro'
                    - 'avro_deflate'
            interval_in_seconds:
                description:
                    - The time window allows you to set the frequency with which the capture to Azure Blobs will happen, value should between 60 to 900 seconds
            size_limit_in_bytes:
                description:
                    - "The size window defines the amount of data built up in your Event Hub before an capture operation, value should be between 10485760
                       to 524288000 bytes"
            destination:
                description:
                    - Properties of Destination where capture will be stored. (Storage Account, Blob Names)
                suboptions:
                    name:
                        description:
                            - Name for capture destination
                    storage_account_resource_id:
                        description:
                            - Resource id of the storage account to be used to create the blobs
                    blob_container:
                        description:
                            - Blob container Name
                    archive_name_format:
                        description:
                            - "Blob naming convention for archive, e.g. {Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}.
                               Here all the parameters (Namespace,EventHub .. etc) are mandatory irrespective of order"
    state:
      description:
        - Assert the state of the Event Hub.
        - Use 'present' to create or update an Event Hub and 'absent' to delete it.
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
  - name: Create (or update) Event Hub
    azure_rm_eventhub:
      resource_group: Default-NotificationHubs-AustraliaEast
      namespace_name: sdk-Namespace-5357
      event_hub_name: sdk-EventHub-6547
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/e2f361f0-3b27-4503-a9cc-21cfba380093/resourceGroups/Default-NotificationHubs-AustraliaEast/providers/Microsoft.EventHub/namespace
            s/sdk-Namespace-716/eventhubs/sdk-EventHub-10"
status:
    description:
        - "Enumerates the possible values for the status of the Event Hub. Possible values include: 'Active', 'Disabled', 'Restoring', 'SendDisabled',
           'ReceiveDisabled', 'Creating', 'Deleting', 'Renaming', 'Unknown'"
    returned: always
    type: str
    sample: Active
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.eventhub import EventHubManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMEventHubs(AzureRMModuleBase):
    """Configuration class for an Azure RM Event Hub resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            namespace_name=dict(
                type='str',
                required=True
            ),
            event_hub_name=dict(
                type='str',
                required=True
            ),
            message_retention_in_days=dict(
                type='int'
            ),
            partition_count=dict(
                type='int'
            ),
            status=dict(
                type='str',
                choices=['active',
                         'disabled',
                         'restoring',
                         'send_disabled',
                         'receive_disabled',
                         'creating',
                         'deleting',
                         'renaming',
                         'unknown']
            ),
            capture_description=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.namespace_name = None
        self.event_hub_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEventHubs, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "message_retention_in_days":
                    self.parameters["message_retention_in_days"] = kwargs[key]
                elif key == "partition_count":
                    self.parameters["partition_count"] = kwargs[key]
                elif key == "status":
                    self.parameters["status"] = _snake_to_camel(kwargs[key], True)
                elif key == "capture_description":
                    ev = kwargs[key]
                    if 'encoding' in ev:
                        if ev['encoding'] == 'avro':
                            ev['encoding'] = 'Avro'
                        elif ev['encoding'] == 'avro_deflate':
                            ev['encoding'] = 'AvroDeflate'
                    self.parameters["capture_description"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_eventhub()

        if not old_response:
            self.log("Event Hub instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Event Hub instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Event Hub instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Event Hub instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_eventhub()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Event Hub instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_eventhub()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_eventhub():
                time.sleep(20)
        else:
            self.log("Event Hub instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_eventhub(self):
        '''
        Creates or updates Event Hub with the specified configuration.

        :return: deserialized Event Hub instance state dictionary
        '''
        self.log("Creating / Updating the Event Hub instance {0}".format(self.event_hub_name))

        try:
            response = self.mgmt_client.event_hubs.create_or_update(resource_group_name=self.resource_group,
                                                                    namespace_name=self.namespace_name,
                                                                    event_hub_name=self.event_hub_name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Event Hub instance.')
            self.fail("Error creating the Event Hub instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_eventhub(self):
        '''
        Deletes specified Event Hub instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Event Hub instance {0}".format(self.event_hub_name))
        try:
            response = self.mgmt_client.event_hubs.delete(resource_group_name=self.resource_group,
                                                          namespace_name=self.namespace_name,
                                                          event_hub_name=self.event_hub_name)
        except CloudError as e:
            self.log('Error attempting to delete the Event Hub instance.')
            self.fail("Error deleting the Event Hub instance: {0}".format(str(e)))

        return True

    def get_eventhub(self):
        '''
        Gets the properties of the specified Event Hub.

        :return: deserialized Event Hub instance state dictionary
        '''
        self.log("Checking if the Event Hub instance {0} is present".format(self.event_hub_name))
        found = False
        try:
            response = self.mgmt_client.event_hubs.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.namespace_name,
                                                       event_hub_name=self.event_hub_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Event Hub instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Event Hub instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMEventHubs()


if __name__ == '__main__':
    main()
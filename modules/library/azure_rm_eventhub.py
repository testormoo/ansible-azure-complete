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
short_description: Manage Azure Event Hub instance.
description:
    - Create, update and delete instance of Azure Event Hub.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    namespace_name:
        description:
            - The Namespace name
        required: True
    name:
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
      name: sdk-EventHub-6547
      message_retention_in_days: 4
      partition_count: 4
      status: Active
      capture_description:
        enabled: True
        encoding: Avro
        interval_in_seconds: 120
        size_limit_in_bytes: 10485763
        destination:
          name: EventHubArchive.AzureBlockBlob
          storage_account_resource_id: /subscriptions/e2f361f0-3b27-4503-a9cc-21cfba380093/resourceGroups/Default-Storage-SouthCentralUS/providers/Microsoft.ClassicStorage/storageAccounts/arjunteststorage
          blob_container: container
          archive_name_format: {Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMEventHub(AzureRMModuleBase):
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
            name=dict(
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
                options=dict(
                    enabled=dict(
                        type='str'
                    ),
                    encoding=dict(
                        type='str',
                        choices=['avro',
                                 'avro_deflate']
                    ),
                    interval_in_seconds=dict(
                        type='int'
                    ),
                    size_limit_in_bytes=dict(
                        type='int'
                    ),
                    destination=dict(
                        type='dict'
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            storage_account_resource_id=dict(
                                type='str'
                            ),
                            blob_container=dict(
                                type='str'
                            ),
                            archive_name_format=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.namespace_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEventHub, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['status'], True)
        dict_camelize(self.parameters, ['capture_description', 'encoding'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Event Hub instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_eventhub()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Event Hub instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_eventhub()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Event Hub instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': response.get('status', None)
                })
        return self.results

    def create_update_eventhub(self):
        '''
        Creates or updates Event Hub with the specified configuration.

        :return: deserialized Event Hub instance state dictionary
        '''
        self.log("Creating / Updating the Event Hub instance {0}".format(self.name))

        try:
            response = self.mgmt_client.event_hubs.create_or_update(resource_group_name=self.resource_group,
                                                                    namespace_name=self.namespace_name,
                                                                    event_hub_name=self.name,
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
        self.log("Deleting the Event Hub instance {0}".format(self.name))
        try:
            response = self.mgmt_client.event_hubs.delete(resource_group_name=self.resource_group,
                                                          namespace_name=self.namespace_name,
                                                          event_hub_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Event Hub instance.')
            self.fail("Error deleting the Event Hub instance: {0}".format(str(e)))

        return True

    def get_eventhub(self):
        '''
        Gets the properties of the specified Event Hub.

        :return: deserialized Event Hub instance state dictionary
        '''
        self.log("Checking if the Event Hub instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.event_hubs.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.namespace_name,
                                                       event_hub_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Event Hub instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Event Hub instance.')
        if found is True:
            return response.as_dict()

        return False


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


def main():
    """Main execution"""
    AzureRMEventHub()


if __name__ == '__main__':
    main()

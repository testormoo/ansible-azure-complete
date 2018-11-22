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
module: azure_rm_servicebusqueue
version_added: "2.8"
short_description: Manage Azure Queue instance.
description:
    - Create, update and delete instance of Azure Queue.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    namespace_name:
        description:
            - The namespace name
        required: True
    name:
        description:
            - The queue name.
        required: True
    lock_duration:
        description:
            - "ISO 8601 timespan duration of a peek-lock; that is, the amount of time that the message is locked for other receivers. The maximum value for
               LockDuration is 5 minutes; the default value is 1 minute."
    max_size_in_megabytes:
        description:
            - The maximum size of the queue in megabytes, which is the size of memory allocated for the queue. Default is 1024.
    requires_duplicate_detection:
        description:
            - A value indicating if this queue requires duplicate detection.
    requires_session:
        description:
            - A value that indicates whether the queue supports the concept of sessions.
    default_message_time_to_live:
        description:
            - "ISO 8601 default message timespan to live value. This is the duration after which the message expires, starting from when the message is sent
               to Service Bus. This is the default value used when TimeToLive is not set on a message itself."
    dead_lettering_on_message_expiration:
        description:
            - A value that indicates whether this queue has dead letter support when a message expires.
    duplicate_detection_history_time_window:
        description:
            - ISO 8601 timeSpan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
    max_delivery_count:
        description:
            - The maximum delivery count. A message is automatically deadlettered after this number of deliveries. default value is 10.
    status:
        description:
            - Enumerates the possible values for the status of a messaging entity.
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
    enable_batched_operations:
        description:
            - Value that indicates whether server-side batched operations are enabled.
    auto_delete_on_idle:
        description:
            - ISO 8061 timeSpan idle interval after which the queue is automatically deleted. The minimum duration is 5 minutes.
    enable_partitioning:
        description:
            - A value that indicates whether the queue is to be partitioned across multiple message brokers.
    enable_express:
        description:
            - "A value that indicates whether Express Entities are enabled. An express queue holds a message in memory temporarily before writing it to
               persistent storage."
    forward_to:
        description:
            - Queue/Topic name to forward the messages
    forward_dead_lettered_messages_to:
        description:
            - Queue/Topic name to forward the Dead Letter message
    state:
      description:
        - Assert the state of the Queue.
        - Use 'present' to create or update an Queue and 'absent' to delete it.
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
  - name: Create (or update) Queue
    azure_rm_servicebusqueue:
      resource_group: ArunMonocle
      namespace_name: sdk-Namespace-3174
      name: sdk-Queues-5647
      enable_partitioning: True
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/5f750a97-50d9-4e36-8081-c9ee4c0210d4/resourceGroups/ArunMonocle/providers/Microsoft.ServiceBus/namespaces/sdk-Namespace-3174/queu
            es/sdk-Queues-5647"
status:
    description:
        - "Enumerates the possible values for the status of a messaging entity. Possible values include: 'Active', 'Disabled', 'Restoring', 'SendDisabled',
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
    from azure.mgmt.servicebus import ServiceBusManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMQueue(AzureRMModuleBase):
    """Configuration class for an Azure RM Queue resource"""

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
            lock_duration=dict(
                type='str'
            ),
            max_size_in_megabytes=dict(
                type='int'
            ),
            requires_duplicate_detection=dict(
                type='str'
            ),
            requires_session=dict(
                type='str'
            ),
            default_message_time_to_live=dict(
                type='str'
            ),
            dead_lettering_on_message_expiration=dict(
                type='str'
            ),
            duplicate_detection_history_time_window=dict(
                type='str'
            ),
            max_delivery_count=dict(
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
            enable_batched_operations=dict(
                type='str'
            ),
            auto_delete_on_idle=dict(
                type='str'
            ),
            enable_partitioning=dict(
                type='str'
            ),
            enable_express=dict(
                type='str'
            ),
            forward_to=dict(
                type='str'
            ),
            forward_dead_lettered_messages_to=dict(
                type='str'
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

        super(AzureRMQueue, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceBusManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_queue()

        if not old_response:
            self.log("Queue instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Queue instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Queue instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_queue()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Queue instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_queue()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_queue():
                time.sleep(20)
        else:
            self.log("Queue instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_queue(self):
        '''
        Creates or updates Queue with the specified configuration.

        :return: deserialized Queue instance state dictionary
        '''
        self.log("Creating / Updating the Queue instance {0}".format(self.name))

        try:
            response = self.mgmt_client.queues.create_or_update(resource_group_name=self.resource_group,
                                                                namespace_name=self.namespace_name,
                                                                queue_name=self.name,
                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Queue instance.')
            self.fail("Error creating the Queue instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_queue(self):
        '''
        Deletes specified Queue instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Queue instance {0}".format(self.name))
        try:
            response = self.mgmt_client.queues.delete(resource_group_name=self.resource_group,
                                                      namespace_name=self.namespace_name,
                                                      queue_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Queue instance.')
            self.fail("Error deleting the Queue instance: {0}".format(str(e)))

        return True

    def get_queue(self):
        '''
        Gets the properties of the specified Queue.

        :return: deserialized Queue instance state dictionary
        '''
        self.log("Checking if the Queue instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.queues.get(resource_group_name=self.resource_group,
                                                   namespace_name=self.namespace_name,
                                                   queue_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Queue instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Queue instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
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
    AzureRMQueue()


if __name__ == '__main__':
    main()

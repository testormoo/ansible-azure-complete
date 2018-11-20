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
module: azure_rm_servicebussubscription
version_added: "2.8"
short_description: Manage Subscription instance.
description:
    - Create, update and delete instance of Subscription.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    namespace_name:
        description:
            - The namespace name
        required: True
    topic_name:
        description:
            - The topic name.
        required: True
    name:
        description:
            - The subscription name.
        required: True
    lock_duration:
        description:
            - ISO 8061 lock duration timespan for the subscription. The default value is 1 minute.
    requires_session:
        description:
            - Value indicating if a subscription supports the concept of sessions.
    default_message_time_to_live:
        description:
            - "ISO 8061 Default message timespan to live value. This is the duration after which the message expires, starting from when the message is sent
               to Service Bus. This is the default value used when TimeToLive is not set on a message itself."
    dead_lettering_on_filter_evaluation_exceptions:
        description:
            - Value that indicates whether a subscription has dead letter support on filter evaluation exceptions.
    dead_lettering_on_message_expiration:
        description:
            - Value that indicates whether a subscription has dead letter support when a message expires.
    duplicate_detection_history_time_window:
        description:
            - ISO 8601 timeSpan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
    max_delivery_count:
        description:
            - Number of maximum deliveries.
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
            - ISO 8061 timeSpan idle interval after which the topic is automatically deleted. The minimum duration is 5 minutes.
    forward_to:
        description:
            - Queue/Topic name to forward the messages
    forward_dead_lettered_messages_to:
        description:
            - Queue/Topic name to forward the Dead Letter message
    state:
      description:
        - Assert the state of the Subscription.
        - Use 'present' to create or update an Subscription and 'absent' to delete it.
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
  - name: Create (or update) Subscription
    azure_rm_servicebussubscription:
      resource_group: ResourceGroup
      namespace_name: sdk-Namespace-1349
      topic_name: sdk-Topics-8740
      name: sdk-Subscriptions-2178
      enable_batched_operations: True
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/Subscriptionid/resourceGroups/ResourceGroup/providers/Microsoft.ServiceBus/namespaces/sdk-Namespace-1349/topics/sdk-Topics-8740/s
            ubscriptions/sdk-Subscriptions-2178"
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


class AzureRMSubscriptions(AzureRMModuleBase):
    """Configuration class for an Azure RM Subscription resource"""

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
            topic_name=dict(
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
            requires_session=dict(
                type='str'
            ),
            default_message_time_to_live=dict(
                type='str'
            ),
            dead_lettering_on_filter_evaluation_exceptions=dict(
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
        self.topic_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSubscriptions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "lock_duration":
                    self.parameters["lock_duration"] = kwargs[key]
                elif key == "requires_session":
                    self.parameters["requires_session"] = kwargs[key]
                elif key == "default_message_time_to_live":
                    self.parameters["default_message_time_to_live"] = kwargs[key]
                elif key == "dead_lettering_on_filter_evaluation_exceptions":
                    self.parameters["dead_lettering_on_filter_evaluation_exceptions"] = kwargs[key]
                elif key == "dead_lettering_on_message_expiration":
                    self.parameters["dead_lettering_on_message_expiration"] = kwargs[key]
                elif key == "duplicate_detection_history_time_window":
                    self.parameters["duplicate_detection_history_time_window"] = kwargs[key]
                elif key == "max_delivery_count":
                    self.parameters["max_delivery_count"] = kwargs[key]
                elif key == "status":
                    self.parameters["status"] = _snake_to_camel(kwargs[key], True)
                elif key == "enable_batched_operations":
                    self.parameters["enable_batched_operations"] = kwargs[key]
                elif key == "auto_delete_on_idle":
                    self.parameters["auto_delete_on_idle"] = kwargs[key]
                elif key == "forward_to":
                    self.parameters["forward_to"] = kwargs[key]
                elif key == "forward_dead_lettered_messages_to":
                    self.parameters["forward_dead_lettered_messages_to"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceBusManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_subscription()

        if not old_response:
            self.log("Subscription instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Subscription instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Subscription instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_subscription()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Subscription instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_subscription()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_subscription():
                time.sleep(20)
        else:
            self.log("Subscription instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_subscription(self):
        '''
        Creates or updates Subscription with the specified configuration.

        :return: deserialized Subscription instance state dictionary
        '''
        self.log("Creating / Updating the Subscription instance {0}".format(self.name))

        try:
            response = self.mgmt_client.subscriptions.create_or_update(resource_group_name=self.resource_group,
                                                                       namespace_name=self.namespace_name,
                                                                       topic_name=self.topic_name,
                                                                       subscription_name=self.name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Subscription instance.')
            self.fail("Error creating the Subscription instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_subscription(self):
        '''
        Deletes specified Subscription instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Subscription instance {0}".format(self.name))
        try:
            response = self.mgmt_client.subscriptions.delete(resource_group_name=self.resource_group,
                                                             namespace_name=self.namespace_name,
                                                             topic_name=self.topic_name,
                                                             subscription_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Subscription instance.')
            self.fail("Error deleting the Subscription instance: {0}".format(str(e)))

        return True

    def get_subscription(self):
        '''
        Gets the properties of the specified Subscription.

        :return: deserialized Subscription instance state dictionary
        '''
        self.log("Checking if the Subscription instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.subscriptions.get(resource_group_name=self.resource_group,
                                                          namespace_name=self.namespace_name,
                                                          topic_name=self.topic_name,
                                                          subscription_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Subscription instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Subscription instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMSubscriptions()


if __name__ == '__main__':
    main()

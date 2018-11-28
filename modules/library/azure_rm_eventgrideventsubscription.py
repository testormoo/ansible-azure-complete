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
module: azure_rm_eventgrideventsubscription
version_added: "2.8"
short_description: Manage Azure Event Subscription instance.
description:
    - Create, update and delete instance of Azure Event Subscription.

options:
    scope:
        description:
            - "The identifier of the resource to which the event subscription needs to be created or updated. The scope can be a subscription, or a resource
               group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use
               '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource
               group, and
               '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for
               a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an
               EventGrid topic."
        required: True
    name:
        description:
            - Name of the event subscription. Event subscription names must be between 3 and 64 characters in length and should use alphanumeric letters only.
        required: True
    destination:
        description:
            - Information about the destination where events have to be delivered for the event subscription.
        suboptions:
            endpoint_type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    filter:
        description:
            - Information about the filter for the event subscription.
        suboptions:
            subject_begins_with:
                description:
                    - "An optional string to filter events for an event subscription based on a resource path prefix.\n"
                    - "The format of this depends on the publisher of the events. \n"
                    - Wildcard characters are not supported in this path.
            subject_ends_with:
                description:
                    - "An optional string to filter events for an event subscription based on a resource path suffix.\n"
                    - Wildcard characters are not supported in this path.
            included_event_types:
                description:
                    - "A list of applicable event types that need to be part of the event subscription. \n"
                    - "If it is desired to subscribe to all event types, the string 'all' needs to be specified as an element in this list."
                type: list
            is_subject_case_sensitive:
                description:
                    - "Specifies if the I(subject_begins_with) and I(subject_ends_with) properties of the filter \n"
                    - should be compared in a case sensitive manner.
            advanced_filters:
                description:
                    - A list of advanced filters.
                type: list
                suboptions:
                    key:
                        description:
                            - The filter key. Represents an event property with upto two levels of nesting.
                    operator_type:
                        description:
                            - Constant filled by server.
                            - Required when C(state) is I(present).
    labels:
        description:
            - List of user defined labels.
        type: list
    expiration_time_utc:
        description:
            - Expiration time of the event subscription.
    event_delivery_schema:
        description:
            - The event delivery schema for the event subscription.
        choices:
            - 'event_grid_schema'
            - 'cloud_event_v01_schema'
            - 'custom_input_schema'
    retry_policy:
        description:
            - The retry policy for events. This can be used to configure maximum number of delivery attempts and time to live for events.
        suboptions:
            max_delivery_attempts:
                description:
                    - Maximum number of delivery retry attempts for events.
            event_time_to_live_in_minutes:
                description:
                    - Time To Live (in minutes) for events.
    dead_letter_destination:
        description:
            - The DeadLetter I(destination) of the event subscription.
        suboptions:
            endpoint_type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Event Subscription.
        - Use 'present' to create or update an Event Subscription and 'absent' to delete it.
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
  - name: Create (or update) Event Subscription
    azure_rm_eventgrideventsubscription:
      scope: subscriptions/5b4b650e-28b9-4790-b3ab-ddbd88d727c4
      name: examplesubscription3
      filter:
        is_subject_case_sensitive: False
'''

RETURN = '''
id:
    description:
        - Fully qualified identifier of the resource
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.eventgrid import EventGridManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMEventSubscription(AzureRMModuleBase):
    """Configuration class for an Azure RM Event Subscription resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            scope=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            destination=dict(
                type='dict',
                options=dict(
                    endpoint_type=dict(
                        type='str'
                    )
                )
            ),
            filter=dict(
                type='dict',
                options=dict(
                    subject_begins_with=dict(
                        type='str'
                    ),
                    subject_ends_with=dict(
                        type='str'
                    ),
                    included_event_types=dict(
                        type='list'
                    ),
                    is_subject_case_sensitive=dict(
                        type='str'
                    ),
                    advanced_filters=dict(
                        type='list',
                        options=dict(
                            key=dict(
                                type='str'
                            ),
                            operator_type=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            labels=dict(
                type='list'
            ),
            expiration_time_utc=dict(
                type='datetime'
            ),
            event_delivery_schema=dict(
                type='str',
                choices=['event_grid_schema',
                         'cloud_event_v01_schema',
                         'custom_input_schema']
            ),
            retry_policy=dict(
                type='dict',
                options=dict(
                    max_delivery_attempts=dict(
                        type='int'
                    ),
                    event_time_to_live_in_minutes=dict(
                        type='int'
                    )
                )
            ),
            dead_letter_destination=dict(
                type='dict',
                options=dict(
                    endpoint_type=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.scope = None
        self.name = None
        self.event_subscription_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEventSubscription, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.event_subscription_info[key] = kwargs[key]

        dict_camelize(self.event_subscription_info, ['event_delivery_schema'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_eventsubscription()

        if not old_response:
            self.log("Event Subscription instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Event Subscription instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.event_subscription_info, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Event Subscription instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_eventsubscription()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Event Subscription instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_eventsubscription()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Event Subscription instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_eventsubscription(self):
        '''
        Creates or updates Event Subscription with the specified configuration.

        :return: deserialized Event Subscription instance state dictionary
        '''
        self.log("Creating / Updating the Event Subscription instance {0}".format(self.name))

        try:
            response = self.mgmt_client.event_subscriptions.create_or_update(scope=self.scope,
                                                                             event_subscription_name=self.name,
                                                                             event_subscription_info=self.event_subscription_info)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Event Subscription instance.')
            self.fail("Error creating the Event Subscription instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_eventsubscription(self):
        '''
        Deletes specified Event Subscription instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Event Subscription instance {0}".format(self.name))
        try:
            response = self.mgmt_client.event_subscriptions.delete(scope=self.scope,
                                                                   event_subscription_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Event Subscription instance.')
            self.fail("Error deleting the Event Subscription instance: {0}".format(str(e)))

        return True

    def get_eventsubscription(self):
        '''
        Gets the properties of the specified Event Subscription.

        :return: deserialized Event Subscription instance state dictionary
        '''
        self.log("Checking if the Event Subscription instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.event_subscriptions.get(scope=self.scope,
                                                                event_subscription_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Event Subscription instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Event Subscription instance.')
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
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


def main():
    """Main execution"""
    AzureRMEventSubscription()


if __name__ == '__main__':
    main()

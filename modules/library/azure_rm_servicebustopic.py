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
module: azure_rm_servicebustopic
version_added: "2.8"
short_description: Manage Azure Topic instance.
description:
    - Create, update and delete instance of Azure Topic.

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
            - The topic name.
        required: True
    default_message_time_to_live:
        description:
            - "ISO 8601 Default message timespan to live value. This is the duration after which the message expires, starting from when the message is sent
               to Service Bus. This is the default value used when TimeToLive is not set on a message itself."
    max_size_in_megabytes:
        description:
            - Maximum size of the topic in megabytes, which is the size of the memory allocated for the topic. Default is 1024.
    requires_duplicate_detection:
        description:
            - Value indicating if this topic requires duplicate detection.
    duplicate_detection_history_time_window:
        description:
            - ISO8601 timespan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
    enable_batched_operations:
        description:
            - Value that indicates whether server-side batched operations are enabled.
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
    support_ordering:
        description:
            - Value that indicates whether the topic supports ordering.
    auto_delete_on_idle:
        description:
            - ISO 8601 timespan idle interval after which the topic is automatically deleted. The minimum duration is 5 minutes.
    enable_partitioning:
        description:
            - Value that indicates whether the topic to be partitioned across multiple message brokers is enabled.
    enable_express:
        description:
            - "Value that indicates whether Express Entities are enabled. An express topic holds a message in memory temporarily before writing it to
               persistent storage."
    state:
      description:
        - Assert the state of the Topic.
        - Use 'present' to create or update an Topic and 'absent' to delete it.
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
  - name: Create (or update) Topic
    azure_rm_servicebustopic:
      resource_group: ArunMonocle
      namespace_name: sdk-Namespace-1617
      name: sdk-Topics-5488
      enable_express: True
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/5f750a97-50d9-4e36-8081-c9ee4c0210d4/resourceGroups/ArunMonocle/providers/Microsoft.ServiceBus/namespaces/sdk-Namespace-1617/topi
            cs/sdk-Topics-5488"
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMTopic(AzureRMModuleBase):
    """Configuration class for an Azure RM Topic resource"""

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
            default_message_time_to_live=dict(
                type='str'
            ),
            max_size_in_megabytes=dict(
                type='int'
            ),
            requires_duplicate_detection=dict(
                type='str'
            ),
            duplicate_detection_history_time_window=dict(
                type='str'
            ),
            enable_batched_operations=dict(
                type='str'
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
            support_ordering=dict(
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

        super(AzureRMTopic, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_topic()

        if not old_response:
            self.log("Topic instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Topic instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Topic instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_topic()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Topic instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_topic()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Topic instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': response.get('status', None)
                })
        return self.results

    def create_update_topic(self):
        '''
        Creates or updates Topic with the specified configuration.

        :return: deserialized Topic instance state dictionary
        '''
        self.log("Creating / Updating the Topic instance {0}".format(self.name))

        try:
            response = self.mgmt_client.topics.create_or_update(resource_group_name=self.resource_group,
                                                                namespace_name=self.namespace_name,
                                                                topic_name=self.name,
                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Topic instance.')
            self.fail("Error creating the Topic instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_topic(self):
        '''
        Deletes specified Topic instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Topic instance {0}".format(self.name))
        try:
            response = self.mgmt_client.topics.delete(resource_group_name=self.resource_group,
                                                      namespace_name=self.namespace_name,
                                                      topic_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Topic instance.')
            self.fail("Error deleting the Topic instance: {0}".format(str(e)))

        return True

    def get_topic(self):
        '''
        Gets the properties of the specified Topic.

        :return: deserialized Topic instance state dictionary
        '''
        self.log("Checking if the Topic instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.topics.get(resource_group_name=self.resource_group,
                                                   namespace_name=self.namespace_name,
                                                   topic_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Topic instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Topic instance.')
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
    AzureRMTopic()


if __name__ == '__main__':
    main()

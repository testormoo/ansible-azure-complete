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
module: azure_rm_eventhubconsumergroup
version_added: "2.8"
short_description: Manage Consumer Group instance.
description:
    - Create, update and delete instance of Consumer Group.

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
    consumer_group_name:
        description:
            - The consumer group name
        required: True
    user_metadata:
        description:
            - "Usermetadata is a placeholder to store user-defined string data with maximum length 1024. e.g. it can be used to store descriptive data, such
               as list of teams and their contact information also user-defined configuration settings can be stored."
    state:
      description:
        - Assert the state of the Consumer Group.
        - Use 'present' to create or update an Consumer Group and 'absent' to delete it.
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
  - name: Create (or update) Consumer Group
    azure_rm_eventhubconsumergroup:
      resource_group: ArunMonocle
      namespace_name: sdk-Namespace-2661
      event_hub_name: sdk-EventHub-6681
      consumer_group_name: sdk-ConsumerGroup-5563
      user_metadata: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/5f750a97-50d9-4e36-8081-c9ee4c0210d4/resourceGroups/ArunMonocle/providers/Microsoft.EventHub/namespaces/sdk-Namespace-2661/eventh
            ubs/sdk-EventHub-6681/consumergroups/sdk-ConsumerGroup-5563"
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


class AzureRMConsumerGroups(AzureRMModuleBase):
    """Configuration class for an Azure RM Consumer Group resource"""

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
            consumer_group_name=dict(
                type='str',
                required=True
            ),
            user_metadata=dict(
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
        self.event_hub_name = None
        self.consumer_group_name = None
        self.user_metadata = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConsumerGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_consumergroup()

        if not old_response:
            self.log("Consumer Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Consumer Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Consumer Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Consumer Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_consumergroup()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Consumer Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_consumergroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_consumergroup():
                time.sleep(20)
        else:
            self.log("Consumer Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_consumergroup(self):
        '''
        Creates or updates Consumer Group with the specified configuration.

        :return: deserialized Consumer Group instance state dictionary
        '''
        self.log("Creating / Updating the Consumer Group instance {0}".format(self.consumer_group_name))

        try:
            response = self.mgmt_client.consumer_groups.create_or_update(resource_group_name=self.resource_group,
                                                                         namespace_name=self.namespace_name,
                                                                         event_hub_name=self.event_hub_name,
                                                                         consumer_group_name=self.consumer_group_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Consumer Group instance.')
            self.fail("Error creating the Consumer Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_consumergroup(self):
        '''
        Deletes specified Consumer Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Consumer Group instance {0}".format(self.consumer_group_name))
        try:
            response = self.mgmt_client.consumer_groups.delete(resource_group_name=self.resource_group,
                                                               namespace_name=self.namespace_name,
                                                               event_hub_name=self.event_hub_name,
                                                               consumer_group_name=self.consumer_group_name)
        except CloudError as e:
            self.log('Error attempting to delete the Consumer Group instance.')
            self.fail("Error deleting the Consumer Group instance: {0}".format(str(e)))

        return True

    def get_consumergroup(self):
        '''
        Gets the properties of the specified Consumer Group.

        :return: deserialized Consumer Group instance state dictionary
        '''
        self.log("Checking if the Consumer Group instance {0} is present".format(self.consumer_group_name))
        found = False
        try:
            response = self.mgmt_client.consumer_groups.get(resource_group_name=self.resource_group,
                                                            namespace_name=self.namespace_name,
                                                            event_hub_name=self.event_hub_name,
                                                            consumer_group_name=self.consumer_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Consumer Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Consumer Group instance.')
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
    AzureRMConsumerGroups()


if __name__ == '__main__':
    main()

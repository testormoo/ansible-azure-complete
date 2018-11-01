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
module: azure_rm_eventgridtopic
version_added: "2.8"
short_description: Manage Topic instance.
description:
    - Create, update and delete instance of Topic.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription."
        required: True
    topic_name:
        description:
            - Name of the topic
        required: True
    topic_info:
        description:
            - Topic information
        required: True
        suboptions:
            location:
                description:
                    - Location of the resource
                required: True
            input_schema:
                description:
                    - This determines the format that Event Grid should expect for incoming events published to the topic.
                choices:
                    - 'event_grid_schema'
                    - 'custom_event_schema'
                    - 'cloud_event_v01_schema'
            input_schema_mapping:
                description:
                    - "This enables publishing using custom event schemas. An InputSchemaMapping can be specified to map various properties of a source
                       schema to various required properties of the EventGridEvent schema."
                suboptions:
                    input_schema_mapping_type:
                        description:
                            - Constant filled by server.
                        required: True
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
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Topic
    azure_rm_eventgridtopic:
      resource_group: examplerg
      topic_name: exampletopic1
      topic_info:
        location: westus2
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


class AzureRMTopics(AzureRMModuleBase):
    """Configuration class for an Azure RM Topic resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            topic_name=dict(
                type='str',
                required=True
            ),
            topic_info=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.topic_name = None
        self.topic_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMTopics, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.topic_info["location"] = kwargs[key]
                elif key == "input_schema":
                    self.topic_info["input_schema"] = _snake_to_camel(kwargs[key], True)
                elif key == "input_schema_mapping":
                    self.topic_info["input_schema_mapping"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(EventGridManagementClient,
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
                self.log("Need to check if Topic instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Topic instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_topic()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Topic instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_topic()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_topic():
                time.sleep(20)
        else:
            self.log("Topic instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_topic(self):
        '''
        Creates or updates Topic with the specified configuration.

        :return: deserialized Topic instance state dictionary
        '''
        self.log("Creating / Updating the Topic instance {0}".format(self.topic_name))

        try:
            response = self.mgmt_client.topics.create_or_update(resource_group_name=self.resource_group,
                                                                topic_name=self.topic_name,
                                                                topic_info=self.topic_info)
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
        self.log("Deleting the Topic instance {0}".format(self.topic_name))
        try:
            response = self.mgmt_client.topics.delete(resource_group_name=self.resource_group,
                                                      topic_name=self.topic_name)
        except CloudError as e:
            self.log('Error attempting to delete the Topic instance.')
            self.fail("Error deleting the Topic instance: {0}".format(str(e)))

        return True

    def get_topic(self):
        '''
        Gets the properties of the specified Topic.

        :return: deserialized Topic instance state dictionary
        '''
        self.log("Checking if the Topic instance {0} is present".format(self.topic_name))
        found = False
        try:
            response = self.mgmt_client.topics.get(resource_group_name=self.resource_group,
                                                   topic_name=self.topic_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Topic instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Topic instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMTopics()


if __name__ == '__main__':
    main()
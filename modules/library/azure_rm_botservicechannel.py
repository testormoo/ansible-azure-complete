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
module: azure_rm_botservicechannel
version_added: "2.8"
short_description: Manage Channel instance.
description:
    - Create, update and delete instance of Channel.

options:
    resource_group:
        description:
            - The name of the C(bot) resource group in the user subscription.
        required: True
    resource_name:
        description:
            - The name of the C(bot) resource.
        required: True
    channel_name:
        description:
            - The name of the Channel resource.
        required: True
        choices:
            - 'facebook_channel'
            - 'email_channel'
            - 'kik_channel'
            - 'telegram_channel'
            - 'slack_channel'
            - 'ms_teams_channel'
            - 'skype_channel'
            - 'web_chat_channel'
            - 'direct_line_channel'
            - 'sms_channel'
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - Gets or sets the SKU of the resource.
        suboptions:
            name:
                description:
                    - The sku name.
                required: True
                choices:
                    - 'f0'
                    - 's1'
    kind:
        description:
            - Required. Gets or sets the Kind of the resource.
        choices:
            - 'sdk'
            - 'designer'
            - 'bot'
            - 'function'
    etag:
        description:
            - Entity Tag
    channel_name:
        description:
            - Constant filled by server.
        required: True
    state:
      description:
        - Assert the state of the Channel.
        - Use 'present' to create or update an Channel and 'absent' to delete it.
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
  - name: Create (or update) Channel
    azure_rm_botservicechannel:
      resource_group: OneResourceGroupName
      resource_name: samplebotname
      channel_name: EmailChannel
      location: eastus
'''

RETURN = '''
id:
    description:
        - Specifies the resource ID.
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
    from azure.mgmt.botservice import AzureBotService
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMChannels(AzureRMModuleBase):
    """Configuration class for an Azure RM Channel resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            channel_name=dict(
                type='str',
                choices=['facebook_channel',
                         'email_channel',
                         'kik_channel',
                         'telegram_channel',
                         'slack_channel',
                         'ms_teams_channel',
                         'skype_channel',
                         'web_chat_channel',
                         'direct_line_channel',
                         'sms_channel'],
                required=True
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            kind=dict(
                type='str',
                choices=['sdk',
                         'designer',
                         'bot',
                         'function']
            ),
            etag=dict(
                type='str'
            ),
            channel_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.resource_name = None
        self.channel_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMChannels, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'f0':
                            ev['name'] = 'F0'
                        elif ev['name'] == 's1':
                            ev['name'] = 'S1'
                    self.parameters["sku"] = ev
                elif key == "kind":
                    self.parameters["kind"] = kwargs[key]
                elif key == "etag":
                    self.parameters["etag"] = kwargs[key]
                elif key == "channel_name":
                    self.parameters.setdefault("properties", {})["channel_name"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureBotService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_channel()

        if not old_response:
            self.log("Channel instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Channel instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Channel instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Channel instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_channel()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Channel instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_channel()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_channel():
                time.sleep(20)
        else:
            self.log("Channel instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_channel(self):
        '''
        Creates or updates Channel with the specified configuration.

        :return: deserialized Channel instance state dictionary
        '''
        self.log("Creating / Updating the Channel instance {0}".format(self.channel_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.channels.create(resource_group_name=self.resource_group,
                                                            resource_name=self.resource_name,
                                                            channel_name=self.channel_name,
                                                            parameters=self.parameters)
            else:
                response = self.mgmt_client.channels.update(resource_group_name=self.resource_group,
                                                            resource_name=self.resource_name,
                                                            channel_name=self.channel_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Channel instance.')
            self.fail("Error creating the Channel instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_channel(self):
        '''
        Deletes specified Channel instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Channel instance {0}".format(self.channel_name))
        try:
            response = self.mgmt_client.channels.delete(resource_group_name=self.resource_group,
                                                        resource_name=self.resource_name,
                                                        channel_name=self.channel_name)
        except CloudError as e:
            self.log('Error attempting to delete the Channel instance.')
            self.fail("Error deleting the Channel instance: {0}".format(str(e)))

        return True

    def get_channel(self):
        '''
        Gets the properties of the specified Channel.

        :return: deserialized Channel instance state dictionary
        '''
        self.log("Checking if the Channel instance {0} is present".format(self.channel_name))
        found = False
        try:
            response = self.mgmt_client.channels.get(resource_group_name=self.resource_group,
                                                     resource_name=self.resource_name,
                                                     channel_name=self.channel_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Channel instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Channel instance.')
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
    AzureRMChannels()


if __name__ == '__main__':
    main()

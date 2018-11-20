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
module: azure_rm_botservicebot
version_added: "2.8"
short_description: Manage Bot instance.
description:
    - Create, update and delete instance of Bot.

options:
    resource_group:
        description:
            - The name of the C(bot) resource group in the user subscription.
        required: True
    name:
        description:
            - The name of the C(bot) resource.
        required: True
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
                    - Required when C(state) is I(present).
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
    display_name:
        description:
            - The Name of the C(bot)
            - Required when C(state) is I(present).
    description:
        description:
            - The description of the C(bot)
    icon_url:
        description:
            - The Icon Url of the C(bot)
    endpoint:
        description:
            - "The C(bot)'s endpoint"
            - Required when C(state) is I(present).
    msa_app_id:
        description:
            - Microsoft App Id for the C(bot)
            - Required when C(state) is I(present).
    developer_app_insight_key:
        description:
            - The Application Insights key
    developer_app_insights_api_key:
        description:
            - The Application Insights Api Key
    developer_app_insights_application_id:
        description:
            - The Application Insights App Id
    luis_app_ids:
        description:
            - Collection of LUIS App Ids
        type: list
    luis_key:
        description:
            - The LUIS Key
    state:
      description:
        - Assert the state of the Bot.
        - Use 'present' to create or update an Bot and 'absent' to delete it.
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
  - name: Create (or update) Bot
    azure_rm_botservicebot:
      resource_group: OneResourceGroupName
      name: samplebotname
      location: eastus
      sku:
        name: S1
      kind: sdk
      display_name: The Name of the bot
      description: The description of the bot
      icon_url: http://myicon
      endpoint: http://mybot.coffee
      msa_app_id: exampleappid
      developer_app_insight_key: appinsightskey
      developer_app_insights_api_key: appinsightsapikey
      developer_app_insights_application_id: appinsightsappid
      luis_app_ids:
        - [
  "luisappid1",
  "luisappid2"
]
      luis_key: luiskey
'''

RETURN = '''
id:
    description:
        - Specifies the resource ID.
    returned: always
    type: str
    sample: someid
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


class AzureRMBots(AzureRMModuleBase):
    """Configuration class for an Azure RM Bot resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
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
            display_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            icon_url=dict(
                type='str'
            ),
            endpoint=dict(
                type='str'
            ),
            msa_app_id=dict(
                type='str'
            ),
            developer_app_insight_key=dict(
                type='str'
            ),
            developer_app_insights_api_key=dict(
                type='str'
            ),
            developer_app_insights_application_id=dict(
                type='str'
            ),
            luis_app_ids=dict(
                type='list'
            ),
            luis_key=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBots, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "display_name":
                    self.parameters.setdefault("properties", {})["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters.setdefault("properties", {})["description"] = kwargs[key]
                elif key == "icon_url":
                    self.parameters.setdefault("properties", {})["icon_url"] = kwargs[key]
                elif key == "endpoint":
                    self.parameters.setdefault("properties", {})["endpoint"] = kwargs[key]
                elif key == "msa_app_id":
                    self.parameters.setdefault("properties", {})["msa_app_id"] = kwargs[key]
                elif key == "developer_app_insight_key":
                    self.parameters.setdefault("properties", {})["developer_app_insight_key"] = kwargs[key]
                elif key == "developer_app_insights_api_key":
                    self.parameters.setdefault("properties", {})["developer_app_insights_api_key"] = kwargs[key]
                elif key == "developer_app_insights_application_id":
                    self.parameters.setdefault("properties", {})["developer_app_insights_application_id"] = kwargs[key]
                elif key == "luis_app_ids":
                    self.parameters.setdefault("properties", {})["luis_app_ids"] = kwargs[key]
                elif key == "luis_key":
                    self.parameters.setdefault("properties", {})["luis_key"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureBotService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_bot()

        if not old_response:
            self.log("Bot instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Bot instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Bot instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_bot()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Bot instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_bot()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_bot():
                time.sleep(20)
        else:
            self.log("Bot instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_bot(self):
        '''
        Creates or updates Bot with the specified configuration.

        :return: deserialized Bot instance state dictionary
        '''
        self.log("Creating / Updating the Bot instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.bots.create(resource_group_name=self.resource_group,
                                                        resource_name=self.name,
                                                        parameters=self.parameters)
            else:
                response = self.mgmt_client.bots.update(resource_group_name=self.resource_group,
                                                        resource_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Bot instance.')
            self.fail("Error creating the Bot instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_bot(self):
        '''
        Deletes specified Bot instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Bot instance {0}".format(self.name))
        try:
            response = self.mgmt_client.bots.delete(resource_group_name=self.resource_group,
                                                    resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Bot instance.')
            self.fail("Error deleting the Bot instance: {0}".format(str(e)))

        return True

    def get_bot(self):
        '''
        Gets the properties of the specified Bot.

        :return: deserialized Bot instance state dictionary
        '''
        self.log("Checking if the Bot instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.bots.get(resource_group_name=self.resource_group,
                                                 resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Bot instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Bot instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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


def main():
    """Main execution"""
    AzureRMBots()


if __name__ == '__main__':
    main()

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
module: azure_rm_botservicebotconnection
version_added: "2.8"
short_description: Manage Azure Bot Connection instance.
description:
    - Create, update and delete instance of Azure Bot Connection.

options:
    resource_group:
        description:
            - The name of the C(bot) resource group in the user subscription.
        required: True
    resource_name:
        description:
            - The name of the C(bot) resource.
        required: True
    name:
        description:
            - The name of the C(bot) Service Connection Setting resource
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
    client_id:
        description:
            - Client Id associated with the Connection Setting.
    client_secret:
        description:
            - Client Secret associated with the Connection Setting
    scopes:
        description:
            - Scopes associated with the Connection Setting
    service_provider_id:
        description:
            - Service Provider Id associated with the Connection Setting
    service_provider_display_name:
        description:
            - Service Provider Display Name associated with the Connection Setting
    parameters:
        description:
            - Service Provider Parameters associated with the Connection Setting
        type: list
        suboptions:
            key:
                description:
                    - Key for the Connection Setting Parameter.
            value:
                description:
                    - Value associated with the Connection Setting Parameter.
    state:
      description:
        - Assert the state of the Bot Connection.
        - Use 'present' to create or update an Bot Connection and 'absent' to delete it.
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
  - name: Create (or update) Bot Connection
    azure_rm_botservicebotconnection:
      resource_group: OneResourceGroupName
      resource_name: samplebotname
      name: sampleConnection
      location: eastus
      client_id: sampleclientid
      client_secret: samplesecret
      scopes: samplescope
      service_provider_id: serviceproviderid
      parameters:
        - key: key1
          value: value1
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMBotConnection(AzureRMModuleBase):
    """Configuration class for an Azure RM Bot Connection resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['f0',
                                 's1']
                    )
                )
            ),
            kind=dict(
                type='str',
                choices=['sdk',
                         'designer',
                         'bot',
                         'function']
            ),
            client_id=dict(
                type='str'
            ),
            client_secret=dict(
                type='str'
            ),
            scopes=dict(
                type='str'
            ),
            service_provider_id=dict(
                type='str'
            ),
            service_provider_display_name=dict(
                type='str'
            ),
            parameters=dict(
                type='list',
                options=dict(
                    key=dict(
                        type='str'
                    ),
                    value=dict(
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

        self.resource_group = None
        self.resource_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBotConnection, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_expand(self.parameters, ['client_id'])
        dict_expand(self.parameters, ['client_secret'])
        dict_expand(self.parameters, ['scopes'])
        dict_expand(self.parameters, ['service_provider_id'])
        dict_expand(self.parameters, ['service_provider_display_name'])
        dict_expand(self.parameters, ['parameters'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureBotService,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_botconnection()

        if not old_response:
            self.log("Bot Connection instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Bot Connection instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Bot Connection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_botconnection()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Bot Connection instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_botconnection()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Bot Connection instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_botconnection(self):
        '''
        Creates or updates Bot Connection with the specified configuration.

        :return: deserialized Bot Connection instance state dictionary
        '''
        self.log("Creating / Updating the Bot Connection instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.bot_connection.create(resource_group_name=self.resource_group,
                                                                  resource_name=self.resource_name,
                                                                  connection_name=self.name,
                                                                  parameters=self.parameters)
            else:
                response = self.mgmt_client.bot_connection.update(resource_group_name=self.resource_group,
                                                                  resource_name=self.resource_name,
                                                                  connection_name=self.name,
                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Bot Connection instance.')
            self.fail("Error creating the Bot Connection instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_botconnection(self):
        '''
        Deletes specified Bot Connection instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Bot Connection instance {0}".format(self.name))
        try:
            response = self.mgmt_client.bot_connection.delete(resource_group_name=self.resource_group,
                                                              resource_name=self.resource_name,
                                                              connection_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Bot Connection instance.')
            self.fail("Error deleting the Bot Connection instance: {0}".format(str(e)))

        return True

    def get_botconnection(self):
        '''
        Gets the properties of the specified Bot Connection.

        :return: deserialized Bot Connection instance state dictionary
        '''
        self.log("Checking if the Bot Connection instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.bot_connection.get(resource_group_name=self.resource_group,
                                                           resource_name=self.resource_name,
                                                           connection_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Bot Connection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Bot Connection instance.')
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
            else:
                key = list(old[0])[0]
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


def main():
    """Main execution"""
    AzureRMBotConnection()


if __name__ == '__main__':
    main()

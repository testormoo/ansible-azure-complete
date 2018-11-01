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
module: azure_rm_automationconnection
version_added: "2.8"
short_description: Manage Connection instance.
description:
    - Create, update and delete instance of Connection.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    connection_name:
        description:
            - The parameters supplied to the create or update connection operation.
        required: True
    name:
        description:
            - Gets or sets the name of the connection.
        required: True
    description:
        description:
            - Gets or sets the description of the connection.
    connection_type:
        description:
            - Gets or sets the connectionType of the connection.
        required: True
        suboptions:
            name:
                description:
                    - Gets or sets the name of the connection type.
    field_definition_values:
        description:
            - Gets or sets the field definition properties of the connection.
    state:
      description:
        - Assert the state of the Connection.
        - Use 'present' to create or update an Connection and 'absent' to delete it.
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
  - name: Create (or update) Connection
    azure_rm_automationconnection:
      resource_group: rg
      automation_account_name: myAutomationAccount28
      connection_name: mysConnection
      name: mysConnection
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount29/connections/myConnection
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMConnection(AzureRMModuleBase):
    """Configuration class for an Azure RM Connection resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            connection_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            connection_type=dict(
                type='dict',
                required=True
            ),
            field_definition_values=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.connection_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConnection, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "connection_type":
                    self.parameters["connection_type"] = kwargs[key]
                elif key == "field_definition_values":
                    self.parameters["field_definition_values"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_connection()

        if not old_response:
            self.log("Connection instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Connection instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Connection instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Connection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_connection()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Connection instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_connection()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_connection():
                time.sleep(20)
        else:
            self.log("Connection instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_connection(self):
        '''
        Creates or updates Connection with the specified configuration.

        :return: deserialized Connection instance state dictionary
        '''
        self.log("Creating / Updating the Connection instance {0}".format(self.connection_name))

        try:
            response = self.mgmt_client.connection.create_or_update(resource_group_name=self.resource_group,
                                                                    automation_account_name=self.automation_account_name,
                                                                    connection_name=self.connection_name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Connection instance.')
            self.fail("Error creating the Connection instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_connection(self):
        '''
        Deletes specified Connection instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Connection instance {0}".format(self.connection_name))
        try:
            response = self.mgmt_client.connection.delete(resource_group_name=self.resource_group,
                                                          automation_account_name=self.automation_account_name,
                                                          connection_name=self.connection_name)
        except CloudError as e:
            self.log('Error attempting to delete the Connection instance.')
            self.fail("Error deleting the Connection instance: {0}".format(str(e)))

        return True

    def get_connection(self):
        '''
        Gets the properties of the specified Connection.

        :return: deserialized Connection instance state dictionary
        '''
        self.log("Checking if the Connection instance {0} is present".format(self.connection_name))
        found = False
        try:
            response = self.mgmt_client.connection.get(resource_group_name=self.resource_group,
                                                       automation_account_name=self.automation_account_name,
                                                       connection_name=self.connection_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Connection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Connection instance.')
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
    AzureRMConnection()


if __name__ == '__main__':
    main()
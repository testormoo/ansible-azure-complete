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
module: azure_rm_sqlserverconnectionpolicy
version_added: "2.8"
short_description: Manage Server Connection Policy instance.
description:
    - Create, update and delete instance of Server Connection Policy.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    connection_policy_name:
        description:
            - The name of the connection policy.
        required: True
    connection_type:
        description:
            - The server connection type.
        required: True
        choices:
            - 'default'
            - 'proxy'
            - 'redirect'
    state:
      description:
        - Assert the state of the Server Connection Policy.
        - Use 'present' to create or update an Server Connection Policy and 'absent' to delete it.
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
  - name: Create (or update) Server Connection Policy
    azure_rm_sqlserverconnectionpolicy:
      resource_group: test-1234
      server_name: test-5678
      connection_policy_name: default
      connection_type: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/test-1234/providers/Microsoft.Sql/servers/test-5678/connectionPolicies/default
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMServerConnectionPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Server Connection Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            connection_policy_name=dict(
                type='str',
                required=True
            ),
            connection_type=dict(
                type='str',
                choices=['default',
                         'proxy',
                         'redirect'],
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.connection_policy_name = None
        self.connection_type = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServerConnectionPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_serverconnectionpolicy()

        if not old_response:
            self.log("Server Connection Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Server Connection Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Server Connection Policy instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Server Connection Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_serverconnectionpolicy()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Server Connection Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_serverconnectionpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_serverconnectionpolicy():
                time.sleep(20)
        else:
            self.log("Server Connection Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_serverconnectionpolicy(self):
        '''
        Creates or updates Server Connection Policy with the specified configuration.

        :return: deserialized Server Connection Policy instance state dictionary
        '''
        self.log("Creating / Updating the Server Connection Policy instance {0}".format(self.connection_policy_name))

        try:
            response = self.mgmt_client.server_connection_policies.create_or_update(resource_group_name=self.resource_group,
                                                                                    server_name=self.server_name,
                                                                                    connection_policy_name=self.connection_policy_name,
                                                                                    connection_type=self.connection_type)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Server Connection Policy instance.')
            self.fail("Error creating the Server Connection Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serverconnectionpolicy(self):
        '''
        Deletes specified Server Connection Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Server Connection Policy instance {0}".format(self.connection_policy_name))
        try:
            response = self.mgmt_client.server_connection_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Server Connection Policy instance.')
            self.fail("Error deleting the Server Connection Policy instance: {0}".format(str(e)))

        return True

    def get_serverconnectionpolicy(self):
        '''
        Gets the properties of the specified Server Connection Policy.

        :return: deserialized Server Connection Policy instance state dictionary
        '''
        self.log("Checking if the Server Connection Policy instance {0} is present".format(self.connection_policy_name))
        found = False
        try:
            response = self.mgmt_client.server_connection_policies.get(resource_group_name=self.resource_group,
                                                                       server_name=self.server_name,
                                                                       connection_policy_name=self.connection_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Server Connection Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Server Connection Policy instance.')
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
    AzureRMServerConnectionPolicies()


if __name__ == '__main__':
    main()

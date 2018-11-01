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
module: azure_rm_sqlmanagedinstancekey
version_added: "2.8"
short_description: Manage Managed Instance Key instance.
description:
    - Create, update and delete instance of Managed Instance Key.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    managed_instance_name:
        description:
            - The name of the managed instance.
        required: True
    key_name:
        description:
            - The name of the managed instance key to be operated on (updated or created).
        required: True
    server_key_type:
        description:
            - "The key type like 'C(service_managed)', 'C(azure_key_vault)'."
        required: True
        choices:
            - 'service_managed'
            - 'azure_key_vault'
    uri:
        description:
            - The URI of the key. If the I(server_key_type) is C(azure_key_vault), then the URI is required.
    state:
      description:
        - Assert the state of the Managed Instance Key.
        - Use 'present' to create or update an Managed Instance Key and 'absent' to delete it.
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
  - name: Create (or update) Managed Instance Key
    azure_rm_sqlmanagedinstancekey:
      resource_group: sqlcrudtest-7398
      managed_instance_name: sqlcrudtest-4645
      key_name: someVault_someKey_01234567890123456789012345678901
      server_key_type: NOT FOUND
      uri: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-7398/providers/Microsoft.Sql/managedInstances/sqlcrudtest-4645/ke
            ys/someVault_someKey_01234567890123456789012345678901"
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


class AzureRMManagedInstanceKeys(AzureRMModuleBase):
    """Configuration class for an Azure RM Managed Instance Key resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            managed_instance_name=dict(
                type='str',
                required=True
            ),
            key_name=dict(
                type='str',
                required=True
            ),
            server_key_type=dict(
                type='str',
                choices=['service_managed',
                         'azure_key_vault'],
                required=True
            ),
            uri=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.managed_instance_name = None
        self.key_name = None
        self.server_key_type = None
        self.uri = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagedInstanceKeys, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_managedinstancekey()

        if not old_response:
            self.log("Managed Instance Key instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Managed Instance Key instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Managed Instance Key instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Managed Instance Key instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managedinstancekey()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Managed Instance Key instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managedinstancekey()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_managedinstancekey():
                time.sleep(20)
        else:
            self.log("Managed Instance Key instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_managedinstancekey(self):
        '''
        Creates or updates Managed Instance Key with the specified configuration.

        :return: deserialized Managed Instance Key instance state dictionary
        '''
        self.log("Creating / Updating the Managed Instance Key instance {0}".format(self.key_name))

        try:
            response = self.mgmt_client.managed_instance_keys.create_or_update(resource_group_name=self.resource_group,
                                                                               managed_instance_name=self.managed_instance_name,
                                                                               key_name=self.key_name,
                                                                               server_key_type=self.server_key_type)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Managed Instance Key instance.')
            self.fail("Error creating the Managed Instance Key instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_managedinstancekey(self):
        '''
        Deletes specified Managed Instance Key instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Managed Instance Key instance {0}".format(self.key_name))
        try:
            response = self.mgmt_client.managed_instance_keys.delete(resource_group_name=self.resource_group,
                                                                     managed_instance_name=self.managed_instance_name,
                                                                     key_name=self.key_name)
        except CloudError as e:
            self.log('Error attempting to delete the Managed Instance Key instance.')
            self.fail("Error deleting the Managed Instance Key instance: {0}".format(str(e)))

        return True

    def get_managedinstancekey(self):
        '''
        Gets the properties of the specified Managed Instance Key.

        :return: deserialized Managed Instance Key instance state dictionary
        '''
        self.log("Checking if the Managed Instance Key instance {0} is present".format(self.key_name))
        found = False
        try:
            response = self.mgmt_client.managed_instance_keys.get(resource_group_name=self.resource_group,
                                                                  managed_instance_name=self.managed_instance_name,
                                                                  key_name=self.key_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Managed Instance Key instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Managed Instance Key instance.')
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
    AzureRMManagedInstanceKeys()


if __name__ == '__main__':
    main()

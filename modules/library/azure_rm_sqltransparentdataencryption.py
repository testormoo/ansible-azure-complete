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
module: azure_rm_sqltransparentdataencryption
version_added: "2.8"
short_description: Manage Transparent Data Encryption instance.
description:
    - Create, update and delete instance of Transparent Data Encryption.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database for which setting the transparent data encryption applies.
        required: True
    transparent_data_encryption_name:
        description:
            - The name of the transparent data encryption configuration.
        required: True
    status:
        description:
            - The status of the database transparent data encryption.
        choices:
            - 'enabled'
            - 'disabled'
    state:
      description:
        - Assert the state of the Transparent Data Encryption.
        - Use 'present' to create or update an Transparent Data Encryption and 'absent' to delete it.
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
  - name: Create (or update) Transparent Data Encryption
    azure_rm_sqltransparentdataencryption:
      resource_group: sqlcrudtest-6852
      server_name: sqlcrudtest-2080
      database_name: sqlcrudtest-9187
      transparent_data_encryption_name: current
      status: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-6852/providers/Microsoft.Sql/servers/sqlcrudtest-2080/databases/s
            qlcrudtest-9187/transparentDataEncryption/current"
status:
    description:
        - "The status of the database transparent data encryption. Possible values include: 'Enabled', 'Disabled'"
    returned: always
    type: str
    sample: Enabled
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


class AzureRMTransparentDataEncryptions(AzureRMModuleBase):
    """Configuration class for an Azure RM Transparent Data Encryption resource"""

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
            database_name=dict(
                type='str',
                required=True
            ),
            transparent_data_encryption_name=dict(
                type='str',
                required=True
            ),
            status=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.database_name = None
        self.transparent_data_encryption_name = None
        self.status = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMTransparentDataEncryptions, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_transparentdataencryption()

        if not old_response:
            self.log("Transparent Data Encryption instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Transparent Data Encryption instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Transparent Data Encryption instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Transparent Data Encryption instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_transparentdataencryption()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Transparent Data Encryption instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_transparentdataencryption()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_transparentdataencryption():
                time.sleep(20)
        else:
            self.log("Transparent Data Encryption instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_transparentdataencryption(self):
        '''
        Creates or updates Transparent Data Encryption with the specified configuration.

        :return: deserialized Transparent Data Encryption instance state dictionary
        '''
        self.log("Creating / Updating the Transparent Data Encryption instance {0}".format(self.transparent_data_encryption_name))

        try:
            response = self.mgmt_client.transparent_data_encryptions.create_or_update(resource_group_name=self.resource_group,
                                                                                      server_name=self.server_name,
                                                                                      database_name=self.database_name,
                                                                                      transparent_data_encryption_name=self.transparent_data_encryption_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Transparent Data Encryption instance.')
            self.fail("Error creating the Transparent Data Encryption instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_transparentdataencryption(self):
        '''
        Deletes specified Transparent Data Encryption instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Transparent Data Encryption instance {0}".format(self.transparent_data_encryption_name))
        try:
            response = self.mgmt_client.transparent_data_encryptions.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Transparent Data Encryption instance.')
            self.fail("Error deleting the Transparent Data Encryption instance: {0}".format(str(e)))

        return True

    def get_transparentdataencryption(self):
        '''
        Gets the properties of the specified Transparent Data Encryption.

        :return: deserialized Transparent Data Encryption instance state dictionary
        '''
        self.log("Checking if the Transparent Data Encryption instance {0} is present".format(self.transparent_data_encryption_name))
        found = False
        try:
            response = self.mgmt_client.transparent_data_encryptions.get(resource_group_name=self.resource_group,
                                                                         server_name=self.server_name,
                                                                         database_name=self.database_name,
                                                                         transparent_data_encryption_name=self.transparent_data_encryption_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Transparent Data Encryption instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Transparent Data Encryption instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMTransparentDataEncryptions()


if __name__ == '__main__':
    main()

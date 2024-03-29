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
module: azure_rm_sqlrestorepoint
version_added: "2.8"
short_description: Manage Azure Restore Point instance.
description:
    - Create, update and delete instance of Azure Restore Point.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the database.
        required: True
    restore_point_label:
        description:
            - The restore point label to apply
        required: True
    state:
      description:
        - Assert the state of the Restore Point.
        - Use 'present' to create or update an Restore Point and 'absent' to delete it.
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
  - name: Create (or update) Restore Point
    azure_rm_sqlrestorepoint:
      resource_group: Default-SQL-SouthEastAsia
      server_name: testserver
      name: testDatabase
      restore_point_label: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/providers/Microsoft.Sql/servers/testserver/databases/testDatabase/restorePoints/131546477590
            000000"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMRestorePoint(AzureRMModuleBase):
    """Configuration class for an Azure RM Restore Point resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            restore_point_label=dict(
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
        self.server_name = None
        self.name = None
        self.restore_point_label = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRestorePoint, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_restorepoint()

        if not old_response:
            self.log("Restore Point instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Restore Point instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Restore Point instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_restorepoint()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Restore Point instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_restorepoint()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Restore Point instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_restorepoint(self):
        '''
        Creates or updates Restore Point with the specified configuration.

        :return: deserialized Restore Point instance state dictionary
        '''
        self.log("Creating / Updating the Restore Point instance {0}".format(self.restore_point_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.restore_points.create(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  database_name=self.name,
                                                                  restore_point_label=self.restore_point_label)
            else:
                response = self.mgmt_client.restore_points.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Restore Point instance.')
            self.fail("Error creating the Restore Point instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_restorepoint(self):
        '''
        Deletes specified Restore Point instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Restore Point instance {0}".format(self.restore_point_name))
        try:
            response = self.mgmt_client.restore_points.delete(resource_group_name=self.resource_group,
                                                              server_name=self.server_name,
                                                              database_name=self.name,
                                                              restore_point_name=self.restore_point_name)
        except CloudError as e:
            self.log('Error attempting to delete the Restore Point instance.')
            self.fail("Error deleting the Restore Point instance: {0}".format(str(e)))

        return True

    def get_restorepoint(self):
        '''
        Gets the properties of the specified Restore Point.

        :return: deserialized Restore Point instance state dictionary
        '''
        self.log("Checking if the Restore Point instance {0} is present".format(self.restore_point_name))
        found = False
        try:
            response = self.mgmt_client.restore_points.get(resource_group_name=self.resource_group,
                                                           server_name=self.server_name,
                                                           database_name=self.name,
                                                           restore_point_name=self.restore_point_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Restore Point instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Restore Point instance.')
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


def main():
    """Main execution"""
    AzureRMRestorePoint()


if __name__ == '__main__':
    main()

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
module: azure_rm_sqlserver
version_added: "2.8"
short_description: Manage Azure SQL Server instance.
description:
    - Create, update and delete instance of Azure SQL Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the server.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    identity:
        description:
            - "The identity type. Set this to 'C(system_assigned)' in order to automatically create and assign an Azure Active Directory principal for the
               resource."
        choices:
            - 'system_assigned'
    admin_username:
        description:
            - Administrator username for the server. Once created it cannot be changed.
    admin_password:
        description:
            - The administrator login password (required for server creation).
    version:
        description:
            - "The version of the server. For example '12.0'."
    state:
      description:
        - Assert the state of the SQL Server.
        - Use 'present' to create or update an SQL Server and 'absent' to delete it.
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
  - name: Create (or update) SQL Server
    azure_rm_sqlserver:
      resource_group: resource_group
      name: sqlcrudtest-4645
      location: westus
      admin_username: mylogin
      admin_password: Testpasswordxyz12!
      version: 12.0
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-7398/providers/Microsoft.Sql/servers/sqlcrudtest-4645
version:
    description:
        - The version of the server.
    returned: always
    type: str
    sample: 12.0
state:
    description:
        - The state of the server.
    returned: always
    type: str
    sample: Ready
fully_qualified_domain_name:
    description:
        - The fully qualified domain name of the server.
    returned: always
    type: str
    sample: sqlcrudtest-4645.database.windows.net
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


class AzureRMSQLServer(AzureRMModuleBase):
    """Configuration class for an Azure RM SQL Server resource"""

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
            identity=dict(
                type='str',
                choices=['system_assigned']
            ),
            admin_username=dict(
                type='str'
            ),
            admin_password=dict(
                type='str',
                no_log=True
            ),
            version=dict(
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

        super(AzureRMSQLServer, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_rename(self.parameters, ['identity'], 'identity')
        dict_expand(self.parameters, ['identity'])
        dict_camelize(self.parameters, ['identity'], True)
        dict_rename(self.parameters, ['admin_username'], 'administrator_login')
        dict_rename(self.parameters, ['admin_password'], 'administrator_login_password')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_sqlserver()

        if not old_response:
            self.log("SQL Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("SQL Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the SQL Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_sqlserver()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("SQL Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sqlserver()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("SQL Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'version': response.get('version', None),
                'state': response.get('state', None),
                'fully_qualified_domain_name': response.get('fully_qualified_domain_name', None)
                })
        return self.results

    def create_update_sqlserver(self):
        '''
        Creates or updates SQL Server with the specified configuration.

        :return: deserialized SQL Server instance state dictionary
        '''
        self.log("Creating / Updating the SQL Server instance {0}".format(self.name))

        try:
            response = self.mgmt_client.servers.create_or_update(resource_group_name=self.resource_group,
                                                                 server_name=self.name,
                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the SQL Server instance.')
            self.fail("Error creating the SQL Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_sqlserver(self):
        '''
        Deletes specified SQL Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SQL Server instance {0}".format(self.name))
        try:
            response = self.mgmt_client.servers.delete(resource_group_name=self.resource_group,
                                                       server_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the SQL Server instance.')
            self.fail("Error deleting the SQL Server instance: {0}".format(str(e)))

        return True

    def get_sqlserver(self):
        '''
        Gets the properties of the specified SQL Server.

        :return: deserialized SQL Server instance state dictionary
        '''
        self.log("Checking if the SQL Server instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.servers.get(resource_group_name=self.resource_group,
                                                    server_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SQL Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SQL Server instance.')
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


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


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
    AzureRMSQLServer()


if __name__ == '__main__':
    main()

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
module: azure_rm_mariadbserver
version_added: "2.8"
short_description: Manage Azure MariaDB Server instance.
description:
    - Create, update and delete instance of Azure MariaDB Server.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the server.
        required: True
    sku:
        description:
            - The SKU (pricing tier) of the server.
        suboptions:
            name:
                description:
                    - The name of the sku, typically, I(tier) + I(family) + cores, e.g. B_Gen4_1, GP_Gen5_8.
            tier:
                description:
                    - The tier of the particular SKU, e.g. C(basic).
                choices:
                    - 'basic'
                    - 'general_purpose'
                    - 'memory_optimized'
            capacity:
                description:
                    - "The scale up/out capacity, representing server's compute units."
            size:
                description:
                    - The size code, to be interpreted by resource as appropriate.
            family:
                description:
                    - The family of hardware.
    version:
        description:
            - Server version.
        choices:
            - '5.6'
            - '5.7'
    enforce_ssl:
        description:
            - "Enable ssl enforcement or not when connect to server. Possible values include: 'Enabled', 'Disabled'"
        type: bool
    storage_profile:
        description:
            - Storage profile of a server.
        suboptions:
            backup_retention_days:
                description:
                    - Backup retention days for the server.
            geo_redundant_backup:
                description:
                    - "Enable Geo-redundant or not for server backup. Possible values include: 'Enabled', 'Disabled'"
                type: bool
            storage_mb:
                description:
                    - Max storage allowed for a server.
    admin_username:
        description:
            - "The administrator's login name of a server. Can only be specified when the server is being created (and is required for creation)."
    admin_password:
        description:
            - The password of the administrator login.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
      description:
        - Assert the state of the MariaDB Server.
        - Use 'present' to create or update an MariaDB Server and 'absent' to delete it.
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
  - name: Create (or update) MariaDB Server
    azure_rm_mariadbserver:
      resource_group: testrg
      name: mariadbtestsvc4
      sku:
        name: GP_Gen5_2
        tier: GeneralPurpose
        capacity: 2
        family: Gen5
      enforce_ssl: True
      storage_profile:
        backup_retention_days: 7
        geo_redundant_backup: geo_redundant_backup
        storage_mb: 128000
      admin_username: cloudsa
      admin_password: pass$w0rd
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID
    returned: always
    type: str
    sample: /subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/testrg/providers/Microsoft.DBforMariaDB/servers/mariadbtestsvc4
version:
    description:
        - "Server version. Possible values include: '5.6', '5.7'"
    returned: always
    type: str
    sample: 5.7
user_visible_state:
    description:
        - "A state of a server that is visible to user. Possible values include: 'Ready', 'Dropping', 'Disabled'"
    returned: always
    type: str
    sample: user_visible_state
fully_qualified_domain_name:
    description:
        - The fully qualified domain name of a server.
    returned: always
    type: str
    sample: fully_qualified_domain_name
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.mariadb import MariaDBManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMMariaDBServer(AzureRMModuleBase):
    """Configuration class for an Azure RM MariaDB Server resource"""

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
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    tier=dict(
                        type='str',
                        choices=['basic',
                                 'general_purpose',
                                 'memory_optimized']
                    ),
                    capacity=dict(
                        type='int'
                    ),
                    size=dict(
                        type='str'
                    ),
                    family=dict(
                        type='str'
                    )
                )
            ),
            version=dict(
                type='str',
                choices=['5.6',
                         '5.7']
            ),
            enforce_ssl=dict(
                type='bool'
            ),
            storage_profile=dict(
                type='dict',
                options=dict(
                    backup_retention_days=dict(
                        type='int'
                    ),
                    geo_redundant_backup=dict(
                        type='bool'
                    ),
                    storage_mb=dict(
                        type='int'
                    )
                )
            ),
            create_mode=dict(
                type='str',
                default='Default'
            ),
            admin_username=dict(
                type='str'
            ),
            admin_password=dict(
                type='str',
                no_log=True
            ),
            location=dict(
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

        super(AzureRMMariaDBServer, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'tier'], True)
        dict_expand(self.parameters, ['version'])
        dict_rename(self.parameters, ['enforce_ssl'], 'properties')
        dict_expand(self.parameters, ['enforce_ssl'])
        dict_map(self.parameters, ['enforce_ssl'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.parameters, ['storage_profile', 'geo_redundant_backup'], {True: 'Enabled', False: 'Disabled'})
        dict_expand(self.parameters, ['storage_profile'])
        dict_expand(self.parameters, ['create_mode'])
        dict_rename(self.parameters, ['admin_username'], 'properties')
        dict_expand(self.parameters, ['admin_username'])
        dict_rename(self.parameters, ['admin_password'], 'properties')
        dict_expand(self.parameters, ['admin_password'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MariaDBManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_mariadbserver()

        if not old_response:
            self.log("MariaDB Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("MariaDB Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the MariaDB Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_mariadbserver()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("MariaDB Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_mariadbserver()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("MariaDB Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'version': response.get('version', None),
                'user_visible_state': response.get('user_visible_state', None),
                'fully_qualified_domain_name': response.get('fully_qualified_domain_name', None)
                })
        return self.results

    def create_update_mariadbserver(self):
        '''
        Creates or updates MariaDB Server with the specified configuration.

        :return: deserialized MariaDB Server instance state dictionary
        '''
        self.log("Creating / Updating the MariaDB Server instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.servers.create(resource_group_name=self.resource_group,
                                                           server_name=self.name,
                                                           parameters=self.parameters)
            else:
                response = self.mgmt_client.servers.update(resource_group_name=self.resource_group,
                                                           server_name=self.name,
                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the MariaDB Server instance.')
            self.fail("Error creating the MariaDB Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_mariadbserver(self):
        '''
        Deletes specified MariaDB Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the MariaDB Server instance {0}".format(self.name))
        try:
            response = self.mgmt_client.servers.delete(resource_group_name=self.resource_group,
                                                       server_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the MariaDB Server instance.')
            self.fail("Error deleting the MariaDB Server instance: {0}".format(str(e)))

        return True

    def get_mariadbserver(self):
        '''
        Gets the properties of the specified MariaDB Server.

        :return: deserialized MariaDB Server instance state dictionary
        '''
        self.log("Checking if the MariaDB Server instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.servers.get(resource_group_name=self.resource_group,
                                                    server_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("MariaDB Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the MariaDB Server instance.')
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


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
    AzureRMMariaDBServer()


if __name__ == '__main__':
    main()

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
module: azure_rm_postgresqlserver
version_added: "2.8"
short_description: Manage PostgreSQL Server instance.
description:
    - Create, update and delete instance of PostgreSQL Server.

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
                    - The name of the sku, typically, a letter + Number code, e.g. P3.
            tier:
                description:
                    - The tier of the particular SKU, e.g. C(basic).
                choices:
                    - 'basic'
                    - 'standard'
            capacity:
                description:
                    - "The scale up/out capacity, representing server's compute units."
            size:
                description:
                    - The size code, to be interpreted by resource as appropriate.
    storage_mb:
        description:
            - The maximum storage allowed for a server.
    version:
        description:
            - Server version.
        choices:
            - '9.5'
            - '9.6'
    enforce_ssl:
        description:
            - Enable SSL enforcement.
        type: bool
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
        - Assert the state of the PostgreSQL Server.
        - Use 'present' to create or update an PostgreSQL Server and 'absent' to delete it.
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
  - name: Create (or update) PostgreSQL Server
    azure_rm_postgresqlserver:
      resource_group: TestGroup
      name: testserver
      sku:
        name: PGSQLS100
        tier: Basic
        capacity: 100
      storage_mb: 1024
      enforce_ssl: True
      admin_username: cloudsa
      admin_password: password
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID
    returned: always
    type: str
    sample: /subscriptions/12345678-1234-1234-1234-123412341234/resourceGroups/samplerg/providers/Microsoft.DBforPostgreSQL/servers/mysqlsrv1b6dd89593
version:
    description:
        - "Server version. Possible values include: '9.5', '9.6'"
    returned: always
    type: str
    sample: 9.6
state:
    description:
        - "A state of a server that is visible to user. Possible values include: 'Ready', 'Dropping', 'Disabled'"
    returned: always
    type: str
    sample: Ready
fully_qualified_domain_name:
    description:
        - The fully qualified domain name of a server.
    returned: always
    type: str
    sample: postgresqlsrv1b6dd89593.postgresql.database.azure.com
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMServers(AzureRMModuleBase):
    """Configuration class for an Azure RM PostgreSQL Server resource"""

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
                type='dict'
            ),
            storage_mb=dict(
                type='int'
            ),
            version=dict(
                type='str',
                choices=['9.5',
                         '9.6']
            ),
            enforce_ssl=dict(
                type='bool'
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

        super(AzureRMServers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "sku":
                    ev = kwargs[key]
                    if 'tier' in ev:
                        if ev['tier'] == 'basic':
                            ev['tier'] = 'Basic'
                        elif ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                    self.parameters["sku"] = ev
                elif key == "storage_mb":
                    self.parameters.setdefault("properties", {})["storage_mb"] = kwargs[key]
                elif key == "version":
                    self.parameters.setdefault("properties", {})["version"] = kwargs[key]
                elif key == "enforce_ssl":
                    self.parameters.setdefault("properties", {})["ssl_enforcement"] = 'Enabled' if kwargs[key] else 'Disabled'
                elif key == "create_mode":
                    self.parameters.setdefault("properties", {})["create_mode"] = kwargs[key]
                elif key == "admin_username":
                    self.parameters.setdefault("properties", {})["administrator_login"] = kwargs[key]
                elif key == "admin_password":
                    self.parameters.setdefault("properties", {})["administrator_login_password"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]

        self.adjust_parameters()

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(PostgreSQLManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_postgresqlserver()

        if not old_response:
            self.log("PostgreSQL Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("PostgreSQL Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the PostgreSQL Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_postgresqlserver()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("PostgreSQL Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_postgresqlserver()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_postgresqlserver():
                time.sleep(20)
        else:
            self.log("PostgreSQL Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def adjust_parameters(self):
        if self.parameters.get('properties', None) is not None:
            self.rename_key(self.parameters['properties'], 'enforce_ssl', 'ssl_enforcement')
            self.rename_key(self.parameters['properties'], 'admin_username', 'administrator_login')
            self.rename_key(self.parameters['properties'], 'admin_password', 'administrator_login_password')

    def rename_key(self, d, old_name, new_name):
        old_value = d.get(old_name, None)
        if old_value is not None:
            d.pop(old_name, None)
            d[new_name] = old_value

    def create_update_postgresqlserver(self):
        '''
        Creates or updates PostgreSQL Server with the specified configuration.

        :return: deserialized PostgreSQL Server instance state dictionary
        '''
        self.log("Creating / Updating the PostgreSQL Server instance {0}".format(self.name))

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
            self.log('Error attempting to create the PostgreSQL Server instance.')
            self.fail("Error creating the PostgreSQL Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_postgresqlserver(self):
        '''
        Deletes specified PostgreSQL Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the PostgreSQL Server instance {0}".format(self.name))
        try:
            response = self.mgmt_client.servers.delete(resource_group_name=self.resource_group,
                                                       server_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the PostgreSQL Server instance.')
            self.fail("Error deleting the PostgreSQL Server instance: {0}".format(str(e)))

        return True

    def get_postgresqlserver(self):
        '''
        Gets the properties of the specified PostgreSQL Server.

        :return: deserialized PostgreSQL Server instance state dictionary
        '''
        self.log("Checking if the PostgreSQL Server instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.servers.get(resource_group_name=self.resource_group,
                                                    server_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("PostgreSQL Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the PostgreSQL Server instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'version': d.get('version', None),
            'state': d.get('user_visible_state', None),
            'fully_qualified_domain_name': d.get('fully_qualified_domain_name', None)
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
    AzureRMServers()


if __name__ == '__main__':
    main()

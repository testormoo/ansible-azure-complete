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
module: azure_rm_sqldatabase
version_added: "2.8"
short_description: Manage Azure SQL Database instance.
description:
    - Create, update and delete instance of Azure SQL Database.

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
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as C(default).
    sku:
        description:
            - The name and tier of the SKU.
        suboptions:
            name:
                description:
                    - The name of the SKU. Ex - P3. It is typically a letter+number code
                    - Required when C(state) is I(present).
            tier:
                description:
                    - This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
            size:
                description:
                    - The SKU size. When the name field is the combination of I(tier) and some other value, this would be the standalone code.
            family:
                description:
                    - If the service has different generations of hardware, for the same SKU, then that can be captured here.
            capacity:
                description:
                    - "If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource this
                       may be omitted."
    create_mode:
        description:
            - Specifies the mode of database creation.
            - "C(default): regular database creation."
            - "C(copy): creates a database as a copy of an existing database."
            - "C(online_secondary)/C(non_readable_secondary): creates a database as a (readable or nonreadable) secondary replica of an existing database."
            - "C(point_in_time_restore): Creates a database by restoring a point in time backup of an existing database."
            - "C(recovery): Creates a database by restoring a geo-replicated backup."
            - "C(restore): Creates a database by restoring a backup of a deleted database."
            - "C(restore_long_term_retention_backup): Creates a database by restoring from a long term retention vault."
            - C(copy), C(non_readable_secondary), C(online_secondary) and C(restore_long_term_retention_backup) are not supported for C(data_warehouse) edition.
        choices:
            - 'default'
            - 'copy'
            - 'secondary'
            - 'point_in_time_restore'
            - 'restore'
            - 'recovery'
            - 'restore_external_backup'
            - 'restore_external_backup_secondary'
            - 'restore_long_term_retention_backup'
            - 'online_secondary'
    collation:
        description:
            - The collation of the database.
    max_size_bytes:
        description:
            - The max size of the database expressed in bytes.
    sample_name:
        description:
            - The name of the sample schema to apply when creating this database.
        choices:
            - 'adventure_works_lt'
            - 'wide_world_importers_std'
            - 'wide_world_importers_full'
    elastic_pool_id:
        description:
            - The resource identifier of the elastic pool containing this database.
    source_database_id:
        description:
            - Required unless I(create_mode) is C(default) or C(restore_long_term_retention_backup).
            - Specifies the resource ID of the source database
    restore_point_in_time:
        description:
            - Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
    source_database_deletion_date:
        description:
            - Specifies the time that the database was deleted.
    recovery_services_recovery_point_id:
        description:
            - The resource identifier of the C(recovery) point associated with create operation of this database.
    long_term_retention_backup_resource_id:
        description:
            - The resource identifier of the long term retention backup associated with create operation of this database.
    recoverable_database_id:
        description:
            - The resource identifier of the recoverable database associated with create operation of this database.
    restorable_dropped_database_id:
        description:
            - The resource identifier of the restorable dropped database associated with create operation of this database.
    catalog_collation:
        description:
            - I(collation) of the metadata catalog.
        choices:
            - 'database_default'
            - 'sql_latin1_general_cp1_ci_as'
    zone_redundant:
        description:
            - Is this database is zone redundant? It means the replicas of this database will be spread across multiple availability zones.
        type: bool
    license_type:
        description:
            - The license type to apply for this database.
        choices:
            - 'license_included'
            - 'base_price'
    read_scale:
        description:
            - "If the database is a geo-C(secondary), readScale indicates whether read-only connections are allowed to this database or not. Not supported
               for DataWarehouse edition."
        type: bool
    force_update:
      description:
          - SQL Database will be updated if given parameters differ from existing resource state.
          - To force SQL Database update in any circumstances set this parameter to True.
      type: bool
    state:
      description:
        - Assert the state of the SQL Database.
        - Use 'present' to create or update an SQL Database and 'absent' to delete it.
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
  - name: Create (or update) SQL Database
    azure_rm_sqldatabase:
      resource_group: Default-SQL-SouthEastAsia
      server_name: testsvr
      name: testdb
      location: eastus
      read_scale: read_scale

  - name: Restore SQL Database
    azure_rm_sqldatabase:
      resource_group: sqlcrudtest-4799
      server_name: sqlcrudtest-5961
      name: restoreddb
      location: eastus
      create_mode: restore
      restorable_dropped_database_id: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default-SQL-SouthEastAsia/providers/Microsoft.Sql/s
                                      ervers/testsvr/restorableDroppedDatabases/testdb2,131444841315030000"

  - name: Create SQL Database in Copy Mode
    azure_rm_sqldatabase:
      resource_group: sqlcrudtest-4799
      server_name: sqlcrudtest-5961
      name: copydb
      location: eastus
      create_mode: copy
      source_database_id: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default-SQL-SouthEastAsia/providers/Microsoft.Sql/servers/tests
                          vr/databases/testdb"

'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default-SQL-SouthEastAsia/providers/Microsoft.Sql/servers/testsvr/databases/t
            estdb"
status:
    description:
        - "The status of the database. Possible values include: 'Online', 'Restoring', 'RecoveryPending', 'Recovering', 'Suspect', 'Offline', 'Standby',
           'Shutdown', 'EmergencyMode', 'AutoClosed', 'Copying', 'Creating', 'Inaccessible', 'OfflineSecondary', 'Pausing', 'Paused', 'Resuming', 'Scaling'"
    returned: always
    type: str
    sample: Online
database_id:
    description:
        - The ID of the database.
    returned: always
    type: str
    sample: database_id
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


class AzureRMSQLDatabase(AzureRMModuleBase):
    """Configuration class for an Azure RM SQL Database resource"""

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
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    tier=dict(
                        type='str'
                    ),
                    size=dict(
                        type='str'
                    ),
                    family=dict(
                        type='str'
                    ),
                    capacity=dict(
                        type='int'
                    )
                )
            ),
            create_mode=dict(
                type='str',
                choices=['default',
                         'copy',
                         'secondary',
                         'point_in_time_restore',
                         'restore',
                         'recovery',
                         'restore_external_backup',
                         'restore_external_backup_secondary',
                         'restore_long_term_retention_backup',
                         'online_secondary']
            ),
            collation=dict(
                type='str'
            ),
            max_size_bytes=dict(
                type='int'
            ),
            sample_name=dict(
                type='str',
                choices=['adventure_works_lt',
                         'wide_world_importers_std',
                         'wide_world_importers_full']
            ),
            elastic_pool_id=dict(
                type='str'
            ),
            source_database_id=dict(
                type='str'
            ),
            restore_point_in_time=dict(
                type='datetime'
            ),
            source_database_deletion_date=dict(
                type='datetime'
            ),
            recovery_services_recovery_point_id=dict(
                type='str'
            ),
            long_term_retention_backup_resource_id=dict(
                type='str'
            ),
            recoverable_database_id=dict(
                type='str'
            ),
            restorable_dropped_database_id=dict(
                type='str'
            ),
            catalog_collation=dict(
                type='str',
                choices=['database_default',
                         'sql_latin1_general_cp1_ci_as']
            ),
            zone_redundant=dict(
                type='bool'
            ),
            license_type=dict(
                type='str',
                choices=['license_included',
                         'base_price']
            ),
            read_scale=dict(
                type='bool'
            ),
            force_update=dict(
                type='bool'
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
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSQLDatabase, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['create_mode'], True)
        dict_camelize(self.parameters, ['sample_name'], True)
        dict_map(self.parameters, ['sample_name'], {'adventure_works_lt': 'AdventureWorksLT'})
        dict_upper(self.parameters, ['catalog_collation'])
        dict_map(self.parameters, ['catalog_collation'], {'sql_latin1_general_cp1_ci_as': 'SQL_Latin1_General_CP1_CI_AS'})
        dict_map(self.parameters, ['zone_redundant'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.parameters, ['license_type'], True)
        dict_map(self.parameters, ['read_scale'], {True: 'Enabled', False: 'Disabled'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_sqldatabase()

        if not old_response:
            self.log("SQL Database instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("SQL Database instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the SQL Database instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_sqldatabase()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("SQL Database instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sqldatabase()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("SQL Database instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': response.get('status', None),
                'database_id': response.get('database_id', None)
                })
        return self.results

    def create_update_sqldatabase(self):
        '''
        Creates or updates SQL Database with the specified configuration.

        :return: deserialized SQL Database instance state dictionary
        '''
        self.log("Creating / Updating the SQL Database instance {0}".format(self.name))

        try:
            response = self.mgmt_client.databases.create_or_update(resource_group_name=self.resource_group,
                                                                   server_name=self.server_name,
                                                                   database_name=self.name,
                                                                   parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the SQL Database instance.')
            self.fail("Error creating the SQL Database instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_sqldatabase(self):
        '''
        Deletes specified SQL Database instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SQL Database instance {0}".format(self.name))
        try:
            response = self.mgmt_client.databases.delete(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         database_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the SQL Database instance.')
            self.fail("Error deleting the SQL Database instance: {0}".format(str(e)))

        return True

    def get_sqldatabase(self):
        '''
        Gets the properties of the specified SQL Database.

        :return: deserialized SQL Database instance state dictionary
        '''
        self.log("Checking if the SQL Database instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.databases.get(resource_group_name=self.resource_group,
                                                      server_name=self.server_name,
                                                      database_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SQL Database instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SQL Database instance.')
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


def dict_upper(d, path):
   if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def main():
    """Main execution"""
    AzureRMSQLDatabase()


if __name__ == '__main__':
    main()

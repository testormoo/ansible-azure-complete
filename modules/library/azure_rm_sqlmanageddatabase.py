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
module: azure_rm_sqlmanageddatabase
version_added: "2.8"
short_description: Manage Managed Database instance.
description:
    - Create, update and delete instance of Managed Database.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    managed_instance_name:
        description:
            - The name of the managed instance.
        required: True
    name:
        description:
            - The name of the database.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as C(default).
    collation:
        description:
            - Collation of the managed database.
    restore_point_in_time:
        description:
            - "Conditional. If I(create_mode) is C(point_in_time_restore), this value is required. Specifies the point in time (ISO8601 format) of the
               source database that will be restored to create the new database."
    catalog_collation:
        description:
            - I(collation) of the metadata catalog.
        choices:
            - 'database_default'
            - 'sql_latin1_general_cp1_ci_as'
    create_mode:
        description:
            - "Managed database create mode. C(point_in_time_restore): Create a database by restoring a point in time backup of an existing database.
               SourceDatabaseName, SourceManagedInstanceName and PointInTime must be specified. C(restore_external_backup): Create a database by restoring
               from external backup files. I(collation), I(storage_container_uri) and I(storage_container_sas_token) must be specified."
        choices:
            - 'default'
            - 'restore_external_backup'
            - 'point_in_time_restore'
    storage_container_uri:
        description:
            - "Conditional. If I(create_mode) is C(restore_external_backup), this value is required. Specifies the uri of the storage container where
               backups for this restore are stored."
    source_database_id:
        description:
            - The resource identifier of the source database associated with create operation of this database.
    storage_container_sas_token:
        description:
            - Conditional. If I(create_mode) is C(restore_external_backup), this value is required. Specifies the storage container sas token.
    state:
      description:
        - Assert the state of the Managed Database.
        - Use 'present' to create or update an Managed Database and 'absent' to delete it.
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
  - name: Create (or update) Managed Database
    azure_rm_sqlmanageddatabase:
      resource_group: Default-SQL-SouthEastAsia
      managed_instance_name: managedInstance
      name: managedDatabase
      location: eastus
      collation: SQL_Latin1_General_CP1_CI_AS
      create_mode: RestoreExternalBackup
      storage_container_uri: https://myaccountname.blob.core.windows.net/backups
      storage_container_sas_token: sv=2015-12-11&sr=c&sp=rl&sig=1234
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
        - "Status for the database. Possible values include: 'Online', 'Offline', 'Shutdown', 'Creating', 'Inaccessible'"
    returned: always
    type: str
    sample: status
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


class AzureRMManagedDatabases(AzureRMModuleBase):
    """Configuration class for an Azure RM Managed Database resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            collation=dict(
                type='str'
            ),
            restore_point_in_time=dict(
                type='datetime'
            ),
            catalog_collation=dict(
                type='str',
                choices=['database_default',
                         'sql_latin1_general_cp1_ci_as']
            ),
            create_mode=dict(
                type='str',
                choices=['default',
                         'restore_external_backup',
                         'point_in_time_restore']
            ),
            storage_container_uri=dict(
                type='str'
            ),
            source_database_id=dict(
                type='str'
            ),
            storage_container_sas_token=dict(
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagedDatabases, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "collation":
                    self.parameters["collation"] = kwargs[key]
                elif key == "restore_point_in_time":
                    self.parameters["restore_point_in_time"] = kwargs[key]
                elif key == "catalog_collation":
                    ev = kwargs[key]
                    if ev == 'database_default':
                        ev = 'DATABASE_DEFAULT'
                    elif ev == 'sql_latin1_general_cp1_ci_as':
                        ev = 'SQL_Latin1_General_CP1_CI_AS'
                    self.parameters["catalog_collation"] = ev
                elif key == "create_mode":
                    self.parameters["create_mode"] = _snake_to_camel(kwargs[key], True)
                elif key == "storage_container_uri":
                    self.parameters["storage_container_uri"] = kwargs[key]
                elif key == "source_database_id":
                    self.parameters["source_database_id"] = kwargs[key]
                elif key == "storage_container_sas_token":
                    self.parameters["storage_container_sas_token"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_manageddatabase()

        if not old_response:
            self.log("Managed Database instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Managed Database instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Managed Database instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_manageddatabase()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Managed Database instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_manageddatabase()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_manageddatabase():
                time.sleep(20)
        else:
            self.log("Managed Database instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_manageddatabase(self):
        '''
        Creates or updates Managed Database with the specified configuration.

        :return: deserialized Managed Database instance state dictionary
        '''
        self.log("Creating / Updating the Managed Database instance {0}".format(self.name))

        try:
            response = self.mgmt_client.managed_databases.create_or_update(resource_group_name=self.resource_group,
                                                                           managed_instance_name=self.managed_instance_name,
                                                                           database_name=self.name,
                                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Managed Database instance.')
            self.fail("Error creating the Managed Database instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_manageddatabase(self):
        '''
        Deletes specified Managed Database instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Managed Database instance {0}".format(self.name))
        try:
            response = self.mgmt_client.managed_databases.delete(resource_group_name=self.resource_group,
                                                                 managed_instance_name=self.managed_instance_name,
                                                                 database_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Managed Database instance.')
            self.fail("Error deleting the Managed Database instance: {0}".format(str(e)))

        return True

    def get_manageddatabase(self):
        '''
        Gets the properties of the specified Managed Database.

        :return: deserialized Managed Database instance state dictionary
        '''
        self.log("Checking if the Managed Database instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.managed_databases.get(resource_group_name=self.resource_group,
                                                              managed_instance_name=self.managed_instance_name,
                                                              database_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Managed Database instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Managed Database instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMManagedDatabases()


if __name__ == '__main__':
    main()

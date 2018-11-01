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
module: azure_rm_kustodatabase
version_added: "2.8"
short_description: Manage Database instance.
description:
    - Create, update and delete instance of Database.

options:
    resource_group:
        description:
            - The name of the resource group containing the Kusto cluster.
        required: True
    cluster_name:
        description:
            - The name of the Kusto cluster.
        required: True
    database_name:
        description:
            - The name of the database in the Kusto cluster.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    soft_delete_period_in_days:
        description:
            - The number of days data should be kept before it stops being accessible to queries.
        required: True
    hot_cache_period_in_days:
        description:
            - The number of days of data that should be kept in cache for fast queries.
    statistics:
        description:
            - The statistics of the database.
        suboptions:
            size:
                description:
                    - The database size - the total size of compressed data and index in bytes.
    state:
      description:
        - Assert the state of the Database.
        - Use 'present' to create or update an Database and 'absent' to delete it.
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
  - name: Create (or update) Database
    azure_rm_kustodatabase:
      resource_group: kustorptest
      cluster_name: KustoClusterRPTest4
      database_name: KustoDatabase8
      location: eastus
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/12345678-1234-1234-1234-123456789098/resourceGroups/kustorptest/providers/Microsoft.Kusto/Clusters/KustoClusterRPTest4/Databases/
            KustoDatabase8"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.kusto import KustoManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDatabases(AzureRMModuleBase):
    """Configuration class for an Azure RM Database resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
                type='str',
                required=True
            ),
            database_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            soft_delete_period_in_days=dict(
                type='int',
                required=True
            ),
            hot_cache_period_in_days=dict(
                type='int'
            ),
            statistics=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.cluster_name = None
        self.database_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDatabases, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "soft_delete_period_in_days":
                    self.parameters["soft_delete_period_in_days"] = kwargs[key]
                elif key == "hot_cache_period_in_days":
                    self.parameters["hot_cache_period_in_days"] = kwargs[key]
                elif key == "statistics":
                    self.parameters["statistics"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(KustoManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_database()

        if not old_response:
            self.log("Database instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Database instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Database instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Database instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_database()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Database instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_database()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_database():
                time.sleep(20)
        else:
            self.log("Database instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_database(self):
        '''
        Creates or updates Database with the specified configuration.

        :return: deserialized Database instance state dictionary
        '''
        self.log("Creating / Updating the Database instance {0}".format(self.database_name))

        try:
            response = self.mgmt_client.databases.create_or_update(resource_group_name=self.resource_group,
                                                                   cluster_name=self.cluster_name,
                                                                   database_name=self.database_name,
                                                                   parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Database instance.')
            self.fail("Error creating the Database instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_database(self):
        '''
        Deletes specified Database instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Database instance {0}".format(self.database_name))
        try:
            response = self.mgmt_client.databases.delete(resource_group_name=self.resource_group,
                                                         cluster_name=self.cluster_name,
                                                         database_name=self.database_name)
        except CloudError as e:
            self.log('Error attempting to delete the Database instance.')
            self.fail("Error deleting the Database instance: {0}".format(str(e)))

        return True

    def get_database(self):
        '''
        Gets the properties of the specified Database.

        :return: deserialized Database instance state dictionary
        '''
        self.log("Checking if the Database instance {0} is present".format(self.database_name))
        found = False
        try:
            response = self.mgmt_client.databases.get(resource_group_name=self.resource_group,
                                                      cluster_name=self.cluster_name,
                                                      database_name=self.database_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Database instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Database instance.')
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
    AzureRMDatabases()


if __name__ == '__main__':
    main()

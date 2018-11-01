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
module: azure_rm_sqlelasticpool
version_added: "2.8"
short_description: Manage SQL Elastic Pool instance.
description:
    - Create, update and delete instance of SQL Elastic Pool.

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
            - The name of the elastic pool.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
        suboptions:
            name:
                description:
                    - The name of the SKU. Ex - P3. It is typically a letter+number code
                required: True
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
    max_size_bytes:
        description:
            - The storage limit for the database elastic pool in bytes.
    per_database_settings:
        description:
            - The per database settings for the elastic pool.
        suboptions:
            min_capacity:
                description:
                    - The minimum capacity all databases are guaranteed.
            max_capacity:
                description:
                    - The maximum capacity any one database can consume.
    zone_redundant:
        description:
            - "Whether or not this elastic pool is zone redundant, which means the replicas of this elastic pool will be spread across multiple availability
               zones."
    license_type:
        description:
            - The license type to apply for this elastic pool.
        choices:
            - 'license_included'
            - 'base_price'
    state:
      description:
        - Assert the state of the SQL Elastic Pool.
        - Use 'present' to create or update an SQL Elastic Pool and 'absent' to delete it.
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
  - name: Create (or update) SQL Elastic Pool
    azure_rm_sqlelasticpool:
      resource_group: sqlcrudtest-2369
      server_name: sqlcrudtest-8069
      name: sqlcrudtest-8102
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-2369/providers/Microsoft.Sql/servers/sqlcrudtest-8069/elasticPool
            s/sqlcrudtest-8102"
state:
    description:
        - "The state of the elastic pool. Possible values include: 'Creating', 'Ready', 'Disabled'"
    returned: always
    type: str
    sample: Ready
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


class AzureRMElasticPools(AzureRMModuleBase):
    """Configuration class for an Azure RM SQL Elastic Pool resource"""

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
                type='dict'
            ),
            max_size_bytes=dict(
                type='int'
            ),
            per_database_settings=dict(
                type='dict'
            ),
            zone_redundant=dict(
                type='str'
            ),
            license_type=dict(
                type='str',
                choices=['license_included',
                         'base_price']
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

        super(AzureRMElasticPools, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "sku":
                    self.parameters["sku"] = kwargs[key]
                elif key == "max_size_bytes":
                    self.parameters["max_size_bytes"] = kwargs[key]
                elif key == "per_database_settings":
                    self.parameters["per_database_settings"] = kwargs[key]
                elif key == "zone_redundant":
                    self.parameters["zone_redundant"] = kwargs[key]
                elif key == "license_type":
                    self.parameters["license_type"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_sqlelasticpool()

        if not old_response:
            self.log("SQL Elastic Pool instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("SQL Elastic Pool instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if SQL Elastic Pool instance has to be deleted or may be updated")
                if ('zone_redundant' in self.parameters) and (self.parameters['zone_redundant'] != old_response['zone_redundant']):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the SQL Elastic Pool instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_sqlelasticpool()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("SQL Elastic Pool instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sqlelasticpool()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_sqlelasticpool():
                time.sleep(20)
        else:
            self.log("SQL Elastic Pool instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_sqlelasticpool(self):
        '''
        Creates or updates SQL Elastic Pool with the specified configuration.

        :return: deserialized SQL Elastic Pool instance state dictionary
        '''
        self.log("Creating / Updating the SQL Elastic Pool instance {0}".format(self.name))

        try:
            response = self.mgmt_client.elastic_pools.create_or_update(resource_group_name=self.resource_group,
                                                                       server_name=self.server_name,
                                                                       elastic_pool_name=self.name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the SQL Elastic Pool instance.')
            self.fail("Error creating the SQL Elastic Pool instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_sqlelasticpool(self):
        '''
        Deletes specified SQL Elastic Pool instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SQL Elastic Pool instance {0}".format(self.name))
        try:
            response = self.mgmt_client.elastic_pools.delete(resource_group_name=self.resource_group,
                                                             server_name=self.server_name,
                                                             elastic_pool_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the SQL Elastic Pool instance.')
            self.fail("Error deleting the SQL Elastic Pool instance: {0}".format(str(e)))

        return True

    def get_sqlelasticpool(self):
        '''
        Gets the properties of the specified SQL Elastic Pool.

        :return: deserialized SQL Elastic Pool instance state dictionary
        '''
        self.log("Checking if the SQL Elastic Pool instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.elastic_pools.get(resource_group_name=self.resource_group,
                                                          server_name=self.server_name,
                                                          elastic_pool_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SQL Elastic Pool instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SQL Elastic Pool instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMElasticPools()


if __name__ == '__main__':
    main()

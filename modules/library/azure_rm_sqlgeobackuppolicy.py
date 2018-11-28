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
module: azure_rm_sqlgeobackuppolicy
version_added: "2.8"
short_description: Manage Azure Geo Backup Policy instance.
description:
    - Create, update and delete instance of Azure Geo Backup Policy.

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
            - The name of the database.
        required: True
    name:
        description:
            - The name of the geo backup policy.
        required: True
    policy_state:
        description:
            - The state of the geo backup policy.
        required: True
        choices:
            - 'disabled'
            - 'enabled'
    state:
      description:
        - Assert the state of the Geo Backup Policy.
        - Use 'present' to create or update an Geo Backup Policy and 'absent' to delete it.
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
  - name: Create (or update) Geo Backup Policy
    azure_rm_sqlgeobackuppolicy:
      resource_group: sqlcrudtest-4799
      server_name: sqlcrudtest-5961
      database_name: testdw
      name: Default
      policy_state: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-4799/providers/Microsoft.Sql/servers/sqlcrudtest-5961/databases/t
            estdw/geoBackupPolicies/Default"
state:
    description:
        - "The state of the geo backup policy. Possible values include: 'Disabled', 'Enabled'"
    returned: always
    type: str
    sample: Enabled
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


class AzureRMGeoBackupPolicy(AzureRMModuleBase):
    """Configuration class for an Azure RM Geo Backup Policy resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            policy_state=dict(
                type='str',
                choices=['disabled',
                         'enabled'],
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
        self.database_name = None
        self.name = None
        self.policy_state = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGeoBackupPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_geobackuppolicy()

        if not old_response:
            self.log("Geo Backup Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Geo Backup Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Geo Backup Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_geobackuppolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Geo Backup Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_geobackuppolicy()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Geo Backup Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None)
                })
        return self.results

    def create_update_geobackuppolicy(self):
        '''
        Creates or updates Geo Backup Policy with the specified configuration.

        :return: deserialized Geo Backup Policy instance state dictionary
        '''
        self.log("Creating / Updating the Geo Backup Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.geo_backup_policies.create_or_update(resource_group_name=self.resource_group,
                                                                             server_name=self.server_name,
                                                                             database_name=self.database_name,
                                                                             geo_backup_policy_name=self.name,
                                                                             state=self.policy_state)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Geo Backup Policy instance.')
            self.fail("Error creating the Geo Backup Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_geobackuppolicy(self):
        '''
        Deletes specified Geo Backup Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Geo Backup Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.geo_backup_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Geo Backup Policy instance.')
            self.fail("Error deleting the Geo Backup Policy instance: {0}".format(str(e)))

        return True

    def get_geobackuppolicy(self):
        '''
        Gets the properties of the specified Geo Backup Policy.

        :return: deserialized Geo Backup Policy instance state dictionary
        '''
        self.log("Checking if the Geo Backup Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.geo_backup_policies.get(resource_group_name=self.resource_group,
                                                                server_name=self.server_name,
                                                                database_name=self.database_name,
                                                                geo_backup_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Geo Backup Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Geo Backup Policy instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMGeoBackupPolicy()


if __name__ == '__main__':
    main()

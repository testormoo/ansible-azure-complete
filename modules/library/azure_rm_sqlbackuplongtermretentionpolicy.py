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
module: azure_rm_sqlbackuplongtermretentionpolicy
version_added: "2.8"
short_description: Manage Backup Long Term Retention Policy instance.
description:
    - Create, update and delete instance of Backup Long Term Retention Policy.

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
            - The policy name. Should always be Default.
        required: True
    weekly_retention:
        description:
            - The weekly retention policy for an LTR backup in an ISO 8601 format.
    monthly_retention:
        description:
            - The montly retention policy for an LTR backup in an ISO 8601 format.
    yearly_retention:
        description:
            - The yearly retention policy for an LTR backup in an ISO 8601 format.
    week_of_year:
        description:
            - The week of year to take the yearly backup in an ISO 8601 format.
    state:
      description:
        - Assert the state of the Backup Long Term Retention Policy.
        - Use 'present' to create or update an Backup Long Term Retention Policy and 'absent' to delete it.
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
  - name: Create (or update) Backup Long Term Retention Policy
    azure_rm_sqlbackuplongtermretentionpolicy:
      resource_group: resourceGroup
      server_name: testserver
      database_name: testDatabase
      name: default
      weekly_retention: P1M
      monthly_retention: P1Y
      yearly_retention: P5Y
      week_of_year: 5
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/providers/Microsoft.Sql/resourceGroups/resourceGroup/servers/testserver/databases/testDataba
            se/backupLongTermRetentionPolicies/default"
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


class AzureRMBackupLongTermRetentionPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Backup Long Term Retention Policy resource"""

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
            weekly_retention=dict(
                type='str'
            ),
            monthly_retention=dict(
                type='str'
            ),
            yearly_retention=dict(
                type='str'
            ),
            week_of_year=dict(
                type='int'
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
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBackupLongTermRetentionPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "weekly_retention":
                    self.parameters["weekly_retention"] = kwargs[key]
                elif key == "monthly_retention":
                    self.parameters["monthly_retention"] = kwargs[key]
                elif key == "yearly_retention":
                    self.parameters["yearly_retention"] = kwargs[key]
                elif key == "week_of_year":
                    self.parameters["week_of_year"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_backuplongtermretentionpolicy()

        if not old_response:
            self.log("Backup Long Term Retention Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Backup Long Term Retention Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Backup Long Term Retention Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_backuplongtermretentionpolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Backup Long Term Retention Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_backuplongtermretentionpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_backuplongtermretentionpolicy():
                time.sleep(20)
        else:
            self.log("Backup Long Term Retention Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_backuplongtermretentionpolicy(self):
        '''
        Creates or updates Backup Long Term Retention Policy with the specified configuration.

        :return: deserialized Backup Long Term Retention Policy instance state dictionary
        '''
        self.log("Creating / Updating the Backup Long Term Retention Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.backup_long_term_retention_policies.create_or_update(resource_group_name=self.resource_group,
                                                                                             server_name=self.server_name,
                                                                                             database_name=self.database_name,
                                                                                             policy_name=self.name,
                                                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Backup Long Term Retention Policy instance.')
            self.fail("Error creating the Backup Long Term Retention Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_backuplongtermretentionpolicy(self):
        '''
        Deletes specified Backup Long Term Retention Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Backup Long Term Retention Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.backup_long_term_retention_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Backup Long Term Retention Policy instance.')
            self.fail("Error deleting the Backup Long Term Retention Policy instance: {0}".format(str(e)))

        return True

    def get_backuplongtermretentionpolicy(self):
        '''
        Gets the properties of the specified Backup Long Term Retention Policy.

        :return: deserialized Backup Long Term Retention Policy instance state dictionary
        '''
        self.log("Checking if the Backup Long Term Retention Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.backup_long_term_retention_policies.get(resource_group_name=self.resource_group,
                                                                                server_name=self.server_name,
                                                                                database_name=self.database_name,
                                                                                policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Backup Long Term Retention Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Backup Long Term Retention Policy instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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
    AzureRMBackupLongTermRetentionPolicies()


if __name__ == '__main__':
    main()

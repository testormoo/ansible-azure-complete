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
module: azure_rm_sqldatamaskingpolicy
version_added: "2.8"
short_description: Manage Data Masking Policy instance.
description:
    - Create, update and delete instance of Data Masking Policy.

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
            - The name of the database for which the data masking rule applies.
        required: True
    data_masking_state:
        description:
            - The state of the data masking policy.
        required: True
        choices:
            - 'disabled'
            - 'enabled'
    exempt_principals:
        description:
            - "The list of the exempt principals. Specifies the semicolon-separated list of database users for which the data masking policy does not apply.
               The specified users receive data results without masking for all of the database queries."
    state:
      description:
        - Assert the state of the Data Masking Policy.
        - Use 'present' to create or update an Data Masking Policy and 'absent' to delete it.
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
  - name: Create (or update) Data Masking Policy
    azure_rm_sqldatamaskingpolicy:
      resource_group: sqlcrudtest-6852
      server_name: sqlcrudtest-2080
      database_name: sqlcrudtest-331
      name: Default
      data_masking_state: NOT FOUND
      exempt_principals: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-6852/providers/Microsoft.Sql/servers/sqlcrudtest-2080/databases/s
            qlcrudtest-331/dataMaskingPolicies/Default"
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


class AzureRMDataMaskingPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Data Masking Policy resource"""

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
            data_masking_state=dict(
                type='str',
                choices=['disabled',
                         'enabled'],
                required=True
            ),
            exempt_principals=dict(
                type='str'
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
        self.data_masking_state = None
        self.exempt_principals = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDataMaskingPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_datamaskingpolicy()

        if not old_response:
            self.log("Data Masking Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Data Masking Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Data Masking Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_datamaskingpolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Data Masking Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_datamaskingpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_datamaskingpolicy():
                time.sleep(20)
        else:
            self.log("Data Masking Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_datamaskingpolicy(self):
        '''
        Creates or updates Data Masking Policy with the specified configuration.

        :return: deserialized Data Masking Policy instance state dictionary
        '''
        self.log("Creating / Updating the Data Masking Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.data_masking_policies.create_or_update(resource_group_name=self.resource_group,
                                                                               server_name=self.server_name,
                                                                               database_name=self.database_name,
                                                                               data_masking_policy_name=self.name,
                                                                               data_masking_state=self.data_masking_state)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Data Masking Policy instance.')
            self.fail("Error creating the Data Masking Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_datamaskingpolicy(self):
        '''
        Deletes specified Data Masking Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Data Masking Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.data_masking_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Data Masking Policy instance.')
            self.fail("Error deleting the Data Masking Policy instance: {0}".format(str(e)))

        return True

    def get_datamaskingpolicy(self):
        '''
        Gets the properties of the specified Data Masking Policy.

        :return: deserialized Data Masking Policy instance state dictionary
        '''
        self.log("Checking if the Data Masking Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.data_masking_policies.get(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  database_name=self.database_name,
                                                                  data_masking_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Data Masking Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Data Masking Policy instance.')
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
    AzureRMDataMaskingPolicies()


if __name__ == '__main__':
    main()

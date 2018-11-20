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
module: azure_rm_netapppool
version_added: "2.8"
short_description: Manage Pool instance.
description:
    - Create, update and delete instance of Pool.

options:
    body:
        description:
            - Capacity pool object supplied in the body of the operation.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                    - Required when C(state) is I(present).
            account_id:
                description:
                    - UUID v4 used to identify the Account
                    - Required when C(state) is I(present).
            size:
                description:
                    - Provisioned size of the pool (in GB)
            service_level:
                description:
                    - The service level of the file system.
                choices:
                    - 'basic'
                    - 'standard'
                    - 'premium'
    resource_group:
        description:
            - The name of the resource group.
        required: True
    account_name:
        description:
            - The name of the NetApp account
        required: True
    name:
        description:
            - The name of the capacity pool
        required: True
    state:
      description:
        - Assert the state of the Pool.
        - Use 'present' to create or update an Pool and 'absent' to delete it.
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
  - name: Create (or update) Pool
    azure_rm_netapppool:
      resource_group: resourceGroup
      account_name: accountName
      name: poolName
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.netapp import AzureNetAppFilesManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPools(AzureRMModuleBase):
    """Configuration class for an Azure RM Pool resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            body=dict(
                type='dict',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.body = dict()
        self.resource_group = None
        self.account_name = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPools, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.body["location"] = kwargs[key]
                elif key == "account_id":
                    self.body["account_id"] = kwargs[key]
                elif key == "size":
                    self.body["size"] = kwargs[key]
                elif key == "service_level":
                    self.body["service_level"] = _snake_to_camel(kwargs[key], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureNetAppFilesManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_pool()

        if not old_response:
            self.log("Pool instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Pool instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Pool instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_pool()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Pool instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_pool()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_pool():
                time.sleep(20)
        else:
            self.log("Pool instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_pool(self):
        '''
        Creates or updates Pool with the specified configuration.

        :return: deserialized Pool instance state dictionary
        '''
        self.log("Creating / Updating the Pool instance {0}".format(self.name))

        try:
            response = self.mgmt_client.pools.create_or_update(body=self.body,
                                                               resource_group=self.resource_group,
                                                               account_name=self.account_name,
                                                               pool_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Pool instance.')
            self.fail("Error creating the Pool instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_pool(self):
        '''
        Deletes specified Pool instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Pool instance {0}".format(self.name))
        try:
            response = self.mgmt_client.pools.delete(resource_group=self.resource_group,
                                                     account_name=self.account_name,
                                                     pool_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Pool instance.')
            self.fail("Error deleting the Pool instance: {0}".format(str(e)))

        return True

    def get_pool(self):
        '''
        Gets the properties of the specified Pool.

        :return: deserialized Pool instance state dictionary
        '''
        self.log("Checking if the Pool instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.pools.get(resource_group=self.resource_group,
                                                  account_name=self.account_name,
                                                  pool_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Pool instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Pool instance.')
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMPools()


if __name__ == '__main__':
    main()

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
module: azure_rm_searchquerykey
version_added: "2.8"
short_description: Manage Azure Query Key instance.
description:
    - Create, update and delete instance of Azure Query Key.

options:
    resource_group:
        description:
            - The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    search_service_name:
        description:
            - The name of the Azure Search service associated with the specified resource group.
        required: True
    name:
        description:
            - The name of the new query API key.
        required: True
    client_request_id:
        description:
            - "A client-generated GUID value that identifies this request. If specified, this will be included in response information as a way to track the
               request."
    state:
      description:
        - Assert the state of the Query Key.
        - Use 'present' to create or update an Query Key and 'absent' to delete it.
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
  - name: Create (or update) Query Key
    azure_rm_searchquerykey:
      resource_group: rg1
      search_service_name: mysearchservice
      name: Query key for browser-based clients
'''

RETURN = '''
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.search import SearchManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMQueryKey(AzureRMModuleBase):
    """Configuration class for an Azure RM Query Key resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            search_service_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            client_request_id=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.search_service_name = None
        self.name = None
        self.search_management_request_options = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMQueryKey, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.search_management_request_options[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SearchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_querykey()

        if not old_response:
            self.log("Query Key instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Query Key instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.search_management_request_options, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Query Key instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_querykey()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Query Key instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_querykey()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Query Key instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                })
        return self.results

    def create_update_querykey(self):
        '''
        Creates or updates Query Key with the specified configuration.

        :return: deserialized Query Key instance state dictionary
        '''
        self.log("Creating / Updating the Query Key instance {0}".format(self.search_management_request_options))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.query_keys.create(resource_group_name=self.resource_group,
                                                              search_service_name=self.search_service_name,
                                                              name=self.name)
            else:
                response = self.mgmt_client.query_keys.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Query Key instance.')
            self.fail("Error creating the Query Key instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_querykey(self):
        '''
        Deletes specified Query Key instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Query Key instance {0}".format(self.search_management_request_options))
        try:
            response = self.mgmt_client.query_keys.delete(resource_group_name=self.resource_group,
                                                          search_service_name=self.search_service_name,
                                                          key=self.key)
        except CloudError as e:
            self.log('Error attempting to delete the Query Key instance.')
            self.fail("Error deleting the Query Key instance: {0}".format(str(e)))

        return True

    def get_querykey(self):
        '''
        Gets the properties of the specified Query Key.

        :return: deserialized Query Key instance state dictionary
        '''
        self.log("Checking if the Query Key instance {0} is present".format(self.search_management_request_options))
        found = False
        try:
            response = self.mgmt_client.query_keys.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Query Key instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Query Key instance.')
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
    AzureRMQueryKey()


if __name__ == '__main__':
    main()

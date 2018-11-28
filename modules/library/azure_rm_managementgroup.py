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
module: azure_rm_managementgroup
version_added: "2.8"
short_description: Manage Azure Management Group instance.
description:
    - Create, update and delete instance of Azure Management Group.

options:
    group_id:
        description:
            - Management Group ID.
        required: True
    cache_control:
        description:
            - "Indicates that the request shouldn't utilize any caches."
    name:
        description:
            - The name of the management group. For example, 00000000-0000-0000-0000-000000000000
    display_name:
        description:
            - The friendly name of the management group. If no value is passed then this  field will be set to the I(group_id).
    details:
        description:
        suboptions:
            parent:
                description:
                suboptions:
                    id:
                        description:
                            - "The fully qualified ID for the parent management group.  For example,
                               /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000"
    state:
      description:
        - Assert the state of the Management Group.
        - Use 'present' to create or update an Management Group and 'absent' to delete it.
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
  - name: Create (or update) Management Group
    azure_rm_managementgroup:
      group_id: ChildGroup
      cache_control: no-cache
      name: ChildGroup
      display_name: ChildGroup
      details:
        parent:
          id: /providers/Microsoft.Management/managementGroups/RootGroup
'''

RETURN = '''
id:
    description:
        - The fully qualified ID for the management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
    returned: always
    type: str
    sample: /providers/Microsoft.Management/managementGroups/ChildGroup
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.managementgroups import ManagementGroupsAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagementGroup(AzureRMModuleBase):
    """Configuration class for an Azure RM Management Group resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            group_id=dict(
                type='str',
                required=True
            ),
            cache_control=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            display_name=dict(
                type='str'
            ),
            details=dict(
                type='dict',
                options=dict(
                    parent=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.group_id = None
        self.cache_control = None
        self.create_management_group_request = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagementGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.create_management_group_request[key] = kwargs[key]

        dict_resource_id(self.create_management_group_request, ['details', 'parent', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ManagementGroupsAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_managementgroup()

        if not old_response:
            self.log("Management Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Management Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.create_management_group_request, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Management Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managementgroup()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Management Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managementgroup()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Management Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_managementgroup(self):
        '''
        Creates or updates Management Group with the specified configuration.

        :return: deserialized Management Group instance state dictionary
        '''
        self.log("Creating / Updating the Management Group instance {0}".format(self.cache_control))

        try:
            response = self.mgmt_client.management_groups.create_or_update(group_id=self.group_id,
                                                                           create_management_group_request=self.create_management_group_request)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Management Group instance.')
            self.fail("Error creating the Management Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_managementgroup(self):
        '''
        Deletes specified Management Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Management Group instance {0}".format(self.cache_control))
        try:
            response = self.mgmt_client.management_groups.delete(group_id=self.group_id)
        except CloudError as e:
            self.log('Error attempting to delete the Management Group instance.')
            self.fail("Error deleting the Management Group instance: {0}".format(str(e)))

        return True

    def get_managementgroup(self):
        '''
        Gets the properties of the specified Management Group.

        :return: deserialized Management Group instance state dictionary
        '''
        self.log("Checking if the Management Group instance {0} is present".format(self.cache_control))
        found = False
        try:
            response = self.mgmt_client.management_groups.get(group_id=self.group_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Management Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Management Group instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMManagementGroup()


if __name__ == '__main__':
    main()

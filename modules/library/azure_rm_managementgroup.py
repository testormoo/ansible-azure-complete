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
short_description: Manage Management Group instance.
description:
    - Create, update and delete instance of Management Group.

options:
    group_id:
        description:
            - Management Group ID.
        required: True
    cache_control:
        description:
            - "Indicates that the request shouldn't utilize any caches."
    create_management_group_request:
        description:
            - Management group creation parameters.
        required: True
        suboptions:
            name:
                description:
                    - The name of the management group. For example, 00000000-0000-0000-0000-000000000000
            display_name:
                description:
                    - The friendly name of the management group. If no value is passed then this  field will be set to the groupId.
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
      create_management_group_request:
        name: ChildGroup
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


class AzureRMManagementGroups(AzureRMModuleBase):
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
            create_management_group_request=dict(
                type='dict',
                required=True
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

        super(AzureRMManagementGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "name":
                    self.create_management_group_request["name"] = kwargs[key]
                elif key == "display_name":
                    self.create_management_group_request["display_name"] = kwargs[key]
                elif key == "details":
                    self.create_management_group_request["details"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Management Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Management Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managementgroup()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Management Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managementgroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_managementgroup():
                time.sleep(20)
        else:
            self.log("Management Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
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

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMManagementGroups()


if __name__ == '__main__':
    main()

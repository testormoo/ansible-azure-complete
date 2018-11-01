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
module: azure_rm_migrategroup
version_added: "2.8"
short_description: Manage Group instance.
description:
    - Create, update and delete instance of Group.

options:
    resource_group:
        description:
            - Name of the Azure Resource I(group) that project is part of.
        required: True
    project_name:
        description:
            - Name of the Azure Migrate project.
        required: True
    group_name:
        description:
            - Unique name of a I(group) within a project.
        required: True
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.
    group:
        description:
            - New or Updated Group object.
        suboptions:
            e_tag:
                description:
                    - For optimistic concurrency control.
            machines:
                description:
                    - List of machine names that are part of this group.
                required: True
                type: list
    state:
      description:
        - Assert the state of the Group.
        - Use 'present' to create or update an Group and 'absent' to delete it.
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
  - name: Create (or update) Group
    azure_rm_migrategroup:
      resource_group: myResourceGroup
      project_name: project01
      group_name: group01
      self.config.accept_language: NOT FOUND
      group:
        e_tag: "1100637e-0000-0000-0000-59f6ed1f0000"
'''

RETURN = '''
id:
    description:
        - "Path reference to this group.
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}"
    returned: always
    type: str
    sample: /subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/groups/group01
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMGroups(AzureRMModuleBase):
    """Configuration class for an Azure RM Group resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            project_name=dict(
                type='str',
                required=True
            ),
            group_name=dict(
                type='str',
                required=True
            ),
            self.config.accept_language=dict(
                type='str'
            ),
            group=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.project_name = None
        self.group_name = None
        self.self.config.accept_language = None
        self.group = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "e_tag":
                    self.group["e_tag"] = kwargs[key]
                elif key == "machines":
                    self.group["machines"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_group()

        if not old_response:
            self.log("Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_group()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_group()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_group():
                time.sleep(20)
        else:
            self.log("Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_group(self):
        '''
        Creates or updates Group with the specified configuration.

        :return: deserialized Group instance state dictionary
        '''
        self.log("Creating / Updating the Group instance {0}".format(self.self.config.accept_language))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.groups.create(resource_group_name=self.resource_group,
                                                          project_name=self.project_name,
                                                          group_name=self.group_name)
            else:
                response = self.mgmt_client.groups.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Group instance.')
            self.fail("Error creating the Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_group(self):
        '''
        Deletes specified Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Group instance {0}".format(self.self.config.accept_language))
        try:
            response = self.mgmt_client.groups.delete(resource_group_name=self.resource_group,
                                                      project_name=self.project_name,
                                                      group_name=self.group_name)
        except CloudError as e:
            self.log('Error attempting to delete the Group instance.')
            self.fail("Error deleting the Group instance: {0}".format(str(e)))

        return True

    def get_group(self):
        '''
        Gets the properties of the specified Group.

        :return: deserialized Group instance state dictionary
        '''
        self.log("Checking if the Group instance {0} is present".format(self.self.config.accept_language))
        found = False
        try:
            response = self.mgmt_client.groups.get(resource_group_name=self.resource_group,
                                                   project_name=self.project_name,
                                                   group_name=self.group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Group instance.')
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
    AzureRMGroups()


if __name__ == '__main__':
    main()

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
module: azure_rm_csmproject
version_added: "2.8"
short_description: Manage Azure Project instance.
description:
    - Create, update and delete instance of Azure Project.

options:
    location:
        description:
            - Resource location.
    resource_group:
        description:
            - Name of the resource group within the Azure subscription.
        required: True
    root_resource_name:
        description:
            - Name of the Team Services account.
        required: True
    name:
        description:
            - Name of the Team Services project.
        required: True
    validating:
        description:
            - This parameter is ignored and should be set to an empty string.
    state:
      description:
        - Assert the state of the Project.
        - Use 'present' to create or update an Project and 'absent' to delete it.
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
  - name: Create (or update) Project
    azure_rm_csmproject:
      location: Central US
      resource_group: VS-Example-Group
      root_resource_name: ExampleAccount
      name: ExampleProject
      validating: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Unique identifier of the resource.
    returned: always
    type: str
    sample: "/subscriptions/0de7f055-dbea-498d-8e9e-da287eedca90/resourceGroups/VS-Example-Group/providers/microsoft.visualstudio/account/ExampleAccount/proj
            ect/ExampleProject"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.csm import VisualStudioResourceProviderClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMProject(AzureRMModuleBase):
    """Configuration class for an Azure RM Project resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            location=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            root_resource_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            validating=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.body = dict()
        self.resource_group = None
        self.root_resource_name = None
        self.name = None
        self.validating = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProject, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(VisualStudioResourceProviderClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_project()

        if not old_response:
            self.log("Project instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Project instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.body, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Project instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_project()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Project instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_project()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Project instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_project(self):
        '''
        Creates or updates Project with the specified configuration.

        :return: deserialized Project instance state dictionary
        '''
        self.log("Creating / Updating the Project instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.projects.create(body=self.body,
                                                            resource_group_name=self.resource_group,
                                                            root_resource_name=self.root_resource_name,
                                                            resource_name=self.name)
            else:
                response = self.mgmt_client.projects.update(resource_group_name=self.resource_group,
                                                            body=self.body,
                                                            root_resource_name=self.root_resource_name,
                                                            resource_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Project instance.')
            self.fail("Error creating the Project instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_project(self):
        '''
        Deletes specified Project instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Project instance {0}".format(self.name))
        try:
            response = self.mgmt_client.projects.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Project instance.')
            self.fail("Error deleting the Project instance: {0}".format(str(e)))

        return True

    def get_project(self):
        '''
        Gets the properties of the specified Project.

        :return: deserialized Project instance state dictionary
        '''
        self.log("Checking if the Project instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.projects.get(resource_group_name=self.resource_group,
                                                     root_resource_name=self.root_resource_name,
                                                     resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Project instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Project instance.')
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
            else:
                key = list(old[0])[0]
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


def main():
    """Main execution"""
    AzureRMProject()


if __name__ == '__main__':
    main()

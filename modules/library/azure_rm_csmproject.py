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
short_description: Manage Project instance.
description:
    - Create, update and delete instance of Project.

options:
    body:
        description:
            - The request data.
        required: True
        suboptions:
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
    resource_name:
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
      body:
        location: Central US
      resource_group: VS-Example-Group
      root_resource_name: ExampleAccount
      resource_name: ExampleProject
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


class AzureRMProjects(AzureRMModuleBase):
    """Configuration class for an Azure RM Project resource"""

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
            root_resource_name=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
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
        self.resource_name = None
        self.validating = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProjects, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = None
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
                self.log("Need to check if Project instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Project instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_project()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Project instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_project()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_project():
                time.sleep(20)
        else:
            self.log("Project instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_project(self):
        '''
        Creates or updates Project with the specified configuration.

        :return: deserialized Project instance state dictionary
        '''
        self.log("Creating / Updating the Project instance {0}".format(self.resource_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.projects.create(body=self.body,
                                                            resource_group_name=self.resource_group,
                                                            root_resource_name=self.root_resource_name,
                                                            resource_name=self.resource_name)
            else:
                response = self.mgmt_client.projects.update(resource_group_name=self.resource_group,
                                                            body=self.body,
                                                            root_resource_name=self.root_resource_name,
                                                            resource_name=self.resource_name)
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
        self.log("Deleting the Project instance {0}".format(self.resource_name))
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
        self.log("Checking if the Project instance {0} is present".format(self.resource_name))
        found = False
        try:
            response = self.mgmt_client.projects.get(resource_group_name=self.resource_group,
                                                     root_resource_name=self.root_resource_name,
                                                     resource_name=self.resource_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Project instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Project instance.')
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
    AzureRMProjects()


if __name__ == '__main__':
    main()

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
module: azure_rm_datamigrationproject
version_added: "2.8"
short_description: Manage Project instance.
description:
    - Create, update and delete instance of Project.

options:
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    source_platform:
        description:
            - Source platform for the project.
        required: True
        choices:
            - 'sql'
            - 'my_sql'
            - 'postgre_sql'
            - 'mongo_db'
            - 'unknown'
    target_platform:
        description:
            - Target platform for the project.
        required: True
        choices:
            - 'sqldb'
            - 'sqlmi'
            - 'azure_db_for_my_sql'
            - 'azure_db_for_postgre_sql'
            - 'mongo_db'
            - 'unknown'
    source_connection_info:
        description:
            - Information for connecting to source
        suboptions:
            user_name:
                description:
                    - User name
            password:
                description:
                    - Password credential.
            type:
                description:
                    - Constant filled by server.
                required: True
    target_connection_info:
        description:
            - Information for connecting to target
        suboptions:
            user_name:
                description:
                    - User name
            password:
                description:
                    - Password credential.
            type:
                description:
                    - Constant filled by server.
                required: True
    databases_info:
        description:
            - List of DatabaseInfo
        type: list
        suboptions:
            source_database_name:
                description:
                    - Name of the database
                required: True
    group_name:
        description:
            - Name of the resource group
        required: True
    service_name:
        description:
            - Name of the service
        required: True
    project_name:
        description:
            - Name of the project
        required: True
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
    azure_rm_datamigrationproject:
      location: eastus
      group_name: DmsSdkRg
      service_name: DmsSdkService
      project_name: DmsSdkProject
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/fc04246f-04c5-437e-ac5e-206a19e7193f/resourceGroups/DmsSdkRg/providers/Microsoft.DataMigration/services/DmsSdkService/projects/Dm
            sSdkProject"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datamigration import DataMigrationServiceClient
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
            location=dict(
                type='str'
            ),
            source_platform=dict(
                type='str',
                choices=['sql',
                         'my_sql',
                         'postgre_sql',
                         'mongo_db',
                         'unknown'],
                required=True
            ),
            target_platform=dict(
                type='str',
                choices=['sqldb',
                         'sqlmi',
                         'azure_db_for_my_sql',
                         'azure_db_for_postgre_sql',
                         'mongo_db',
                         'unknown'],
                required=True
            ),
            source_connection_info=dict(
                type='dict'
            ),
            target_connection_info=dict(
                type='dict'
            ),
            databases_info=dict(
                type='list'
            ),
            group_name=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            project_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.parameters = dict()
        self.group_name = None
        self.service_name = None
        self.project_name = None

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
                    self.parameters["location"] = kwargs[key]
                elif key == "source_platform":
                    ev = kwargs[key]
                    if ev == 'sql':
                        ev = 'SQL'
                    elif ev == 'my_sql':
                        ev = 'MySQL'
                    self.parameters["source_platform"] = _snake_to_camel(ev, True)
                elif key == "target_platform":
                    ev = kwargs[key]
                    if ev == 'sqldb':
                        ev = 'SQLDB'
                    elif ev == 'sqlmi':
                        ev = 'SQLMI'
                    self.parameters["target_platform"] = _snake_to_camel(ev, True)
                elif key == "source_connection_info":
                    self.parameters["source_connection_info"] = kwargs[key]
                elif key == "target_connection_info":
                    self.parameters["target_connection_info"] = kwargs[key]
                elif key == "databases_info":
                    self.parameters["databases_info"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataMigrationServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

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
        self.log("Creating / Updating the Project instance {0}".format(self.project_name))

        try:
            response = self.mgmt_client.projects.create_or_update(parameters=self.parameters,
                                                                  group_name=self.group_name,
                                                                  service_name=self.service_name,
                                                                  project_name=self.project_name)
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
        self.log("Deleting the Project instance {0}".format(self.project_name))
        try:
            response = self.mgmt_client.projects.delete(group_name=self.group_name,
                                                        service_name=self.service_name,
                                                        project_name=self.project_name)
        except CloudError as e:
            self.log('Error attempting to delete the Project instance.')
            self.fail("Error deleting the Project instance: {0}".format(str(e)))

        return True

    def get_project(self):
        '''
        Gets the properties of the specified Project.

        :return: deserialized Project instance state dictionary
        '''
        self.log("Checking if the Project instance {0} is present".format(self.project_name))
        found = False
        try:
            response = self.mgmt_client.projects.get(group_name=self.group_name,
                                                     service_name=self.service_name,
                                                     project_name=self.project_name)
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMProjects()


if __name__ == '__main__':
    main()

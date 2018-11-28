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
short_description: Manage Azure Project instance.
description:
    - Create, update and delete instance of Azure Project.

options:
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    source_platform:
        description:
            - Source platform for the project.
            - Required when C(state) is I(present).
        choices:
            - 'sql'
            - 'my_sql'
            - 'postgre_sql'
            - 'unknown'
    target_platform:
        description:
            - Target platform for the project.
            - Required when C(state) is I(present).
        choices:
            - 'sqldb'
            - 'sqlmi'
            - 'azure_db_for_my_sql'
            - 'azure_db_for_postgre_sql'
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
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
    databases_info:
        description:
            - List of DatabaseInfo
        type: list
        suboptions:
            source_database_name:
                description:
                    - Name of the database
                    - Required when C(state) is I(present).
    group_name:
        description:
            - Name of the resource group
        required: True
    service_name:
        description:
            - Name of the service
        required: True
    name:
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
      source_platform: SQL
      target_platform: SQLDB
      group_name: DmsSdkRg
      service_name: DmsSdkService
      name: DmsSdkProject
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMProject(AzureRMModuleBase):
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
                         'unknown']
            ),
            target_platform=dict(
                type='str',
                choices=['sqldb',
                         'sqlmi',
                         'azure_db_for_my_sql',
                         'azure_db_for_postgre_sql',
                         'unknown']
            ),
            source_connection_info=dict(
                type='dict',
                options=dict(
                    user_name=dict(
                        type='str'
                    ),
                    password=dict(
                        type='str',
                        no_log=True
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            target_connection_info=dict(
                type='dict',
                options=dict(
                    user_name=dict(
                        type='str'
                    ),
                    password=dict(
                        type='str',
                        no_log=True
                    ),
                    type=dict(
                        type='str'
                    )
                )
            ),
            databases_info=dict(
                type='list',
                options=dict(
                    source_database_name=dict(
                        type='str'
                    )
                )
            ),
            group_name=dict(
                type='str',
                required=True
            ),
            service_name=dict(
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

        self.parameters = dict()
        self.group_name = None
        self.service_name = None
        self.name = None

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
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['source_platform'], True)
        dict_map(self.parameters, ['source_platform'], {'sql': 'SQL', 'my_sql': 'MySQL'})
        dict_camelize(self.parameters, ['target_platform'], True)
        dict_map(self.parameters, ['target_platform'], {'sqldb': 'SQLDB', 'sqlmi': 'SQLMI'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            response = self.mgmt_client.projects.create_or_update(parameters=self.parameters,
                                                                  group_name=self.group_name,
                                                                  service_name=self.service_name,
                                                                  project_name=self.name)
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
            response = self.mgmt_client.projects.delete(group_name=self.group_name,
                                                        service_name=self.service_name,
                                                        project_name=self.name)
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
            response = self.mgmt_client.projects.get(group_name=self.group_name,
                                                     service_name=self.service_name,
                                                     project_name=self.name)
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


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def main():
    """Main execution"""
    AzureRMProject()


if __name__ == '__main__':
    main()

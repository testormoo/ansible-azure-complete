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
module: azure_rm_datamigrationtask
version_added: "2.8"
short_description: Manage Task instance.
description:
    - Create, update and delete instance of Task.

options:
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
    name:
        description:
            - Name of the Task
        required: True
    etag:
        description:
            - HTTP strong entity tag value. This is ignored if submitted.
    task_type:
        description:
            - Constant filled by server.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Task.
        - Use 'present' to create or update an Task and 'absent' to delete it.
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
  - name: Create (or update) Task
    azure_rm_datamigrationtask:
      group_name: DmsSdkRg
      service_name: DmsSdkService
      project_name: DmsSdkProject
      name: DmsSdkTask
      etag: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/fc04246f-04c5-437e-ac5e-206a19e7193f/resourceGroups/DmsSdkRg/providers/Microsoft.DataMigration/services/DmsSdkService/projects/Dm
            sSdkProject/tasks/DmsSdkTask"
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


class AzureRMTasks(AzureRMModuleBase):
    """Configuration class for an Azure RM Task resource"""

    def __init__(self):
        self.module_arg_spec = dict(
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
            name=dict(
                type='str',
                required=True
            ),
            etag=dict(
                type='str'
            ),
            task_type=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.group_name = None
        self.service_name = None
        self.project_name = None
        self.name = None
        self.etag = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMTasks, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "task_type":
                    self.properties["task_type"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataMigrationServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_task()

        if not old_response:
            self.log("Task instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Task instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Task instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_task()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Task instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_task()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_task():
                time.sleep(20)
        else:
            self.log("Task instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_task(self):
        '''
        Creates or updates Task with the specified configuration.

        :return: deserialized Task instance state dictionary
        '''
        self.log("Creating / Updating the Task instance {0}".format(self.name))

        try:
            response = self.mgmt_client.tasks.create_or_update(group_name=self.group_name,
                                                               service_name=self.service_name,
                                                               project_name=self.project_name,
                                                               task_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Task instance.')
            self.fail("Error creating the Task instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_task(self):
        '''
        Deletes specified Task instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Task instance {0}".format(self.name))
        try:
            response = self.mgmt_client.tasks.delete(group_name=self.group_name,
                                                     service_name=self.service_name,
                                                     project_name=self.project_name,
                                                     task_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Task instance.')
            self.fail("Error deleting the Task instance: {0}".format(str(e)))

        return True

    def get_task(self):
        '''
        Gets the properties of the specified Task.

        :return: deserialized Task instance state dictionary
        '''
        self.log("Checking if the Task instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.tasks.get(group_name=self.group_name,
                                                  service_name=self.service_name,
                                                  project_name=self.project_name,
                                                  task_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Task instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Task instance.')
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
    AzureRMTasks()


if __name__ == '__main__':
    main()

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
module: azure_rm_datamigrationfile
version_added: "2.8"
short_description: Manage File instance.
description:
    - Create, update and delete instance of File.

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
    file_name:
        description:
            - Name of the File
        required: True
    etag:
        description:
            - HTTP strong entity tag value. This is ignored if submitted.
    extension:
        description:
            - Optional File extension. If submitted it should not have a leading period and must match the extension from I(file_path).
    file_path:
        description:
            - Relative path of this file resource. This property can be set when creating or updating the file resource.
    media_type:
        description:
            - File content type. This propery can be modified to reflect the file content type.
    state:
      description:
        - Assert the state of the File.
        - Use 'present' to create or update an File and 'absent' to delete it.
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
  - name: Create (or update) File
    azure_rm_datamigrationfile:
      group_name: DmsSdkRg
      service_name: DmsSdkService
      project_name: DmsSdkProject
      file_name: x114d023d8
      etag: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/fc04246f-04c5-437e-ac5e-206a19e7193f/resourceGroups/DmsSdkRg/providers/Microsoft.DataMigration/services/DmsSdkService/projects/Dm
            sSdkProject/files/x114d023d8"
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


class AzureRMFiles(AzureRMModuleBase):
    """Configuration class for an Azure RM File resource"""

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
            file_name=dict(
                type='str',
                required=True
            ),
            etag=dict(
                type='str'
            ),
            extension=dict(
                type='str'
            ),
            file_path=dict(
                type='str'
            ),
            media_type=dict(
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
        self.file_name = None
        self.etag = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFiles, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "extension":
                    self.properties["extension"] = kwargs[key]
                elif key == "file_path":
                    self.properties["file_path"] = kwargs[key]
                elif key == "media_type":
                    self.properties["media_type"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataMigrationServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_file()

        if not old_response:
            self.log("File instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("File instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if File instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the File instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_file()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("File instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_file()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_file():
                time.sleep(20)
        else:
            self.log("File instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_file(self):
        '''
        Creates or updates File with the specified configuration.

        :return: deserialized File instance state dictionary
        '''
        self.log("Creating / Updating the File instance {0}".format(self.file_name))

        try:
            response = self.mgmt_client.files.create_or_update(group_name=self.group_name,
                                                               service_name=self.service_name,
                                                               project_name=self.project_name,
                                                               file_name=self.file_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the File instance.')
            self.fail("Error creating the File instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_file(self):
        '''
        Deletes specified File instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the File instance {0}".format(self.file_name))
        try:
            response = self.mgmt_client.files.delete(group_name=self.group_name,
                                                     service_name=self.service_name,
                                                     project_name=self.project_name,
                                                     file_name=self.file_name)
        except CloudError as e:
            self.log('Error attempting to delete the File instance.')
            self.fail("Error deleting the File instance: {0}".format(str(e)))

        return True

    def get_file(self):
        '''
        Gets the properties of the specified File.

        :return: deserialized File instance state dictionary
        '''
        self.log("Checking if the File instance {0} is present".format(self.file_name))
        found = False
        try:
            response = self.mgmt_client.files.get(group_name=self.group_name,
                                                  service_name=self.service_name,
                                                  project_name=self.project_name,
                                                  file_name=self.file_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("File instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the File instance.')
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
    AzureRMFiles()


if __name__ == '__main__':
    main()

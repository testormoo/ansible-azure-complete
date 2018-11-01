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
module: azure_rm_batchapplicationpackage
version_added: "2.8"
short_description: Manage Application Package instance.
description:
    - Create, update and delete instance of Application Package.

options:
    resource_group:
        description:
            - The name of the resource group that contains the Batch account.
        required: True
    account_name:
        description:
            - The name of the Batch account.
        required: True
    application_id:
        description:
            - The ID of the application.
        required: True
    version:
        description:
            - The version of the application.
        required: True
    state:
      description:
        - Assert the state of the Application Package.
        - Use 'present' to create or update an Application Package and 'absent' to delete it.
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
  - name: Create (or update) Application Package
    azure_rm_batchapplicationpackage:
      resource_group: default-azurebatch-japaneast
      account_name: sampleacct
      application_id: app1
      version: 1
'''

RETURN = '''
id:
    description:
        - The ID of the application.
    returned: always
    type: str
    sample: id
version:
    description:
        - The version of the application package.
    returned: always
    type: str
    sample: version
state:
    description:
        - "The current state of the application package. Possible values include: 'Pending', 'Active', 'Unmapped'"
    returned: always
    type: str
    sample: state
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.batch import BatchManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApplicationPackage(AzureRMModuleBase):
    """Configuration class for an Azure RM Application Package resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            application_id=dict(
                type='str',
                required=True
            ),
            version=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.application_id = None
        self.version = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApplicationPackage, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BatchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_applicationpackage()

        if not old_response:
            self.log("Application Package instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Application Package instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Application Package instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Application Package instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_applicationpackage()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Application Package instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_applicationpackage()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_applicationpackage():
                time.sleep(20)
        else:
            self.log("Application Package instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_applicationpackage(self):
        '''
        Creates or updates Application Package with the specified configuration.

        :return: deserialized Application Package instance state dictionary
        '''
        self.log("Creating / Updating the Application Package instance {0}".format(self.version))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.application_package.create(resource_group_name=self.resource_group,
                                                                       account_name=self.account_name,
                                                                       application_id=self.application_id,
                                                                       version=self.version)
            else:
                response = self.mgmt_client.application_package.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Application Package instance.')
            self.fail("Error creating the Application Package instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_applicationpackage(self):
        '''
        Deletes specified Application Package instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Application Package instance {0}".format(self.version))
        try:
            response = self.mgmt_client.application_package.delete(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   application_id=self.application_id,
                                                                   version=self.version)
        except CloudError as e:
            self.log('Error attempting to delete the Application Package instance.')
            self.fail("Error deleting the Application Package instance: {0}".format(str(e)))

        return True

    def get_applicationpackage(self):
        '''
        Gets the properties of the specified Application Package.

        :return: deserialized Application Package instance state dictionary
        '''
        self.log("Checking if the Application Package instance {0} is present".format(self.version))
        found = False
        try:
            response = self.mgmt_client.application_package.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                application_id=self.application_id,
                                                                version=self.version)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Application Package instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Application Package instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'version': d.get('version', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMApplicationPackage()


if __name__ == '__main__':
    main()

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
module: azure_rm_azurestackregistration
version_added: "2.8"
short_description: Manage Registration instance.
description:
    - Create, update and delete instance of Registration.

options:
    resource_group:
        description:
            - Name of the resource group.
        required: True
    registration_name:
        description:
            - Name of the Azure Stack registration.
        required: True
    token:
        description:
            - Registration token
        required: True
        suboptions:
            registration_token:
                description:
                    - The token identifying registered Azure Stack
                required: True
            location:
                description:
                    - Location of the resource.
                choices:
                    - 'global'
    state:
      description:
        - Assert the state of the Registration.
        - Use 'present' to create or update an Registration and 'absent' to delete it.
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
  - name: Create (or update) Registration
    azure_rm_azurestackregistration:
      resource_group: azurestack
      registration_name: testregistration
      token:
        location: global
'''

RETURN = '''
id:
    description:
        - ID of the resource.
    returned: always
    type: str
    sample: /subscriptions/dd8597b4-8739-4467-8b10-f8679f62bfbf/resourceGroups/azurestack/providers/Microsoft.AzureStack/registrations/testregistration
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.azurestack import AzureStackManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRegistrations(AzureRMModuleBase):
    """Configuration class for an Azure RM Registration resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registration_name=dict(
                type='str',
                required=True
            ),
            token=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.registration_name = None
        self.token = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRegistrations, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "registration_token":
                    self.token["registration_token"] = kwargs[key]
                elif key == "location":
                    self.token["location"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureStackManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_registration()

        if not old_response:
            self.log("Registration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Registration instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Registration instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Registration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_registration()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Registration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_registration()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_registration():
                time.sleep(20)
        else:
            self.log("Registration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_registration(self):
        '''
        Creates or updates Registration with the specified configuration.

        :return: deserialized Registration instance state dictionary
        '''
        self.log("Creating / Updating the Registration instance {0}".format(self.registration_name))

        try:
            response = self.mgmt_client.registrations.create_or_update(resource_group=self.resource_group,
                                                                       registration_name=self.registration_name,
                                                                       token=self.token)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Registration instance.')
            self.fail("Error creating the Registration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_registration(self):
        '''
        Deletes specified Registration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Registration instance {0}".format(self.registration_name))
        try:
            response = self.mgmt_client.registrations.delete(resource_group=self.resource_group,
                                                             registration_name=self.registration_name)
        except CloudError as e:
            self.log('Error attempting to delete the Registration instance.')
            self.fail("Error deleting the Registration instance: {0}".format(str(e)))

        return True

    def get_registration(self):
        '''
        Gets the properties of the specified Registration.

        :return: deserialized Registration instance state dictionary
        '''
        self.log("Checking if the Registration instance {0} is present".format(self.registration_name))
        found = False
        try:
            response = self.mgmt_client.registrations.get(resource_group=self.resource_group,
                                                          registration_name=self.registration_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Registration instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Registration instance.')
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
    AzureRMRegistrations()


if __name__ == '__main__':
    main()

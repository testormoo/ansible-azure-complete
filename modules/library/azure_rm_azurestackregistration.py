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
    name:
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
                    - Required when C(state) is I(present).
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
      name: testregistration
      token:
        registration_token: EyjIAWXSAw5nTw9KZWWiOiJeZxZlbg9wBwvUdCiSIM9iaMVjdeLkijoinwIzyJa2Ytgtowm2yy00OdG4lTlLyJmtztHjZGfJZTC0NZK1iIWiY2XvdWRJzCi6iJy5nDy0oDk1LTNHmWeTnDUwyS05oDI0LTrINzYwoGq5mjAzziIsim1HCmtldHBsYwnLu3LuZGljYXrpB25FBmfIbgVkIJp0CNvLLCJOYXJkd2FYzuLUZM8iOlt7IM51bunvcMVZiJoYlCjcaw9ZiJPBIjNkzDJHmda3yte5ndqZMdq4YmZkZmi5oDM3OTY3ZwNMIL0SIM5PyYI6WyJLZTy0ztJJMwZKy2m0OWNLODDLMwm2zTm0ymzKyjmWySisiJA3njlHmtdlY2q4NjRjnwFIZtC1YZi5ZGyZodM3Y2vjIl0siMnwDsi6wyi2oDUZoTbiY2RhNDa0ymrKoWe4YtK5otblzWrJzGyzNCISIjmYnzC4M2vmnZdIoDRKM2i5ytfkmJlhnDc1zdhLzWm1il0sim5HBwuiOijIqzF1MTvhmDIXmIIsimrpc2SiolsioWNlZjVhnZM1otQ0nDu3NmjlN2M3zmfjzmyZMTJhZtiiLcjLZjLmmZJhmWVhytG0NTu0OTqZNWu1Mda0MZbIYtfjyijdLCj1DWlKijoinwM5Mwu3NjytMju5Os00oTIwlWi0OdmTnGzHotiWm2RjyTCxIIwiBWvTb3J5ijPbijAYZDA3M2fjNzu0YTRMZTfhodkxzDnkogY5ZtAWzdyXIiwINZcWzThLnDQ4otrJndAzZGI5MGzlYtY1ZJA5ZdfiNMQIXX1DlcJpC3n1zxiiOijZb21lB25LIIWIdmVyC2LVbiI6IJeuMcJ9
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
            name=dict(
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
        self.name = None
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
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Registration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_registration()

            self.results['changed'] = True
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
        self.log("Creating / Updating the Registration instance {0}".format(self.name))

        try:
            response = self.mgmt_client.registrations.create_or_update(resource_group=self.resource_group,
                                                                       registration_name=self.name,
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
        self.log("Deleting the Registration instance {0}".format(self.name))
        try:
            response = self.mgmt_client.registrations.delete(resource_group=self.resource_group,
                                                             registration_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Registration instance.')
            self.fail("Error deleting the Registration instance: {0}".format(str(e)))

        return True

    def get_registration(self):
        '''
        Gets the properties of the specified Registration.

        :return: deserialized Registration instance state dictionary
        '''
        self.log("Checking if the Registration instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.registrations.get(resource_group=self.resource_group,
                                                          registration_name=self.name)
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
    AzureRMRegistrations()


if __name__ == '__main__':
    main()

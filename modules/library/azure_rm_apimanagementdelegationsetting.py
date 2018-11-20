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
module: azure_rm_apimanagementdelegationsetting
version_added: "2.8"
short_description: Manage Delegation Setting instance.
description:
    - Create, update and delete instance of Delegation Setting.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    url:
        description:
            - A delegation Url.
    validation_key:
        description:
            - A base64-encoded validation key to validate, that a request is coming from Azure API Management.
    subscriptions:
        description:
            - Subscriptions delegation settings.
        suboptions:
            enabled:
                description:
                    - Enable or disable delegation for subscriptions.
    user_registration:
        description:
            - User registration delegation settings.
        suboptions:
            enabled:
                description:
                    - Enable or disable delegation for user registration.
    state:
      description:
        - Assert the state of the Delegation Setting.
        - Use 'present' to create or update an Delegation Setting and 'absent' to delete it.
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
  - name: Create (or update) Delegation Setting
    azure_rm_apimanagementdelegationsetting:
      resource_group: rg1
      name: apimService1
      url: http://contoso.com/delegation
      validation_key: nVF7aKIvr9mV/RM5lOD0sYoi8ThXTRHQP7o66hvUmjCDkPKR3qxPu/otJcNciz2aQdqPuzJH3ECG4TU2yZjQ7Q==
      subscriptions:
        enabled: True
      user_registration:
        enabled: True
'''

RETURN = '''
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDelegationSettings(AzureRMModuleBase):
    """Configuration class for an Azure RM Delegation Setting resource"""

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
            url=dict(
                type='str'
            ),
            validation_key=dict(
                type='str'
            ),
            subscriptions=dict(
                type='dict'
            ),
            user_registration=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDelegationSettings, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "url":
                    self.parameters["url"] = kwargs[key]
                elif key == "validation_key":
                    self.parameters["validation_key"] = kwargs[key]
                elif key == "subscriptions":
                    self.parameters["subscriptions"] = kwargs[key]
                elif key == "user_registration":
                    self.parameters["user_registration"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_delegationsetting()

        if not old_response:
            self.log("Delegation Setting instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Delegation Setting instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Delegation Setting instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_delegationsetting()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Delegation Setting instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_delegationsetting()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_delegationsetting():
                time.sleep(20)
        else:
            self.log("Delegation Setting instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_delegationsetting(self):
        '''
        Creates or updates Delegation Setting with the specified configuration.

        :return: deserialized Delegation Setting instance state dictionary
        '''
        self.log("Creating / Updating the Delegation Setting instance {0}".format(self.name))

        try:
            response = self.mgmt_client.delegation_settings.create_or_update(resource_group_name=self.resource_group,
                                                                             service_name=self.name,
                                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Delegation Setting instance.')
            self.fail("Error creating the Delegation Setting instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_delegationsetting(self):
        '''
        Deletes specified Delegation Setting instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Delegation Setting instance {0}".format(self.name))
        try:
            response = self.mgmt_client.delegation_settings.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Delegation Setting instance.')
            self.fail("Error deleting the Delegation Setting instance: {0}".format(str(e)))

        return True

    def get_delegationsetting(self):
        '''
        Gets the properties of the specified Delegation Setting.

        :return: deserialized Delegation Setting instance state dictionary
        '''
        self.log("Checking if the Delegation Setting instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.delegation_settings.get(resource_group_name=self.resource_group,
                                                                service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Delegation Setting instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Delegation Setting instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
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
    AzureRMDelegationSettings()


if __name__ == '__main__':
    main()

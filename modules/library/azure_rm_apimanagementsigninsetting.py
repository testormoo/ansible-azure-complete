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
module: azure_rm_apimanagementsigninsetting
version_added: "2.8"
short_description: Manage Sign In Setting instance.
description:
    - Create, update and delete instance of Sign In Setting.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    enabled:
        description:
            - Redirect Anonymous users to the Sign-In page.
    state:
      description:
        - Assert the state of the Sign In Setting.
        - Use 'present' to create or update an Sign In Setting and 'absent' to delete it.
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
  - name: Create (or update) Sign In Setting
    azure_rm_apimanagementsigninsetting:
      resource_group: rg1
      service_name: apimService1
      enabled: NOT FOUND
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


class AzureRMSignInSettings(AzureRMModuleBase):
    """Configuration class for an Azure RM Sign In Setting resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            enabled=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.service_name = None
        self.enabled = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSignInSettings, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_signinsetting()

        if not old_response:
            self.log("Sign In Setting instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Sign In Setting instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Sign In Setting instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Sign In Setting instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_signinsetting()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Sign In Setting instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_signinsetting()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_signinsetting():
                time.sleep(20)
        else:
            self.log("Sign In Setting instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_signinsetting(self):
        '''
        Creates or updates Sign In Setting with the specified configuration.

        :return: deserialized Sign In Setting instance state dictionary
        '''
        self.log("Creating / Updating the Sign In Setting instance {0}".format(self.service_name))

        try:
            response = self.mgmt_client.sign_in_settings.create_or_update(resource_group_name=self.resource_group,
                                                                          service_name=self.service_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Sign In Setting instance.')
            self.fail("Error creating the Sign In Setting instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_signinsetting(self):
        '''
        Deletes specified Sign In Setting instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Sign In Setting instance {0}".format(self.service_name))
        try:
            response = self.mgmt_client.sign_in_settings.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Sign In Setting instance.')
            self.fail("Error deleting the Sign In Setting instance: {0}".format(str(e)))

        return True

    def get_signinsetting(self):
        '''
        Gets the properties of the specified Sign In Setting.

        :return: deserialized Sign In Setting instance state dictionary
        '''
        self.log("Checking if the Sign In Setting instance {0} is present".format(self.service_name))
        found = False
        try:
            response = self.mgmt_client.sign_in_settings.get(resource_group_name=self.resource_group,
                                                             service_name=self.service_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Sign In Setting instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Sign In Setting instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMSignInSettings()


if __name__ == '__main__':
    main()
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
module: azure_rm_apimanagementidentityprovider
version_added: "2.8"
short_description: Manage Identity Provider instance.
description:
    - Create, update and delete instance of Identity Provider.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    name:
        description:
            - Identity Provider Type identifier.
        required: True
        choices:
            - 'facebook'
            - 'google'
            - 'microsoft'
            - 'twitter'
            - 'aad'
            - 'aad_b2_c'
    identity_provider_contract_type:
        description:
            - Identity Provider Type identifier.
        choices:
            - 'facebook'
            - 'google'
            - 'microsoft'
            - 'twitter'
            - 'aad'
            - 'aad_b2_c'
    allowed_tenants:
        description:
            - List of Allowed Tenants when configuring Azure Active Directory login.
        type: list
    signup_policy_name:
        description:
            - Signup Policy Name. Only applies to C(C(aad)) B2C Identity Provider.
    signin_policy_name:
        description:
            - Signin Policy Name. Only applies to C(C(aad)) B2C Identity Provider.
    profile_editing_policy_name:
        description:
            - Profile Editing Policy Name. Only applies to C(C(aad)) B2C Identity Provider.
    password_reset_policy_name:
        description:
            - Password Reset Policy Name. Only applies to C(C(aad)) B2C Identity Provider.
    client_id:
        description:
            - "Client Id of the Application in the external Identity Provider. It is App ID for C(C(facebook)) login, Client ID for C(C(google)) login, App
               ID for C(C(microsoft))."
            - Required when C(state) is I(present).
    client_secret:
        description:
            - "Client secret of the Application in external Identity Provider, used to authenticate login request. For example, it is App Secret for
               C(C(facebook)) login, API Key for C(C(google)) login, Public Key for C(C(microsoft))."
            - Required when C(state) is I(present).
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Identity Provider.
        - Use 'present' to create or update an Identity Provider and 'absent' to delete it.
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
  - name: Create (or update) Identity Provider
    azure_rm_apimanagementidentityprovider:
      resource_group: rg1
      service_name: apimService1
      name: facebook
      client_id: facebookid
      client_secret: facebookapplicationsecret
      if_match: NOT FOUND
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


class AzureRMIdentityProvider(AzureRMModuleBase):
    """Configuration class for an Azure RM Identity Provider resource"""

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
            name=dict(
                type='str',
                choices=['facebook',
                         'google',
                         'microsoft',
                         'twitter',
                         'aad',
                         'aad_b2_c'],
                required=True
            ),
            identity_provider_contract_type=dict(
                type='str',
                choices=['facebook',
                         'google',
                         'microsoft',
                         'twitter',
                         'aad',
                         'aad_b2_c']
            ),
            allowed_tenants=dict(
                type='list'
            ),
            signup_policy_name=dict(
                type='str'
            ),
            signin_policy_name=dict(
                type='str'
            ),
            profile_editing_policy_name=dict(
                type='str'
            ),
            password_reset_policy_name=dict(
                type='str',
                no_log=True
            ),
            client_id=dict(
                type='str'
            ),
            client_secret=dict(
                type='str'
            ),
            if_match=dict(
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
        self.name = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIdentityProvider, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "identity_provider_contract_type":
                    ev = kwargs[key]
                    if ev == 'aad_b2_c':
                        ev = 'aadB2C'
                    self.parameters["identity_provider_contract_type"] = ev
                elif key == "allowed_tenants":
                    self.parameters["allowed_tenants"] = kwargs[key]
                elif key == "signup_policy_name":
                    self.parameters["signup_policy_name"] = kwargs[key]
                elif key == "signin_policy_name":
                    self.parameters["signin_policy_name"] = kwargs[key]
                elif key == "profile_editing_policy_name":
                    self.parameters["profile_editing_policy_name"] = kwargs[key]
                elif key == "password_reset_policy_name":
                    self.parameters["password_reset_policy_name"] = kwargs[key]
                elif key == "client_id":
                    self.parameters["client_id"] = kwargs[key]
                elif key == "client_secret":
                    self.parameters["client_secret"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_identityprovider()

        if not old_response:
            self.log("Identity Provider instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Identity Provider instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Identity Provider instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_identityprovider()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Identity Provider instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_identityprovider()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_identityprovider():
                time.sleep(20)
        else:
            self.log("Identity Provider instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_identityprovider(self):
        '''
        Creates or updates Identity Provider with the specified configuration.

        :return: deserialized Identity Provider instance state dictionary
        '''
        self.log("Creating / Updating the Identity Provider instance {0}".format(self.name))

        try:
            response = self.mgmt_client.identity_provider.create_or_update(resource_group_name=self.resource_group,
                                                                           service_name=self.service_name,
                                                                           identity_provider_name=self.name,
                                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Identity Provider instance.')
            self.fail("Error creating the Identity Provider instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_identityprovider(self):
        '''
        Deletes specified Identity Provider instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Identity Provider instance {0}".format(self.name))
        try:
            response = self.mgmt_client.identity_provider.delete(resource_group_name=self.resource_group,
                                                                 service_name=self.service_name,
                                                                 identity_provider_name=self.name,
                                                                 if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Identity Provider instance.')
            self.fail("Error deleting the Identity Provider instance: {0}".format(str(e)))

        return True

    def get_identityprovider(self):
        '''
        Gets the properties of the specified Identity Provider.

        :return: deserialized Identity Provider instance state dictionary
        '''
        self.log("Checking if the Identity Provider instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.identity_provider.get(resource_group_name=self.resource_group,
                                                              service_name=self.service_name,
                                                              identity_provider_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Identity Provider instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Identity Provider instance.')
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
    AzureRMIdentityProvider()


if __name__ == '__main__':
    main()

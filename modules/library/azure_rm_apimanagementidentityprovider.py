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
short_description: Manage Azure Identity Provider instance.
description:
    - Create, update and delete instance of Azure Identity Provider.

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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['identity_provider_contract_type'], True)
        dict_map(self.parameters, ['identity_provider_contract_type'], {'aad_b2_c': 'aadB2C'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Identity Provider instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                })
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
            else:
                key = list(old[0])[0]
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
    AzureRMIdentityProvider()


if __name__ == '__main__':
    main()

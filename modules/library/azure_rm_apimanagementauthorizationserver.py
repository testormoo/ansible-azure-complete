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
module: azure_rm_apimanagementauthorizationserver
version_added: "2.8"
short_description: Manage Azure Authorization Server instance.
description:
    - Create, update and delete instance of Azure Authorization Server.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    authsid:
        description:
            - Identifier of the authorization server.
        required: True
    description:
        description:
            - Description of the authorization server. Can contain HTML formatting tags.
    authorization_methods:
        description:
            - HTTP verbs supported by the authorization endpoint. GET must be always present. POST is optional.
        type: list
    client_authentication_method:
        description:
            - "Method of authentication supported by the token endpoint of this authorization server. Possible values are Basic and/or Body. When Body is
               specified, client credentials and other parameters are passed within the request body in the application/x-www-form-urlencoded format."
        type: list
    token_body_parameters:
        description:
            - "Additional parameters required by the token endpoint of this authorization server represented as an array of JSON objects with name and value
               string properties, i.e. {'name' : 'name value', 'value': 'a value'}."
        type: list
        suboptions:
            name:
                description:
                    - body parameter name.
                    - Required when C(state) is I(present).
            value:
                description:
                    - body parameter value.
                    - Required when C(state) is I(present).
    token_endpoint:
        description:
            - OAuth token endpoint. Contains absolute URI to entity being referenced.
    support_state:
        description:
            - "If true, authorization server will include state parameter from the authorization request to its response. Client may use state parameter to
               raise protocol security."
    default_scope:
        description:
            - "Access token scope that is going to be requested by default. Can be overridden at the API level. Should be provided in the form of a string
               containing space-delimited values."
    bearer_token_sending_methods:
        description:
            - Specifies the mechanism by which access token is passed to the API.
        type: list
    client_secret:
        description:
            - Client or app secret registered with this authorization server.
    resource_owner_username:
        description:
            - Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner username.
    resource_owner_password:
        description:
            - Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner password.
    display_name:
        description:
            - User-friendly authorization server name.
            - Required when C(state) is I(present).
    client_registration_endpoint:
        description:
            - "Optional reference to a page where client or app registration for this authorization server is performed. Contains absolute URL to entity
               being referenced."
            - Required when C(state) is I(present).
    authorization_endpoint:
        description:
            - "OAuth authorization endpoint. See http://tools.ietf.org/html/rfc6749#section-3.2."
            - Required when C(state) is I(present).
    grant_types:
        description:
            - Form of an authorization grant, which the client uses to request the access token.
            - Required when C(state) is I(present).
        type: list
    client_id:
        description:
            - Client or app id registered with this authorization server.
            - Required when C(state) is I(present).
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Authorization Server.
        - Use 'present' to create or update an Authorization Server and 'absent' to delete it.
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
  - name: Create (or update) Authorization Server
    azure_rm_apimanagementauthorizationserver:
      resource_group: rg1
      name: apimService1
      authsid: newauthServer
      description: test server
      authorization_methods:
        - [
  "GET"
]
      token_endpoint: https://www.contoso.com/oauth2/token
      support_state: True
      default_scope: read write
      bearer_token_sending_methods:
        - [
  "authorizationHeader"
]
      client_secret: 2
      resource_owner_username: un
      resource_owner_password: pwd
      display_name: test2
      client_registration_endpoint: https://www.contoso.com/apps
      authorization_endpoint: https://www.contoso.com/oauth2/auth
      grant_types:
        - [
  "authorizationCode",
  "implicit"
]
      client_id: 1
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


class AzureRMAuthorizationServer(AzureRMModuleBase):
    """Configuration class for an Azure RM Authorization Server resource"""

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
            authsid=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            authorization_methods=dict(
                type='list'
            ),
            client_authentication_method=dict(
                type='list'
            ),
            token_body_parameters=dict(
                type='list'
            ),
            token_endpoint=dict(
                type='str'
            ),
            support_state=dict(
                type='str'
            ),
            default_scope=dict(
                type='str'
            ),
            bearer_token_sending_methods=dict(
                type='list'
            ),
            client_secret=dict(
                type='str'
            ),
            resource_owner_username=dict(
                type='str'
            ),
            resource_owner_password=dict(
                type='str',
                no_log=True
            ),
            display_name=dict(
                type='str'
            ),
            client_registration_endpoint=dict(
                type='str'
            ),
            authorization_endpoint=dict(
                type='str'
            ),
            grant_types=dict(
                type='list'
            ),
            client_id=dict(
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
        self.name = None
        self.authsid = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAuthorizationServer, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_authorizationserver()

        if not old_response:
            self.log("Authorization Server instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Authorization Server instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Authorization Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_authorizationserver()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Authorization Server instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_authorizationserver()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_authorizationserver():
                time.sleep(20)
        else:
            self.log("Authorization Server instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_authorizationserver(self):
        '''
        Creates or updates Authorization Server with the specified configuration.

        :return: deserialized Authorization Server instance state dictionary
        '''
        self.log("Creating / Updating the Authorization Server instance {0}".format(self.authsid))

        try:
            response = self.mgmt_client.authorization_server.create_or_update(resource_group_name=self.resource_group,
                                                                              service_name=self.name,
                                                                              authsid=self.authsid,
                                                                              parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Authorization Server instance.')
            self.fail("Error creating the Authorization Server instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_authorizationserver(self):
        '''
        Deletes specified Authorization Server instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Authorization Server instance {0}".format(self.authsid))
        try:
            response = self.mgmt_client.authorization_server.delete(resource_group_name=self.resource_group,
                                                                    service_name=self.name,
                                                                    authsid=self.authsid,
                                                                    if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Authorization Server instance.')
            self.fail("Error deleting the Authorization Server instance: {0}".format(str(e)))

        return True

    def get_authorizationserver(self):
        '''
        Gets the properties of the specified Authorization Server.

        :return: deserialized Authorization Server instance state dictionary
        '''
        self.log("Checking if the Authorization Server instance {0} is present".format(self.authsid))
        found = False
        try:
            response = self.mgmt_client.authorization_server.get(resource_group_name=self.resource_group,
                                                                 service_name=self.name,
                                                                 authsid=self.authsid)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Authorization Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Authorization Server instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
        }
        return d


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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
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


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMAuthorizationServer()


if __name__ == '__main__':
    main()

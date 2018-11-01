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
short_description: Manage Authorization Server instance.
description:
    - Create, update and delete instance of Authorization Server.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
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
                required: True
            value:
                description:
                    - body parameter value.
                required: True
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
        required: True
    client_registration_endpoint:
        description:
            - "Optional reference to a page where client or app registration for this authorization server is performed. Contains absolute URL to entity
               being referenced."
        required: True
    authorization_endpoint:
        description:
            - "OAuth authorization endpoint. See http://tools.ietf.org/html/rfc6749#section-3.2."
        required: True
    grant_types:
        description:
            - Form of an authorization grant, which the client uses to request the access token.
        required: True
        type: list
    client_id:
        description:
            - Client or app id registered with this authorization server.
        required: True
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
      service_name: apimService1
      authsid: newauthServer
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
            service_name=dict(
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
                type='str',
                required=True
            ),
            client_registration_endpoint=dict(
                type='str',
                required=True
            ),
            authorization_endpoint=dict(
                type='str',
                required=True
            ),
            grant_types=dict(
                type='list',
                required=True
            ),
            client_id=dict(
                type='str',
                required=True
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

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "authorization_methods":
                    self.parameters["authorization_methods"] = kwargs[key]
                elif key == "client_authentication_method":
                    self.parameters["client_authentication_method"] = kwargs[key]
                elif key == "token_body_parameters":
                    self.parameters["token_body_parameters"] = kwargs[key]
                elif key == "token_endpoint":
                    self.parameters["token_endpoint"] = kwargs[key]
                elif key == "support_state":
                    self.parameters["support_state"] = kwargs[key]
                elif key == "default_scope":
                    self.parameters["default_scope"] = kwargs[key]
                elif key == "bearer_token_sending_methods":
                    self.parameters["bearer_token_sending_methods"] = kwargs[key]
                elif key == "client_secret":
                    self.parameters["client_secret"] = kwargs[key]
                elif key == "resource_owner_username":
                    self.parameters["resource_owner_username"] = kwargs[key]
                elif key == "resource_owner_password":
                    self.parameters["resource_owner_password"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "client_registration_endpoint":
                    self.parameters["client_registration_endpoint"] = kwargs[key]
                elif key == "authorization_endpoint":
                    self.parameters["authorization_endpoint"] = kwargs[key]
                elif key == "grant_types":
                    self.parameters["grant_types"] = kwargs[key]
                elif key == "client_id":
                    self.parameters["client_id"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Authorization Server instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Authorization Server instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_authorizationserver()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_authorizationserver(self):
        '''
        Creates or updates Authorization Server with the specified configuration.

        :return: deserialized Authorization Server instance state dictionary
        '''
        self.log("Creating / Updating the Authorization Server instance {0}".format(self.authsid))

        try:
            response = self.mgmt_client.authorization_server.create_or_update(resource_group_name=self.resource_group,
                                                                              service_name=self.service_name,
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
                                                                    service_name=self.service_name,
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
                                                                 service_name=self.service_name,
                                                                 authsid=self.authsid)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Authorization Server instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Authorization Server instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMAuthorizationServer()


if __name__ == '__main__':
    main()

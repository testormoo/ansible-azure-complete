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
module: azure_rm_apimanagementapi
version_added: "2.8"
short_description: Manage Azure Api instance.
description:
    - Create, update and delete instance of Azure Api.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."
        required: True
    description:
        description:
            - Description of the API. May include HTML formatting tags.
    authentication_settings:
        description:
            - Collection of authentication settings included into this API.
        suboptions:
            o_auth2:
                description:
                    - OAuth2 Authentication settings
                suboptions:
                    authorization_server_id:
                        description:
                            - OAuth authorization server identifier.
                    scope:
                        description:
                            - operations scope.
            openid:
                description:
                    - OpenID Connect Authentication Settings
                suboptions:
                    openid_provider_id:
                        description:
                            - OAuth authorization server identifier.
                    bearer_token_sending_methods:
                        description:
                            - How to send token to the server.
                        type: list
            subscription_key_required:
                description:
                    - "Specifies whether subscription key is required during call to this API, true - API is included into closed products only, false - API
                       is included into open products alone, null - there is a mix of products."
    subscription_key_parameter_names:
        description:
            - I(protocols) over which API is made available.
        suboptions:
            header:
                description:
                    - Subscription key header name.
            query:
                description:
                    - Subscription key query string parameter name.
    api_type:
        description:
            - Type of API.
        choices:
            - 'http'
            - 'soap'
    api_revision:
        description:
            - Describes the Revision of the Api. If no value is provided, default revision 1 is created
    api_version:
        description:
            - Indicates the Version identifier of the API if the API is versioned
    api_revision_description:
        description:
            - I(description) of the Api Revision.
    api_version_description:
        description:
            - I(description) of the Api Version.
    api_version_set_id:
        description:
            - A resource identifier for the related I(api_version_set).
    display_name:
        description:
            - API name.
    service_url:
        description:
            - Absolute URL of the backend service implementing this API.
    path:
        description:
            - "Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to the
               API endpoint base URL specified during the service instance creation to form a public URL for this API."
            - Required when C(state) is I(present).
    protocols:
        description:
            - Describes on which protocols the operations in this API can be invoked.
        type: list
    api_version_set:
        description:
        suboptions:
            id:
                description:
                    - Identifier for existing API Version Set. Omit this value to create a new Version Set.
            description:
                description:
                    - Description of API Version Set.
            versioning_scheme:
                description:
                    - An value that determines where the API Version identifer will be located in a HTTP request.
                choices:
                    - 'segment'
                    - 'query'
                    - 'header'
            version_query_name:
                description:
                    - Name of C(query) parameter that indicates the API Version if I(versioning_scheme) is set to `C(query)`.
            version_header_name:
                description:
                    - Name of HTTP C(header) parameter that indicates the API Version if I(versioning_scheme) is set to `C(header)`.
    content_value:
        description:
            - Content value when Importing an API.
    content_format:
        description:
            - Format of the Content in which the API is getting imported.
        choices:
            - 'wadl-xml'
            - 'wadl-link-json'
            - 'swagger-json'
            - 'swagger-link-json'
            - 'wsdl'
            - 'wsdl-link'
    wsdl_selector:
        description:
            - Criteria to limit import of C(wsdl) to a subset of the document.
        suboptions:
            wsdl_service_name:
                description:
                    - Name of service to import from WSDL
            wsdl_endpoint_name:
                description:
                    - Name of endpoint(port) to import from WSDL
    soap_api_type:
        description:
            - Type of Api to create.
            -  * `C(http)` creates a C(soap) to REST API
            -  * `C(soap)` creates a C(soap) pass-through API.
        choices:
            - 'soap_to_rest'
            - 'soap_pass_through'
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Api.
        - Use 'present' to create or update an Api and 'absent' to delete it.
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
  - name: Create (or update) Api
    azure_rm_apimanagementapi:
      resource_group: rg1
      name: apimService1
      api_id: petstore
      path: petstore
      content_value: http://petstore.swagger.io/v2/swagger.json
      content_format: swagger-link-json
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


class AzureRMApi(AzureRMModuleBase):
    """Configuration class for an Azure RM Api resource"""

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
            api_id=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            authentication_settings=dict(
                type='dict'
                options=dict(
                    o_auth2=dict(
                        type='dict'
                        options=dict(
                            authorization_server_id=dict(
                                type='str'
                            ),
                            scope=dict(
                                type='str'
                            )
                        )
                    ),
                    openid=dict(
                        type='dict'
                        options=dict(
                            openid_provider_id=dict(
                                type='str'
                            ),
                            bearer_token_sending_methods=dict(
                                type='list'
                            )
                        )
                    ),
                    subscription_key_required=dict(
                        type='str'
                    )
                )
            ),
            subscription_key_parameter_names=dict(
                type='dict'
                options=dict(
                    header=dict(
                        type='str'
                    ),
                    query=dict(
                        type='str'
                    )
                )
            ),
            api_type=dict(
                type='str',
                choices=['http',
                         'soap']
            ),
            api_revision=dict(
                type='str'
            ),
            api_version=dict(
                type='str'
            ),
            api_revision_description=dict(
                type='str'
            ),
            api_version_description=dict(
                type='str'
            ),
            api_version_set_id=dict(
                type='str'
            ),
            display_name=dict(
                type='str'
            ),
            service_url=dict(
                type='str'
            ),
            path=dict(
                type='str'
            ),
            protocols=dict(
                type='list'
            ),
            api_version_set=dict(
                type='dict'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    description=dict(
                        type='str'
                    ),
                    versioning_scheme=dict(
                        type='str',
                        choices=['segment',
                                 'query',
                                 'header']
                    ),
                    version_query_name=dict(
                        type='str'
                    ),
                    version_header_name=dict(
                        type='str'
                    )
                )
            ),
            content_value=dict(
                type='str'
            ),
            content_format=dict(
                type='str',
                choices=['wadl-xml',
                         'wadl-link-json',
                         'swagger-json',
                         'swagger-link-json',
                         'wsdl',
                         'wsdl-link']
            ),
            wsdl_selector=dict(
                type='dict'
                options=dict(
                    wsdl_service_name=dict(
                        type='str'
                    ),
                    wsdl_endpoint_name=dict(
                        type='str'
                    )
                )
            ),
            soap_api_type=dict(
                type='str',
                choices=['soap_to_rest',
                         'soap_pass_through']
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
        self.api_id = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApi, self).__init__(derived_arg_spec=self.module_arg_spec,
                                         supports_check_mode=True,
                                         supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['api_version_set', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['api_version_set', 'versioning_scheme'], True)
        dict_camelize(self.parameters, ['soap_api_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_api()

        if not old_response:
            self.log("Api instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_api()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_api()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Api instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                })
        return self.results

    def create_update_api(self):
        '''
        Creates or updates Api with the specified configuration.

        :return: deserialized Api instance state dictionary
        '''
        self.log("Creating / Updating the Api instance {0}".format(self.api_id))

        try:
            response = self.mgmt_client.api.create_or_update(resource_group_name=self.resource_group,
                                                             service_name=self.name,
                                                             api_id=self.api_id,
                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api instance.')
            self.fail("Error creating the Api instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_api(self):
        '''
        Deletes specified Api instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api instance {0}".format(self.api_id))
        try:
            response = self.mgmt_client.api.delete(resource_group_name=self.resource_group,
                                                   service_name=self.name,
                                                   api_id=self.api_id,
                                                   if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Api instance.')
            self.fail("Error deleting the Api instance: {0}".format(str(e)))

        return True

    def get_api(self):
        '''
        Gets the properties of the specified Api.

        :return: deserialized Api instance state dictionary
        '''
        self.log("Checking if the Api instance {0} is present".format(self.api_id))
        found = False
        try:
            response = self.mgmt_client.api.get(resource_group_name=self.resource_group,
                                                service_name=self.name,
                                                api_id=self.api_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api instance.')
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


def main():
    """Main execution"""
    AzureRMApi()


if __name__ == '__main__':
    main()

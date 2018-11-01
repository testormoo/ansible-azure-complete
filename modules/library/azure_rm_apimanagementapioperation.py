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
module: azure_rm_apimanagementapioperation
version_added: "2.8"
short_description: Manage Api Operation instance.
description:
    - Create, update and delete instance of Api Operation.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."
        required: True
    operation_id:
        description:
            - Operation identifier within an API. Must be unique in the current API Management service instance.
        required: True
    template_parameters:
        description:
            - Collection of URL template parameters.
        type: list
        suboptions:
            name:
                description:
                    - Parameter name.
                required: True
            description:
                description:
                    - Parameter description.
            type:
                description:
                    - Parameter type.
                required: True
            default_value:
                description:
                    - Default parameter value.
            required:
                description:
                    - whether parameter is required or not.
            values:
                description:
                    - Parameter values.
                type: list
    description:
        description:
            - Description of the operation. May include HTML formatting tags.
    request:
        description:
            - An entity containing request details.
        suboptions:
            description:
                description:
                    - Operation request description.
            query_parameters:
                description:
                    - Collection of operation request query parameters.
                type: list
                suboptions:
                    name:
                        description:
                            - Parameter name.
                        required: True
                    description:
                        description:
                            - Parameter description.
                    type:
                        description:
                            - Parameter type.
                        required: True
                    default_value:
                        description:
                            - Default parameter value.
                    required:
                        description:
                            - whether parameter is required or not.
                    values:
                        description:
                            - Parameter values.
                        type: list
            headers:
                description:
                    - Collection of operation request headers.
                type: list
                suboptions:
                    name:
                        description:
                            - Parameter name.
                        required: True
                    description:
                        description:
                            - Parameter description.
                    type:
                        description:
                            - Parameter type.
                        required: True
                    default_value:
                        description:
                            - Default parameter value.
                    required:
                        description:
                            - whether parameter is required or not.
                    values:
                        description:
                            - Parameter values.
                        type: list
            representations:
                description:
                    - Collection of operation request representations.
                type: list
                suboptions:
                    content_type:
                        description:
                            - Specifies a registered or custom content type for this representation, e.g. application/xml.
                        required: True
                    sample:
                        description:
                            - An example of the representation.
                    schema_id:
                        description:
                            - "Schema identifier. Applicable only if 'I(content_type)' value is neither 'application/x-www-form-urlencoded' nor
                               'multipart/form-data'."
                    type_name:
                        description:
                            - "Type name defined by the schema. Applicable only if 'I(content_type)' value is neither 'application/x-www-form-urlencoded'
                               nor 'multipart/form-data'."
                    form_parameters:
                        description:
                            - "Collection of form parameters. Required if 'I(content_type)' value is either 'application/x-www-form-urlencoded' or
                               'multipart/form-data'.."
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Parameter name.
                                required: True
                            description:
                                description:
                                    - Parameter description.
                            type:
                                description:
                                    - Parameter type.
                                required: True
                            default_value:
                                description:
                                    - Default parameter value.
                            required:
                                description:
                                    - whether parameter is required or not.
                            values:
                                description:
                                    - Parameter values.
                                type: list
    responses:
        description:
            - Array of Operation responses.
        type: list
        suboptions:
            status_code:
                description:
                    - Operation response HTTP status code.
                required: True
            description:
                description:
                    - Operation response description.
            representations:
                description:
                    - Collection of operation response representations.
                type: list
                suboptions:
                    content_type:
                        description:
                            - Specifies a registered or custom content type for this representation, e.g. application/xml.
                        required: True
                    sample:
                        description:
                            - An example of the representation.
                    schema_id:
                        description:
                            - "Schema identifier. Applicable only if 'I(content_type)' value is neither 'application/x-www-form-urlencoded' nor
                               'multipart/form-data'."
                    type_name:
                        description:
                            - "Type name defined by the schema. Applicable only if 'I(content_type)' value is neither 'application/x-www-form-urlencoded'
                               nor 'multipart/form-data'."
                    form_parameters:
                        description:
                            - "Collection of form parameters. Required if 'I(content_type)' value is either 'application/x-www-form-urlencoded' or
                               'multipart/form-data'.."
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Parameter name.
                                required: True
                            description:
                                description:
                                    - Parameter description.
                            type:
                                description:
                                    - Parameter type.
                                required: True
                            default_value:
                                description:
                                    - Default parameter value.
                            required:
                                description:
                                    - whether parameter is required or not.
                            values:
                                description:
                                    - Parameter values.
                                type: list
            headers:
                description:
                    - Collection of operation response headers.
                type: list
                suboptions:
                    name:
                        description:
                            - Parameter name.
                        required: True
                    description:
                        description:
                            - Parameter description.
                    type:
                        description:
                            - Parameter type.
                        required: True
                    default_value:
                        description:
                            - Default parameter value.
                    required:
                        description:
                            - whether parameter is required or not.
                    values:
                        description:
                            - Parameter values.
                        type: list
    policies:
        description:
            - Operation Policies
    display_name:
        description:
            - Operation Name.
        required: True
    method:
        description:
            - A Valid HTTP Operation Method. Typical Http Methods like GET, PUT, POST but not limited by only them.
        required: True
    url_template:
        description:
            - "Relative URL template identifying the target resource for this operation. May include parameters. Example:
               /customers/{cid}/orders/{oid}/?date={date}"
        required: True
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Api Operation.
        - Use 'present' to create or update an Api Operation and 'absent' to delete it.
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
  - name: Create (or update) Api Operation
    azure_rm_apimanagementapioperation:
      resource_group: rg1
      service_name: apimService1
      api_id: PetStoreTemplate2
      operation_id: newoperations
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


class AzureRMApiOperation(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Operation resource"""

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
            api_id=dict(
                type='str',
                required=True
            ),
            operation_id=dict(
                type='str',
                required=True
            ),
            template_parameters=dict(
                type='list'
            ),
            description=dict(
                type='str'
            ),
            request=dict(
                type='dict'
            ),
            responses=dict(
                type='list'
            ),
            policies=dict(
                type='str'
            ),
            display_name=dict(
                type='str',
                required=True
            ),
            method=dict(
                type='str',
                required=True
            ),
            url_template=dict(
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
        self.api_id = None
        self.operation_id = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiOperation, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "template_parameters":
                    self.parameters["template_parameters"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "request":
                    self.parameters["request"] = kwargs[key]
                elif key == "responses":
                    self.parameters["responses"] = kwargs[key]
                elif key == "policies":
                    self.parameters["policies"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "method":
                    self.parameters["method"] = kwargs[key]
                elif key == "url_template":
                    self.parameters["url_template"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_apioperation()

        if not old_response:
            self.log("Api Operation instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Operation instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Api Operation instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Operation instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apioperation()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Operation instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apioperation()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apioperation():
                time.sleep(20)
        else:
            self.log("Api Operation instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_apioperation(self):
        '''
        Creates or updates Api Operation with the specified configuration.

        :return: deserialized Api Operation instance state dictionary
        '''
        self.log("Creating / Updating the Api Operation instance {0}".format(self.operation_id))

        try:
            response = self.mgmt_client.api_operation.create_or_update(resource_group_name=self.resource_group,
                                                                       service_name=self.service_name,
                                                                       api_id=self.api_id,
                                                                       operation_id=self.operation_id,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Operation instance.')
            self.fail("Error creating the Api Operation instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apioperation(self):
        '''
        Deletes specified Api Operation instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Operation instance {0}".format(self.operation_id))
        try:
            response = self.mgmt_client.api_operation.delete(resource_group_name=self.resource_group,
                                                             service_name=self.service_name,
                                                             api_id=self.api_id,
                                                             operation_id=self.operation_id,
                                                             if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Api Operation instance.')
            self.fail("Error deleting the Api Operation instance: {0}".format(str(e)))

        return True

    def get_apioperation(self):
        '''
        Gets the properties of the specified Api Operation.

        :return: deserialized Api Operation instance state dictionary
        '''
        self.log("Checking if the Api Operation instance {0} is present".format(self.operation_id))
        found = False
        try:
            response = self.mgmt_client.api_operation.get(resource_group_name=self.resource_group,
                                                          service_name=self.service_name,
                                                          api_id=self.api_id,
                                                          operation_id=self.operation_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Operation instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Operation instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMApiOperation()


if __name__ == '__main__':
    main()
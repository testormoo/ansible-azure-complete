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
module: azure_rm_apimanagementapischema
version_added: "2.8"
short_description: Manage Api Schema instance.
description:
    - Create, update and delete instance of Api Schema.

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
    schema_id:
        description:
            - Schema identifier within an API. Must be unique in the current API Management service instance.
        required: True
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    content_type:
        description:
            - "Must be a valid a media type used in a Content-Type header as defined in the RFC 2616. Media type of the schema document (e.g.
               application/json, application/xml)."
        required: True
    value:
        description:
            - Json escaped string defining the document representing the Schema.
    state:
      description:
        - Assert the state of the Api Schema.
        - Use 'present' to create or update an Api Schema and 'absent' to delete it.
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
  - name: Create (or update) Api Schema
    azure_rm_apimanagementapischema:
      resource_group: rg1
      service_name: apimService1
      api_id: 59d6bb8f1f7fab13dc67ec9b
      schema_id: ec12520d-9d48-4e7b-8f39-698ca2ac63f1
      if_match: NOT FOUND
      content_type: NOT FOUND
      value: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourcegroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/59d6bb8f1f7fab13dc67ec9b/schemas/ec12520d-9d
            48-4e7b-8f39-698ca2ac63f1"
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


class AzureRMApiSchema(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Schema resource"""

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
            schema_id=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            content_type=dict(
                type='str',
                required=True
            ),
            value=dict(
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
        self.schema_id = None
        self.if_match = None
        self.content_type = None
        self.value = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiSchema, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_apischema()

        if not old_response:
            self.log("Api Schema instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Schema instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Api Schema instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Schema instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apischema()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Schema instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apischema()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apischema():
                time.sleep(20)
        else:
            self.log("Api Schema instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_apischema(self):
        '''
        Creates or updates Api Schema with the specified configuration.

        :return: deserialized Api Schema instance state dictionary
        '''
        self.log("Creating / Updating the Api Schema instance {0}".format(self.schema_id))

        try:
            response = self.mgmt_client.api_schema.create_or_update(resource_group_name=self.resource_group,
                                                                    service_name=self.service_name,
                                                                    api_id=self.api_id,
                                                                    schema_id=self.schema_id,
                                                                    content_type=self.content_type)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Schema instance.')
            self.fail("Error creating the Api Schema instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apischema(self):
        '''
        Deletes specified Api Schema instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Schema instance {0}".format(self.schema_id))
        try:
            response = self.mgmt_client.api_schema.delete(resource_group_name=self.resource_group,
                                                          service_name=self.service_name,
                                                          api_id=self.api_id,
                                                          schema_id=self.schema_id,
                                                          if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Api Schema instance.')
            self.fail("Error deleting the Api Schema instance: {0}".format(str(e)))

        return True

    def get_apischema(self):
        '''
        Gets the properties of the specified Api Schema.

        :return: deserialized Api Schema instance state dictionary
        '''
        self.log("Checking if the Api Schema instance {0} is present".format(self.schema_id))
        found = False
        try:
            response = self.mgmt_client.api_schema.get(resource_group_name=self.resource_group,
                                                       service_name=self.service_name,
                                                       api_id=self.api_id,
                                                       schema_id=self.schema_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Schema instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Schema instance.')
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
    AzureRMApiSchema()


if __name__ == '__main__':
    main()
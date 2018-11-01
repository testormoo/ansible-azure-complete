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
module: azure_rm_apimanagementapiversionset
version_added: "2.8"
short_description: Manage Api Version Set instance.
description:
    - Create, update and delete instance of Api Version Set.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    version_set_id:
        description:
            - Api Version Set identifier. Must be unique in the current API Management service instance.
        required: True
    description:
        description:
            - Description of API Version Set.
    version_query_name:
        description:
            - Name of C(query) parameter that indicates the API Version if I(versioning_scheme) is set to `C(query)`.
    version_header_name:
        description:
            - Name of HTTP C(header) parameter that indicates the API Version if I(versioning_scheme) is set to `C(header)`.
    display_name:
        description:
            - Name of API Version Set
        required: True
    versioning_scheme:
        description:
            - An value that determines where the API Version identifer will be located in a HTTP request.
        required: True
        choices:
            - 'segment'
            - 'query'
            - 'header'
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Api Version Set.
        - Use 'present' to create or update an Api Version Set and 'absent' to delete it.
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
  - name: Create (or update) Api Version Set
    azure_rm_apimanagementapiversionset:
      resource_group: rg1
      service_name: apimService1
      version_set_id: api1
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


class AzureRMApiVersionSet(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Version Set resource"""

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
            version_set_id=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            version_query_name=dict(
                type='str'
            ),
            version_header_name=dict(
                type='str'
            ),
            display_name=dict(
                type='str',
                required=True
            ),
            versioning_scheme=dict(
                type='str',
                choices=['segment',
                         'query',
                         'header'],
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
        self.version_set_id = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiVersionSet, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "version_query_name":
                    self.parameters["version_query_name"] = kwargs[key]
                elif key == "version_header_name":
                    self.parameters["version_header_name"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "versioning_scheme":
                    self.parameters["versioning_scheme"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_apiversionset()

        if not old_response:
            self.log("Api Version Set instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Version Set instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Api Version Set instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Version Set instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apiversionset()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Version Set instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apiversionset()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apiversionset():
                time.sleep(20)
        else:
            self.log("Api Version Set instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_apiversionset(self):
        '''
        Creates or updates Api Version Set with the specified configuration.

        :return: deserialized Api Version Set instance state dictionary
        '''
        self.log("Creating / Updating the Api Version Set instance {0}".format(self.version_set_id))

        try:
            response = self.mgmt_client.api_version_set.create_or_update(resource_group_name=self.resource_group,
                                                                         service_name=self.service_name,
                                                                         version_set_id=self.version_set_id,
                                                                         parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Version Set instance.')
            self.fail("Error creating the Api Version Set instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apiversionset(self):
        '''
        Deletes specified Api Version Set instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Version Set instance {0}".format(self.version_set_id))
        try:
            response = self.mgmt_client.api_version_set.delete(resource_group_name=self.resource_group,
                                                               service_name=self.service_name,
                                                               version_set_id=self.version_set_id,
                                                               if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Api Version Set instance.')
            self.fail("Error deleting the Api Version Set instance: {0}".format(str(e)))

        return True

    def get_apiversionset(self):
        '''
        Gets the properties of the specified Api Version Set.

        :return: deserialized Api Version Set instance state dictionary
        '''
        self.log("Checking if the Api Version Set instance {0} is present".format(self.version_set_id))
        found = False
        try:
            response = self.mgmt_client.api_version_set.get(resource_group_name=self.resource_group,
                                                            service_name=self.service_name,
                                                            version_set_id=self.version_set_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Version Set instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Version Set instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMApiVersionSet()


if __name__ == '__main__':
    main()
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
module: azure_rm_apimanagementproperty
version_added: "2.8"
short_description: Manage Property instance.
description:
    - Create, update and delete instance of Property.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    prop_id:
        description:
            - Identifier of the property.
        required: True
    secret:
        description:
            - Determines whether the I(value) is a secret and should be encrypted or not. Default I(value) is false.
    display_name:
        description:
            - Unique name of Property. It may contain only letters, digits, period, dash, and underscore characters.
        required: True
    value:
        description:
            - Value of the property. Can contain policy expressions. It may not be empty or consist only of whitespace.
        required: True
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Property.
        - Use 'present' to create or update an Property and 'absent' to delete it.
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
  - name: Create (or update) Property
    azure_rm_apimanagementproperty:
      resource_group: rg1
      service_name: apimService1
      prop_id: testprop2
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


class AzureRMProperty(AzureRMModuleBase):
    """Configuration class for an Azure RM Property resource"""

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
            prop_id=dict(
                type='str',
                required=True
            ),
            secret=dict(
                type='str'
            ),
            display_name=dict(
                type='str',
                required=True
            ),
            value=dict(
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
        self.prop_id = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProperty, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "secret":
                    self.parameters["secret"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "value":
                    self.parameters["value"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_property()

        if not old_response:
            self.log("Property instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Property instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Property instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Property instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_property()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Property instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_property()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_property():
                time.sleep(20)
        else:
            self.log("Property instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_property(self):
        '''
        Creates or updates Property with the specified configuration.

        :return: deserialized Property instance state dictionary
        '''
        self.log("Creating / Updating the Property instance {0}".format(self.prop_id))

        try:
            response = self.mgmt_client.property.create_or_update(resource_group_name=self.resource_group,
                                                                  service_name=self.service_name,
                                                                  prop_id=self.prop_id,
                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Property instance.')
            self.fail("Error creating the Property instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_property(self):
        '''
        Deletes specified Property instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Property instance {0}".format(self.prop_id))
        try:
            response = self.mgmt_client.property.delete(resource_group_name=self.resource_group,
                                                        service_name=self.service_name,
                                                        prop_id=self.prop_id,
                                                        if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Property instance.')
            self.fail("Error deleting the Property instance: {0}".format(str(e)))

        return True

    def get_property(self):
        '''
        Gets the properties of the specified Property.

        :return: deserialized Property instance state dictionary
        '''
        self.log("Checking if the Property instance {0} is present".format(self.prop_id))
        found = False
        try:
            response = self.mgmt_client.property.get(resource_group_name=self.resource_group,
                                                     service_name=self.service_name,
                                                     prop_id=self.prop_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Property instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Property instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMProperty()


if __name__ == '__main__':
    main()

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
module: azure_rm_customerinsightsrelationship
version_added: "2.8"
short_description: Manage Relationship instance.
description:
    - Create, update and delete instance of Relationship.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    relationship_name:
        description:
            - The name of the Relationship.
        required: True
    cardinality:
        description:
            - The Relationship Cardinality.
        choices:
            - 'one_to_one'
            - 'one_to_many'
            - 'many_to_many'
    display_name:
        description:
            - Localized display name for the Relationship.
    description:
        description:
            - Localized descriptions for the Relationship.
    expiry_date_time_utc:
        description:
            - The expiry date time in UTC.
    fields:
        description:
            - The properties of the Relationship.
        type: list
        suboptions:
            array_value_separator:
                description:
                    - Array value separator for properties with I(is_array) set.
            enum_valid_values:
                description:
                    - Describes valid values for an enum property.
                type: list
                suboptions:
                    value:
                        description:
                            - The integer value of the enum member.
                    localized_value_names:
                        description:
                            - Localized names of the enum member.
            field_name:
                description:
                    - Name of the property.
                required: True
            field_type:
                description:
                    - Type of the property.
                required: True
            is_array:
                description:
                    - Indicates if the property is actually an array of the I(field_type) above on the data api.
            is_enum:
                description:
                    - Indicates if the property is an enum.
            is_flag_enum:
                description:
                    - Indicates if the property is an flag enum.
            is_image:
                description:
                    - Whether the property is an Image.
            is_localized_string:
                description:
                    - Whether the property is a localized string.
            is_name:
                description:
                    - Whether the property is a name or a part of name.
            is_required:
                description:
                    - "Whether property value is required on instances, IsRequired field only for Intercation. Profile Instance will not check for required
                       field."
            property_id:
                description:
                    - The ID associated with the property.
            schema_item_prop_link:
                description:
                    - URL encoded schema.org item prop link for the property.
            max_length:
                description:
                    - Max length of string. Used only if type is string.
            is_available_in_graph:
                description:
                    - Whether property is available in graph or not.
    lookup_mappings:
        description:
            - Optional property to be used to map I(fields) in profile to their strong ids in related profile.
        type: list
        suboptions:
            field_mappings:
                description:
                    - Maps a profile property with the StrongId of related profile. This is an array to support StrongIds that are composite key as well.
                required: True
                type: list
                suboptions:
                    profile_field_name:
                        description:
                            - Specifies the fieldName in profile.
                        required: True
                    related_profile_key_property:
                        description:
                            - Specifies the KeyProperty (from StrongId) of the related profile.
                        required: True
    profile_type:
        description:
            - Profile type.
        required: True
    related_profile_type:
        description:
            - Related profile being referenced.
        required: True
    state:
      description:
        - Assert the state of the Relationship.
        - Use 'present' to create or update an Relationship and 'absent' to delete it.
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
  - name: Create (or update) Relationship
    azure_rm_customerinsightsrelationship:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      relationship_name: SomeRelationship
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/sdkTestHub/relationships/
            SomeRelationship"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRelationships(AzureRMModuleBase):
    """Configuration class for an Azure RM Relationship resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            relationship_name=dict(
                type='str',
                required=True
            ),
            cardinality=dict(
                type='str',
                choices=['one_to_one',
                         'one_to_many',
                         'many_to_many']
            ),
            display_name=dict(
                type='dict'
            ),
            description=dict(
                type='dict'
            ),
            expiry_date_time_utc=dict(
                type='datetime'
            ),
            fields=dict(
                type='list'
            ),
            lookup_mappings=dict(
                type='list'
            ),
            profile_type=dict(
                type='str',
                required=True
            ),
            related_profile_type=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.relationship_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRelationships, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "cardinality":
                    self.parameters["cardinality"] = _snake_to_camel(kwargs[key], True)
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "expiry_date_time_utc":
                    self.parameters["expiry_date_time_utc"] = kwargs[key]
                elif key == "fields":
                    self.parameters["fields"] = kwargs[key]
                elif key == "lookup_mappings":
                    self.parameters["lookup_mappings"] = kwargs[key]
                elif key == "profile_type":
                    self.parameters["profile_type"] = kwargs[key]
                elif key == "related_profile_type":
                    self.parameters["related_profile_type"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_relationship()

        if not old_response:
            self.log("Relationship instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Relationship instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Relationship instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Relationship instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_relationship()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Relationship instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_relationship()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_relationship():
                time.sleep(20)
        else:
            self.log("Relationship instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_relationship(self):
        '''
        Creates or updates Relationship with the specified configuration.

        :return: deserialized Relationship instance state dictionary
        '''
        self.log("Creating / Updating the Relationship instance {0}".format(self.relationship_name))

        try:
            response = self.mgmt_client.relationships.create_or_update(resource_group_name=self.resource_group,
                                                                       hub_name=self.hub_name,
                                                                       relationship_name=self.relationship_name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Relationship instance.')
            self.fail("Error creating the Relationship instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_relationship(self):
        '''
        Deletes specified Relationship instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Relationship instance {0}".format(self.relationship_name))
        try:
            response = self.mgmt_client.relationships.delete(resource_group_name=self.resource_group,
                                                             hub_name=self.hub_name,
                                                             relationship_name=self.relationship_name)
        except CloudError as e:
            self.log('Error attempting to delete the Relationship instance.')
            self.fail("Error deleting the Relationship instance: {0}".format(str(e)))

        return True

    def get_relationship(self):
        '''
        Gets the properties of the specified Relationship.

        :return: deserialized Relationship instance state dictionary
        '''
        self.log("Checking if the Relationship instance {0} is present".format(self.relationship_name))
        found = False
        try:
            response = self.mgmt_client.relationships.get(resource_group_name=self.resource_group,
                                                          hub_name=self.hub_name,
                                                          relationship_name=self.relationship_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Relationship instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Relationship instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMRelationships()


if __name__ == '__main__':
    main()

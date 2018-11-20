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
module: azure_rm_customerinsightsinteraction
version_added: "2.8"
short_description: Manage Interaction instance.
description:
    - Create, update and delete instance of Interaction.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    name:
        description:
            - The name of the C(interaction).
        required: True
    attributes:
        description:
            - The attributes for the Type.
    description:
        description:
            - Localized descriptions for the property.
    display_name:
        description:
            - Localized display names for the property.
    localized_attributes:
        description:
            - Any custom localized I(attributes) for the Type.
    small_image:
        description:
            - Small Image associated with the Property or I(entity_type).
    medium_image:
        description:
            - Medium Image associated with the Property or I(entity_type).
    large_image:
        description:
            - Large Image associated with the Property or I(entity_type).
    api_entity_set_name:
        description:
            - The api entity set name. This becomes the odata entity set name for the entity Type being refered in this object.
    entity_type:
        description:
            - Type of entity.
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    fields:
        description:
            - The properties of the C(profile).
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
                    - Required when C(state) is I(present).
            field_type:
                description:
                    - Type of the property.
                    - Required when C(state) is I(present).
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
    instances_count:
        description:
            - The instance count.
    schema_item_type_link:
        description:
            - The schema org link. This helps ACI identify and suggest semantic models.
    timestamp_field_name:
        description:
            - The timestamp property name. Represents the time when the C(interaction) or C(profile) update happened.
    type_name:
        description:
            - The name of the entity.
    id_property_names:
        description:
            - The id property names. Properties which uniquely identify an C(interaction) instance.
        type: list
    participant_profiles:
        description:
            - Profiles that participated in the C(interaction).
        type: list
        suboptions:
            profile_type_name:
                description:
                    - Profile type name.
                    - Required when C(state) is I(present).
            participant_property_references:
                description:
                    - The property references.
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    source_property_name:
                        description:
                            - The source property that maps to the target property.
                            - Required when C(state) is I(present).
                    target_property_name:
                        description:
                            - The target property that maps to the source property.
                            - Required when C(state) is I(present).
            participant_name:
                description:
                    - Participant name.
                    - Required when C(state) is I(present).
            display_name:
                description:
                    - Localized display name.
            description:
                description:
                    - Localized descriptions.
            role:
                description:
                    - The role that the participant is playing in the interaction.
    primary_participant_profile_property_name:
        description:
            - "The primary participant property name for an C(interaction) ,This is used to logically represent the agent of the C(interaction), Specify the
               participant name here from ParticipantName."
    is_activity:
        description:
            - "An C(interaction) can be tagged as an activity only during create. This enables the C(interaction) to be editable and can enable merging of
               properties from multiple data sources based on precedence, which is defined at a link level."
    state:
      description:
        - Assert the state of the Interaction.
        - Use 'present' to create or update an Interaction and 'absent' to delete it.
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
  - name: Create (or update) Interaction
    azure_rm_customerinsightsinteraction:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      name: TestProfileType396
      small_image: \\Images\\smallImage
      medium_image: \\Images\\MediumImage
      large_image: \\Images\\LargeImage
      api_entity_set_name: TestInteractionType6358
      fields:
        - field_name: TestInteractionType6358
          field_type: Edm.String
          is_array: False
          is_required: True
      id_property_names:
        - [
  "TestInteractionType6358"
]
      primary_participant_profile_property_name: profile1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/azSdkTestHub/interactions
            /TestInteractionType6358"
status:
    description:
        - "The data source status. Possible values include: 'None', 'Active', 'Deleted'"
    returned: always
    type: str
    sample: status
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


class AzureRMInteractions(AzureRMModuleBase):
    """Configuration class for an Azure RM Interaction resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            attributes=dict(
                type='dict'
            ),
            description=dict(
                type='dict'
            ),
            display_name=dict(
                type='dict'
            ),
            localized_attributes=dict(
                type='dict'
            ),
            small_image=dict(
                type='str'
            ),
            medium_image=dict(
                type='str'
            ),
            large_image=dict(
                type='str'
            ),
            api_entity_set_name=dict(
                type='str'
            ),
            entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship']
            ),
            fields=dict(
                type='list'
            ),
            instances_count=dict(
                type='int'
            ),
            schema_item_type_link=dict(
                type='str'
            ),
            timestamp_field_name=dict(
                type='str'
            ),
            type_name=dict(
                type='str'
            ),
            id_property_names=dict(
                type='list'
            ),
            participant_profiles=dict(
                type='list'
            ),
            primary_participant_profile_property_name=dict(
                type='str'
            ),
            is_activity=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMInteractions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "attributes":
                    self.parameters["attributes"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "localized_attributes":
                    self.parameters["localized_attributes"] = kwargs[key]
                elif key == "small_image":
                    self.parameters["small_image"] = kwargs[key]
                elif key == "medium_image":
                    self.parameters["medium_image"] = kwargs[key]
                elif key == "large_image":
                    self.parameters["large_image"] = kwargs[key]
                elif key == "api_entity_set_name":
                    self.parameters["api_entity_set_name"] = kwargs[key]
                elif key == "entity_type":
                    self.parameters["entity_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "fields":
                    self.parameters["fields"] = kwargs[key]
                elif key == "instances_count":
                    self.parameters["instances_count"] = kwargs[key]
                elif key == "schema_item_type_link":
                    self.parameters["schema_item_type_link"] = kwargs[key]
                elif key == "timestamp_field_name":
                    self.parameters["timestamp_field_name"] = kwargs[key]
                elif key == "type_name":
                    self.parameters["type_name"] = kwargs[key]
                elif key == "id_property_names":
                    self.parameters["id_property_names"] = kwargs[key]
                elif key == "participant_profiles":
                    self.parameters["participant_profiles"] = kwargs[key]
                elif key == "primary_participant_profile_property_name":
                    self.parameters["primary_participant_profile_property_name"] = kwargs[key]
                elif key == "is_activity":
                    self.parameters["is_activity"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_interaction()

        if not old_response:
            self.log("Interaction instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Interaction instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Interaction instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_interaction()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Interaction instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_interaction()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_interaction():
                time.sleep(20)
        else:
            self.log("Interaction instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_interaction(self):
        '''
        Creates or updates Interaction with the specified configuration.

        :return: deserialized Interaction instance state dictionary
        '''
        self.log("Creating / Updating the Interaction instance {0}".format(self.))

        try:
            response = self.mgmt_client.interactions.create_or_update(resource_group_name=self.resource_group,
                                                                      hub_name=self.hub_name,
                                                                      interaction_name=self.name,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Interaction instance.')
            self.fail("Error creating the Interaction instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_interaction(self):
        '''
        Deletes specified Interaction instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Interaction instance {0}".format(self.))
        try:
            response = self.mgmt_client.interactions.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Interaction instance.')
            self.fail("Error deleting the Interaction instance: {0}".format(str(e)))

        return True

    def get_interaction(self):
        '''
        Gets the properties of the specified Interaction.

        :return: deserialized Interaction instance state dictionary
        '''
        self.log("Checking if the Interaction instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.interactions.get(resource_group_name=self.resource_group,
                                                         hub_name=self.hub_name,
                                                         interaction_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Interaction instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Interaction instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMInteractions()


if __name__ == '__main__':
    main()

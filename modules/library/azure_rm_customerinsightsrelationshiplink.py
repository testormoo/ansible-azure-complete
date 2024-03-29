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
module: azure_rm_customerinsightsrelationshiplink
version_added: "2.8"
short_description: Manage Azure Relationship Link instance.
description:
    - Create, update and delete instance of Azure Relationship Link.

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
            - The name of the relationship link.
        required: True
    display_name:
        description:
            - Localized display name for the Relationship Link.
    description:
        description:
            - Localized descriptions for the Relationship Link.
    interaction_type:
        description:
            - The InteractionType associated with the Relationship Link.
            - Required when C(state) is I(present).
    mappings:
        description:
            - The mappings between Interaction and Relationship fields.
        type: list
        suboptions:
            interaction_field_name:
                description:
                    - The field name on the Interaction Type.
                    - Required when C(state) is I(present).
            link_type:
                description:
                    - Link type.
                choices:
                    - 'update_always'
                    - 'copy_if_null'
            relationship_field_name:
                description:
                    - The field name on the Relationship metadata.
                    - Required when C(state) is I(present).
    profile_property_references:
        description:
            - The property references for the Profile of the Relationship.
            - Required when C(state) is I(present).
        type: list
        suboptions:
            interaction_property_name:
                description:
                    - The source interaction property that maps to the target profile property.
                    - Required when C(state) is I(present).
            profile_property_name:
                description:
                    - The target profile property that maps to the source interaction property.
                    - Required when C(state) is I(present).
    related_profile_property_references:
        description:
            - The property references for the Related Profile of the Relationship.
            - Required when C(state) is I(present).
        type: list
        suboptions:
            interaction_property_name:
                description:
                    - The source interaction property that maps to the target profile property.
                    - Required when C(state) is I(present).
            profile_property_name:
                description:
                    - The target profile property that maps to the source interaction property.
                    - Required when C(state) is I(present).
    relationship_name:
        description:
            - The Relationship associated with the Link.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Relationship Link.
        - Use 'present' to create or update an Relationship Link and 'absent' to delete it.
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
  - name: Create (or update) Relationship Link
    azure_rm_customerinsightsrelationshiplink:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      name: Somelink
      display_name: {
  "en-us": "Link DisplayName"
}
      description: {
  "en-us": "Link Description"
}
      interaction_type: testInteraction4332
      profile_property_references:
        - interaction_property_name: profile1
          profile_property_name: ProfileId
      related_profile_property_references:
        - interaction_property_name: profile1
          profile_property_name: ProfileId
      relationship_name: testProfile2326994
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/sdkTestHub/relationshipLi
            nks/Somelink"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMRelationshipLink(AzureRMModuleBase):
    """Configuration class for an Azure RM Relationship Link resource"""

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
            display_name=dict(
                type='dict'
            ),
            description=dict(
                type='dict'
            ),
            interaction_type=dict(
                type='str'
            ),
            mappings=dict(
                type='list',
                options=dict(
                    interaction_field_name=dict(
                        type='str'
                    ),
                    link_type=dict(
                        type='str',
                        choices=['update_always',
                                 'copy_if_null']
                    ),
                    relationship_field_name=dict(
                        type='str'
                    )
                )
            ),
            profile_property_references=dict(
                type='list',
                options=dict(
                    interaction_property_name=dict(
                        type='str'
                    ),
                    profile_property_name=dict(
                        type='str'
                    )
                )
            ),
            related_profile_property_references=dict(
                type='list',
                options=dict(
                    interaction_property_name=dict(
                        type='str'
                    ),
                    profile_property_name=dict(
                        type='str'
                    )
                )
            ),
            relationship_name=dict(
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

        super(AzureRMRelationshipLink, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['mappings', 'link_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_relationshiplink()

        if not old_response:
            self.log("Relationship Link instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Relationship Link instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Relationship Link instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_relationshiplink()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Relationship Link instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_relationshiplink()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Relationship Link instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_relationshiplink(self):
        '''
        Creates or updates Relationship Link with the specified configuration.

        :return: deserialized Relationship Link instance state dictionary
        '''
        self.log("Creating / Updating the Relationship Link instance {0}".format(self.name))

        try:
            response = self.mgmt_client.relationship_links.create_or_update(resource_group_name=self.resource_group,
                                                                            hub_name=self.hub_name,
                                                                            relationship_link_name=self.name,
                                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Relationship Link instance.')
            self.fail("Error creating the Relationship Link instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_relationshiplink(self):
        '''
        Deletes specified Relationship Link instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Relationship Link instance {0}".format(self.name))
        try:
            response = self.mgmt_client.relationship_links.delete(resource_group_name=self.resource_group,
                                                                  hub_name=self.hub_name,
                                                                  relationship_link_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Relationship Link instance.')
            self.fail("Error deleting the Relationship Link instance: {0}".format(str(e)))

        return True

    def get_relationshiplink(self):
        '''
        Gets the properties of the specified Relationship Link.

        :return: deserialized Relationship Link instance state dictionary
        '''
        self.log("Checking if the Relationship Link instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.relationship_links.get(resource_group_name=self.resource_group,
                                                               hub_name=self.hub_name,
                                                               relationship_link_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Relationship Link instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Relationship Link instance.')
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


def main():
    """Main execution"""
    AzureRMRelationshipLink()


if __name__ == '__main__':
    main()

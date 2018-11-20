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
short_description: Manage Relationship Link instance.
description:
    - Create, update and delete instance of Relationship Link.

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


class AzureRMRelationshipLinks(AzureRMModuleBase):
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
                type='list'
            ),
            profile_property_references=dict(
                type='list'
            ),
            related_profile_property_references=dict(
                type='list'
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

        super(AzureRMRelationshipLinks, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "interaction_type":
                    self.parameters["interaction_type"] = kwargs[key]
                elif key == "mappings":
                    ev = kwargs[key]
                    if 'link_type' in ev:
                        if ev['link_type'] == 'update_always':
                            ev['link_type'] = 'UpdateAlways'
                        elif ev['link_type'] == 'copy_if_null':
                            ev['link_type'] = 'CopyIfNull'
                    self.parameters["mappings"] = ev
                elif key == "profile_property_references":
                    self.parameters["profile_property_references"] = kwargs[key]
                elif key == "related_profile_property_references":
                    self.parameters["related_profile_property_references"] = kwargs[key]
                elif key == "relationship_name":
                    self.parameters["relationship_name"] = kwargs[key]

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
                if (not default_compare(self.parameters, old_response, '')):
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
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_relationshiplink():
                time.sleep(20)
        else:
            self.log("Relationship Link instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
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

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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


def main():
    """Main execution"""
    AzureRMRelationshipLinks()


if __name__ == '__main__':
    main()

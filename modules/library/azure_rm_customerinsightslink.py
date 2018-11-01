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
module: azure_rm_customerinsightslink
version_added: "2.8"
short_description: Manage Link instance.
description:
    - Create, update and delete instance of Link.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    link_name:
        description:
            - The name of the link.
        required: True
    source_entity_type:
        description:
            - Type of source entity.
        required: True
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    target_entity_type:
        description:
            - Type of target entity.
        required: True
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    source_entity_type_name:
        description:
            - Name of the source Entity Type.
        required: True
    target_entity_type_name:
        description:
            - Name of the target Entity Type.
        required: True
    display_name:
        description:
            - Localized display name for the Link.
    description:
        description:
            - Localized descriptions for the Link.
    mappings:
        description:
            - The set of properties mappings between the source and target Types.
        type: list
        suboptions:
            source_property_name:
                description:
                    -  Property name on the source Entity Type.
                required: True
            target_property_name:
                description:
                    - Property name on the target Entity Type.
                required: True
            link_type:
                description:
                    - Link type.
                choices:
                    - 'update_always'
                    - 'copy_if_null'
    participant_property_references:
        description:
            - The properties that represent the participating C(C(profile)).
        required: True
        type: list
        suboptions:
            source_property_name:
                description:
                    - The source property that maps to the target property.
                required: True
            target_property_name:
                description:
                    - The target property that maps to the source property.
                required: True
    reference_only:
        description:
            - "Indicating whether the link is reference only link. This flag is ingored if the I(mappings) are defined. If the I(mappings) are not defined
               and it is set to true, links processing will not create or update profiles."
    operation_type:
        description:
            - Determines whether this link is supposed to create or C(delete) instances if Link is NOT Reference Only.
        choices:
            - 'upsert'
            - 'delete'
    state:
      description:
        - Assert the state of the Link.
        - Use 'present' to create or update an Link and 'absent' to delete it.
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
  - name: Create (or update) Link
    azure_rm_customerinsightslink:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      link_name: linkTest4806
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/azSdkTestHub/links/linkTe
            st4806"
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


class AzureRMLinks(AzureRMModuleBase):
    """Configuration class for an Azure RM Link resource"""

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
            link_name=dict(
                type='str',
                required=True
            ),
            source_entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship'],
                required=True
            ),
            target_entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship'],
                required=True
            ),
            source_entity_type_name=dict(
                type='str',
                required=True
            ),
            target_entity_type_name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='dict'
            ),
            description=dict(
                type='dict'
            ),
            mappings=dict(
                type='list'
            ),
            participant_property_references=dict(
                type='list',
                required=True
            ),
            reference_only=dict(
                type='str'
            ),
            operation_type=dict(
                type='str',
                choices=['upsert',
                         'delete']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.link_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLinks, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "source_entity_type":
                    self.parameters["source_entity_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "target_entity_type":
                    self.parameters["target_entity_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "source_entity_type_name":
                    self.parameters["source_entity_type_name"] = kwargs[key]
                elif key == "target_entity_type_name":
                    self.parameters["target_entity_type_name"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "mappings":
                    ev = kwargs[key]
                    if 'link_type' in ev:
                        if ev['link_type'] == 'update_always':
                            ev['link_type'] = 'UpdateAlways'
                        elif ev['link_type'] == 'copy_if_null':
                            ev['link_type'] = 'CopyIfNull'
                    self.parameters["mappings"] = ev
                elif key == "participant_property_references":
                    self.parameters["participant_property_references"] = kwargs[key]
                elif key == "reference_only":
                    self.parameters["reference_only"] = kwargs[key]
                elif key == "operation_type":
                    self.parameters["operation_type"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_link()

        if not old_response:
            self.log("Link instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Link instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Link instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Link instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_link()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Link instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_link()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_link():
                time.sleep(20)
        else:
            self.log("Link instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_link(self):
        '''
        Creates or updates Link with the specified configuration.

        :return: deserialized Link instance state dictionary
        '''
        self.log("Creating / Updating the Link instance {0}".format(self.link_name))

        try:
            response = self.mgmt_client.links.create_or_update(resource_group_name=self.resource_group,
                                                               hub_name=self.hub_name,
                                                               link_name=self.link_name,
                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Link instance.')
            self.fail("Error creating the Link instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_link(self):
        '''
        Deletes specified Link instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Link instance {0}".format(self.link_name))
        try:
            response = self.mgmt_client.links.delete(resource_group_name=self.resource_group,
                                                     hub_name=self.hub_name,
                                                     link_name=self.link_name)
        except CloudError as e:
            self.log('Error attempting to delete the Link instance.')
            self.fail("Error deleting the Link instance: {0}".format(str(e)))

        return True

    def get_link(self):
        '''
        Gets the properties of the specified Link.

        :return: deserialized Link instance state dictionary
        '''
        self.log("Checking if the Link instance {0} is present".format(self.link_name))
        found = False
        try:
            response = self.mgmt_client.links.get(resource_group_name=self.resource_group,
                                                  hub_name=self.hub_name,
                                                  link_name=self.link_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Link instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Link instance.')
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
    AzureRMLinks()


if __name__ == '__main__':
    main()

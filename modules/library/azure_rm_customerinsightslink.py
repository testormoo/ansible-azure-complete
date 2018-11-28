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
short_description: Manage Azure Link instance.
description:
    - Create, update and delete instance of Azure Link.

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
            - The name of the link.
        required: True
    source_entity_type:
        description:
            - Type of source entity.
            - Required when C(state) is I(present).
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    target_entity_type:
        description:
            - Type of target entity.
            - Required when C(state) is I(present).
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    source_entity_type_name:
        description:
            - Name of the source Entity Type.
            - Required when C(state) is I(present).
    target_entity_type_name:
        description:
            - Name of the target Entity Type.
            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
            target_property_name:
                description:
                    - Property name on the target Entity Type.
                    - Required when C(state) is I(present).
            link_type:
                description:
                    - Link type.
                choices:
                    - 'update_always'
                    - 'copy_if_null'
    participant_property_references:
        description:
            - The properties that represent the participating C(C(profile)).
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
      name: linkTest4806
      source_entity_type: Interaction
      target_entity_type: Profile
      source_entity_type_name: testInteraction1949
      target_entity_type_name: testProfile1446
      display_name: {
  "en-us": "Link DisplayName"
}
      description: {
  "en-us": "Link Description"
}
      mappings:
        - source_property_name: testInteraction1949
          target_property_name: testProfile1446
          link_type: UpdateAlways
      participant_property_references:
        - source_property_name: testInteraction1949
          target_property_name: ProfileId
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


class AzureRMLink(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            source_entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship']
            ),
            target_entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship']
            ),
            source_entity_type_name=dict(
                type='str'
            ),
            target_entity_type_name=dict(
                type='str'
            ),
            display_name=dict(
                type='dict'
            ),
            description=dict(
                type='dict'
            ),
            mappings=dict(
                type='list'
                options=dict(
                    source_property_name=dict(
                        type='str'
                    ),
                    target_property_name=dict(
                        type='str'
                    ),
                    link_type=dict(
                        type='str',
                        choices=['update_always',
                                 'copy_if_null']
                    )
                )
            ),
            participant_property_references=dict(
                type='list'
                options=dict(
                    source_property_name=dict(
                        type='str'
                    ),
                    target_property_name=dict(
                        type='str'
                    )
                )
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLink, self).__init__(derived_arg_spec=self.module_arg_spec,
                                          supports_check_mode=True,
                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['source_entity_type'], True)
        dict_camelize(self.parameters, ['target_entity_type'], True)
        dict_camelize(self.parameters, ['mappings', 'link_type'], True)
        dict_camelize(self.parameters, ['operation_type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Link instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_link()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Link instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_link()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Link instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_link(self):
        '''
        Creates or updates Link with the specified configuration.

        :return: deserialized Link instance state dictionary
        '''
        self.log("Creating / Updating the Link instance {0}".format(self.name))

        try:
            response = self.mgmt_client.links.create_or_update(resource_group_name=self.resource_group,
                                                               hub_name=self.hub_name,
                                                               link_name=self.name,
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
        self.log("Deleting the Link instance {0}".format(self.name))
        try:
            response = self.mgmt_client.links.delete(resource_group_name=self.resource_group,
                                                     hub_name=self.hub_name,
                                                     link_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Link instance.')
            self.fail("Error deleting the Link instance: {0}".format(str(e)))

        return True

    def get_link(self):
        '''
        Gets the properties of the specified Link.

        :return: deserialized Link instance state dictionary
        '''
        self.log("Checking if the Link instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.links.get(resource_group_name=self.resource_group,
                                                  hub_name=self.hub_name,
                                                  link_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Link instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Link instance.')
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
    AzureRMLink()


if __name__ == '__main__':
    main()

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
module: azure_rm_frontdoorroutingrule
version_added: "2.8"
short_description: Manage Azure Routing Rule instance.
description:
    - Create, update and delete instance of Azure Routing Rule.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    name:
        description:
            - Name of the Routing Rule which is unique within the Front Door.
        required: True
    id:
        description:
            - Resource ID.
    frontend_endpoints:
        description:
            - Frontend endpoints associated with this rule
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
    accepted_protocols:
        description:
            - Protocol schemes to match for this rule
        type: list
    patterns_to_match:
        description:
            - The route patterns of the rule.
        type: list
    custom_forwarding_path:
        description:
            - A custom path used to rewrite resource paths matched by this rule. Leave empty to use incoming path.
    forwarding_protocol:
        description:
            - Protocol this rule will use when forwarding traffic to backends.
        choices:
            - 'http_only'
            - 'https_only'
            - 'match_request'
    cache_configuration:
        description:
            - The caching configuration associated with this rule.
        suboptions:
            query_parameter_strip_directive:
                description:
                    - Treatment of URL query terms when forming the cache key.
                choices:
                    - 'strip_none'
                    - 'strip_all'
            dynamic_compression:
                description:
                    - "Whether to use dynamic compression for cached content. Possible values include: 'Enabled', 'Disabled'"
                type: bool
    backend_pool:
        description:
            - A reference to the BackendPool which this rule routes to.
        suboptions:
            id:
                description:
                    - Resource ID.
    enabled_state:
        description:
            - "Whether to enable use of this rule. Permitted values are 'C(enabled)' or 'C(disabled)'. Possible values include: 'C(enabled)', 'C(disabled)'"
        type: bool
    resource_state:
        description:
            - Resource status.
        choices:
            - 'creating'
            - 'enabling'
            - 'enabled'
            - 'disabling'
            - 'disabled'
            - 'deleting'
    name:
        description:
            - Resource name.
    state:
      description:
        - Assert the state of the Routing Rule.
        - Use 'present' to create or update an Routing Rule and 'absent' to delete it.
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
  - name: Create (or update) Routing Rule
    azure_rm_frontdoorroutingrule:
      resource_group: rg1
      front_door_name: frontDoor1
      name: routingRule1
      frontend_endpoints:
        - id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/frontendEndpoints/frontendEndpoint1
      accepted_protocols:
        - [
  "Http"
]
      patterns_to_match:
        - [
  "/*"
]
      cache_configuration:
        dynamic_compression: dynamic_compression
      backend_pool:
        id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/backendPools/backendPool1
      enabled_state: enabled_state
      name: routingRule1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/routingRule1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.frontdoor import FrontDoorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRoutingRule(AzureRMModuleBase):
    """Configuration class for an Azure RM Routing Rule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            front_door_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            frontend_endpoints=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            accepted_protocols=dict(
                type='list'
            ),
            patterns_to_match=dict(
                type='list'
            ),
            custom_forwarding_path=dict(
                type='str'
            ),
            forwarding_protocol=dict(
                type='str',
                choices=['http_only',
                         'https_only',
                         'match_request']
            ),
            cache_configuration=dict(
                type='dict'
                options=dict(
                    query_parameter_strip_directive=dict(
                        type='str',
                        choices=['strip_none',
                                 'strip_all']
                    ),
                    dynamic_compression=dict(
                        type='bool'
                    )
                )
            ),
            backend_pool=dict(
                type='dict'
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            enabled_state=dict(
                type='bool'
            ),
            resource_state=dict(
                type='str',
                choices=['creating',
                         'enabling',
                         'enabled',
                         'disabling',
                         'disabled',
                         'deleting']
            ),
            name=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.front_door_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRoutingRule, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.routing_rule_parameters[key] = kwargs[key]

        dict_resource_id(self.routing_rule_parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.routing_rule_parameters, ['frontend_endpoints', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.routing_rule_parameters, ['forwarding_protocol'], True)
        dict_camelize(self.routing_rule_parameters, ['cache_configuration', 'query_parameter_strip_directive'], True)
        dict_map(self.routing_rule_parameters, ['cache_configuration', 'dynamic_compression'], {True: 'Enabled', False: 'Disabled'})
        dict_resource_id(self.routing_rule_parameters, ['backend_pool', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_map(self.routing_rule_parameters, ['enabled_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.routing_rule_parameters, ['resource_state'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_routingrule()

        if not old_response:
            self.log("Routing Rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Routing Rule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.routing_rule_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Routing Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_routingrule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Routing Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_routingrule()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Routing Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_routingrule(self):
        '''
        Creates or updates Routing Rule with the specified configuration.

        :return: deserialized Routing Rule instance state dictionary
        '''
        self.log("Creating / Updating the Routing Rule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.routing_rules.create_or_update(resource_group_name=self.resource_group,
                                                                       front_door_name=self.front_door_name,
                                                                       routing_rule_name=self.name,
                                                                       routing_rule_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Routing Rule instance.')
            self.fail("Error creating the Routing Rule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_routingrule(self):
        '''
        Deletes specified Routing Rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Routing Rule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.routing_rules.delete(resource_group_name=self.resource_group,
                                                             front_door_name=self.front_door_name,
                                                             routing_rule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Routing Rule instance.')
            self.fail("Error deleting the Routing Rule instance: {0}".format(str(e)))

        return True

    def get_routingrule(self):
        '''
        Gets the properties of the specified Routing Rule.

        :return: deserialized Routing Rule instance state dictionary
        '''
        self.log("Checking if the Routing Rule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.routing_rules.get(resource_group_name=self.resource_group,
                                                          front_door_name=self.front_door_name,
                                                          routing_rule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Routing Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Routing Rule instance.')
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


def main():
    """Main execution"""
    AzureRMRoutingRule()


if __name__ == '__main__':
    main()

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
short_description: Manage Routing Rule instance.
description:
    - Create, update and delete instance of Routing Rule.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    routing_rule_name:
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
                    - Whether to use dynamic compression for cached content.
                choices:
                    - 'enabled'
                    - 'disabled'
    backend_pool:
        description:
            - A reference to the BackendPool which this rule routes to.
        suboptions:
            id:
                description:
                    - Resource ID.
    enabled_state:
        description:
            - "Whether to enable use of this rule. Permitted values are 'C(C(enabled))' or 'C(C(disabled))'."
        choices:
            - 'enabled'
            - 'disabled'
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
      routing_rule_name: routingRule1
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


class AzureRMRoutingRules(AzureRMModuleBase):
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
            routing_rule_name=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            frontend_endpoints=dict(
                type='list'
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
            ),
            backend_pool=dict(
                type='dict'
            ),
            enabled_state=dict(
                type='str',
                choices=['enabled',
                         'disabled']
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
        self.routing_rule_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRoutingRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "id":
                    self.parameters["id"] = kwargs[key]
                elif key == "frontend_endpoints":
                    self.parameters["frontend_endpoints"] = kwargs[key]
                elif key == "accepted_protocols":
                    self.parameters["accepted_protocols"] = kwargs[key]
                elif key == "patterns_to_match":
                    self.parameters["patterns_to_match"] = kwargs[key]
                elif key == "custom_forwarding_path":
                    self.parameters["custom_forwarding_path"] = kwargs[key]
                elif key == "forwarding_protocol":
                    self.parameters["forwarding_protocol"] = _snake_to_camel(kwargs[key], True)
                elif key == "cache_configuration":
                    ev = kwargs[key]
                    if 'query_parameter_strip_directive' in ev:
                        if ev['query_parameter_strip_directive'] == 'strip_none':
                            ev['query_parameter_strip_directive'] = 'StripNone'
                        elif ev['query_parameter_strip_directive'] == 'strip_all':
                            ev['query_parameter_strip_directive'] = 'StripAll'
                    if 'dynamic_compression' in ev:
                        if ev['dynamic_compression'] == 'enabled':
                            ev['dynamic_compression'] = 'Enabled'
                        elif ev['dynamic_compression'] == 'disabled':
                            ev['dynamic_compression'] = 'Disabled'
                    self.parameters["cache_configuration"] = ev
                elif key == "backend_pool":
                    self.parameters["backend_pool"] = kwargs[key]
                elif key == "enabled_state":
                    self.parameters["enabled_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "resource_state":
                    self.parameters["resource_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Routing Rule instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Routing Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_routingrule()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Routing Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_routingrule()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_routingrule():
                time.sleep(20)
        else:
            self.log("Routing Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_routingrule(self):
        '''
        Creates or updates Routing Rule with the specified configuration.

        :return: deserialized Routing Rule instance state dictionary
        '''
        self.log("Creating / Updating the Routing Rule instance {0}".format(self.routing_rule_name))

        try:
            response = self.mgmt_client.routing_rules.create_or_update(resource_group_name=self.resource_group,
                                                                       front_door_name=self.front_door_name,
                                                                       routing_rule_name=self.routing_rule_name,
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
        self.log("Deleting the Routing Rule instance {0}".format(self.routing_rule_name))
        try:
            response = self.mgmt_client.routing_rules.delete(resource_group_name=self.resource_group,
                                                             front_door_name=self.front_door_name,
                                                             routing_rule_name=self.routing_rule_name)
        except CloudError as e:
            self.log('Error attempting to delete the Routing Rule instance.')
            self.fail("Error deleting the Routing Rule instance: {0}".format(str(e)))

        return True

    def get_routingrule(self):
        '''
        Gets the properties of the specified Routing Rule.

        :return: deserialized Routing Rule instance state dictionary
        '''
        self.log("Checking if the Routing Rule instance {0} is present".format(self.routing_rule_name))
        found = False
        try:
            response = self.mgmt_client.routing_rules.get(resource_group_name=self.resource_group,
                                                          front_door_name=self.front_door_name,
                                                          routing_rule_name=self.routing_rule_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Routing Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Routing Rule instance.')
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
    AzureRMRoutingRules()


if __name__ == '__main__':
    main()
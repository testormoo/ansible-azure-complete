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
module: azure_rm_frontdoor
version_added: "2.8"
short_description: Manage Azure Front Door instance.
description:
    - Create, update and delete instance of Azure Front Door.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    location:
        description:
            - Resource location.
    friendly_name:
        description:
            - A friendly name for the frontDoor
    routing_rules:
        description:
            - Routing rules associated with this Front Door.
        type: list
        suboptions:
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
                    - "Whether to enable use of this rule. Permitted values are 'C(enabled)' or 'C(disabled)'. Possible values include: 'C(enabled)',
                       'C(disabled)'"
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
    load_balancing_settings:
        description:
            - Load balancing settings associated with this Front Door instance.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            sample_size:
                description:
                    - The number of samples to consider for load balancing decisions
            successful_samples_required:
                description:
                    - The number of samples within the sample period that must succeed
            additional_latency_milliseconds:
                description:
                    - The additional latency in milliseconds for probes to fall into the lowest latency bucket
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
    health_probe_settings:
        description:
            - Health probe settings associated with this Front Door instance.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            path:
                description:
                    - The path to use for the health probe. Default is /
            protocol:
                description:
                    - Protocol scheme to use for this probe.
                choices:
                    - 'http'
                    - 'https'
            interval_in_seconds:
                description:
                    - The number of seconds between health probes.
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
    backend_pools:
        description:
            - Backend pools available to routing rules.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            backends:
                description:
                    - The set of backends for this pool
                type: list
                suboptions:
                    address:
                        description:
                            - Location of the backend (IP address or FQDN)
                    http_port:
                        description:
                            - The HTTP TCP port number. Must be between 1 and 65535.
                    https_port:
                        description:
                            - The HTTPS TCP port number. Must be between 1 and 65535.
                    enabled_state:
                        description:
                            - "Whether to enable use of this backend. Permitted values are 'Enabled' or 'Disabled'. Possible values include: 'Enabled',
                               'Disabled'"
                        type: bool
                    priority:
                        description:
                            - "Priority to use for load balancing. Higher priorities will not be used for load balancing if any lower priority backend is
                               healthy."
                    weight:
                        description:
                            - Weight of this endpoint for load balancing purposes.
                    backend_host_header:
                        description:
                            - The value to use as the host header sent to the backend. If blank or unspecified, this defaults to the incoming host.
            load_balancing_settings:
                description:
                    - Load balancing settings for a backend pool
                suboptions:
                    id:
                        description:
                            - Resource ID.
            health_probe_settings:
                description:
                    - L7 health probe settings for a backend pool
                suboptions:
                    id:
                        description:
                            - Resource ID.
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
    frontend_endpoints:
        description:
            - Frontend endpoints available to routing rules.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            host_name:
                description:
                    - The host name of the frontendEndpoint. Must be a domain name.
            session_affinity_enabled_state:
                description:
                    - "Whether to allow session affinity on this host. Valid options are 'C(enabled)' or 'C(disabled)'. Possible values include:
                       'C(enabled)', 'C(disabled)'"
                type: bool
            session_affinity_ttl_seconds:
                description:
                    - UNUSED. This field will be ignored. The TTL to use in seconds for session affinity, if applicable.
            web_application_firewall_policy_link:
                description:
                    - Defines the Web Application Firewall policy for each host (if applicable)
                suboptions:
                    id:
                        description:
                            - Resource ID.
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
    enabled_state:
        description:
            - "Operational status of the Front Door load balancer. Permitted values are 'C(enabled)' or 'C(disabled)'. Possible values include:
               'C(enabled)', 'C(disabled)'"
        type: bool
    resource_state:
        description:
            - Resource status of the Front Door.
        choices:
            - 'creating'
            - 'enabling'
            - 'enabled'
            - 'disabling'
            - 'disabled'
            - 'deleting'
    state:
      description:
        - Assert the state of the Front Door.
        - Use 'present' to create or update an Front Door and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Front Door
    azure_rm_frontdoor:
      resource_group: rg1
      name: frontDoor1
      location: westus
      routing_rules:
        - frontend_endpoints:
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
      load_balancing_settings:
        - sample_size: 4
          successful_samples_required: 2
          name: loadBalancingSettings1
      health_probe_settings:
        - path: /
          protocol: Http
          interval_in_seconds: 120
          name: healthProbeSettings1
      backend_pools:
        - backends:
            - address: w3.contoso.com
              http_port: 80
              https_port: 443
              enabled_state: enabled_state
              priority: 2
              weight: 1
          load_balancing_settings:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/loadBalancingSettings/loadBalancingSettings1
          health_probe_settings:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/healthProbeSettings/healthProbeSettings1
          name: backendPool1
      frontend_endpoints:
        - host_name: www.contoso.com
          session_affinity_enabled_state: session_affinity_enabled_state
          session_affinity_ttl_seconds: 60
          web_application_firewall_policy_link:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoorWebApplicationFirewallPolicies/policy1
          name: frontendEndpoint1
      enabled_state: enabled_state
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1
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


class AzureRMFrontDoor(AzureRMModuleBase):
    """Configuration class for an Azure RM Front Door resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            friendly_name=dict(
                type='str'
            ),
            routing_rules=dict(
                type='list'
            ),
            load_balancing_settings=dict(
                type='list'
            ),
            health_probe_settings=dict(
                type='list'
            ),
            backend_pools=dict(
                type='list'
            ),
            frontend_endpoints=dict(
                type='list'
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
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFrontDoor, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.front_door_parameters[key] = kwargs[key]

        dict_camelize(self.front_door_parameters, ['routing_rules', 'forwarding_protocol'], True)
        dict_camelize(self.front_door_parameters, ['routing_rules', 'cache_configuration', 'query_parameter_strip_directive'], True)
        dict_map(self.front_door_parameters, ['routing_rules', 'cache_configuration', 'dynamic_compression'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.front_door_parameters, ['routing_rules', 'enabled_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.front_door_parameters, ['routing_rules', 'resource_state'], True)
        dict_camelize(self.front_door_parameters, ['load_balancing_settings', 'resource_state'], True)
        dict_camelize(self.front_door_parameters, ['health_probe_settings', 'protocol'], True)
        dict_camelize(self.front_door_parameters, ['health_probe_settings', 'resource_state'], True)
        dict_map(self.front_door_parameters, ['backend_pools', 'backends', 'enabled_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.front_door_parameters, ['backend_pools', 'resource_state'], True)
        dict_map(self.front_door_parameters, ['frontend_endpoints', 'session_affinity_enabled_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.front_door_parameters, ['frontend_endpoints', 'resource_state'], True)
        dict_map(self.front_door_parameters, ['enabled_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.front_door_parameters, ['resource_state'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_frontdoor()

        if not old_response:
            self.log("Front Door instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Front Door instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.front_door_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Front Door instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_frontdoor()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Front Door instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_frontdoor()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_frontdoor():
                time.sleep(20)
        else:
            self.log("Front Door instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_frontdoor(self):
        '''
        Creates or updates Front Door with the specified configuration.

        :return: deserialized Front Door instance state dictionary
        '''
        self.log("Creating / Updating the Front Door instance {0}".format(self.name))

        try:
            response = self.mgmt_client.front_doors.create_or_update(resource_group_name=self.resource_group,
                                                                     front_door_name=self.name,
                                                                     front_door_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Front Door instance.')
            self.fail("Error creating the Front Door instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_frontdoor(self):
        '''
        Deletes specified Front Door instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Front Door instance {0}".format(self.name))
        try:
            response = self.mgmt_client.front_doors.delete(resource_group_name=self.resource_group,
                                                           front_door_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Front Door instance.')
            self.fail("Error deleting the Front Door instance: {0}".format(str(e)))

        return True

    def get_frontdoor(self):
        '''
        Gets the properties of the specified Front Door.

        :return: deserialized Front Door instance state dictionary
        '''
        self.log("Checking if the Front Door instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.front_doors.get(resource_group_name=self.resource_group,
                                                        front_door_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Front Door instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Front Door instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMFrontDoor()


if __name__ == '__main__':
    main()

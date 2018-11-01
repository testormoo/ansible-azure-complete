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
short_description: Manage Front Door instance.
description:
    - Create, update and delete instance of Front Door.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
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
                            - "Whether to enable use of this backend. Permitted values are 'C(enabled)' or 'C(disabled)'."
                        choices:
                            - 'enabled'
                            - 'disabled'
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
                    - "Whether to allow session affinity on this host. Valid options are 'C(C(enabled))' or 'C(C(disabled))'."
                choices:
                    - 'enabled'
                    - 'disabled'
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
            - "Operational status of the Front Door load balancer. Permitted values are 'C(C(enabled))' or 'C(C(disabled))'."
        choices:
            - 'enabled'
            - 'disabled'
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
      front_door_name: frontDoor1
      location: westus
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


class AzureRMFrontDoors(AzureRMModuleBase):
    """Configuration class for an Azure RM Front Door resource"""

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
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.front_door_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFrontDoors, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "friendly_name":
                    self.parameters["friendly_name"] = kwargs[key]
                elif key == "routing_rules":
                    ev = kwargs[key]
                    if 'forwarding_protocol' in ev:
                        if ev['forwarding_protocol'] == 'http_only':
                            ev['forwarding_protocol'] = 'HttpOnly'
                        elif ev['forwarding_protocol'] == 'https_only':
                            ev['forwarding_protocol'] = 'HttpsOnly'
                        elif ev['forwarding_protocol'] == 'match_request':
                            ev['forwarding_protocol'] = 'MatchRequest'
                    if 'enabled_state' in ev:
                        if ev['enabled_state'] == 'enabled':
                            ev['enabled_state'] = 'Enabled'
                        elif ev['enabled_state'] == 'disabled':
                            ev['enabled_state'] = 'Disabled'
                    if 'resource_state' in ev:
                        if ev['resource_state'] == 'creating':
                            ev['resource_state'] = 'Creating'
                        elif ev['resource_state'] == 'enabling':
                            ev['resource_state'] = 'Enabling'
                        elif ev['resource_state'] == 'enabled':
                            ev['resource_state'] = 'Enabled'
                        elif ev['resource_state'] == 'disabling':
                            ev['resource_state'] = 'Disabling'
                        elif ev['resource_state'] == 'disabled':
                            ev['resource_state'] = 'Disabled'
                        elif ev['resource_state'] == 'deleting':
                            ev['resource_state'] = 'Deleting'
                    self.parameters["routing_rules"] = ev
                elif key == "load_balancing_settings":
                    ev = kwargs[key]
                    if 'resource_state' in ev:
                        if ev['resource_state'] == 'creating':
                            ev['resource_state'] = 'Creating'
                        elif ev['resource_state'] == 'enabling':
                            ev['resource_state'] = 'Enabling'
                        elif ev['resource_state'] == 'enabled':
                            ev['resource_state'] = 'Enabled'
                        elif ev['resource_state'] == 'disabling':
                            ev['resource_state'] = 'Disabling'
                        elif ev['resource_state'] == 'disabled':
                            ev['resource_state'] = 'Disabled'
                        elif ev['resource_state'] == 'deleting':
                            ev['resource_state'] = 'Deleting'
                    self.parameters["load_balancing_settings"] = ev
                elif key == "health_probe_settings":
                    ev = kwargs[key]
                    if 'protocol' in ev:
                        if ev['protocol'] == 'http':
                            ev['protocol'] = 'Http'
                        elif ev['protocol'] == 'https':
                            ev['protocol'] = 'Https'
                    if 'resource_state' in ev:
                        if ev['resource_state'] == 'creating':
                            ev['resource_state'] = 'Creating'
                        elif ev['resource_state'] == 'enabling':
                            ev['resource_state'] = 'Enabling'
                        elif ev['resource_state'] == 'enabled':
                            ev['resource_state'] = 'Enabled'
                        elif ev['resource_state'] == 'disabling':
                            ev['resource_state'] = 'Disabling'
                        elif ev['resource_state'] == 'disabled':
                            ev['resource_state'] = 'Disabled'
                        elif ev['resource_state'] == 'deleting':
                            ev['resource_state'] = 'Deleting'
                    self.parameters["health_probe_settings"] = ev
                elif key == "backend_pools":
                    ev = kwargs[key]
                    if 'resource_state' in ev:
                        if ev['resource_state'] == 'creating':
                            ev['resource_state'] = 'Creating'
                        elif ev['resource_state'] == 'enabling':
                            ev['resource_state'] = 'Enabling'
                        elif ev['resource_state'] == 'enabled':
                            ev['resource_state'] = 'Enabled'
                        elif ev['resource_state'] == 'disabling':
                            ev['resource_state'] = 'Disabling'
                        elif ev['resource_state'] == 'disabled':
                            ev['resource_state'] = 'Disabled'
                        elif ev['resource_state'] == 'deleting':
                            ev['resource_state'] = 'Deleting'
                    self.parameters["backend_pools"] = ev
                elif key == "frontend_endpoints":
                    ev = kwargs[key]
                    if 'session_affinity_enabled_state' in ev:
                        if ev['session_affinity_enabled_state'] == 'enabled':
                            ev['session_affinity_enabled_state'] = 'Enabled'
                        elif ev['session_affinity_enabled_state'] == 'disabled':
                            ev['session_affinity_enabled_state'] = 'Disabled'
                    if 'resource_state' in ev:
                        if ev['resource_state'] == 'creating':
                            ev['resource_state'] = 'Creating'
                        elif ev['resource_state'] == 'enabling':
                            ev['resource_state'] = 'Enabling'
                        elif ev['resource_state'] == 'enabled':
                            ev['resource_state'] = 'Enabled'
                        elif ev['resource_state'] == 'disabling':
                            ev['resource_state'] = 'Disabling'
                        elif ev['resource_state'] == 'disabled':
                            ev['resource_state'] = 'Disabled'
                        elif ev['resource_state'] == 'deleting':
                            ev['resource_state'] = 'Deleting'
                    self.parameters["frontend_endpoints"] = ev
                elif key == "enabled_state":
                    self.parameters["enabled_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "resource_state":
                    self.parameters["resource_state"] = _snake_to_camel(kwargs[key], True)

        old_response = None
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
                self.log("Need to check if Front Door instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Front Door instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_frontdoor()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_frontdoor(self):
        '''
        Creates or updates Front Door with the specified configuration.

        :return: deserialized Front Door instance state dictionary
        '''
        self.log("Creating / Updating the Front Door instance {0}".format(self.front_door_name))

        try:
            response = self.mgmt_client.front_doors.create_or_update(resource_group_name=self.resource_group,
                                                                     front_door_name=self.front_door_name,
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
        self.log("Deleting the Front Door instance {0}".format(self.front_door_name))
        try:
            response = self.mgmt_client.front_doors.delete(resource_group_name=self.resource_group,
                                                           front_door_name=self.front_door_name)
        except CloudError as e:
            self.log('Error attempting to delete the Front Door instance.')
            self.fail("Error deleting the Front Door instance: {0}".format(str(e)))

        return True

    def get_frontdoor(self):
        '''
        Gets the properties of the specified Front Door.

        :return: deserialized Front Door instance state dictionary
        '''
        self.log("Checking if the Front Door instance {0} is present".format(self.front_door_name))
        found = False
        try:
            response = self.mgmt_client.front_doors.get(resource_group_name=self.resource_group,
                                                        front_door_name=self.front_door_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Front Door instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Front Door instance.')
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
    AzureRMFrontDoors()


if __name__ == '__main__':
    main()

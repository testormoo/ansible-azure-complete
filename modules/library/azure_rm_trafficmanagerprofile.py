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
module: azure_rm_trafficmanagerprofile
version_added: "2.8"
short_description: Manage Azure Profile instance.
description:
    - Create, update and delete instance of Azure Profile.

options:
    resource_group:
        description:
            - The name of the resource group containing the Traffic Manager profile.
        required: True
    name:
        description:
            - The name of the Traffic Manager profile.
        required: True
    id:
        description:
            - "Fully qualified resource Id for the resource. Ex -
               /subscriptions/{subscriptionId}/resourceGroups/{I(resource_group)}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
    name:
        description:
            - The name of the resource
    type:
        description:
            - The type of the resource. Ex- Microsoft.Network/trafficmanagerProfiles.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    profile_status:
        description:
            - "The status of the Traffic Manager profile. Possible values include: 'Enabled', 'Disabled'"
        type: bool
    traffic_routing_method:
        description:
            - The traffic routing method of the Traffic Manager profile.
        choices:
            - 'performance'
            - 'priority'
            - 'weighted'
            - 'geographic'
            - 'multi_value'
            - 'subnet'
    dns_config:
        description:
            - The DNS settings of the Traffic Manager profile.
        suboptions:
            relative_name:
                description:
                    - "The relative DNS name provided by this Traffic Manager profile. This value is combined with the DNS domain name used by Azure Traffic
                       Manager to form the fully-qualified domain name (FQDN) of the profile."
            ttl:
                description:
                    - "The DNS Time-To-Live (TTL), in seconds. This informs the local DNS resolvers and DNS clients how long to cache DNS responses provided
                       by this Traffic Manager profile."
    monitor_config:
        description:
            - The endpoint monitoring settings of the Traffic Manager profile.
        suboptions:
            profile_monitor_status:
                description:
                    - The profile-level monitoring status of the Traffic Manager profile.
                choices:
                    - 'checking_endpoints'
                    - 'online'
                    - 'degraded'
                    - 'disabled'
                    - 'inactive'
            protocol:
                description:
                    - The protocol (C(http), C(https) or C(tcp)) used to probe for endpoint health.
                choices:
                    - 'http'
                    - 'https'
                    - 'tcp'
            port:
                description:
                    - The C(tcp) port used to probe for endpoint health.
            path:
                description:
                    - The path relative to the endpoint domain name used to probe for endpoint health.
            interval_in_seconds:
                description:
                    - "The monitor interval for endpoints in this profile. This is the interval at which Traffic Manager will check the health of each
                       endpoint in this profile."
            timeout_in_seconds:
                description:
                    - "The monitor timeout for endpoints in this profile. This is the time that Traffic Manager allows endpoints in this profile to response
                       to the health check."
            tolerated_number_of_failures:
                description:
                    - "The number of consecutive failed health check that Traffic Manager tolerates before declaring an endpoint in this profile C(degraded)
                       after the next failed health check."
            custom_headers:
                description:
                    - List of custom headers.
                type: list
                suboptions:
                    name:
                        description:
                            - Header name.
                    value:
                        description:
                            - Header value.
            expected_status_code_ranges:
                description:
                    - List of expected status code ranges.
                type: list
                suboptions:
                    min:
                        description:
                            - Min status code.
                    max:
                        description:
                            - Max status code.
    endpoints:
        description:
            - The list of endpoints in the Traffic Manager profile.
        type: list
        suboptions:
            id:
                description:
                    - "Fully qualified resource Id for the resource. Ex -
                       /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
            name:
                description:
                    - The name of the resource
            type:
                description:
                    - The type of the resource. Ex- Microsoft.Network/trafficmanagerProfiles.
            target_resource_id:
                description:
                    - "The Azure Resource URI of the of the endpoint. Not applicable to endpoints of I(type) 'ExternalEndpoints'."
            target:
                description:
                    - "The fully-qualified DNS name or IP address of the endpoint. Traffic Manager returns this value in DNS responses to direct traffic to
                       this endpoint."
            endpoint_status:
                description:
                    - "The status of the endpoint. If the endpoint is Enabled, it is probed for endpoint health and is included in the traffic routing
                       method. Possible values include: 'Enabled', 'C(disabled)'"
                type: bool
            weight:
                description:
                    - "The weight of this endpoint when using the 'Weighted' traffic routing method. Possible values are from 1 to 1000."
            priority:
                description:
                    - "The priority of this endpoint when using the 'Priority' traffic routing method. Possible values are from 1 to 1000, lower values
                       represent higher priority. This is an optional parameter.  If specified, it must be specified on all endpoints, and no two endpoints
                       can share the same priority value."
            endpoint_location:
                description:
                    - "Specifies the location of the external or nested endpoints when using the 'Performance' traffic routing method."
            endpoint_monitor_status:
                description:
                    - The monitoring status of the endpoint.
                choices:
                    - 'checking_endpoint'
                    - 'online'
                    - 'degraded'
                    - 'disabled'
                    - 'inactive'
                    - 'stopped'
            min_child_endpoints:
                description:
                    - "The minimum number of endpoints that must be available in the child profile in order for the parent profile to be considered
                       available. Only applicable to endpoint of I(type) 'NestedEndpoints'."
            geo_mapping:
                description:
                    - "The list of countries/regions mapped to this endpoint when using the 'Geographic' traffic routing method. Please consult Traffic
                       Manager Geographic documentation for a full list of accepted values."
                type: list
            subnets:
                description:
                    - "The list of subnets, IP addresses, and/or address ranges mapped to this endpoint when using the 'Subnet' traffic routing method. An
                       empty list will match all ranges not covered by other endpoints."
                type: list
                suboptions:
                    first:
                        description:
                            - First address in the subnet.
                    last:
                        description:
                            - Last address in the subnet.
                    scope:
                        description:
                            - Block size (number of leading bits in the subnet mask).
            custom_headers:
                description:
                    - List of custom headers.
                type: list
                suboptions:
                    name:
                        description:
                            - Header name.
                    value:
                        description:
                            - Header value.
    traffic_view_enrollment_status:
        description:
            - "Indicates whether Traffic View is 'Enabled' or 'Disabled' for the Traffic Manager profile. Null, indicates 'Disabled'. Enabling this feature
               will increase the cost of the Traffic Manage profile. Possible values include: 'Enabled', 'Disabled'"
        type: bool
    max_return:
        description:
            - Maximum number of I(endpoints) to be returned for C(multi_value) routing I(type).
    state:
      description:
        - Assert the state of the Profile.
        - Use 'present' to create or update an Profile and 'absent' to delete it.
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
  - name: Create (or update) Profile
    azure_rm_trafficmanagerprofile:
      resource_group: azuresdkfornetautoresttrafficmanager1421
      name: azsmnet6386
      location: eastus
      profile_status: profile_status
      traffic_routing_method: Performance
      dns_config:
        relative_name: azsmnet6386
        ttl: 35
      monitor_config:
        protocol: HTTP
        port: 80
        path: /testpath.aspx
      endpoints:
        - endpoint_status: endpoint_status
      traffic_view_enrollment_status: traffic_view_enrollment_status
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/{subscription-id}/resourceGroups/azuresdkfornetautoresttrafficmanager2583/providers/Microsoft.Network/trafficManagerProfiles/azur
            esdkfornetautoresttrafficmanager6192"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.trafficmanager import TrafficManagerManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMProfile(AzureRMModuleBase):
    """Configuration class for an Azure RM Profile resource"""

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
            id=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            type=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            profile_status=dict(
                type='bool'
            ),
            traffic_routing_method=dict(
                type='str',
                choices=['performance',
                         'priority',
                         'weighted',
                         'geographic',
                         'multi_value',
                         'subnet']
            ),
            dns_config=dict(
                type='dict'
            ),
            monitor_config=dict(
                type='dict'
            ),
            endpoints=dict(
                type='list'
            ),
            traffic_view_enrollment_status=dict(
                type='bool'
            ),
            max_return=dict(
                type='int'
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

        super(AzureRMProfile, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_map(self.parameters, ['profile_status'], '{True: 'Enabled', False: 'Disabled'}')
        dict_camelize(self.parameters, ['traffic_routing_method'], True)
        dict_camelize(self.parameters, ['monitor_config', 'profile_monitor_status'], True)
        dict_upper(self.parameters, ['monitor_config', 'protocol'])
        dict_map(self.parameters, ['endpoints', 'endpoint_status'], '{True: 'Enabled', False: 'Disabled'}')
        dict_camelize(self.parameters, ['endpoints', 'endpoint_monitor_status'], True)
        dict_map(self.parameters, ['traffic_view_enrollment_status'], '{True: 'Enabled', False: 'Disabled'}')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(TrafficManagerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_profile()

        if not old_response:
            self.log("Profile instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Profile instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Profile instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_profile()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Profile instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_profile()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_profile():
                time.sleep(20)
        else:
            self.log("Profile instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_profile(self):
        '''
        Creates or updates Profile with the specified configuration.

        :return: deserialized Profile instance state dictionary
        '''
        self.log("Creating / Updating the Profile instance {0}".format(self.name))

        try:
            response = self.mgmt_client.profiles.create_or_update(resource_group_name=self.resource_group,
                                                                  profile_name=self.name,
                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Profile instance.')
            self.fail("Error creating the Profile instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_profile(self):
        '''
        Deletes specified Profile instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Profile instance {0}".format(self.name))
        try:
            response = self.mgmt_client.profiles.delete(resource_group_name=self.resource_group,
                                                        profile_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Profile instance.')
            self.fail("Error deleting the Profile instance: {0}".format(str(e)))

        return True

    def get_profile(self):
        '''
        Gets the properties of the specified Profile.

        :return: deserialized Profile instance state dictionary
        '''
        self.log("Checking if the Profile instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.profiles.get(resource_group_name=self.resource_group,
                                                     profile_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Profile instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Profile instance.')
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
    AzureRMProfile()


if __name__ == '__main__':
    main()

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
module: azure_rm_trafficmanagerendpoint
version_added: "2.8"
short_description: Manage Azure Endpoint instance.
description:
    - Create, update and delete instance of Azure Endpoint.

options:
    resource_group:
        description:
            - The name of the resource group containing the Traffic Manager endpoint to be created or updated.
        required: True
    profile_name:
        description:
            - The name of the Traffic Manager profile.
        required: True
    endpoint_type:
        description:
            - The I(type) of the Traffic Manager endpoint to be created or updated.
        required: True
    name:
        description:
            - The name of the Traffic Manager endpoint to be created or updated.
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
    target_resource_id:
        description:
            - "The Azure Resource URI of the of the endpoint. Not applicable to endpoints of I(type) 'ExternalEndpoints'."
    target:
        description:
            - "The fully-qualified DNS name or IP address of the endpoint. Traffic Manager returns this value in DNS responses to direct traffic to this
               endpoint."
    endpoint_status:
        description:
            - "The status of the endpoint. If the endpoint is Enabled, it is probed for endpoint health and is included in the traffic routing method.
               Possible values include: 'Enabled', 'C(disabled)'"
        type: bool
    weight:
        description:
            - "The weight of this endpoint when using the 'Weighted' traffic routing method. Possible values are from 1 to 1000."
    priority:
        description:
            - "The priority of this endpoint when using the 'Priority' traffic routing method. Possible values are from 1 to 1000, lower values represent
               higher priority. This is an optional parameter.  If specified, it must be specified on all endpoints, and no two endpoints can share the
               same priority value."
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
            - "The minimum number of endpoints that must be available in the child profile in order for the parent profile to be considered available. Only
               applicable to endpoint of I(type) 'NestedEndpoints'."
    geo_mapping:
        description:
            - "The list of countries/regions mapped to this endpoint when using the 'Geographic' traffic routing method. Please consult Traffic Manager
               Geographic documentation for a full list of accepted values."
        type: list
    subnets:
        description:
            - "The list of subnets, IP addresses, and/or address ranges mapped to this endpoint when using the 'Subnet' traffic routing method. An empty
               list will match all ranges not covered by other endpoints."
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
    state:
      description:
        - Assert the state of the Endpoint.
        - Use 'present' to create or update an Endpoint and 'absent' to delete it.
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
  - name: Create (or update) Endpoint
    azure_rm_trafficmanagerendpoint:
      resource_group: azuresdkfornetautoresttrafficmanager2191
      profile_name: azuresdkfornetautoresttrafficmanager8224
      endpoint_type: ExternalEndpoints
      name: My%20external%20endpoint
      name: My external endpoint
      type: Microsoft.network/TrafficManagerProfiles/ExternalEndpoints
      target: foobar.contoso.com
      endpoint_status: endpoint_status
      geo_mapping:
        - [
  "GEO-AS",
  "GEO-AF"
]
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
    returned: always
    type: str
    sample: "/subscriptions/{subscription-id}/resourceGroups/azuresdkfornetautoresttrafficmanager1421/providers/Microsoft.Network/trafficManagerProfiles/azsm
            net6386/externalEndpoints/azsmnet7187"
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


class AzureRMEndpoint(AzureRMModuleBase):
    """Configuration class for an Azure RM Endpoint resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            endpoint_type=dict(
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
            target_resource_id=dict(
                type='str'
            ),
            target=dict(
                type='str'
            ),
            endpoint_status=dict(
                type='bool'
            ),
            weight=dict(
                type='int'
            ),
            priority=dict(
                type='int'
            ),
            endpoint_location=dict(
                type='str'
            ),
            endpoint_monitor_status=dict(
                type='str',
                choices=['checking_endpoint',
                         'online',
                         'degraded',
                         'disabled',
                         'inactive',
                         'stopped']
            ),
            min_child_endpoints=dict(
                type='int'
            ),
            geo_mapping=dict(
                type='list'
            ),
            subnets=dict(
                type='list'
            ),
            custom_headers=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.profile_name = None
        self.endpoint_type = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEndpoint, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_map(self.parameters, ['endpoint_status'], '{True: 'Enabled', False: 'Disabled'}')
        dict_camelize(self.parameters, ['endpoint_monitor_status'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(TrafficManagerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_endpoint()

        if not old_response:
            self.log("Endpoint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Endpoint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_endpoint()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Endpoint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_endpoint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_endpoint():
                time.sleep(20)
        else:
            self.log("Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_endpoint(self):
        '''
        Creates or updates Endpoint with the specified configuration.

        :return: deserialized Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Endpoint instance {0}".format(self.name))

        try:
            response = self.mgmt_client.endpoints.create_or_update(resource_group_name=self.resource_group,
                                                                   profile_name=self.profile_name,
                                                                   endpoint_type=self.endpoint_type,
                                                                   endpoint_name=self.name,
                                                                   parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Endpoint instance.')
            self.fail("Error creating the Endpoint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_endpoint(self):
        '''
        Deletes specified Endpoint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Endpoint instance {0}".format(self.name))
        try:
            response = self.mgmt_client.endpoints.delete(resource_group_name=self.resource_group,
                                                         profile_name=self.profile_name,
                                                         endpoint_type=self.endpoint_type,
                                                         endpoint_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Endpoint instance.')
            self.fail("Error deleting the Endpoint instance: {0}".format(str(e)))

        return True

    def get_endpoint(self):
        '''
        Gets the properties of the specified Endpoint.

        :return: deserialized Endpoint instance state dictionary
        '''
        self.log("Checking if the Endpoint instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.endpoints.get(resource_group_name=self.resource_group,
                                                      profile_name=self.profile_name,
                                                      endpoint_type=self.endpoint_type,
                                                      endpoint_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Endpoint instance.')
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
    AzureRMEndpoint()


if __name__ == '__main__':
    main()

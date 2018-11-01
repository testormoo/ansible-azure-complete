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
short_description: Manage Endpoint instance.
description:
    - Create, update and delete instance of Endpoint.

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
    endpoint_name:
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
            - The status of the endpoint. If the endpoint is C(enabled), it is probed for endpoint health and is included in the traffic routing method.
        choices:
            - 'enabled'
            - 'disabled'
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
      endpoint_name: My%20external%20endpoint
      name: My external endpoint
      type: Microsoft.network/TrafficManagerProfiles/ExternalEndpoints
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


class AzureRMEndpoints(AzureRMModuleBase):
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
            endpoint_name=dict(
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
                type='str',
                choices=['enabled',
                         'disabled']
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
        self.endpoint_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEndpoints, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "type":
                    self.parameters["type"] = kwargs[key]
                elif key == "target_resource_id":
                    self.parameters["target_resource_id"] = kwargs[key]
                elif key == "target":
                    self.parameters["target"] = kwargs[key]
                elif key == "endpoint_status":
                    self.parameters["endpoint_status"] = _snake_to_camel(kwargs[key], True)
                elif key == "weight":
                    self.parameters["weight"] = kwargs[key]
                elif key == "priority":
                    self.parameters["priority"] = kwargs[key]
                elif key == "endpoint_location":
                    self.parameters["endpoint_location"] = kwargs[key]
                elif key == "endpoint_monitor_status":
                    self.parameters["endpoint_monitor_status"] = _snake_to_camel(kwargs[key], True)
                elif key == "min_child_endpoints":
                    self.parameters["min_child_endpoints"] = kwargs[key]
                elif key == "geo_mapping":
                    self.parameters["geo_mapping"] = kwargs[key]
                elif key == "subnets":
                    self.parameters["subnets"] = kwargs[key]
                elif key == "custom_headers":
                    self.parameters["custom_headers"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Endpoint instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_endpoint()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_endpoint(self):
        '''
        Creates or updates Endpoint with the specified configuration.

        :return: deserialized Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Endpoint instance {0}".format(self.endpoint_name))

        try:
            response = self.mgmt_client.endpoints.create_or_update(resource_group_name=self.resource_group,
                                                                   profile_name=self.profile_name,
                                                                   endpoint_type=self.endpoint_type,
                                                                   endpoint_name=self.endpoint_name,
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
        self.log("Deleting the Endpoint instance {0}".format(self.endpoint_name))
        try:
            response = self.mgmt_client.endpoints.delete(resource_group_name=self.resource_group,
                                                         profile_name=self.profile_name,
                                                         endpoint_type=self.endpoint_type,
                                                         endpoint_name=self.endpoint_name)
        except CloudError as e:
            self.log('Error attempting to delete the Endpoint instance.')
            self.fail("Error deleting the Endpoint instance: {0}".format(str(e)))

        return True

    def get_endpoint(self):
        '''
        Gets the properties of the specified Endpoint.

        :return: deserialized Endpoint instance state dictionary
        '''
        self.log("Checking if the Endpoint instance {0} is present".format(self.endpoint_name))
        found = False
        try:
            response = self.mgmt_client.endpoints.get(resource_group_name=self.resource_group,
                                                      profile_name=self.profile_name,
                                                      endpoint_type=self.endpoint_type,
                                                      endpoint_name=self.endpoint_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Endpoint instance.')
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
    AzureRMEndpoints()


if __name__ == '__main__':
    main()

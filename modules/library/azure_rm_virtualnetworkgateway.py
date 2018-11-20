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
module: azure_rm_virtualnetworkgateway
version_added: "2.8"
short_description: Manage Virtual Network Gateway instance.
description:
    - Create, update and delete instance of Virtual Network Gateway.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the virtual network gateway.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    ip_configurations:
        description:
            - IP configurations for virtual network gateway.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            private_ip_allocation_method:
                description:
                    - "The private IP allocation method. Possible values are: 'C(static)' and 'C(dynamic)'."
                choices:
                    - 'static'
                    - 'dynamic'
            subnet:
                description:
                    - The reference of the subnet resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            public_ip_address:
                description:
                    - The reference of the public IP resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    gateway_type:
        description:
            - "The type of this virtual network gateway. Possible values are: 'C(vpn)' and 'C(express_route)'."
        choices:
            - 'vpn'
            - 'express_route'
    vpn_type:
        description:
            - "The type of this virtual network gateway. Possible values are: 'C(policy_based)' and 'C(route_based)'."
        choices:
            - 'policy_based'
            - 'route_based'
    enable_bgp:
        description:
            - Whether BGP is enabled for this virtual network gateway or not.
    active_active:
        description:
            - ActiveActive flag
    gateway_default_site:
        description:
            - "The reference of the LocalNetworkGateway resource which represents local network site having default routes. Assign Null value in case of
               removing existing default site setting."
        suboptions:
            id:
                description:
                    - Resource ID.
    sku:
        description:
            - The reference of the VirtualNetworkGatewaySku resource which represents the SKU selected for Virtual network gateway.
        suboptions:
            name:
                description:
                    - Gateway SKU name.
                choices:
                    - 'basic'
                    - 'high_performance'
                    - 'standard'
                    - 'ultra_performance'
                    - 'vpn_gw1'
                    - 'vpn_gw2'
                    - 'vpn_gw3'
            tier:
                description:
                    - Gateway SKU tier.
                choices:
                    - 'basic'
                    - 'high_performance'
                    - 'standard'
                    - 'ultra_performance'
                    - 'vpn_gw1'
                    - 'vpn_gw2'
                    - 'vpn_gw3'
            capacity:
                description:
                    - The capacity.
    vpn_client_configuration:
        description:
            - The reference of the VpnClientConfiguration resource which represents the P2S VpnClient configurations.
        suboptions:
            vpn_client_address_pool:
                description:
                    - The reference of the address space resource which represents Address space for P2S VpnClient.
                suboptions:
                    address_prefixes:
                        description:
                            - A list of address blocks reserved for this virtual network in CIDR notation.
                        type: list
            vpn_client_root_certificates:
                description:
                    - VpnClientRootCertificate for virtual network gateway.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    public_cert_data:
                        description:
                            - The certificate public data.
                            - Required when C(state) is I(present).
                    name:
                        description:
                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            vpn_client_revoked_certificates:
                description:
                    - VpnClientRevokedCertificate for Virtual network gateway.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    thumbprint:
                        description:
                            - The revoked VPN client certificate thumbprint.
                    name:
                        description:
                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            vpn_client_protocols:
                description:
                    - VpnClientProtocols for Virtual network gateway.
                type: list
            radius_server_address:
                description:
                    - The radius server address property of the VirtualNetworkGateway resource for vpn client connection.
            radius_server_secret:
                description:
                    - The radius secret property of the VirtualNetworkGateway resource for vpn client connection.
    bgp_settings:
        description:
            - "Virtual network gateway's BGP speaker settings."
        suboptions:
            asn:
                description:
                    - "The BGP speaker's ASN."
            bgp_peering_address:
                description:
                    - The BGP peering address and BGP identifier of this BGP speaker.
            peer_weight:
                description:
                    - The weight added to routes learned from this BGP speaker.
    resource_guid:
        description:
            - The resource GUID property of the VirtualNetworkGateway resource.
    state:
      description:
        - Assert the state of the Virtual Network Gateway.
        - Use 'present' to create or update an Virtual Network Gateway and 'absent' to delete it.
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
  - name: Create (or update) Virtual Network Gateway
    azure_rm_virtualnetworkgateway:
      resource_group: NOT FOUND
      name: NOT FOUND
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVirtualNetworkGateways(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network Gateway resource"""

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
            location=dict(
                type='str'
            ),
            ip_configurations=dict(
                type='list'
            ),
            gateway_type=dict(
                type='str',
                choices=['vpn',
                         'express_route']
            ),
            vpn_type=dict(
                type='str',
                choices=['policy_based',
                         'route_based']
            ),
            enable_bgp=dict(
                type='str'
            ),
            active_active=dict(
                type='str'
            ),
            gateway_default_site=dict(
                type='dict'
            ),
            sku=dict(
                type='dict'
            ),
            vpn_client_configuration=dict(
                type='dict'
            ),
            bgp_settings=dict(
                type='dict'
            ),
            resource_guid=dict(
                type='str'
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

        super(AzureRMVirtualNetworkGateways, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "id":
                    self.parameters["id"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "ip_configurations":
                    ev = kwargs[key]
                    if 'private_ip_allocation_method' in ev:
                        if ev['private_ip_allocation_method'] == 'static':
                            ev['private_ip_allocation_method'] = 'Static'
                        elif ev['private_ip_allocation_method'] == 'dynamic':
                            ev['private_ip_allocation_method'] = 'Dynamic'
                    self.parameters["ip_configurations"] = ev
                elif key == "gateway_type":
                    self.parameters["gateway_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "vpn_type":
                    self.parameters["vpn_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "enable_bgp":
                    self.parameters["enable_bgp"] = kwargs[key]
                elif key == "active_active":
                    self.parameters["active_active"] = kwargs[key]
                elif key == "gateway_default_site":
                    self.parameters["gateway_default_site"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                        elif ev['name'] == 'high_performance':
                            ev['name'] = 'HighPerformance'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                        elif ev['name'] == 'ultra_performance':
                            ev['name'] = 'UltraPerformance'
                        elif ev['name'] == 'vpn_gw1':
                            ev['name'] = 'VpnGw1'
                        elif ev['name'] == 'vpn_gw2':
                            ev['name'] = 'VpnGw2'
                        elif ev['name'] == 'vpn_gw3':
                            ev['name'] = 'VpnGw3'
                    if 'tier' in ev:
                        if ev['tier'] == 'basic':
                            ev['tier'] = 'Basic'
                        elif ev['tier'] == 'high_performance':
                            ev['tier'] = 'HighPerformance'
                        elif ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                        elif ev['tier'] == 'ultra_performance':
                            ev['tier'] = 'UltraPerformance'
                        elif ev['tier'] == 'vpn_gw1':
                            ev['tier'] = 'VpnGw1'
                        elif ev['tier'] == 'vpn_gw2':
                            ev['tier'] = 'VpnGw2'
                        elif ev['tier'] == 'vpn_gw3':
                            ev['tier'] = 'VpnGw3'
                    self.parameters["sku"] = ev
                elif key == "vpn_client_configuration":
                    self.parameters["vpn_client_configuration"] = kwargs[key]
                elif key == "bgp_settings":
                    self.parameters["bgp_settings"] = kwargs[key]
                elif key == "resource_guid":
                    self.parameters["resource_guid"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_virtualnetworkgateway()

        if not old_response:
            self.log("Virtual Network Gateway instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Network Gateway instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network Gateway instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkgateway()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network Gateway instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetworkgateway()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_virtualnetworkgateway():
                time.sleep(20)
        else:
            self.log("Virtual Network Gateway instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_virtualnetworkgateway(self):
        '''
        Creates or updates Virtual Network Gateway with the specified configuration.

        :return: deserialized Virtual Network Gateway instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network Gateway instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_network_gateways.create_or_update(resource_group_name=self.resource_group,
                                                                                  virtual_network_gateway_name=self.name,
                                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Network Gateway instance.')
            self.fail("Error creating the Virtual Network Gateway instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetworkgateway(self):
        '''
        Deletes specified Virtual Network Gateway instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Network Gateway instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_network_gateways.delete(resource_group_name=self.resource_group,
                                                                        virtual_network_gateway_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network Gateway instance.')
            self.fail("Error deleting the Virtual Network Gateway instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkgateway(self):
        '''
        Gets the properties of the specified Virtual Network Gateway.

        :return: deserialized Virtual Network Gateway instance state dictionary
        '''
        self.log("Checking if the Virtual Network Gateway instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_gateways.get(resource_group_name=self.resource_group,
                                                                     virtual_network_gateway_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network Gateway instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network Gateway instance.')
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMVirtualNetworkGateways()


if __name__ == '__main__':
    main()

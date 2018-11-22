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
module: azure_rm_virtualnetworkgatewayconnection
version_added: "2.8"
short_description: Manage Azure Virtual Network Gateway Connection instance.
description:
    - Create, update and delete instance of Azure Virtual Network Gateway Connection.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the virtual network gateway connection.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    authorization_key:
        description:
            - The authorizationKey.
    virtual_network_gateway1:
        description:
            - The reference to virtual network gateway resource.
            - Required when C(state) is I(present).
        suboptions:
            id:
                description:
                    - Resource ID.
            location:
                description:
                    - Resource location.
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
                    - "The reference of the LocalNetworkGateway resource which represents local network site having default routes. Assign Null value in
                       case of removing existing default site setting."
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
    virtual_network_gateway2:
        description:
            - The reference to virtual network gateway resource.
        suboptions:
            id:
                description:
                    - Resource ID.
            location:
                description:
                    - Resource location.
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
                    - "The reference of the LocalNetworkGateway resource which represents local network site having default routes. Assign Null value in
                       case of removing existing default site setting."
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
    local_network_gateway2:
        description:
            - The reference to local network gateway resource.
        suboptions:
            id:
                description:
                    - Resource ID.
            location:
                description:
                    - Resource location.
            local_network_address_space:
                description:
                    - Local network site address space.
                suboptions:
                    address_prefixes:
                        description:
                            - A list of address blocks reserved for this virtual network in CIDR notation.
                        type: list
            gateway_ip_address:
                description:
                    - IP address of local network gateway.
            bgp_settings:
                description:
                    - "Local network gateway's BGP speaker settings."
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
                    - The resource GUID property of the LocalNetworkGateway resource.
    connection_type:
        description:
            - "Gateway connection type. Possible values are: 'C(ipsec)','C(vnet2_vnet)','C(express_route)', and 'C(vpn_client)."
            - Required when C(state) is I(present).
        choices:
            - 'ipsec'
            - 'vnet2_vnet'
            - 'express_route'
            - 'vpn_client'
    routing_weight:
        description:
            - The routing weight.
    shared_key:
        description:
            - The C(ipsec) shared key.
    peer:
        description:
            - The reference to peerings resource.
        suboptions:
            id:
                description:
                    - Resource ID.
    enable_bgp:
        description:
            - EnableBgp flag
    use_policy_based_traffic_selectors:
        description:
            - Enable policy-based traffic selectors.
    ipsec_policies:
        description:
            - The C(ipsec) Policies to be considered by this connection.
        type: list
        suboptions:
            sa_life_time_seconds:
                description:
                    - The IPSec Security Association (also called Quick Mode or Phase 2 SA) lifetime in seconds for a site to site VPN tunnel.
                    - Required when C(state) is I(present).
            sa_data_size_kilobytes:
                description:
                    - The IPSec Security Association (also called Quick Mode or Phase 2 SA) payload size in KB for a site to site VPN tunnel.
                    - Required when C(state) is I(present).
            ipsec_encryption:
                description:
                    - The IPSec encryption algorithm (IKE phase 1).
                    - Required when C(state) is I(present).
                choices:
                    - 'none'
                    - 'des'
                    - 'des3'
                    - 'aes128'
                    - 'aes192'
                    - 'aes256'
                    - 'gcmaes128'
                    - 'gcmaes192'
                    - 'gcmaes256'
            ipsec_integrity:
                description:
                    - The IPSec integrity algorithm (IKE phase 1).
                    - Required when C(state) is I(present).
                choices:
                    - 'md5'
                    - 'sha1'
                    - 'sha256'
                    - 'gcmaes128'
                    - 'gcmaes192'
                    - 'gcmaes256'
            ike_encryption:
                description:
                    - The IKE encryption algorithm (IKE phase 2).
                    - Required when C(state) is I(present).
                choices:
                    - 'des'
                    - 'des3'
                    - 'aes128'
                    - 'aes192'
                    - 'aes256'
            ike_integrity:
                description:
                    - The IKE integrity algorithm (IKE phase 2).
                    - Required when C(state) is I(present).
                choices:
                    - 'md5'
                    - 'sha1'
                    - 'sha256'
                    - 'sha384'
            dh_group:
                description:
                    - The DH Groups used in IKE Phase 1 for initial SA.
                    - Required when C(state) is I(present).
                choices:
                    - 'none'
                    - 'dh_group1'
                    - 'dh_group2'
                    - 'dh_group14'
                    - 'dh_group2048'
                    - 'ecp256'
                    - 'ecp384'
                    - 'dh_group24'
            pfs_group:
                description:
                    - The DH Groups used in IKE Phase 2 for new child SA.
                    - Required when C(state) is I(present).
                choices:
                    - 'none'
                    - 'pfs1'
                    - 'pfs2'
                    - 'pfs2048'
                    - 'ecp256'
                    - 'ecp384'
                    - 'pfs24'
    resource_guid:
        description:
            - The resource GUID property of the VirtualNetworkGatewayConnection resource.
    state:
      description:
        - Assert the state of the Virtual Network Gateway Connection.
        - Use 'present' to create or update an Virtual Network Gateway Connection and 'absent' to delete it.
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
  - name: Create (or update) Virtual Network Gateway Connection
    azure_rm_virtualnetworkgatewayconnection:
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


class AzureRMVirtualNetworkGatewayConnection(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network Gateway Connection resource"""

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
            authorization_key=dict(
                type='str'
            ),
            virtual_network_gateway1=dict(
                type='dict'
            ),
            virtual_network_gateway2=dict(
                type='dict'
            ),
            local_network_gateway2=dict(
                type='dict'
            ),
            connection_type=dict(
                type='str',
                choices=['ipsec',
                         'vnet2_vnet',
                         'express_route',
                         'vpn_client']
            ),
            routing_weight=dict(
                type='int'
            ),
            shared_key=dict(
                type='str'
            ),
            peer=dict(
                type='dict'
            ),
            enable_bgp=dict(
                type='str'
            ),
            use_policy_based_traffic_selectors=dict(
                type='str'
            ),
            ipsec_policies=dict(
                type='list'
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

        super(AzureRMVirtualNetworkGatewayConnection, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                        supports_check_mode=True,
                                                                        supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['virtual_network_gateway1', 'ip_configurations', 'private_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway1', 'gateway_type'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway1', 'vpn_type'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway1', 'sku', 'name'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway1', 'sku', 'tier'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway2', 'ip_configurations', 'private_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway2', 'gateway_type'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway2', 'vpn_type'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway2', 'sku', 'name'], True)
        dict_camelize(self.parameters, ['virtual_network_gateway2', 'sku', 'tier'], True)
        dict_camelize(self.parameters, ['connection_type'], True)
        dict_map(self.parameters, ['connection_type'], ''ipsec': 'IPsec', 'vpn_client': 'VPNClient'')
        dict_upper(self.parameters, ['ipsec_policies', 'ipsec_encryption'])
        dict_map(self.parameters, ['ipsec_policies', 'ipsec_encryption'], ''none': 'None'')
        dict_upper(self.parameters, ['ipsec_policies', 'ipsec_integrity'])
        dict_upper(self.parameters, ['ipsec_policies', 'ike_encryption'])
        dict_upper(self.parameters, ['ipsec_policies', 'ike_integrity'])
        dict_upper(self.parameters, ['ipsec_policies', 'dh_group'])
        dict_map(self.parameters, ['ipsec_policies', 'dh_group'], ''none': 'None', 'dh_group1': 'DHGroup1', 'dh_group2': 'DHGroup2', 'dh_group14': 'DHGroup14', 'dh_group2048': 'DHGroup2048', 'dh_group24': 'DHGroup24'')
        dict_upper(self.parameters, ['ipsec_policies', 'pfs_group'])
        dict_map(self.parameters, ['ipsec_policies', 'pfs_group'], ''none': 'None'')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_virtualnetworkgatewayconnection()

        if not old_response:
            self.log("Virtual Network Gateway Connection instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Network Gateway Connection instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network Gateway Connection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkgatewayconnection()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network Gateway Connection instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetworkgatewayconnection()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_virtualnetworkgatewayconnection():
                time.sleep(20)
        else:
            self.log("Virtual Network Gateway Connection instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_virtualnetworkgatewayconnection(self):
        '''
        Creates or updates Virtual Network Gateway Connection with the specified configuration.

        :return: deserialized Virtual Network Gateway Connection instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network Gateway Connection instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_network_gateway_connections.create_or_update(resource_group_name=self.resource_group,
                                                                                             virtual_network_gateway_connection_name=self.name,
                                                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Network Gateway Connection instance.')
            self.fail("Error creating the Virtual Network Gateway Connection instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetworkgatewayconnection(self):
        '''
        Deletes specified Virtual Network Gateway Connection instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Network Gateway Connection instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_network_gateway_connections.delete(resource_group_name=self.resource_group,
                                                                                   virtual_network_gateway_connection_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network Gateway Connection instance.')
            self.fail("Error deleting the Virtual Network Gateway Connection instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkgatewayconnection(self):
        '''
        Gets the properties of the specified Virtual Network Gateway Connection.

        :return: deserialized Virtual Network Gateway Connection instance state dictionary
        '''
        self.log("Checking if the Virtual Network Gateway Connection instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_gateway_connections.get(resource_group_name=self.resource_group,
                                                                                virtual_network_gateway_connection_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network Gateway Connection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network Gateway Connection instance.')
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
    AzureRMVirtualNetworkGatewayConnection()


if __name__ == '__main__':
    main()

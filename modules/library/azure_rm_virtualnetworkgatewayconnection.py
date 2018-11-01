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
short_description: Manage Virtual Network Gateway Connection instance.
description:
    - Create, update and delete instance of Virtual Network Gateway Connection.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    virtual_network_gateway_connection_name:
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
        required: True
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
                    etag:
                        description:
                            - A unique read-only string that changes whenever the resource is updated.
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
                                required: True
                            name:
                                description:
                                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                            etag:
                                description:
                                    - A unique read-only string that changes whenever the resource is updated.
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
                            etag:
                                description:
                                    - A unique read-only string that changes whenever the resource is updated.
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
            etag:
                description:
                    - Gets a unique read-only string that changes whenever the resource is updated.
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
                    etag:
                        description:
                            - A unique read-only string that changes whenever the resource is updated.
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
                                required: True
                            name:
                                description:
                                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                            etag:
                                description:
                                    - A unique read-only string that changes whenever the resource is updated.
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
                            etag:
                                description:
                                    - A unique read-only string that changes whenever the resource is updated.
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
            etag:
                description:
                    - Gets a unique read-only string that changes whenever the resource is updated.
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
            etag:
                description:
                    - A unique read-only string that changes whenever the resource is updated.
    connection_type:
        description:
            - "Gateway connection type. Possible values are: 'C(ipsec)','C(vnet2_vnet)','C(express_route)', and 'C(vpn_client)."
        required: True
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
                required: True
            sa_data_size_kilobytes:
                description:
                    - The IPSec Security Association (also called Quick Mode or Phase 2 SA) payload size in KB for a site to site VPN tunnel.
                required: True
            ipsec_encryption:
                description:
                    - The IPSec encryption algorithm (IKE phase 1).
                required: True
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
                required: True
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
                required: True
                choices:
                    - 'des'
                    - 'des3'
                    - 'aes128'
                    - 'aes192'
                    - 'aes256'
            ike_integrity:
                description:
                    - The IKE integrity algorithm (IKE phase 2).
                required: True
                choices:
                    - 'md5'
                    - 'sha1'
                    - 'sha256'
                    - 'sha384'
            dh_group:
                description:
                    - The DH Groups used in IKE Phase 1 for initial SA.
                required: True
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
                required: True
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
    etag:
        description:
            - Gets a unique read-only string that changes whenever the resource is updated.
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
      virtual_network_gateway_connection_name: NOT FOUND
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


class AzureRMVirtualNetworkGatewayConnections(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network Gateway Connection resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            virtual_network_gateway_connection_name=dict(
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
                type='dict',
                required=True
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
                         'vpn_client'],
                required=True
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
            etag=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.virtual_network_gateway_connection_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualNetworkGatewayConnections, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "authorization_key":
                    self.parameters["authorization_key"] = kwargs[key]
                elif key == "virtual_network_gateway1":
                    ev = kwargs[key]
                    if 'gateway_type' in ev:
                        if ev['gateway_type'] == 'vpn':
                            ev['gateway_type'] = 'Vpn'
                        elif ev['gateway_type'] == 'express_route':
                            ev['gateway_type'] = 'ExpressRoute'
                    if 'vpn_type' in ev:
                        if ev['vpn_type'] == 'policy_based':
                            ev['vpn_type'] = 'PolicyBased'
                        elif ev['vpn_type'] == 'route_based':
                            ev['vpn_type'] = 'RouteBased'
                    self.parameters["virtual_network_gateway1"] = ev
                elif key == "virtual_network_gateway2":
                    ev = kwargs[key]
                    if 'gateway_type' in ev:
                        if ev['gateway_type'] == 'vpn':
                            ev['gateway_type'] = 'Vpn'
                        elif ev['gateway_type'] == 'express_route':
                            ev['gateway_type'] = 'ExpressRoute'
                    if 'vpn_type' in ev:
                        if ev['vpn_type'] == 'policy_based':
                            ev['vpn_type'] = 'PolicyBased'
                        elif ev['vpn_type'] == 'route_based':
                            ev['vpn_type'] = 'RouteBased'
                    self.parameters["virtual_network_gateway2"] = ev
                elif key == "local_network_gateway2":
                    self.parameters["local_network_gateway2"] = kwargs[key]
                elif key == "connection_type":
                    ev = kwargs[key]
                    if ev == 'ipsec':
                        ev = 'IPsec'
                    elif ev == 'vpn_client':
                        ev = 'VPNClient'
                    self.parameters["connection_type"] = _snake_to_camel(ev, True)
                elif key == "routing_weight":
                    self.parameters["routing_weight"] = kwargs[key]
                elif key == "shared_key":
                    self.parameters["shared_key"] = kwargs[key]
                elif key == "peer":
                    self.parameters["peer"] = kwargs[key]
                elif key == "enable_bgp":
                    self.parameters["enable_bgp"] = kwargs[key]
                elif key == "use_policy_based_traffic_selectors":
                    self.parameters["use_policy_based_traffic_selectors"] = kwargs[key]
                elif key == "ipsec_policies":
                    ev = kwargs[key]
                    if 'ipsec_encryption' in ev:
                        if ev['ipsec_encryption'] == 'none':
                            ev['ipsec_encryption'] = 'None'
                        elif ev['ipsec_encryption'] == 'des':
                            ev['ipsec_encryption'] = 'DES'
                        elif ev['ipsec_encryption'] == 'des3':
                            ev['ipsec_encryption'] = 'DES3'
                        elif ev['ipsec_encryption'] == 'aes128':
                            ev['ipsec_encryption'] = 'AES128'
                        elif ev['ipsec_encryption'] == 'aes192':
                            ev['ipsec_encryption'] = 'AES192'
                        elif ev['ipsec_encryption'] == 'aes256':
                            ev['ipsec_encryption'] = 'AES256'
                        elif ev['ipsec_encryption'] == 'gcmaes128':
                            ev['ipsec_encryption'] = 'GCMAES128'
                        elif ev['ipsec_encryption'] == 'gcmaes192':
                            ev['ipsec_encryption'] = 'GCMAES192'
                        elif ev['ipsec_encryption'] == 'gcmaes256':
                            ev['ipsec_encryption'] = 'GCMAES256'
                    if 'ipsec_integrity' in ev:
                        if ev['ipsec_integrity'] == 'md5':
                            ev['ipsec_integrity'] = 'MD5'
                        elif ev['ipsec_integrity'] == 'sha1':
                            ev['ipsec_integrity'] = 'SHA1'
                        elif ev['ipsec_integrity'] == 'sha256':
                            ev['ipsec_integrity'] = 'SHA256'
                        elif ev['ipsec_integrity'] == 'gcmaes128':
                            ev['ipsec_integrity'] = 'GCMAES128'
                        elif ev['ipsec_integrity'] == 'gcmaes192':
                            ev['ipsec_integrity'] = 'GCMAES192'
                        elif ev['ipsec_integrity'] == 'gcmaes256':
                            ev['ipsec_integrity'] = 'GCMAES256'
                    if 'ike_encryption' in ev:
                        if ev['ike_encryption'] == 'des':
                            ev['ike_encryption'] = 'DES'
                        elif ev['ike_encryption'] == 'des3':
                            ev['ike_encryption'] = 'DES3'
                        elif ev['ike_encryption'] == 'aes128':
                            ev['ike_encryption'] = 'AES128'
                        elif ev['ike_encryption'] == 'aes192':
                            ev['ike_encryption'] = 'AES192'
                        elif ev['ike_encryption'] == 'aes256':
                            ev['ike_encryption'] = 'AES256'
                    if 'ike_integrity' in ev:
                        if ev['ike_integrity'] == 'md5':
                            ev['ike_integrity'] = 'MD5'
                        elif ev['ike_integrity'] == 'sha1':
                            ev['ike_integrity'] = 'SHA1'
                        elif ev['ike_integrity'] == 'sha256':
                            ev['ike_integrity'] = 'SHA256'
                        elif ev['ike_integrity'] == 'sha384':
                            ev['ike_integrity'] = 'SHA384'
                    if 'dh_group' in ev:
                        if ev['dh_group'] == 'none':
                            ev['dh_group'] = 'None'
                        elif ev['dh_group'] == 'dh_group1':
                            ev['dh_group'] = 'DHGroup1'
                        elif ev['dh_group'] == 'dh_group2':
                            ev['dh_group'] = 'DHGroup2'
                        elif ev['dh_group'] == 'dh_group14':
                            ev['dh_group'] = 'DHGroup14'
                        elif ev['dh_group'] == 'dh_group2048':
                            ev['dh_group'] = 'DHGroup2048'
                        elif ev['dh_group'] == 'ecp256':
                            ev['dh_group'] = 'ECP256'
                        elif ev['dh_group'] == 'ecp384':
                            ev['dh_group'] = 'ECP384'
                        elif ev['dh_group'] == 'dh_group24':
                            ev['dh_group'] = 'DHGroup24'
                    if 'pfs_group' in ev:
                        if ev['pfs_group'] == 'none':
                            ev['pfs_group'] = 'None'
                        elif ev['pfs_group'] == 'pfs1':
                            ev['pfs_group'] = 'PFS1'
                        elif ev['pfs_group'] == 'pfs2':
                            ev['pfs_group'] = 'PFS2'
                        elif ev['pfs_group'] == 'pfs2048':
                            ev['pfs_group'] = 'PFS2048'
                        elif ev['pfs_group'] == 'ecp256':
                            ev['pfs_group'] = 'ECP256'
                        elif ev['pfs_group'] == 'ecp384':
                            ev['pfs_group'] = 'ECP384'
                        elif ev['pfs_group'] == 'pfs24':
                            ev['pfs_group'] = 'PFS24'
                    self.parameters["ipsec_policies"] = ev
                elif key == "resource_guid":
                    self.parameters["resource_guid"] = kwargs[key]
                elif key == "etag":
                    self.parameters["etag"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Virtual Network Gateway Connection instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network Gateway Connection instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkgatewayconnection()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_virtualnetworkgatewayconnection(self):
        '''
        Creates or updates Virtual Network Gateway Connection with the specified configuration.

        :return: deserialized Virtual Network Gateway Connection instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network Gateway Connection instance {0}".format(self.virtual_network_gateway_connection_name))

        try:
            response = self.mgmt_client.virtual_network_gateway_connections.create_or_update(resource_group_name=self.resource_group,
                                                                                             virtual_network_gateway_connection_name=self.virtual_network_gateway_connection_name,
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
        self.log("Deleting the Virtual Network Gateway Connection instance {0}".format(self.virtual_network_gateway_connection_name))
        try:
            response = self.mgmt_client.virtual_network_gateway_connections.delete(resource_group_name=self.resource_group,
                                                                                   virtual_network_gateway_connection_name=self.virtual_network_gateway_connection_name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network Gateway Connection instance.')
            self.fail("Error deleting the Virtual Network Gateway Connection instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkgatewayconnection(self):
        '''
        Gets the properties of the specified Virtual Network Gateway Connection.

        :return: deserialized Virtual Network Gateway Connection instance state dictionary
        '''
        self.log("Checking if the Virtual Network Gateway Connection instance {0} is present".format(self.virtual_network_gateway_connection_name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_gateway_connections.get(resource_group_name=self.resource_group,
                                                                                virtual_network_gateway_connection_name=self.virtual_network_gateway_connection_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network Gateway Connection instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network Gateway Connection instance.')
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
    AzureRMVirtualNetworkGatewayConnections()


if __name__ == '__main__':
    main()

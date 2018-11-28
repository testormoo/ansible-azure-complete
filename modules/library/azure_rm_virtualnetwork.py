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
module: azure_rm_virtualnetwork
version_added: "2.8"
short_description: Manage Azure Virtual Network instance.
description:
    - Create, update and delete instance of Azure Virtual Network.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the virtual network.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    address_space:
        description:
            - The AddressSpace that contains an array of IP address ranges that can be used by I(subnets).
        suboptions:
            address_prefixes:
                description:
                    - A list of address blocks reserved for this virtual network in CIDR notation.
                type: list
    dhcp_options:
        description:
            - The dhcpOptions that contains an array of DNS servers available to VMs deployed in the virtual network.
        suboptions:
            dns_servers:
                description:
                    - The list of DNS servers IP addresses.
                type: list
    subnets:
        description:
            - A list of subnets in a Virtual Network.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            address_prefix:
                description:
                    - The address prefix for the subnet.
            network_security_group:
                description:
                    - The reference of the NetworkSecurityGroup resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    location:
                        description:
                            - Resource location.
                    security_rules:
                        description:
                            - A collection of security rules of the network security group.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - C(*)ResourceC(*) C(*)IDC(*).
                            description:
                                description:
                                    - "C(*)AC(*) C(*)descriptionC(*) C(*)forC(*) C(*)thisC(*) C(*)ruleC(*). C(*)RestrictedC(*) C(*)toC(*) C(*)140C(*)
                                       C(*)charsC(*)."
                            protocol:
                                description:
                                    - "C(*)NetworkC(*) C(*)protocolC(*) C(*)thisC(*) C(*)ruleC(*) C(*)appliesC(*) C(*)toC(*). C(*)PossibleC(*)
                                       C(*)valuesC(*) C(*)areC(*) 'C(*)CC(*)(C(*)tcpC(*))', 'C(*)CC(*)(C(*)udpC(*))', C(*)andC(*) '*'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'tcp'
                                    - 'udp'
                                    - '*'
                            source_port_range:
                                description:
                                    - "C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*)
                                       C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                                       C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                            destination_port_range:
                                description:
                                    - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*)
                                       C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                                       C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                            source_address_prefix:
                                description:
                                    - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*)
                                       C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*).
                                       C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)'
                                       C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*). C(*)IfC(*) C(*)thisC(*) C(*)isC(*)
                                       C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*), C(*)specifiesC(*) C(*)whereC(*) C(*)networkC(*) C(*)trafficC(*)
                                       C(*)originatesC(*) C(*)fromC(*). "
                            source_address_prefixes:
                                description:
                                    - C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangesC(*).
                                type: list
                            source_application_security_groups:
                                description:
                                    - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)sourceC(*).
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                            destination_address_prefix:
                                description:
                                    - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                       C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                                       C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*)
                                       'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*)
                                       C(*)beC(*) C(*)usedC(*)."
                            destination_address_prefixes:
                                description:
                                    - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                       C(*)IPC(*) C(*)rangesC(*)."
                                type: list
                            destination_application_security_groups:
                                description:
                                    - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)destinationC(*).
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                            source_port_ranges:
                                description:
                                    - C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)rangesC(*).
                                type: list
                            destination_port_ranges:
                                description:
                                    - C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)rangesC(*).
                                type: list
                            access:
                                description:
                                    - "C(*)TheC(*) C(*)networkC(*) C(*)trafficC(*) C(*)isC(*) C(*)allowedC(*) C(*)orC(*) C(*)deniedC(*). C(*)PossibleC(*)
                                       C(*)valuesC(*) C(*)areC(*): 'C(*)AllowC(*)' C(*)andC(*) 'C(*)DenyC(*)'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'allow'
                                    - 'deny'
                            priority:
                                description:
                                    - "C(*)TheC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)valueC(*) C(*)canC(*) C(*)beC(*)
                                       C(*)betweenC(*) C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*) C(*)mustC(*)
                                       C(*)beC(*) C(*)uniqueC(*) C(*)forC(*) C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*) C(*)collectionC(*).
                                       C(*)TheC(*) C(*)lowerC(*) C(*)theC(*) C(*)priorityC(*) C(*)numberC(*), C(*)theC(*) C(*)higherC(*) C(*)theC(*)
                                       C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*)."
                            direction:
                                description:
                                    - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*) C(*)specifiesC(*)
                                       C(*)ifC(*) C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*) C(*)incomingC(*) C(*)orC(*)
                                       C(*)outcomingC(*) C(*)trafficC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)InboundC(*)' C(*)andC(*)
                                       'C(*)OutboundC(*)'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'inbound'
                                    - 'outbound'
                            name:
                                description:
                                    - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*)
                                       C(*)withinC(*) C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*)
                                       C(*)usedC(*) C(*)toC(*) C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
                    default_security_rules:
                        description:
                            - The default security rules of network security group.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - C(*)ResourceC(*) C(*)IDC(*).
                            description:
                                description:
                                    - "C(*)AC(*) C(*)descriptionC(*) C(*)forC(*) C(*)thisC(*) C(*)ruleC(*). C(*)RestrictedC(*) C(*)toC(*) C(*)140C(*)
                                       C(*)charsC(*)."
                            protocol:
                                description:
                                    - "C(*)NetworkC(*) C(*)protocolC(*) C(*)thisC(*) C(*)ruleC(*) C(*)appliesC(*) C(*)toC(*). C(*)PossibleC(*)
                                       C(*)valuesC(*) C(*)areC(*) 'C(*)CC(*)(C(*)tcpC(*))', 'C(*)CC(*)(C(*)udpC(*))', C(*)andC(*) '*'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'tcp'
                                    - 'udp'
                                    - '*'
                            source_port_range:
                                description:
                                    - "C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*)
                                       C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                                       C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                            destination_port_range:
                                description:
                                    - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*)
                                       C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                                       C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                            source_address_prefix:
                                description:
                                    - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*)
                                       C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*).
                                       C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)'
                                       C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*). C(*)IfC(*) C(*)thisC(*) C(*)isC(*)
                                       C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*), C(*)specifiesC(*) C(*)whereC(*) C(*)networkC(*) C(*)trafficC(*)
                                       C(*)originatesC(*) C(*)fromC(*). "
                            source_address_prefixes:
                                description:
                                    - C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangesC(*).
                                type: list
                            source_application_security_groups:
                                description:
                                    - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)sourceC(*).
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                            destination_address_prefix:
                                description:
                                    - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                       C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                                       C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*)
                                       'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*)
                                       C(*)beC(*) C(*)usedC(*)."
                            destination_address_prefixes:
                                description:
                                    - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                       C(*)IPC(*) C(*)rangesC(*)."
                                type: list
                            destination_application_security_groups:
                                description:
                                    - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)destinationC(*).
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                            source_port_ranges:
                                description:
                                    - C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)rangesC(*).
                                type: list
                            destination_port_ranges:
                                description:
                                    - C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)rangesC(*).
                                type: list
                            access:
                                description:
                                    - "C(*)TheC(*) C(*)networkC(*) C(*)trafficC(*) C(*)isC(*) C(*)allowedC(*) C(*)orC(*) C(*)deniedC(*). C(*)PossibleC(*)
                                       C(*)valuesC(*) C(*)areC(*): 'C(*)AllowC(*)' C(*)andC(*) 'C(*)DenyC(*)'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'allow'
                                    - 'deny'
                            priority:
                                description:
                                    - "C(*)TheC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)valueC(*) C(*)canC(*) C(*)beC(*)
                                       C(*)betweenC(*) C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*) C(*)mustC(*)
                                       C(*)beC(*) C(*)uniqueC(*) C(*)forC(*) C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*) C(*)collectionC(*).
                                       C(*)TheC(*) C(*)lowerC(*) C(*)theC(*) C(*)priorityC(*) C(*)numberC(*), C(*)theC(*) C(*)higherC(*) C(*)theC(*)
                                       C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*)."
                            direction:
                                description:
                                    - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*) C(*)specifiesC(*)
                                       C(*)ifC(*) C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*) C(*)incomingC(*) C(*)orC(*)
                                       C(*)outcomingC(*) C(*)trafficC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)InboundC(*)' C(*)andC(*)
                                       'C(*)OutboundC(*)'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'inbound'
                                    - 'outbound'
                            name:
                                description:
                                    - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*)
                                       C(*)withinC(*) C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*)
                                       C(*)usedC(*) C(*)toC(*) C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
                    resource_guid:
                        description:
                            - The resource GUID property of the network security group resource.
            route_table:
                description:
                    - The reference of the RouteTable resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    location:
                        description:
                            - Resource location.
                    routes:
                        description:
                            - Collection of routes contained within a route table.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            address_prefix:
                                description:
                                    - The destination CIDR to which the route applies.
                            next_hop_type:
                                description:
                                    - "The type of Azure hop the packet should be sent to. Possible values are: 'C(virtual_network_gateway)',
                                       'C(vnet_local)', 'C(internet)', 'C(virtual_appliance)', and 'C(none)'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'virtual_network_gateway'
                                    - 'vnet_local'
                                    - 'internet'
                                    - 'virtual_appliance'
                                    - 'none'
                            next_hop_ip_address:
                                description:
                                    - "The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is
                                       C(virtual_appliance)."
                            name:
                                description:
                                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                    disable_bgp_route_propagation:
                        description:
                            - Gets or sets whether to disable the I(routes) learned by BGP on that route table. True means disable.
            service_endpoints:
                description:
                    - An array of service endpoints.
                type: list
                suboptions:
                    service:
                        description:
                            - The type of the endpoint service.
                    locations:
                        description:
                            - A list of locations.
                        type: list
            resource_navigation_links:
                description:
                    - Gets an array of references to the external resources using subnet.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    linked_resource_type:
                        description:
                            - Resource type of the linked resource.
                    link:
                        description:
                            - Link to the external resource
                    name:
                        description:
                            - Name of the resource that is unique within a resource group. This name can be used to access the resource.
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    virtual_network_peerings:
        description:
            - A list of peerings in a Virtual Network.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            allow_virtual_network_access:
                description:
                    - Whether the VMs in the linked virtual network space would be able to access all the VMs in local Virtual network space.
            allow_forwarded_traffic:
                description:
                    - Whether the forwarded traffic from the VMs in the remote virtual network will be allowed/disallowed.
            allow_gateway_transit:
                description:
                    - If gateway links can be used in remote virtual networking to link to this virtual network.
            use_remote_gateways:
                description:
                    - "If remote gateways can be used on this virtual network. If the flag is set to true, and I(allow_gateway_transit) on remote peering is
                       also true, virtual network will use gateways of remote virtual network for transit. Only one peering can have this flag set to true.
                       This flag cannot be set if virtual network already has a gateway."
            remote_virtual_network:
                description:
                    - "The reference of the remote virtual network. The remote virtual network can be in the same or different region (preview). See here to
                       register for the preview and learn more (https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-create-peering)."
                suboptions:
                    id:
                        description:
                            - Resource ID.
            remote_address_space:
                description:
                    - The reference of the remote virtual network address space.
                suboptions:
                    address_prefixes:
                        description:
                            - A list of address blocks reserved for this virtual network in CIDR notation.
                        type: list
            peering_state:
                description:
                    - "The status of the virtual network peering. Possible values are 'C(initiated)', 'C(connected)', and 'C(disconnected)'."
                choices:
                    - 'initiated'
                    - 'connected'
                    - 'disconnected'
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    resource_guid:
        description:
            - The resourceGuid property of the Virtual Network resource.
    enable_ddos_protection:
        description:
            - Indicates if DDoS protection is enabled for all the protected resources in a Virtual Network.
    enable_vm_protection:
        description:
            - Indicates if Vm protection is enabled for all the I(subnets) in a Virtual Network.
    state:
      description:
        - Assert the state of the Virtual Network.
        - Use 'present' to create or update an Virtual Network and 'absent' to delete it.
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
  - name: Create (or update) Virtual Network
    azure_rm_virtualnetwork:
      resource_group: rg1
      name: test-vnet
      location: eastus
      address_space:
        address_prefixes:
          - [
  "10.0.0.0/16"
]
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/virtualNetworks/test-vnet
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMVirtualNetwork(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network resource"""

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
            address_space=dict(
                type='dict',
                options=dict(
                    address_prefixes=dict(
                        type='list'
                    )
                )
            ),
            dhcp_options=dict(
                type='dict',
                options=dict(
                    dns_servers=dict(
                        type='list'
                    )
                )
            ),
            subnets=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    address_prefix=dict(
                        type='str'
                    ),
                    network_security_group=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            location=dict(
                                type='str'
                            ),
                            security_rules=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    description=dict(
                                        type='str'
                                    ),
                                    protocol=dict(
                                        type='str',
                                        choices=['tcp',
                                                 'udp',
                                                 '*']
                                    ),
                                    source_port_range=dict(
                                        type='str'
                                    ),
                                    destination_port_range=dict(
                                        type='str'
                                    ),
                                    source_address_prefix=dict(
                                        type='str'
                                    ),
                                    source_address_prefixes=dict(
                                        type='list'
                                    ),
                                    source_application_security_groups=dict(
                                        type='list',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    destination_address_prefix=dict(
                                        type='str'
                                    ),
                                    destination_address_prefixes=dict(
                                        type='list'
                                    ),
                                    destination_application_security_groups=dict(
                                        type='list',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    source_port_ranges=dict(
                                        type='list'
                                    ),
                                    destination_port_ranges=dict(
                                        type='list'
                                    ),
                                    access=dict(
                                        type='str',
                                        choices=['allow',
                                                 'deny']
                                    ),
                                    priority=dict(
                                        type='int'
                                    ),
                                    direction=dict(
                                        type='str',
                                        choices=['inbound',
                                                 'outbound']
                                    ),
                                    name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            default_security_rules=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    description=dict(
                                        type='str'
                                    ),
                                    protocol=dict(
                                        type='str',
                                        choices=['tcp',
                                                 'udp',
                                                 '*']
                                    ),
                                    source_port_range=dict(
                                        type='str'
                                    ),
                                    destination_port_range=dict(
                                        type='str'
                                    ),
                                    source_address_prefix=dict(
                                        type='str'
                                    ),
                                    source_address_prefixes=dict(
                                        type='list'
                                    ),
                                    source_application_security_groups=dict(
                                        type='list',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    destination_address_prefix=dict(
                                        type='str'
                                    ),
                                    destination_address_prefixes=dict(
                                        type='list'
                                    ),
                                    destination_application_security_groups=dict(
                                        type='list',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    source_port_ranges=dict(
                                        type='list'
                                    ),
                                    destination_port_ranges=dict(
                                        type='list'
                                    ),
                                    access=dict(
                                        type='str',
                                        choices=['allow',
                                                 'deny']
                                    ),
                                    priority=dict(
                                        type='int'
                                    ),
                                    direction=dict(
                                        type='str',
                                        choices=['inbound',
                                                 'outbound']
                                    ),
                                    name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            resource_guid=dict(
                                type='str'
                            )
                        )
                    ),
                    route_table=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            location=dict(
                                type='str'
                            ),
                            routes=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    address_prefix=dict(
                                        type='str'
                                    ),
                                    next_hop_type=dict(
                                        type='str',
                                        choices=['virtual_network_gateway',
                                                 'vnet_local',
                                                 'internet',
                                                 'virtual_appliance',
                                                 'none']
                                    ),
                                    next_hop_ip_address=dict(
                                        type='str'
                                    ),
                                    name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            disable_bgp_route_propagation=dict(
                                type='str'
                            )
                        )
                    ),
                    service_endpoints=dict(
                        type='list',
                        options=dict(
                            service=dict(
                                type='str'
                            ),
                            locations=dict(
                                type='list'
                            )
                        )
                    ),
                    resource_navigation_links=dict(
                        type='list',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            linked_resource_type=dict(
                                type='str'
                            ),
                            link=dict(
                                type='str'
                            ),
                            name=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            virtual_network_peerings=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    allow_virtual_network_access=dict(
                        type='str'
                    ),
                    allow_forwarded_traffic=dict(
                        type='str'
                    ),
                    allow_gateway_transit=dict(
                        type='str'
                    ),
                    use_remote_gateways=dict(
                        type='str'
                    ),
                    remote_virtual_network=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    remote_address_space=dict(
                        type='dict',
                        options=dict(
                            address_prefixes=dict(
                                type='list'
                            )
                        )
                    ),
                    peering_state=dict(
                        type='str',
                        choices=['initiated',
                                 'connected',
                                 'disconnected']
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            resource_guid=dict(
                type='str'
            ),
            enable_ddos_protection=dict(
                type='str'
            ),
            enable_vm_protection=dict(
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

        super(AzureRMVirtualNetwork, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['subnets', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['subnets', 'network_security_group', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['subnets', 'network_security_group', 'security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['subnets', 'network_security_group', 'security_rules', 'protocol'], True)
        dict_resource_id(self.parameters, ['subnets', 'network_security_group', 'security_rules', 'source_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['subnets', 'network_security_group', 'security_rules', 'destination_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['subnets', 'network_security_group', 'security_rules', 'access'], True)
        dict_camelize(self.parameters, ['subnets', 'network_security_group', 'security_rules', 'direction'], True)
        dict_resource_id(self.parameters, ['subnets', 'network_security_group', 'default_security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['subnets', 'network_security_group', 'default_security_rules', 'protocol'], True)
        dict_resource_id(self.parameters, ['subnets', 'network_security_group', 'default_security_rules', 'source_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['subnets', 'network_security_group', 'default_security_rules', 'destination_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['subnets', 'network_security_group', 'default_security_rules', 'access'], True)
        dict_camelize(self.parameters, ['subnets', 'network_security_group', 'default_security_rules', 'direction'], True)
        dict_resource_id(self.parameters, ['subnets', 'route_table', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['subnets', 'route_table', 'routes', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['subnets', 'route_table', 'routes', 'next_hop_type'], True)
        dict_resource_id(self.parameters, ['subnets', 'resource_navigation_links', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['virtual_network_peerings', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['virtual_network_peerings', 'remote_virtual_network', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['virtual_network_peerings', 'peering_state'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_virtualnetwork()

        if not old_response:
            self.log("Virtual Network instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Network instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetwork()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetwork()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Network instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_virtualnetwork(self):
        '''
        Creates or updates Virtual Network with the specified configuration.

        :return: deserialized Virtual Network instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_networks.create_or_update(resource_group_name=self.resource_group,
                                                                          virtual_network_name=self.name,
                                                                          parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Network instance.')
            self.fail("Error creating the Virtual Network instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetwork(self):
        '''
        Deletes specified Virtual Network instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Network instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_networks.delete(resource_group_name=self.resource_group,
                                                                virtual_network_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network instance.')
            self.fail("Error deleting the Virtual Network instance: {0}".format(str(e)))

        return True

    def get_virtualnetwork(self):
        '''
        Gets the properties of the specified Virtual Network.

        :return: deserialized Virtual Network instance state dictionary
        '''
        self.log("Checking if the Virtual Network instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_networks.get(resource_group_name=self.resource_group,
                                                             virtual_network_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network instance.')
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMVirtualNetwork()


if __name__ == '__main__':
    main()

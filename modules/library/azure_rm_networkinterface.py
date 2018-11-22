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
module: azure_rm_networkinterface
version_added: "2.8"
short_description: Manage Azure Network Interface instance.
description:
    - Create, update and delete instance of Azure Network Interface.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the network interface.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    virtual_machine:
        description:
            - The reference of a virtual machine.
        suboptions:
            id:
                description:
                    - Resource ID.
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
                            - C(*)AC(*) C(*)descriptionC(*) C(*)forC(*) C(*)thisC(*) C(*)ruleC(*). C(*)RestrictedC(*) C(*)toC(*) C(*)140C(*) C(*)charsC(*).
                    protocol:
                        description:
                            - "C(*)NetworkC(*) C(*)protocolC(*) C(*)thisC(*) C(*)ruleC(*) C(*)appliesC(*) C(*)toC(*). C(*)PossibleC(*) C(*)valuesC(*)
                               C(*)areC(*) 'C(*)CC(*)(C(*)tcpC(*))', 'C(*)CC(*)(C(*)udpC(*))', C(*)andC(*) '*'."
                            - Required when C(state) is I(present).
                        choices:
                            - 'tcp'
                            - 'udp'
                            - '*'
                    source_port_range:
                        description:
                            - "C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*) C(*)betweenC(*)
                               C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                               C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                    destination_port_range:
                        description:
                            - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*)
                               C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)
                               C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                    source_address_prefix:
                        description:
                            - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*)
                               C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*)
                               C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*)
                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*). C(*)IfC(*) C(*)thisC(*) C(*)isC(*) C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*),
                               C(*)specifiesC(*) C(*)whereC(*) C(*)networkC(*) C(*)trafficC(*) C(*)originatesC(*) C(*)fromC(*). "
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
                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*)
                               C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*)
                               C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)',
                               'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)."
                    destination_address_prefixes:
                        description:
                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*)
                               C(*)rangesC(*)."
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
                               C(*)betweenC(*) C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*) C(*)mustC(*) C(*)beC(*)
                               C(*)uniqueC(*) C(*)forC(*) C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*) C(*)collectionC(*). C(*)TheC(*) C(*)lowerC(*)
                               C(*)theC(*) C(*)priorityC(*) C(*)numberC(*), C(*)theC(*) C(*)higherC(*) C(*)theC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*)
                               C(*)ruleC(*)."
                    direction:
                        description:
                            - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*) C(*)specifiesC(*) C(*)ifC(*)
                               C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*) C(*)incomingC(*) C(*)orC(*) C(*)outcomingC(*)
                               C(*)trafficC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)InboundC(*)' C(*)andC(*) 'C(*)OutboundC(*)'."
                            - Required when C(state) is I(present).
                        choices:
                            - 'inbound'
                            - 'outbound'
                    name:
                        description:
                            - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*) C(*)withinC(*)
                               C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                               C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
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
                            - C(*)AC(*) C(*)descriptionC(*) C(*)forC(*) C(*)thisC(*) C(*)ruleC(*). C(*)RestrictedC(*) C(*)toC(*) C(*)140C(*) C(*)charsC(*).
                    protocol:
                        description:
                            - "C(*)NetworkC(*) C(*)protocolC(*) C(*)thisC(*) C(*)ruleC(*) C(*)appliesC(*) C(*)toC(*). C(*)PossibleC(*) C(*)valuesC(*)
                               C(*)areC(*) 'C(*)CC(*)(C(*)tcpC(*))', 'C(*)CC(*)(C(*)udpC(*))', C(*)andC(*) '*'."
                            - Required when C(state) is I(present).
                        choices:
                            - 'tcp'
                            - 'udp'
                            - '*'
                    source_port_range:
                        description:
                            - "C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*) C(*)betweenC(*)
                               C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                               C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                    destination_port_range:
                        description:
                            - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*)
                               C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)
                               C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                    source_address_prefix:
                        description:
                            - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*)
                               C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*)
                               C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*)
                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*). C(*)IfC(*) C(*)thisC(*) C(*)isC(*) C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*),
                               C(*)specifiesC(*) C(*)whereC(*) C(*)networkC(*) C(*)trafficC(*) C(*)originatesC(*) C(*)fromC(*). "
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
                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*)
                               C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*)
                               C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)',
                               'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)."
                    destination_address_prefixes:
                        description:
                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*)
                               C(*)rangesC(*)."
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
                               C(*)betweenC(*) C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*) C(*)mustC(*) C(*)beC(*)
                               C(*)uniqueC(*) C(*)forC(*) C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*) C(*)collectionC(*). C(*)TheC(*) C(*)lowerC(*)
                               C(*)theC(*) C(*)priorityC(*) C(*)numberC(*), C(*)theC(*) C(*)higherC(*) C(*)theC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*)
                               C(*)ruleC(*)."
                    direction:
                        description:
                            - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*) C(*)specifiesC(*) C(*)ifC(*)
                               C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*) C(*)incomingC(*) C(*)orC(*) C(*)outcomingC(*)
                               C(*)trafficC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)InboundC(*)' C(*)andC(*) 'C(*)OutboundC(*)'."
                            - Required when C(state) is I(present).
                        choices:
                            - 'inbound'
                            - 'outbound'
                    name:
                        description:
                            - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*) C(*)withinC(*)
                               C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                               C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
            resource_guid:
                description:
                    - The resource GUID property of the network security group resource.
    ip_configurations:
        description:
            - A list of IPConfigurations of the network interface.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            application_gateway_backend_address_pools:
                description:
                    - The reference of ApplicationGatewayBackendAddressPool resource.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    backend_ip_configurations:
                        description:
                            - Collection of references to IPs defined in network interfaces.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            application_gateway_backend_address_pools:
                                description:
                                    - The reference of ApplicationGatewayBackendAddressPool resource.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    backend_ip_configurations:
                                        description:
                                            - Collection of references to IPs defined in network interfaces.
                                        type: list
                                    backend_addresses:
                                        description:
                                            - Backend addresses
                                        type: list
                                    name:
                                        description:
                                            - Resource that is unique within a resource group. This name can be used to access the resource.
                                    type:
                                        description:
                                            - Type of the resource.
                            load_balancer_backend_address_pools:
                                description:
                                    - The reference of LoadBalancerBackendAddressPool resource.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    name:
                                        description:
                                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                            load_balancer_inbound_nat_rules:
                                description:
                                    - A list of references of LoadBalancerInboundNatRules.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    frontend_ip_configuration:
                                        description:
                                            - A reference to frontend IP addresses.
                                    protocol:
                                        description:
                                            - "Possible values include: 'C(udp)', 'C(tcp)', 'C(all)'"
                                        choices:
                                            - 'udp'
                                            - 'tcp'
                                            - 'all'
                                    frontend_port:
                                        description:
                                            - "The port for the external endpoint. Port numbers for each rule must be unique within the Load Balancer.
                                               Acceptable values range from 1 to 65534."
                                    backend_port:
                                        description:
                                            - The port used for the internal endpoint. Acceptable values range from 1 to 65535.
                                    idle_timeout_in_minutes:
                                        description:
                                            - "The timeout for the C(tcp) idle connection. The value can be set between 4 and 30 minutes. The default value
                                               is 4 minutes. This element is only used when the I(protocol) is set to C(tcp)."
                                    enable_floating_ip:
                                        description:
                                            - "Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn
                                               Availability Group. This setting is required when using the SQL AlwaysOn Availability Groups in SQL server.
                                               This setting can't be changed after you create the endpoint."
                                    name:
                                        description:
                                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                            private_ip_address:
                                description:
                                    - Private IP address of the IP configuration.
                            private_ip_allocation_method:
                                description:
                                    - "Defines how a private IP address is assigned. Possible values are: 'C(static)' and 'C(dynamic)'."
                                choices:
                                    - 'static'
                                    - 'dynamic'
                            private_ip_address_version:
                                description:
                                    - "Available from Api-Version 2016-03-30 onwards, it represents whether the specific ipconfiguration is C(ipv4) or
                                       C(ipv6). Default is taken as C(ipv4).  Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                                choices:
                                    - 'ipv4'
                                    - 'ipv6'
                            subnet:
                                description:
                                    - Subnet bound to the IP configuration.
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
                                    route_table:
                                        description:
                                            - The reference of the RouteTable resource.
                                    service_endpoints:
                                        description:
                                            - An array of service endpoints.
                                        type: list
                                    resource_navigation_links:
                                        description:
                                            - Gets an array of references to the external resources using subnet.
                                        type: list
                                    name:
                                        description:
                                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                            primary:
                                description:
                                    - Gets whether this is a primary customer address on the network interface.
                            public_ip_address:
                                description:
                                    - Public IP address bound to the IP configuration.
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                                    sku:
                                        description:
                                            - The public IP address SKU.
                                    public_ip_allocation_method:
                                        description:
                                            - "The public IP allocation method. Possible values are: 'C(static)' and 'C(dynamic)'."
                                        choices:
                                            - 'static'
                                            - 'dynamic'
                                    public_ip_address_version:
                                        description:
                                            - "The public IP address version. Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                                        choices:
                                            - 'ipv4'
                                            - 'ipv6'
                                    dns_settings:
                                        description:
                                            - The FQDN of the DNS record associated with the public IP address.
                                    ip_address:
                                        description:
                                            - The IP address associated with the public IP address resource.
                                    idle_timeout_in_minutes:
                                        description:
                                            - The idle timeout of the public IP address.
                                    resource_guid:
                                        description:
                                            - The resource GUID property of the public IP resource.
                                    zones:
                                        description:
                                            - A list of availability zones denoting the IP allocated for the resource needs to come from.
                                        type: list
                            application_security_groups:
                                description:
                                    - Application security groups in which the IP configuration is included.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                            name:
                                description:
                                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                    backend_addresses:
                        description:
                            - Backend addresses
                        type: list
                        suboptions:
                            fqdn:
                                description:
                                    - Fully qualified domain name (FQDN).
                            ip_address:
                                description:
                                    - IP address
                    name:
                        description:
                            - Resource that is unique within a resource group. This name can be used to access the resource.
                    type:
                        description:
                            - Type of the resource.
            load_balancer_backend_address_pools:
                description:
                    - The reference of LoadBalancerBackendAddressPool resource.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    name:
                        description:
                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
            load_balancer_inbound_nat_rules:
                description:
                    - A list of references of LoadBalancerInboundNatRules.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    frontend_ip_configuration:
                        description:
                            - A reference to frontend IP addresses.
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                    protocol:
                        description:
                            - "Possible values include: 'C(udp)', 'C(tcp)', 'C(all)'"
                        choices:
                            - 'udp'
                            - 'tcp'
                            - 'all'
                    frontend_port:
                        description:
                            - "The port for the external endpoint. Port numbers for each rule must be unique within the Load Balancer. Acceptable values
                               range from 1 to 65534."
                    backend_port:
                        description:
                            - The port used for the internal endpoint. Acceptable values range from 1 to 65535.
                    idle_timeout_in_minutes:
                        description:
                            - "The timeout for the C(tcp) idle connection. The value can be set between 4 and 30 minutes. The default value is 4 minutes.
                               This element is only used when the I(protocol) is set to C(tcp)."
                    enable_floating_ip:
                        description:
                            - "Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn Availability
                               Group. This setting is required when using the SQL AlwaysOn Availability Groups in SQL server. This setting can't be changed
                               after you create the endpoint."
                    name:
                        description:
                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
            private_ip_address:
                description:
                    - Private IP address of the IP configuration.
            private_ip_allocation_method:
                description:
                    - "Defines how a private IP address is assigned. Possible values are: 'C(static)' and 'C(dynamic)'."
                choices:
                    - 'static'
                    - 'dynamic'
            private_ip_address_version:
                description:
                    - "Available from Api-Version 2016-03-30 onwards, it represents whether the specific ipconfiguration is C(ipv4) or C(ipv6). Default is
                       taken as C(ipv4).  Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                choices:
                    - 'ipv4'
                    - 'ipv6'
            subnet:
                description:
                    - Subnet bound to the IP configuration.
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
                                            - "C(*)AC(*) C(*)descriptionC(*) C(*)forC(*) C(*)thisC(*) C(*)ruleC(*). C(*)RestrictedC(*) C(*)toC(*)
                                               C(*)140C(*) C(*)charsC(*)."
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
                                            - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*)
                                               C(*)rangeC(*) C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*)
                                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                                    source_address_prefix:
                                        description:
                                            - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*)
                                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*).
                                               C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)'
                                               C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*). C(*)IfC(*) C(*)thisC(*)
                                               C(*)isC(*) C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*), C(*)specifiesC(*) C(*)whereC(*) C(*)networkC(*)
                                               C(*)trafficC(*) C(*)originatesC(*) C(*)fromC(*). "
                                    source_address_prefixes:
                                        description:
                                            - C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangesC(*).
                                        type: list
                                    source_application_security_groups:
                                        description:
                                            - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)sourceC(*).
                                        type: list
                                    destination_address_prefix:
                                        description:
                                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                               C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                                               C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*)
                                               'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*)
                                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)."
                                    destination_address_prefixes:
                                        description:
                                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                               C(*)IPC(*) C(*)rangesC(*)."
                                        type: list
                                    destination_application_security_groups:
                                        description:
                                            - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)destinationC(*).
                                        type: list
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
                                            - "C(*)TheC(*) C(*)networkC(*) C(*)trafficC(*) C(*)isC(*) C(*)allowedC(*) C(*)orC(*) C(*)deniedC(*).
                                               C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)AllowC(*)' C(*)andC(*) 'C(*)DenyC(*)'."
                                            - Required when C(state) is I(present).
                                        choices:
                                            - 'allow'
                                            - 'deny'
                                    priority:
                                        description:
                                            - "C(*)TheC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)valueC(*) C(*)canC(*)
                                               C(*)beC(*) C(*)betweenC(*) C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*)
                                               C(*)mustC(*) C(*)beC(*) C(*)uniqueC(*) C(*)forC(*) C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*)
                                               C(*)collectionC(*). C(*)TheC(*) C(*)lowerC(*) C(*)theC(*) C(*)priorityC(*) C(*)numberC(*), C(*)theC(*)
                                               C(*)higherC(*) C(*)theC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*)."
                                    direction:
                                        description:
                                            - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*)
                                               C(*)specifiesC(*) C(*)ifC(*) C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*)
                                               C(*)incomingC(*) C(*)orC(*) C(*)outcomingC(*) C(*)trafficC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*):
                                               'C(*)InboundC(*)' C(*)andC(*) 'C(*)OutboundC(*)'."
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
                                            - "C(*)AC(*) C(*)descriptionC(*) C(*)forC(*) C(*)thisC(*) C(*)ruleC(*). C(*)RestrictedC(*) C(*)toC(*)
                                               C(*)140C(*) C(*)charsC(*)."
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
                                            - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*)
                                               C(*)rangeC(*) C(*)betweenC(*) C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*)
                                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)portsC(*)."
                                    source_address_prefix:
                                        description:
                                            - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*)
                                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*).
                                               C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)'
                                               C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*). C(*)IfC(*) C(*)thisC(*)
                                               C(*)isC(*) C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*), C(*)specifiesC(*) C(*)whereC(*) C(*)networkC(*)
                                               C(*)trafficC(*) C(*)originatesC(*) C(*)fromC(*). "
                                    source_address_prefixes:
                                        description:
                                            - C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangesC(*).
                                        type: list
                                    source_application_security_groups:
                                        description:
                                            - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)sourceC(*).
                                        type: list
                                    destination_address_prefix:
                                        description:
                                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                               C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                                               C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*)
                                               'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*)
                                               C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)."
                                    destination_address_prefixes:
                                        description:
                                            - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*)
                                               C(*)IPC(*) C(*)rangesC(*)."
                                        type: list
                                    destination_application_security_groups:
                                        description:
                                            - C(*)TheC(*) C(*)applicationC(*) C(*)securityC(*) C(*)groupC(*) C(*)specifiedC(*) C(*)asC(*) C(*)destinationC(*).
                                        type: list
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
                                            - "C(*)TheC(*) C(*)networkC(*) C(*)trafficC(*) C(*)isC(*) C(*)allowedC(*) C(*)orC(*) C(*)deniedC(*).
                                               C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)AllowC(*)' C(*)andC(*) 'C(*)DenyC(*)'."
                                            - Required when C(state) is I(present).
                                        choices:
                                            - 'allow'
                                            - 'deny'
                                    priority:
                                        description:
                                            - "C(*)TheC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)valueC(*) C(*)canC(*)
                                               C(*)beC(*) C(*)betweenC(*) C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*)
                                               C(*)mustC(*) C(*)beC(*) C(*)uniqueC(*) C(*)forC(*) C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*)
                                               C(*)collectionC(*). C(*)TheC(*) C(*)lowerC(*) C(*)theC(*) C(*)priorityC(*) C(*)numberC(*), C(*)theC(*)
                                               C(*)higherC(*) C(*)theC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*)."
                                    direction:
                                        description:
                                            - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*)
                                               C(*)specifiesC(*) C(*)ifC(*) C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*)
                                               C(*)incomingC(*) C(*)orC(*) C(*)outcomingC(*) C(*)trafficC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*):
                                               'C(*)InboundC(*)' C(*)andC(*) 'C(*)OutboundC(*)'."
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
                                            - "The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop
                                               type is C(virtual_appliance)."
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
            primary:
                description:
                    - Gets whether this is a primary customer address on the network interface.
            public_ip_address:
                description:
                    - Public IP address bound to the IP configuration.
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    location:
                        description:
                            - Resource location.
                    sku:
                        description:
                            - The public IP address SKU.
                        suboptions:
                            name:
                                description:
                                    - Name of a public IP address SKU.
                                choices:
                                    - 'basic'
                                    - 'standard'
                    public_ip_allocation_method:
                        description:
                            - "The public IP allocation method. Possible values are: 'C(static)' and 'C(dynamic)'."
                        choices:
                            - 'static'
                            - 'dynamic'
                    public_ip_address_version:
                        description:
                            - "The public IP address version. Possible values are: 'C(ipv4)' and 'C(ipv6)'."
                        choices:
                            - 'ipv4'
                            - 'ipv6'
                    dns_settings:
                        description:
                            - The FQDN of the DNS record associated with the public IP address.
                        suboptions:
                            domain_name_label:
                                description:
                                    - "Gets or sets the Domain name label.The concatenation of the domain name label and the regionalized DNS zone make up
                                       the fully qualified domain name associated with the public IP address. If a domain name label is specified, an A DNS
                                       record is created for the public IP in the Microsoft Azure DNS system."
                            fqdn:
                                description:
                                    - "Gets the FQDN, Fully qualified domain name of the A DNS record associated with the public IP. This is the
                                       concatenation of the I(domain_name_label) and the regionalized DNS zone."
                            reverse_fqdn:
                                description:
                                    - "Gets or Sets the Reverse I(fqdn). A user-visible, fully qualified domain name that resolves to this public IP
                                       address. If the reverseFqdn is specified, then a PTR DNS record is created pointing from the IP address in the
                                       in-addr.arpa domain to the reverse I(fqdn). "
                    ip_address:
                        description:
                            - The IP address associated with the public IP address resource.
                    idle_timeout_in_minutes:
                        description:
                            - The idle timeout of the public IP address.
                    resource_guid:
                        description:
                            - The resource GUID property of the public IP resource.
                    zones:
                        description:
                            - A list of availability zones denoting the IP allocated for the resource needs to come from.
                        type: list
            application_security_groups:
                description:
                    - Application security groups in which the IP configuration is included.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    location:
                        description:
                            - Resource location.
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    dns_settings:
        description:
            - The DNS settings in network interface.
        suboptions:
            dns_servers:
                description:
                    - "List of DNS servers IP addresses. Use 'AzureProvidedDNS' to switch to azure provided DNS resolution. 'AzureProvidedDNS' value cannot
                       be combined with other IPs, it must be the only value in dnsServers collection."
                type: list
            applied_dns_servers:
                description:
                    - "If the VM that uses this NIC is part of an Availability Set, then this list will have the union of all DNS servers from all NICs that
                       are part of the Availability Set. This property is what is configured on each of those VMs."
                type: list
            internal_dns_name_label:
                description:
                    - Relative DNS name for this NIC used for internal communications between VMs in the same virtual network.
            internal_fqdn:
                description:
                    - Fully qualified DNS name supporting internal communications between VMs in the same virtual network.
            internal_domain_name_suffix:
                description:
                    - "Even if I(internal_dns_name_label) is not specified, a DNS entry is created for the primary NIC of the VM. This DNS name can be
                       constructed by concatenating the VM name with the value of internalDomainNameSuffix."
    mac_address:
        description:
            - The MAC address of the network interface.
    primary:
        description:
            - Gets whether this is a primary network interface on a virtual machine.
    enable_accelerated_networking:
        description:
            - If the network interface is accelerated networking enabled.
    enable_ip_forwarding:
        description:
            - Indicates whether IP forwarding is enabled on this network interface.
    resource_guid:
        description:
            - The resource GUID property of the network interface resource.
    state:
      description:
        - Assert the state of the Network Interface.
        - Use 'present' to create or update an Network Interface and 'absent' to delete it.
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
  - name: Create (or update) Network Interface
    azure_rm_networkinterface:
      resource_group: rg1
      name: test-nic
      location: eastus
      ip_configurations:
        - subnet:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/virtualNetworks/rg1-vnet/subnets/default
          public_ip_address:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/publicIPAddresses/test-ip
          name: ipconfig1
      enable_accelerated_networking: True
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/networkInterfaces/test-nic
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


class AzureRMNetworkInterface(AzureRMModuleBase):
    """Configuration class for an Azure RM Network Interface resource"""

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
            virtual_machine=dict(
                type='dict'
            ),
            network_security_group=dict(
                type='dict'
            ),
            ip_configurations=dict(
                type='list'
            ),
            dns_settings=dict(
                type='dict'
            ),
            mac_address=dict(
                type='str'
            ),
            primary=dict(
                type='str'
            ),
            enable_accelerated_networking=dict(
                type='str'
            ),
            enable_ip_forwarding=dict(
                type='str'
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

        super(AzureRMNetworkInterface, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['network_security_group', 'security_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['network_security_group', 'security_rules', 'access'], True)
        dict_camelize(self.parameters, ['network_security_group', 'security_rules', 'direction'], True)
        dict_camelize(self.parameters, ['network_security_group', 'default_security_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['network_security_group', 'default_security_rules', 'access'], True)
        dict_camelize(self.parameters, ['network_security_group', 'default_security_rules', 'direction'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'load_balancer_inbound_nat_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'private_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'private_ip_address_version'], True)
        dict_map(self.parameters, ['ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'private_ip_address_version'], ''ipv4': 'IPv4', 'ipv6': 'IPv6'')
        dict_camelize(self.parameters, ['ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'public_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'public_ip_address_version'], True)
        dict_map(self.parameters, ['ip_configurations', 'application_gateway_backend_address_pools', 'backend_ip_configurations', 'public_ip_address', 'public_ip_address_version'], ''ipv4': 'IPv4', 'ipv6': 'IPv6'')
        dict_camelize(self.parameters, ['ip_configurations', 'load_balancer_inbound_nat_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'private_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'private_ip_address_version'], True)
        dict_map(self.parameters, ['ip_configurations', 'private_ip_address_version'], ''ipv4': 'IPv4', 'ipv6': 'IPv6'')
        dict_camelize(self.parameters, ['ip_configurations', 'subnet', 'network_security_group', 'security_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'subnet', 'network_security_group', 'security_rules', 'access'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'subnet', 'network_security_group', 'security_rules', 'direction'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'subnet', 'network_security_group', 'default_security_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'subnet', 'network_security_group', 'default_security_rules', 'access'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'subnet', 'network_security_group', 'default_security_rules', 'direction'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'subnet', 'route_table', 'routes', 'next_hop_type'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'public_ip_address', 'sku', 'name'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'public_ip_address', 'public_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['ip_configurations', 'public_ip_address', 'public_ip_address_version'], True)
        dict_map(self.parameters, ['ip_configurations', 'public_ip_address', 'public_ip_address_version'], ''ipv4': 'IPv4', 'ipv6': 'IPv6'')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_networkinterface()

        if not old_response:
            self.log("Network Interface instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Network Interface instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Network Interface instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_networkinterface()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Network Interface instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_networkinterface()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_networkinterface():
                time.sleep(20)
        else:
            self.log("Network Interface instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_networkinterface(self):
        '''
        Creates or updates Network Interface with the specified configuration.

        :return: deserialized Network Interface instance state dictionary
        '''
        self.log("Creating / Updating the Network Interface instance {0}".format(self.name))

        try:
            response = self.mgmt_client.network_interfaces.create_or_update(resource_group_name=self.resource_group,
                                                                            network_interface_name=self.name,
                                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Network Interface instance.')
            self.fail("Error creating the Network Interface instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_networkinterface(self):
        '''
        Deletes specified Network Interface instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Network Interface instance {0}".format(self.name))
        try:
            response = self.mgmt_client.network_interfaces.delete(resource_group_name=self.resource_group,
                                                                  network_interface_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Network Interface instance.')
            self.fail("Error deleting the Network Interface instance: {0}".format(str(e)))

        return True

    def get_networkinterface(self):
        '''
        Gets the properties of the specified Network Interface.

        :return: deserialized Network Interface instance state dictionary
        '''
        self.log("Checking if the Network Interface instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.network_interfaces.get(resource_group_name=self.resource_group,
                                                               network_interface_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Network Interface instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Network Interface instance.')
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
    AzureRMNetworkInterface()


if __name__ == '__main__':
    main()

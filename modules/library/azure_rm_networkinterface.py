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
short_description: Manage Network Interface instance.
description:
    - Create, update and delete instance of Network Interface.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    network_interface_name:
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
                        required: True
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
                        required: True
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
                        required: True
                        choices:
                            - 'inbound'
                            - 'outbound'
                    provisioning_state:
                        description:
                            - "C(*)TheC(*) C(*)provisioningC(*) C(*)stateC(*) C(*)ofC(*) C(*)theC(*) C(*)publicC(*) C(*)IPC(*) C(*)resourceC(*).
                               C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)UpdatingC(*)', 'C(*)DeletingC(*)', C(*)andC(*) 'C(*)FailedC(*)'."
                    name:
                        description:
                            - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*) C(*)withinC(*)
                               C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                               C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
                    etag:
                        description:
                            - "C(*)AC(*) C(*)uniqueC(*) C(*)readC(*)-C(*)onlyC(*) C(*)stringC(*) C(*)thatC(*) C(*)changesC(*) C(*)wheneverC(*) C(*)theC(*)
                               C(*)resourceC(*) C(*)isC(*) C(*)updatedC(*)."
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
                        required: True
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
                        required: True
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
                        required: True
                        choices:
                            - 'inbound'
                            - 'outbound'
                    provisioning_state:
                        description:
                            - "C(*)TheC(*) C(*)provisioningC(*) C(*)stateC(*) C(*)ofC(*) C(*)theC(*) C(*)publicC(*) C(*)IPC(*) C(*)resourceC(*).
                               C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)UpdatingC(*)', 'C(*)DeletingC(*)', C(*)andC(*) 'C(*)FailedC(*)'."
                    name:
                        description:
                            - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*) C(*)withinC(*)
                               C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*)
                               C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
                    etag:
                        description:
                            - "C(*)AC(*) C(*)uniqueC(*) C(*)readC(*)-C(*)onlyC(*) C(*)stringC(*) C(*)thatC(*) C(*)changesC(*) C(*)wheneverC(*) C(*)theC(*)
                               C(*)resourceC(*) C(*)isC(*) C(*)updatedC(*)."
            resource_guid:
                description:
                    - The resource GUID property of the network security group resource.
            provisioning_state:
                description:
                    - "The provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
            etag:
                description:
                    - A unique read-only string that changes whenever the resource is updated.
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
                                    provisioning_state:
                                        description:
                                            - "Provisioning state of the backend address pool resource. Possible values are: 'Updating', 'Deleting', and
                                               'Failed'."
                                    name:
                                        description:
                                            - Resource that is unique within a resource group. This name can be used to access the resource.
                                    etag:
                                        description:
                                            - A unique read-only string that changes whenever the resource is updated.
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
                                    provisioning_state:
                                        description:
                                            - "Get provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                                    name:
                                        description:
                                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                                    etag:
                                        description:
                                            - A unique read-only string that changes whenever the resource is updated.
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
                                    provisioning_state:
                                        description:
                                            - "Gets the provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and
                                               'Failed'."
                                    name:
                                        description:
                                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                                    etag:
                                        description:
                                            - A unique read-only string that changes whenever the resource is updated.
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
                                    provisioning_state:
                                        description:
                                            - The provisioning state of the resource.
                                    name:
                                        description:
                                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                                    etag:
                                        description:
                                            - A unique read-only string that changes whenever the resource is updated.
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
                                    provisioning_state:
                                        description:
                                            - "The provisioning state of the PublicIP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                                    etag:
                                        description:
                                            - A unique read-only string that changes whenever the resource is updated.
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
                            provisioning_state:
                                description:
                                    - "The provisioning state of the network interface IP configuration. Possible values are: 'Updating', 'Deleting', and
                                       'Failed'."
                            name:
                                description:
                                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                            etag:
                                description:
                                    - A unique read-only string that changes whenever the resource is updated.
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
                    provisioning_state:
                        description:
                            - "Provisioning state of the backend address pool resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                    name:
                        description:
                            - Resource that is unique within a resource group. This name can be used to access the resource.
                    etag:
                        description:
                            - A unique read-only string that changes whenever the resource is updated.
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
                    provisioning_state:
                        description:
                            - "Get provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                    name:
                        description:
                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                    etag:
                        description:
                            - A unique read-only string that changes whenever the resource is updated.
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
                    provisioning_state:
                        description:
                            - "Gets the provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                    name:
                        description:
                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                    etag:
                        description:
                            - A unique read-only string that changes whenever the resource is updated.
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
                                        required: True
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
                                        required: True
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
                                        required: True
                                        choices:
                                            - 'inbound'
                                            - 'outbound'
                                    provisioning_state:
                                        description:
                                            - "C(*)TheC(*) C(*)provisioningC(*) C(*)stateC(*) C(*)ofC(*) C(*)theC(*) C(*)publicC(*) C(*)IPC(*)
                                               C(*)resourceC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)UpdatingC(*)', 'C(*)DeletingC(*)',
                                               C(*)andC(*) 'C(*)FailedC(*)'."
                                    name:
                                        description:
                                            - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*)
                                               C(*)withinC(*) C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*)
                                               C(*)usedC(*) C(*)toC(*) C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
                                    etag:
                                        description:
                                            - "C(*)AC(*) C(*)uniqueC(*) C(*)readC(*)-C(*)onlyC(*) C(*)stringC(*) C(*)thatC(*) C(*)changesC(*)
                                               C(*)wheneverC(*) C(*)theC(*) C(*)resourceC(*) C(*)isC(*) C(*)updatedC(*)."
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
                                        required: True
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
                                        required: True
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
                                        required: True
                                        choices:
                                            - 'inbound'
                                            - 'outbound'
                                    provisioning_state:
                                        description:
                                            - "C(*)TheC(*) C(*)provisioningC(*) C(*)stateC(*) C(*)ofC(*) C(*)theC(*) C(*)publicC(*) C(*)IPC(*)
                                               C(*)resourceC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)UpdatingC(*)', 'C(*)DeletingC(*)',
                                               C(*)andC(*) 'C(*)FailedC(*)'."
                                    name:
                                        description:
                                            - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*)
                                               C(*)withinC(*) C(*)aC(*) C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*)
                                               C(*)usedC(*) C(*)toC(*) C(*)IC(*)(C(*)accessC(*)) C(*)theC(*) C(*)resourceC(*)."
                                    etag:
                                        description:
                                            - "C(*)AC(*) C(*)uniqueC(*) C(*)readC(*)-C(*)onlyC(*) C(*)stringC(*) C(*)thatC(*) C(*)changesC(*)
                                               C(*)wheneverC(*) C(*)theC(*) C(*)resourceC(*) C(*)isC(*) C(*)updatedC(*)."
                            resource_guid:
                                description:
                                    - The resource GUID property of the network security group resource.
                            provisioning_state:
                                description:
                                    - "The provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                            etag:
                                description:
                                    - A unique read-only string that changes whenever the resource is updated.
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
                                        required: True
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
                                    provisioning_state:
                                        description:
                                            - "The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                                    name:
                                        description:
                                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                                    etag:
                                        description:
                                            - A unique read-only string that changes whenever the resource is updated.
                            disable_bgp_route_propagation:
                                description:
                                    - Gets or sets whether to disable the I(routes) learned by BGP on that route table. True means disable.
                            provisioning_state:
                                description:
                                    - "The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                            etag:
                                description:
                                    - Gets a unique read-only string that changes whenever the resource is updated.
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
                            provisioning_state:
                                description:
                                    - The provisioning state of the resource.
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
                    provisioning_state:
                        description:
                            - The provisioning state of the resource.
                    name:
                        description:
                            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
                    etag:
                        description:
                            - A unique read-only string that changes whenever the resource is updated.
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
                    provisioning_state:
                        description:
                            - "The provisioning state of the PublicIP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
                    etag:
                        description:
                            - A unique read-only string that changes whenever the resource is updated.
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
            provisioning_state:
                description:
                    - "The provisioning state of the network interface IP configuration. Possible values are: 'Updating', 'Deleting', and 'Failed'."
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            etag:
                description:
                    - A unique read-only string that changes whenever the resource is updated.
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
    provisioning_state:
        description:
            - "The provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
    etag:
        description:
            - A unique read-only string that changes whenever the resource is updated.
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
      network_interface_name: test-nic
      location: eastus
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


class AzureRMNetworkInterfaces(AzureRMModuleBase):
    """Configuration class for an Azure RM Network Interface resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            network_interface_name=dict(
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
            provisioning_state=dict(
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
        self.network_interface_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMNetworkInterfaces, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "virtual_machine":
                    self.parameters["virtual_machine"] = kwargs[key]
                elif key == "network_security_group":
                    self.parameters["network_security_group"] = kwargs[key]
                elif key == "ip_configurations":
                    ev = kwargs[key]
                    if 'private_ip_allocation_method' in ev:
                        if ev['private_ip_allocation_method'] == 'static':
                            ev['private_ip_allocation_method'] = 'Static'
                        elif ev['private_ip_allocation_method'] == 'dynamic':
                            ev['private_ip_allocation_method'] = 'Dynamic'
                    if 'private_ip_address_version' in ev:
                        if ev['private_ip_address_version'] == 'ipv4':
                            ev['private_ip_address_version'] = 'IPv4'
                        elif ev['private_ip_address_version'] == 'ipv6':
                            ev['private_ip_address_version'] = 'IPv6'
                    self.parameters["ip_configurations"] = ev
                elif key == "dns_settings":
                    self.parameters["dns_settings"] = kwargs[key]
                elif key == "mac_address":
                    self.parameters["mac_address"] = kwargs[key]
                elif key == "primary":
                    self.parameters["primary"] = kwargs[key]
                elif key == "enable_accelerated_networking":
                    self.parameters["enable_accelerated_networking"] = kwargs[key]
                elif key == "enable_ip_forwarding":
                    self.parameters["enable_ip_forwarding"] = kwargs[key]
                elif key == "resource_guid":
                    self.parameters["resource_guid"] = kwargs[key]
                elif key == "provisioning_state":
                    self.parameters["provisioning_state"] = kwargs[key]
                elif key == "etag":
                    self.parameters["etag"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Network Interface instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Network Interface instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_networkinterface()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_networkinterface(self):
        '''
        Creates or updates Network Interface with the specified configuration.

        :return: deserialized Network Interface instance state dictionary
        '''
        self.log("Creating / Updating the Network Interface instance {0}".format(self.network_interface_name))

        try:
            response = self.mgmt_client.network_interfaces.create_or_update(resource_group_name=self.resource_group,
                                                                            network_interface_name=self.network_interface_name,
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
        self.log("Deleting the Network Interface instance {0}".format(self.network_interface_name))
        try:
            response = self.mgmt_client.network_interfaces.delete(resource_group_name=self.resource_group,
                                                                  network_interface_name=self.network_interface_name)
        except CloudError as e:
            self.log('Error attempting to delete the Network Interface instance.')
            self.fail("Error deleting the Network Interface instance: {0}".format(str(e)))

        return True

    def get_networkinterface(self):
        '''
        Gets the properties of the specified Network Interface.

        :return: deserialized Network Interface instance state dictionary
        '''
        self.log("Checking if the Network Interface instance {0} is present".format(self.network_interface_name))
        found = False
        try:
            response = self.mgmt_client.network_interfaces.get(resource_group_name=self.resource_group,
                                                               network_interface_name=self.network_interface_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Network Interface instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Network Interface instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMNetworkInterfaces()


if __name__ == '__main__':
    main()

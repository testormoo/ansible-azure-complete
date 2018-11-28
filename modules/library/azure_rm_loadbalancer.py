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
module: azure_rm_loadbalancer
version_added: "2.8"
short_description: Manage Azure Load Balancer instance.
description:
    - Create, update and delete instance of Azure Load Balancer.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the load balancer.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The load balancer SKU.
        suboptions:
            name:
                description:
                    - Name of a load balancer SKU.
                choices:
                    - 'basic'
                    - 'standard'
    frontend_ip_configurations:
        description:
            - Object representing the frontend IPs to be used for the load balancer
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            private_ip_address:
                description:
                    - The private IP address of the IP configuration.
            private_ip_allocation_method:
                description:
                    - "The Private IP allocation method. Possible values are: 'C(static)' and 'C(dynamic)'."
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
            public_ip_address:
                description:
                    - The reference of the Public IP resource.
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
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            zones:
                description:
                    - A list of availability zones denoting the IP allocated for the resource needs to come from.
                type: list
    backend_address_pools:
        description:
            - Collection of backend address pools used by a load balancer
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            name:
                description:
                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    load_balancing_rules:
        description:
            - Object collection representing the load balancing rules Gets the provisioning
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
            backend_address_pool:
                description:
                    - A reference to a pool of DIPs. Inbound traffic is randomly load balanced across IPs in the backend IPs.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            probe:
                description:
                    - The reference of the load balancer probe used by the load balancing rule.
                suboptions:
                    id:
                        description:
                            - Resource ID.
            protocol:
                description:
                    - "Possible values include: 'C(udp)', 'C(tcp)', 'C(all)'"
                    - Required when C(state) is I(present).
                choices:
                    - 'udp'
                    - 'tcp'
                    - 'all'
            load_distribution:
                description:
                    - "The load distribution policy for this rule. Possible values are 'C(default)', 'C(source_ip)', and 'C(source_ip_protocol)'."
                choices:
                    - 'default'
                    - 'source_ip'
                    - 'source_ip_protocol'
            frontend_port:
                description:
                    - "The port for the external endpoint. Port numbers for each rule must be unique within the Load Balancer. Acceptable values are between
                       0 and 65534. Note that value 0 enables 'Any Port'"
                    - Required when C(state) is I(present).
            backend_port:
                description:
                    - "The port used for internal connections on the endpoint. Acceptable values are between 0 and 65535. Note that value 0 enables 'Any
                       Port'"
            idle_timeout_in_minutes:
                description:
                    - "The timeout for the C(tcp) idle connection. The value can be set between 4 and 30 minutes. The C(default) value is 4 minutes. This
                       element is only used when the I(protocol) is set to C(tcp)."
            enable_floating_ip:
                description:
                    - "Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn Availability Group. This
                       setting is required when using the SQL AlwaysOn Availability Groups in SQL server. This setting can't be changed after you create
                       the endpoint."
            disable_outbound_snat:
                description:
                    - Configures SNAT for the VMs in the backend pool to use the publicIP address specified in the frontend of the load balancing rule.
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    probes:
        description:
            - Collection of probe objects used in the load balancer
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            protocol:
                description:
                    - "The protocol of the end point. Possible values are: 'C(http)' or 'C(tcp)'. If 'C(tcp)' is specified, a received ACK is required for
                       the probe to be successful. If 'C(http)' is specified, a 200 OK response from the specifies URI is required for the probe to be
                       successful."
                    - Required when C(state) is I(present).
                choices:
                    - 'http'
                    - 'tcp'
            port:
                description:
                    - The port for communicating the probe. Possible values range from 1 to 65535, inclusive.
                    - Required when C(state) is I(present).
            interval_in_seconds:
                description:
                    - "The interval, in seconds, for how frequently to probe the endpoint for health status. Typically, the interval is slightly less than
                       half the allocated timeout period (in seconds) which allows two full probes before taking the instance out of rotation. The default
                       value is 15, the minimum value is 5."
            number_of_probes:
                description:
                    - "The number of probes where if no response, will result in stopping further traffic from being delivered to the endpoint. This values
                       allows endpoints to be taken out of rotation faster or slower than the typical times used in Azure."
            request_path:
                description:
                    - "The URI used for requesting health status from the VM. Path is required if a I(protocol) is set to C(http). Otherwise, it is not
                       allowed. There is no default value."
            name:
                description:
                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    inbound_nat_rules:
        description:
            - "Collection of inbound NAT Rules used by a load balancer. Defining inbound NAT rules on your load balancer is mutually exclusive with defining
               an inbound NAT pool. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual
               machines cannot reference an Inbound NAT pool. They have to reference individual inbound NAT rules."
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
                    - "The port for the external endpoint. Port numbers for each rule must be unique within the Load Balancer. Acceptable values range from
                       1 to 65534."
            backend_port:
                description:
                    - The port used for the internal endpoint. Acceptable values range from 1 to 65535.
            idle_timeout_in_minutes:
                description:
                    - "The timeout for the C(tcp) idle connection. The value can be set between 4 and 30 minutes. The default value is 4 minutes. This
                       element is only used when the I(protocol) is set to C(tcp)."
            enable_floating_ip:
                description:
                    - "Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn Availability Group. This
                       setting is required when using the SQL AlwaysOn Availability Groups in SQL server. This setting can't be changed after you create
                       the endpoint."
            name:
                description:
                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    inbound_nat_pools:
        description:
            - "Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer. Inbound NAT rules are
               created automatically for each NIC associated with the Load Balancer using an external port from this range. Defining an Inbound NAT pool on
               your Load Balancer is mutually exclusive with defining inbound Nat rules. Inbound NAT pools are referenced from virtual machine scale sets.
               NICs that are associated with individual virtual machines cannot reference an inbound NAT pool. They have to reference individual inbound
               NAT rules."
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
                    - Required when C(state) is I(present).
                choices:
                    - 'udp'
                    - 'tcp'
                    - 'all'
            frontend_port_range_start:
                description:
                    - "The first port number in the range of external ports that will be used to provide Inbound Nat to NICs associated with a load
                       balancer. Acceptable values range between 1 and 65534."
                    - Required when C(state) is I(present).
            frontend_port_range_end:
                description:
                    - "The last port number in the range of external ports that will be used to provide Inbound Nat to NICs associated with a load balancer.
                       Acceptable values range between 1 and 65535."
                    - Required when C(state) is I(present).
            backend_port:
                description:
                    - The port used for internal connections on the endpoint. Acceptable values are between 1 and 65535.
                    - Required when C(state) is I(present).
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    outbound_nat_rules:
        description:
            - The outbound NAT rules.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            allocated_outbound_ports:
                description:
                    - The number of outbound ports to be used for NAT.
            frontend_ip_configurations:
                description:
                    - The Frontend IP addresses of the load balancer.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
            backend_address_pool:
                description:
                    - A reference to a pool of DIPs. Outbound traffic is randomly load balanced across IPs in the backend IPs.
                    - Required when C(state) is I(present).
                suboptions:
                    id:
                        description:
                            - Resource ID.
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    resource_guid:
        description:
            - The resource GUID property of the load balancer resource.
    state:
      description:
        - Assert the state of the Load Balancer.
        - Use 'present' to create or update an Load Balancer and 'absent' to delete it.
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
  - name: Create (or update) Load Balancer
    azure_rm_loadbalancer:
      resource_group: rg1
      name: lb
      location: eastus
      frontend_ip_configurations:
        - subnet:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/virtualNetworks/vnetlb/subnets/subnetlb
          name: fe-lb
      backend_address_pools:
        - name: be-lb
      load_balancing_rules:
        - frontend_ip_configuration:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/loadBalancers/lb/frontendIPConfigurations/fe-lb
          backend_address_pool:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/loadBalancers/lb/backendAddressPools/be-lb
          probe:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/loadBalancers/lb/probes/probe-lb
          protocol: Tcp
          load_distribution: Default
          frontend_port: 80
          backend_port: 80
          idle_timeout_in_minutes: 15
          enable_floating_ip: True
          name: rulelb
      probes:
        - protocol: Http
          port: 80
          interval_in_seconds: 15
          number_of_probes: 2
          request_path: healthcheck.aspx
          name: probe-lb
      inbound_nat_rules:
        - frontend_ip_configuration:
            id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/loadBalancers/lb/frontendIPConfigurations/fe-lb
          protocol: Tcp
          frontend_port: 3389
          backend_port: 3389
          idle_timeout_in_minutes: 15
          enable_floating_ip: True
          name: in-nat-rule
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/loadBalancers/lb
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


class AzureRMLoadBalancer(AzureRMModuleBase):
    """Configuration class for an Azure RM Load Balancer resource"""

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
            sku=dict(
                type='dict'
                options=dict(
                    name=dict(
                        type='str',
                        choices=['basic',
                                 'standard']
                    )
                )
            ),
            frontend_ip_configurations=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    private_ip_address=dict(
                        type='str'
                    ),
                    private_ip_allocation_method=dict(
                        type='str',
                        choices=['static',
                                 'dynamic']
                    ),
                    subnet=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            address_prefix=dict(
                                type='str'
                            ),
                            network_security_group=dict(
                                type='dict'
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    location=dict(
                                        type='str'
                                    ),
                                    security_rules=dict(
                                        type='list'
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
                                                type='list'
                                            ),
                                            destination_address_prefix=dict(
                                                type='str'
                                            ),
                                            destination_address_prefixes=dict(
                                                type='list'
                                            ),
                                            destination_application_security_groups=dict(
                                                type='list'
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
                                        type='list'
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
                                                type='list'
                                            ),
                                            destination_address_prefix=dict(
                                                type='str'
                                            ),
                                            destination_address_prefixes=dict(
                                                type='list'
                                            ),
                                            destination_application_security_groups=dict(
                                                type='list'
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
                                type='dict'
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    location=dict(
                                        type='str'
                                    ),
                                    routes=dict(
                                        type='list'
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
                                type='list'
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
                                type='list'
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
                    public_ip_address=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            location=dict(
                                type='str'
                            ),
                            sku=dict(
                                type='dict'
                                options=dict(
                                    name=dict(
                                        type='str',
                                        choices=['basic',
                                                 'standard']
                                    )
                                )
                            ),
                            public_ip_allocation_method=dict(
                                type='str',
                                choices=['static',
                                         'dynamic']
                            ),
                            public_ip_address_version=dict(
                                type='str',
                                choices=['ipv4',
                                         'ipv6']
                            ),
                            dns_settings=dict(
                                type='dict'
                                options=dict(
                                    domain_name_label=dict(
                                        type='str'
                                    ),
                                    fqdn=dict(
                                        type='str'
                                    ),
                                    reverse_fqdn=dict(
                                        type='str'
                                    )
                                )
                            ),
                            ip_address=dict(
                                type='str'
                            ),
                            idle_timeout_in_minutes=dict(
                                type='int'
                            ),
                            resource_guid=dict(
                                type='str'
                            ),
                            zones=dict(
                                type='list'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    ),
                    zones=dict(
                        type='list'
                    )
                )
            ),
            backend_address_pools=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            load_balancing_rules=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    frontend_ip_configuration=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    backend_address_pool=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    probe=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    protocol=dict(
                        type='str',
                        choices=['udp',
                                 'tcp',
                                 'all']
                    ),
                    load_distribution=dict(
                        type='str',
                        choices=['default',
                                 'source_ip',
                                 'source_ip_protocol']
                    ),
                    frontend_port=dict(
                        type='int'
                    ),
                    backend_port=dict(
                        type='int'
                    ),
                    idle_timeout_in_minutes=dict(
                        type='int'
                    ),
                    enable_floating_ip=dict(
                        type='str'
                    ),
                    disable_outbound_snat=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            probes=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    protocol=dict(
                        type='str',
                        choices=['http',
                                 'tcp']
                    ),
                    port=dict(
                        type='int'
                    ),
                    interval_in_seconds=dict(
                        type='int'
                    ),
                    number_of_probes=dict(
                        type='int'
                    ),
                    request_path=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            inbound_nat_rules=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    frontend_ip_configuration=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    protocol=dict(
                        type='str',
                        choices=['udp',
                                 'tcp',
                                 'all']
                    ),
                    frontend_port=dict(
                        type='int'
                    ),
                    backend_port=dict(
                        type='int'
                    ),
                    idle_timeout_in_minutes=dict(
                        type='int'
                    ),
                    enable_floating_ip=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            inbound_nat_pools=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    frontend_ip_configuration=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    protocol=dict(
                        type='str',
                        choices=['udp',
                                 'tcp',
                                 'all']
                    ),
                    frontend_port_range_start=dict(
                        type='int'
                    ),
                    frontend_port_range_end=dict(
                        type='int'
                    ),
                    backend_port=dict(
                        type='int'
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            outbound_nat_rules=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    allocated_outbound_ports=dict(
                        type='int'
                    ),
                    frontend_ip_configurations=dict(
                        type='list'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    backend_address_pool=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
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

        super(AzureRMLoadBalancer, self).__init__(derived_arg_spec=self.module_arg_spec,
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
        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'private_ip_allocation_method'], True)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'security_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'security_rules', 'access'], True)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'security_rules', 'direction'], True)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'default_security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'default_security_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'default_security_rules', 'access'], True)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'subnet', 'network_security_group', 'default_security_rules', 'direction'], True)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'route_table', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'route_table', 'routes', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'subnet', 'route_table', 'routes', 'next_hop_type'], True)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'subnet', 'resource_navigation_links', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['frontend_ip_configurations', 'public_ip_address', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'public_ip_address', 'sku', 'name'], True)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'public_ip_address', 'public_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['frontend_ip_configurations', 'public_ip_address', 'public_ip_address_version'], True)
        dict_map(self.parameters, ['frontend_ip_configurations', 'public_ip_address', 'public_ip_address_version'], {'ipv4': 'IPv4', 'ipv6': 'IPv6'})
        dict_resource_id(self.parameters, ['backend_address_pools', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['load_balancing_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['load_balancing_rules', 'frontend_ip_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['load_balancing_rules', 'backend_address_pool', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['load_balancing_rules', 'probe', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['load_balancing_rules', 'protocol'], True)
        dict_camelize(self.parameters, ['load_balancing_rules', 'load_distribution'], True)
        dict_map(self.parameters, ['load_balancing_rules', 'load_distribution'], {'source_ip': 'SourceIP', 'source_ip_protocol': 'SourceIPProtocol'})
        dict_resource_id(self.parameters, ['probes', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['probes', 'protocol'], True)
        dict_resource_id(self.parameters, ['inbound_nat_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['inbound_nat_rules', 'frontend_ip_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['inbound_nat_rules', 'protocol'], True)
        dict_resource_id(self.parameters, ['inbound_nat_pools', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['inbound_nat_pools', 'frontend_ip_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['inbound_nat_pools', 'protocol'], True)
        dict_resource_id(self.parameters, ['outbound_nat_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['outbound_nat_rules', 'frontend_ip_configurations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['outbound_nat_rules', 'backend_address_pool', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_loadbalancer()

        if not old_response:
            self.log("Load Balancer instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Load Balancer instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Load Balancer instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_loadbalancer()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Load Balancer instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_loadbalancer()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Load Balancer instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_loadbalancer(self):
        '''
        Creates or updates Load Balancer with the specified configuration.

        :return: deserialized Load Balancer instance state dictionary
        '''
        self.log("Creating / Updating the Load Balancer instance {0}".format(self.name))

        try:
            response = self.mgmt_client.load_balancers.create_or_update(resource_group_name=self.resource_group,
                                                                        load_balancer_name=self.name,
                                                                        parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Load Balancer instance.')
            self.fail("Error creating the Load Balancer instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_loadbalancer(self):
        '''
        Deletes specified Load Balancer instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Load Balancer instance {0}".format(self.name))
        try:
            response = self.mgmt_client.load_balancers.delete(resource_group_name=self.resource_group,
                                                              load_balancer_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Load Balancer instance.')
            self.fail("Error deleting the Load Balancer instance: {0}".format(str(e)))

        return True

    def get_loadbalancer(self):
        '''
        Gets the properties of the specified Load Balancer.

        :return: deserialized Load Balancer instance state dictionary
        '''
        self.log("Checking if the Load Balancer instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.load_balancers.get(resource_group_name=self.resource_group,
                                                           load_balancer_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Load Balancer instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Load Balancer instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMLoadBalancer()


if __name__ == '__main__':
    main()

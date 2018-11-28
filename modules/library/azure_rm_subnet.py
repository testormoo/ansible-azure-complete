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
module: azure_rm_subnet
version_added: "2.8"
short_description: Manage Azure Subnet instance.
description:
    - Create, update and delete instance of Azure Subnet.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    virtual_network_name:
        description:
            - The name of the virtual network.
        required: True
    name:
        description:
            - The name of the subnet.
        required: True
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
                            - "The type of Azure hop the packet should be sent to. Possible values are: 'C(virtual_network_gateway)', 'C(vnet_local)',
                               'C(internet)', 'C(virtual_appliance)', and 'C(none)'."
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
    state:
      description:
        - Assert the state of the Subnet.
        - Use 'present' to create or update an Subnet and 'absent' to delete it.
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
  - name: Create (or update) Subnet
    azure_rm_subnet:
      resource_group: subnet-test
      virtual_network_name: vnetname
      name: subnet1
      address_prefix: 10.0.0.0/16
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/subnet-test/providers/Microsoft.Network/virtualNetworks/vnetname/subnets/subnet1
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


class AzureRMSubnet(AzureRMModuleBase):
    """Configuration class for an Azure RM Subnet resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            virtual_network_name=dict(
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
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.virtual_network_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSubnet, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.subnet_parameters[key] = kwargs[key]

        dict_resource_id(self.subnet_parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.subnet_parameters, ['network_security_group', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.subnet_parameters, ['network_security_group', 'security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.subnet_parameters, ['network_security_group', 'security_rules', 'protocol'], True)
        dict_resource_id(self.subnet_parameters, ['network_security_group', 'security_rules', 'source_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.subnet_parameters, ['network_security_group', 'security_rules', 'destination_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.subnet_parameters, ['network_security_group', 'security_rules', 'access'], True)
        dict_camelize(self.subnet_parameters, ['network_security_group', 'security_rules', 'direction'], True)
        dict_resource_id(self.subnet_parameters, ['network_security_group', 'default_security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.subnet_parameters, ['network_security_group', 'default_security_rules', 'protocol'], True)
        dict_resource_id(self.subnet_parameters, ['network_security_group', 'default_security_rules', 'source_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.subnet_parameters, ['network_security_group', 'default_security_rules', 'destination_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.subnet_parameters, ['network_security_group', 'default_security_rules', 'access'], True)
        dict_camelize(self.subnet_parameters, ['network_security_group', 'default_security_rules', 'direction'], True)
        dict_resource_id(self.subnet_parameters, ['route_table', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.subnet_parameters, ['route_table', 'routes', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.subnet_parameters, ['route_table', 'routes', 'next_hop_type'], True)
        dict_resource_id(self.subnet_parameters, ['resource_navigation_links', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_subnet()

        if not old_response:
            self.log("Subnet instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Subnet instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.subnet_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Subnet instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_subnet()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Subnet instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_subnet()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Subnet instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_subnet(self):
        '''
        Creates or updates Subnet with the specified configuration.

        :return: deserialized Subnet instance state dictionary
        '''
        self.log("Creating / Updating the Subnet instance {0}".format(self.name))

        try:
            response = self.mgmt_client.subnets.create_or_update(resource_group_name=self.resource_group,
                                                                 virtual_network_name=self.virtual_network_name,
                                                                 subnet_name=self.name,
                                                                 subnet_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Subnet instance.')
            self.fail("Error creating the Subnet instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_subnet(self):
        '''
        Deletes specified Subnet instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Subnet instance {0}".format(self.name))
        try:
            response = self.mgmt_client.subnets.delete(resource_group_name=self.resource_group,
                                                       virtual_network_name=self.virtual_network_name,
                                                       subnet_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Subnet instance.')
            self.fail("Error deleting the Subnet instance: {0}".format(str(e)))

        return True

    def get_subnet(self):
        '''
        Gets the properties of the specified Subnet.

        :return: deserialized Subnet instance state dictionary
        '''
        self.log("Checking if the Subnet instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.subnets.get(resource_group_name=self.resource_group,
                                                    virtual_network_name=self.virtual_network_name,
                                                    subnet_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Subnet instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Subnet instance.')
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
    AzureRMSubnet()


if __name__ == '__main__':
    main()

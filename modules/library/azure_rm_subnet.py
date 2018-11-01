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
short_description: Manage Subnet instance.
description:
    - Create, update and delete instance of Subnet.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    virtual_network_name:
        description:
            - The name of the virtual network.
        required: True
    subnet_name:
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
                        required: True
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
      subnet_name: subnet1
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


class AzureRMSubnets(AzureRMModuleBase):
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
            subnet_name=dict(
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
                type='dict'
            ),
            route_table=dict(
                type='dict'
            ),
            service_endpoints=dict(
                type='list'
            ),
            resource_navigation_links=dict(
                type='list'
            ),
            provisioning_state=dict(
                type='str'
            ),
            name=dict(
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
        self.virtual_network_name = None
        self.subnet_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSubnets, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "address_prefix":
                    self.parameters["address_prefix"] = kwargs[key]
                elif key == "network_security_group":
                    self.parameters["network_security_group"] = kwargs[key]
                elif key == "route_table":
                    self.parameters["route_table"] = kwargs[key]
                elif key == "service_endpoints":
                    self.parameters["service_endpoints"] = kwargs[key]
                elif key == "resource_navigation_links":
                    self.parameters["resource_navigation_links"] = kwargs[key]
                elif key == "provisioning_state":
                    self.parameters["provisioning_state"] = kwargs[key]
                elif key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "etag":
                    self.parameters["etag"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Subnet instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Subnet instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_subnet()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Subnet instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_subnet()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_subnet():
                time.sleep(20)
        else:
            self.log("Subnet instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_subnet(self):
        '''
        Creates or updates Subnet with the specified configuration.

        :return: deserialized Subnet instance state dictionary
        '''
        self.log("Creating / Updating the Subnet instance {0}".format(self.subnet_name))

        try:
            response = self.mgmt_client.subnets.create_or_update(resource_group_name=self.resource_group,
                                                                 virtual_network_name=self.virtual_network_name,
                                                                 subnet_name=self.subnet_name,
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
        self.log("Deleting the Subnet instance {0}".format(self.subnet_name))
        try:
            response = self.mgmt_client.subnets.delete(resource_group_name=self.resource_group,
                                                       virtual_network_name=self.virtual_network_name,
                                                       subnet_name=self.subnet_name)
        except CloudError as e:
            self.log('Error attempting to delete the Subnet instance.')
            self.fail("Error deleting the Subnet instance: {0}".format(str(e)))

        return True

    def get_subnet(self):
        '''
        Gets the properties of the specified Subnet.

        :return: deserialized Subnet instance state dictionary
        '''
        self.log("Checking if the Subnet instance {0} is present".format(self.subnet_name))
        found = False
        try:
            response = self.mgmt_client.subnets.get(resource_group_name=self.resource_group,
                                                    virtual_network_name=self.virtual_network_name,
                                                    subnet_name=self.subnet_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Subnet instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Subnet instance.')
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
    AzureRMSubnets()


if __name__ == '__main__':
    main()

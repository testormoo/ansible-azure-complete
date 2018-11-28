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
module: azure_rm_networksecuritygroup
version_added: "2.8"
short_description: Manage Azure Network Security Group instance.
description:
    - Create, update and delete instance of Azure Network Security Group.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the network security group.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
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
                    - "C(*)NetworkC(*) C(*)protocolC(*) C(*)thisC(*) C(*)ruleC(*) C(*)appliesC(*) C(*)toC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*)
                       'C(*)CC(*)(C(*)tcpC(*))', 'C(*)CC(*)(C(*)udpC(*))', C(*)andC(*) '*'."
                    - Required when C(state) is I(present).
                choices:
                    - 'tcp'
                    - 'udp'
                    - '*'
            source_port_range:
                description:
                    - "C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*) C(*)betweenC(*) C(*)0C(*)
                       C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*)
                       C(*)portsC(*)."
            destination_port_range:
                description:
                    - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*) C(*)betweenC(*)
                       C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*)
                       C(*)allC(*) C(*)portsC(*)."
            source_address_prefix:
                description:
                    - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                       C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*)
                       'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                       C(*)usedC(*). C(*)IfC(*) C(*)thisC(*) C(*)isC(*) C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*), C(*)specifiesC(*) C(*)whereC(*)
                       C(*)networkC(*) C(*)trafficC(*) C(*)originatesC(*) C(*)fromC(*). "
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
                    - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*) C(*)rangeC(*).
                       C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*)
                       C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*)
                       'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)."
            destination_address_prefixes:
                description:
                    - C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*) C(*)rangesC(*).
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
                    - "C(*)TheC(*) C(*)networkC(*) C(*)trafficC(*) C(*)isC(*) C(*)allowedC(*) C(*)orC(*) C(*)deniedC(*). C(*)PossibleC(*) C(*)valuesC(*)
                       C(*)areC(*): 'C(*)AllowC(*)' C(*)andC(*) 'C(*)DenyC(*)'."
                    - Required when C(state) is I(present).
                choices:
                    - 'allow'
                    - 'deny'
            priority:
                description:
                    - "C(*)TheC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)valueC(*) C(*)canC(*) C(*)beC(*) C(*)betweenC(*)
                       C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*) C(*)mustC(*) C(*)beC(*) C(*)uniqueC(*) C(*)forC(*)
                       C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*) C(*)collectionC(*). C(*)TheC(*) C(*)lowerC(*) C(*)theC(*) C(*)priorityC(*)
                       C(*)numberC(*), C(*)theC(*) C(*)higherC(*) C(*)theC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*)."
            direction:
                description:
                    - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*) C(*)specifiesC(*) C(*)ifC(*)
                       C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*) C(*)incomingC(*) C(*)orC(*) C(*)outcomingC(*) C(*)trafficC(*).
                       C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)InboundC(*)' C(*)andC(*) 'C(*)OutboundC(*)'."
                    - Required when C(state) is I(present).
                choices:
                    - 'inbound'
                    - 'outbound'
            name:
                description:
                    - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*) C(*)withinC(*) C(*)aC(*)
                       C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)IC(*)(C(*)accessC(*))
                       C(*)theC(*) C(*)resourceC(*)."
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
                    - "C(*)NetworkC(*) C(*)protocolC(*) C(*)thisC(*) C(*)ruleC(*) C(*)appliesC(*) C(*)toC(*). C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*)
                       'C(*)CC(*)(C(*)tcpC(*))', 'C(*)CC(*)(C(*)udpC(*))', C(*)andC(*) '*'."
                    - Required when C(state) is I(present).
                choices:
                    - 'tcp'
                    - 'udp'
                    - '*'
            source_port_range:
                description:
                    - "C(*)TheC(*) C(*)sourceC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*) C(*)betweenC(*) C(*)0C(*)
                       C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*)
                       C(*)portsC(*)."
            destination_port_range:
                description:
                    - "C(*)TheC(*) C(*)destinationC(*) C(*)portC(*) C(*)orC(*) C(*)rangeC(*). C(*)IntegerC(*) C(*)orC(*) C(*)rangeC(*) C(*)betweenC(*)
                       C(*)0C(*) C(*)andC(*) C(*)65535C(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*)
                       C(*)allC(*) C(*)portsC(*)."
            source_address_prefix:
                description:
                    - "C(*)TheC(*) C(*)CIDRC(*) C(*)orC(*) C(*)sourceC(*) C(*)IPC(*) C(*)rangeC(*). C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                       C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*) C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*)
                       'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*) 'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*)
                       C(*)usedC(*). C(*)IfC(*) C(*)thisC(*) C(*)isC(*) C(*)anC(*) C(*)ingressC(*) C(*)ruleC(*), C(*)specifiesC(*) C(*)whereC(*)
                       C(*)networkC(*) C(*)trafficC(*) C(*)originatesC(*) C(*)fromC(*). "
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
                    - "C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*) C(*)rangeC(*).
                       C(*)AsterixC(*) '*' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)matchC(*) C(*)allC(*) C(*)sourceC(*)
                       C(*)IPsC(*). C(*)DefaultC(*) C(*)tagsC(*) C(*)suchC(*) C(*)asC(*) 'C(*)VirtualNetworkC(*)', 'C(*)AzureLoadBalancerC(*)' C(*)andC(*)
                       'C(*)InternetC(*)' C(*)canC(*) C(*)alsoC(*) C(*)beC(*) C(*)usedC(*)."
            destination_address_prefixes:
                description:
                    - C(*)TheC(*) C(*)destinationC(*) C(*)addressC(*) C(*)prefixesC(*). C(*)CIDRC(*) C(*)orC(*) C(*)destinationC(*) C(*)IPC(*) C(*)rangesC(*).
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
                    - "C(*)TheC(*) C(*)networkC(*) C(*)trafficC(*) C(*)isC(*) C(*)allowedC(*) C(*)orC(*) C(*)deniedC(*). C(*)PossibleC(*) C(*)valuesC(*)
                       C(*)areC(*): 'C(*)AllowC(*)' C(*)andC(*) 'C(*)DenyC(*)'."
                    - Required when C(state) is I(present).
                choices:
                    - 'allow'
                    - 'deny'
            priority:
                description:
                    - "C(*)TheC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)valueC(*) C(*)canC(*) C(*)beC(*) C(*)betweenC(*)
                       C(*)100C(*) C(*)andC(*) C(*)4096C(*). C(*)TheC(*) C(*)priorityC(*) C(*)numberC(*) C(*)mustC(*) C(*)beC(*) C(*)uniqueC(*) C(*)forC(*)
                       C(*)eachC(*) C(*)ruleC(*) C(*)inC(*) C(*)theC(*) C(*)collectionC(*). C(*)TheC(*) C(*)lowerC(*) C(*)theC(*) C(*)priorityC(*)
                       C(*)numberC(*), C(*)theC(*) C(*)higherC(*) C(*)theC(*) C(*)priorityC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*)."
            direction:
                description:
                    - "C(*)TheC(*) C(*)directionC(*) C(*)ofC(*) C(*)theC(*) C(*)ruleC(*). C(*)TheC(*) C(*)directionC(*) C(*)specifiesC(*) C(*)ifC(*)
                       C(*)ruleC(*) C(*)willC(*) C(*)beC(*) C(*)evaluatedC(*) C(*)onC(*) C(*)incomingC(*) C(*)orC(*) C(*)outcomingC(*) C(*)trafficC(*).
                       C(*)PossibleC(*) C(*)valuesC(*) C(*)areC(*): 'C(*)InboundC(*)' C(*)andC(*) 'C(*)OutboundC(*)'."
                    - Required when C(state) is I(present).
                choices:
                    - 'inbound'
                    - 'outbound'
            name:
                description:
                    - "C(*)TheC(*) C(*)nameC(*) C(*)ofC(*) C(*)theC(*) C(*)resourceC(*) C(*)thatC(*) C(*)isC(*) C(*)uniqueC(*) C(*)withinC(*) C(*)aC(*)
                       C(*)resourceC(*) C(*)groupC(*). C(*)ThisC(*) C(*)nameC(*) C(*)canC(*) C(*)beC(*) C(*)usedC(*) C(*)toC(*) C(*)IC(*)(C(*)accessC(*))
                       C(*)theC(*) C(*)resourceC(*)."
    resource_guid:
        description:
            - The resource GUID property of the network security group resource.
    state:
      description:
        - Assert the state of the Network Security Group.
        - Use 'present' to create or update an Network Security Group and 'absent' to delete it.
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
  - name: Create (or update) Network Security Group
    azure_rm_networksecuritygroup:
      resource_group: rg1
      name: testnsg
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/networkSecurityGroups/testnsg
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


class AzureRMNetworkSecurityGroup(AzureRMModuleBase):
    """Configuration class for an Azure RM Network Security Group resource"""

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
                        type='list'
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
                        type='list'
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

        super(AzureRMNetworkSecurityGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
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
        dict_resource_id(self.parameters, ['security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['security_rules', 'protocol'], True)
        dict_resource_id(self.parameters, ['security_rules', 'source_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['security_rules', 'destination_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['security_rules', 'access'], True)
        dict_camelize(self.parameters, ['security_rules', 'direction'], True)
        dict_resource_id(self.parameters, ['default_security_rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['default_security_rules', 'protocol'], True)
        dict_resource_id(self.parameters, ['default_security_rules', 'source_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['default_security_rules', 'destination_application_security_groups', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['default_security_rules', 'access'], True)
        dict_camelize(self.parameters, ['default_security_rules', 'direction'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_networksecuritygroup()

        if not old_response:
            self.log("Network Security Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Network Security Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Network Security Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_networksecuritygroup()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Network Security Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_networksecuritygroup()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Network Security Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_networksecuritygroup(self):
        '''
        Creates or updates Network Security Group with the specified configuration.

        :return: deserialized Network Security Group instance state dictionary
        '''
        self.log("Creating / Updating the Network Security Group instance {0}".format(self.name))

        try:
            response = self.mgmt_client.network_security_groups.create_or_update(resource_group_name=self.resource_group,
                                                                                 network_security_group_name=self.name,
                                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Network Security Group instance.')
            self.fail("Error creating the Network Security Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_networksecuritygroup(self):
        '''
        Deletes specified Network Security Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Network Security Group instance {0}".format(self.name))
        try:
            response = self.mgmt_client.network_security_groups.delete(resource_group_name=self.resource_group,
                                                                       network_security_group_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Network Security Group instance.')
            self.fail("Error deleting the Network Security Group instance: {0}".format(str(e)))

        return True

    def get_networksecuritygroup(self):
        '''
        Gets the properties of the specified Network Security Group.

        :return: deserialized Network Security Group instance state dictionary
        '''
        self.log("Checking if the Network Security Group instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.network_security_groups.get(resource_group_name=self.resource_group,
                                                                    network_security_group_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Network Security Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Network Security Group instance.')
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
    AzureRMNetworkSecurityGroup()


if __name__ == '__main__':
    main()

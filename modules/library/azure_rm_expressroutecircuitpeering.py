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
module: azure_rm_expressroutecircuitpeering
version_added: "2.8"
short_description: Manage Express Route Circuit Peering instance.
description:
    - Create, update and delete instance of Express Route Circuit Peering.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    circuit_name:
        description:
            - The name of the express route circuit.
        required: True
    name:
        description:
            - The name of the peering.
        required: True
    id:
        description:
            - Resource ID.
    peering_type:
        description:
            - "The PeeringType. Possible values are: 'C(azure_public_peering)', 'C(azure_private_peering)', and 'C(microsoft_peering)'."
        choices:
            - 'azure_public_peering'
            - 'azure_private_peering'
            - 'microsoft_peering'
    state:
        description:
            - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
        choices:
            - 'disabled'
            - 'enabled'
    azure_asn:
        description:
            - The Azure ASN.
    peer_asn:
        description:
            - The peer ASN.
    primary_peer_address_prefix:
        description:
            - The primary address prefix.
    secondary_peer_address_prefix:
        description:
            - The secondary address prefix.
    primary_azure_port:
        description:
            - The primary port.
    secondary_azure_port:
        description:
            - The secondary port.
    shared_key:
        description:
            - The shared key.
    vlan_id:
        description:
            - The VLAN ID.
    microsoft_peering_config:
        description:
            - The Microsoft peering configuration.
        suboptions:
            advertised_public_prefixes:
                description:
                    - The reference of AdvertisedPublicPrefixes.
                type: list
            advertised_communities:
                description:
                    - The communities of bgp peering. Spepcified for microsoft peering
                type: list
            advertised_public_prefixes_state:
                description:
                    - "AdvertisedPublicPrefixState of the Peering resource. Possible values are 'C(not_configured)', 'C(configuring)', 'C(configured)', and
                       'C(validation_needed)'."
                choices:
                    - 'not_configured'
                    - 'configuring'
                    - 'configured'
                    - 'validation_needed'
            legacy_mode:
                description:
                    - The legacy mode of the peering.
            customer_asn:
                description:
                    - The CustomerASN of the peering.
            routing_registry_name:
                description:
                    - The RoutingRegistryName of the configuration.
    stats:
        description:
            - Gets peering stats.
        suboptions:
            primarybytes_in:
                description:
                    - Gets BytesIn of the peering.
            primarybytes_out:
                description:
                    - Gets BytesOut of the peering.
            secondarybytes_in:
                description:
                    - Gets BytesIn of the peering.
            secondarybytes_out:
                description:
                    - Gets BytesOut of the peering.
    gateway_manager_etag:
        description:
            - The GatewayManager Etag.
    last_modified_by:
        description:
            - Gets whether the provider or the customer last modified the peering.
    route_filter:
        description:
            - The reference of the RouteFilter resource.
        suboptions:
            id:
                description:
                    - Resource ID.
            location:
                description:
                    - Resource location.
            rules:
                description:
                    - Collection of RouteFilterRules contained within a route filter.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    access:
                        description:
                            - "The access type of the rule. Valid values are: 'C(allow)', 'C(deny)'."
                            - Required when C(state) is I(present).
                        choices:
                            - 'allow'
                            - 'deny'
                    route_filter_rule_type:
                        description:
                            - "The rule type of the rule. Valid value is: 'Community'"
                            - Required when C(state) is I(present).
                    communities:
                        description:
                            - "The collection for bgp community values to filter on. e.g. ['12076:5010','12076:5020']"
                            - Required when C(state) is I(present).
                        type: list
                    name:
                        description:
                            - The name of the resource that is unique within a resource group. This name can be used to I(access) the resource.
                    location:
                        description:
                            - Resource location.
            peerings:
                description:
                    - A collection of references to express route circuit peerings.
                type: list
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    peering_type:
                        description:
                            - "The PeeringType. Possible values are: 'C(azure_public_peering)', 'C(azure_private_peering)', and 'C(microsoft_peering)'."
                        choices:
                            - 'azure_public_peering'
                            - 'azure_private_peering'
                            - 'microsoft_peering'
                    state:
                        description:
                            - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                        choices:
                            - 'disabled'
                            - 'enabled'
                    azure_asn:
                        description:
                            - The Azure ASN.
                    peer_asn:
                        description:
                            - The peer ASN.
                    primary_peer_address_prefix:
                        description:
                            - The primary address prefix.
                    secondary_peer_address_prefix:
                        description:
                            - The secondary address prefix.
                    primary_azure_port:
                        description:
                            - The primary port.
                    secondary_azure_port:
                        description:
                            - The secondary port.
                    shared_key:
                        description:
                            - The shared key.
                    vlan_id:
                        description:
                            - The VLAN ID.
                    microsoft_peering_config:
                        description:
                            - The Microsoft peering configuration.
                        suboptions:
                            advertised_public_prefixes:
                                description:
                                    - The reference of AdvertisedPublicPrefixes.
                                type: list
                            advertised_communities:
                                description:
                                    - The communities of bgp peering. Spepcified for microsoft peering
                                type: list
                            advertised_public_prefixes_state:
                                description:
                                    - "AdvertisedPublicPrefixState of the Peering resource. Possible values are 'C(not_configured)', 'C(configuring)',
                                       'C(configured)', and 'C(validation_needed)'."
                                choices:
                                    - 'not_configured'
                                    - 'configuring'
                                    - 'configured'
                                    - 'validation_needed'
                            legacy_mode:
                                description:
                                    - The legacy mode of the peering.
                            customer_asn:
                                description:
                                    - The CustomerASN of the peering.
                            routing_registry_name:
                                description:
                                    - The RoutingRegistryName of the configuration.
                    stats:
                        description:
                            - Gets peering stats.
                        suboptions:
                            primarybytes_in:
                                description:
                                    - Gets BytesIn of the peering.
                            primarybytes_out:
                                description:
                                    - Gets BytesOut of the peering.
                            secondarybytes_in:
                                description:
                                    - Gets BytesIn of the peering.
                            secondarybytes_out:
                                description:
                                    - Gets BytesOut of the peering.
                    gateway_manager_etag:
                        description:
                            - The GatewayManager Etag.
                    last_modified_by:
                        description:
                            - Gets whether the provider or the customer last modified the peering.
                    route_filter:
                        description:
                            - The reference of the RouteFilter resource.
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            location:
                                description:
                                    - Resource location.
                            rules:
                                description:
                                    - Collection of RouteFilterRules contained within a route filter.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    access:
                                        description:
                                            - "The access type of the rule. Valid values are: 'C(allow)', 'C(deny)'."
                                            - Required when C(state) is I(present).
                                        choices:
                                            - 'allow'
                                            - 'deny'
                                    route_filter_rule_type:
                                        description:
                                            - "The rule type of the rule. Valid value is: 'Community'"
                                            - Required when C(state) is I(present).
                                    communities:
                                        description:
                                            - "The collection for bgp community values to filter on. e.g. ['12076:5010','12076:5020']"
                                            - Required when C(state) is I(present).
                                        type: list
                                    name:
                                        description:
                                            - The name of the resource that is unique within a resource group. This name can be used to I(access) the resource.
                                    location:
                                        description:
                                            - Resource location.
                            peerings:
                                description:
                                    - A collection of references to express route circuit peerings.
                                type: list
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    peering_type:
                                        description:
                                            - "The PeeringType. Possible values are: 'C(azure_public_peering)', 'C(azure_private_peering)', and
                                               'C(microsoft_peering)'."
                                        choices:
                                            - 'azure_public_peering'
                                            - 'azure_private_peering'
                                            - 'microsoft_peering'
                                    state:
                                        description:
                                            - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                                        choices:
                                            - 'disabled'
                                            - 'enabled'
                                    azure_asn:
                                        description:
                                            - The Azure ASN.
                                    peer_asn:
                                        description:
                                            - The peer ASN.
                                    primary_peer_address_prefix:
                                        description:
                                            - The primary address prefix.
                                    secondary_peer_address_prefix:
                                        description:
                                            - The secondary address prefix.
                                    primary_azure_port:
                                        description:
                                            - The primary port.
                                    secondary_azure_port:
                                        description:
                                            - The secondary port.
                                    shared_key:
                                        description:
                                            - The shared key.
                                    vlan_id:
                                        description:
                                            - The VLAN ID.
                                    microsoft_peering_config:
                                        description:
                                            - The Microsoft peering configuration.
                                    stats:
                                        description:
                                            - Gets peering stats.
                                    gateway_manager_etag:
                                        description:
                                            - The GatewayManager Etag.
                                    last_modified_by:
                                        description:
                                            - Gets whether the provider or the customer last modified the peering.
                                    route_filter:
                                        description:
                                            - The reference of the RouteFilter resource.
                                    ipv6_peering_config:
                                        description:
                                            - The IPv6 peering configuration.
                                    name:
                                        description:
                                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
                    ipv6_peering_config:
                        description:
                            - The IPv6 peering configuration.
                        suboptions:
                            primary_peer_address_prefix:
                                description:
                                    - The primary address prefix.
                            secondary_peer_address_prefix:
                                description:
                                    - The secondary address prefix.
                            microsoft_peering_config:
                                description:
                                    - The Microsoft peering configuration.
                                suboptions:
                                    advertised_public_prefixes:
                                        description:
                                            - The reference of AdvertisedPublicPrefixes.
                                        type: list
                                    advertised_communities:
                                        description:
                                            - The communities of bgp peering. Spepcified for microsoft peering
                                        type: list
                                    advertised_public_prefixes_state:
                                        description:
                                            - "AdvertisedPublicPrefixState of the Peering resource. Possible values are 'C(not_configured)',
                                               'C(configuring)', 'C(configured)', and 'C(validation_needed)'."
                                        choices:
                                            - 'not_configured'
                                            - 'configuring'
                                            - 'configured'
                                            - 'validation_needed'
                                    legacy_mode:
                                        description:
                                            - The legacy mode of the peering.
                                    customer_asn:
                                        description:
                                            - The CustomerASN of the peering.
                                    routing_registry_name:
                                        description:
                                            - The RoutingRegistryName of the configuration.
                            route_filter:
                                description:
                                    - The reference of the RouteFilter resource.
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                                    rules:
                                        description:
                                            - Collection of RouteFilterRules contained within a route filter.
                                        type: list
                                    peerings:
                                        description:
                                            - A collection of references to express route circuit peerings.
                                        type: list
                            state:
                                description:
                                    - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                                choices:
                                    - 'disabled'
                                    - 'enabled'
                    name:
                        description:
                            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    ipv6_peering_config:
        description:
            - The IPv6 peering configuration.
        suboptions:
            primary_peer_address_prefix:
                description:
                    - The primary address prefix.
            secondary_peer_address_prefix:
                description:
                    - The secondary address prefix.
            microsoft_peering_config:
                description:
                    - The Microsoft peering configuration.
                suboptions:
                    advertised_public_prefixes:
                        description:
                            - The reference of AdvertisedPublicPrefixes.
                        type: list
                    advertised_communities:
                        description:
                            - The communities of bgp peering. Spepcified for microsoft peering
                        type: list
                    advertised_public_prefixes_state:
                        description:
                            - "AdvertisedPublicPrefixState of the Peering resource. Possible values are 'C(not_configured)', 'C(configuring)',
                               'C(configured)', and 'C(validation_needed)'."
                        choices:
                            - 'not_configured'
                            - 'configuring'
                            - 'configured'
                            - 'validation_needed'
                    legacy_mode:
                        description:
                            - The legacy mode of the peering.
                    customer_asn:
                        description:
                            - The CustomerASN of the peering.
                    routing_registry_name:
                        description:
                            - The RoutingRegistryName of the configuration.
            route_filter:
                description:
                    - The reference of the RouteFilter resource.
                suboptions:
                    id:
                        description:
                            - Resource ID.
                    location:
                        description:
                            - Resource location.
                    rules:
                        description:
                            - Collection of RouteFilterRules contained within a route filter.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            access:
                                description:
                                    - "The access type of the rule. Valid values are: 'C(allow)', 'C(deny)'."
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'allow'
                                    - 'deny'
                            route_filter_rule_type:
                                description:
                                    - "The rule type of the rule. Valid value is: 'Community'"
                                    - Required when C(state) is I(present).
                            communities:
                                description:
                                    - "The collection for bgp community values to filter on. e.g. ['12076:5010','12076:5020']"
                                    - Required when C(state) is I(present).
                                type: list
                            name:
                                description:
                                    - The name of the resource that is unique within a resource group. This name can be used to I(access) the resource.
                            location:
                                description:
                                    - Resource location.
                    peerings:
                        description:
                            - A collection of references to express route circuit peerings.
                        type: list
                        suboptions:
                            id:
                                description:
                                    - Resource ID.
                            peering_type:
                                description:
                                    - "The PeeringType. Possible values are: 'C(azure_public_peering)', 'C(azure_private_peering)', and
                                       'C(microsoft_peering)'."
                                choices:
                                    - 'azure_public_peering'
                                    - 'azure_private_peering'
                                    - 'microsoft_peering'
                            state:
                                description:
                                    - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                                choices:
                                    - 'disabled'
                                    - 'enabled'
                            azure_asn:
                                description:
                                    - The Azure ASN.
                            peer_asn:
                                description:
                                    - The peer ASN.
                            primary_peer_address_prefix:
                                description:
                                    - The primary address prefix.
                            secondary_peer_address_prefix:
                                description:
                                    - The secondary address prefix.
                            primary_azure_port:
                                description:
                                    - The primary port.
                            secondary_azure_port:
                                description:
                                    - The secondary port.
                            shared_key:
                                description:
                                    - The shared key.
                            vlan_id:
                                description:
                                    - The VLAN ID.
                            microsoft_peering_config:
                                description:
                                    - The Microsoft peering configuration.
                                suboptions:
                                    advertised_public_prefixes:
                                        description:
                                            - The reference of AdvertisedPublicPrefixes.
                                        type: list
                                    advertised_communities:
                                        description:
                                            - The communities of bgp peering. Spepcified for microsoft peering
                                        type: list
                                    advertised_public_prefixes_state:
                                        description:
                                            - "AdvertisedPublicPrefixState of the Peering resource. Possible values are 'C(not_configured)',
                                               'C(configuring)', 'C(configured)', and 'C(validation_needed)'."
                                        choices:
                                            - 'not_configured'
                                            - 'configuring'
                                            - 'configured'
                                            - 'validation_needed'
                                    legacy_mode:
                                        description:
                                            - The legacy mode of the peering.
                                    customer_asn:
                                        description:
                                            - The CustomerASN of the peering.
                                    routing_registry_name:
                                        description:
                                            - The RoutingRegistryName of the configuration.
                            stats:
                                description:
                                    - Gets peering stats.
                                suboptions:
                                    primarybytes_in:
                                        description:
                                            - Gets BytesIn of the peering.
                                    primarybytes_out:
                                        description:
                                            - Gets BytesOut of the peering.
                                    secondarybytes_in:
                                        description:
                                            - Gets BytesIn of the peering.
                                    secondarybytes_out:
                                        description:
                                            - Gets BytesOut of the peering.
                            gateway_manager_etag:
                                description:
                                    - The GatewayManager Etag.
                            last_modified_by:
                                description:
                                    - Gets whether the provider or the customer last modified the peering.
                            route_filter:
                                description:
                                    - The reference of the RouteFilter resource.
                                suboptions:
                                    id:
                                        description:
                                            - Resource ID.
                                    location:
                                        description:
                                            - Resource location.
                                    rules:
                                        description:
                                            - Collection of RouteFilterRules contained within a route filter.
                                        type: list
                                    peerings:
                                        description:
                                            - A collection of references to express route circuit peerings.
                                        type: list
                            ipv6_peering_config:
                                description:
                                    - The IPv6 peering configuration.
                                suboptions:
                                    primary_peer_address_prefix:
                                        description:
                                            - The primary address prefix.
                                    secondary_peer_address_prefix:
                                        description:
                                            - The secondary address prefix.
                                    microsoft_peering_config:
                                        description:
                                            - The Microsoft peering configuration.
                                    route_filter:
                                        description:
                                            - The reference of the RouteFilter resource.
                                    state:
                                        description:
                                            - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                                        choices:
                                            - 'disabled'
                                            - 'enabled'
                            name:
                                description:
                                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
            state:
                description:
                    - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                choices:
                    - 'disabled'
                    - 'enabled'
    name:
        description:
            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    state:
      description:
        - Assert the state of the Express Route Circuit Peering.
        - Use 'present' to create or update an Express Route Circuit Peering and 'absent' to delete it.
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
  - name: Create (or update) Express Route Circuit Peering
    azure_rm_expressroutecircuitpeering:
      resource_group: NOT FOUND
      circuit_name: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: id
state:
    description:
        - "The state of peering. Possible values are: 'Disabled' and 'Enabled'. Possible values include: 'Disabled', 'Enabled'"
    returned: always
    type: str
    sample: state
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


class AzureRMExpressRouteCircuitPeerings(AzureRMModuleBase):
    """Configuration class for an Azure RM Express Route Circuit Peering resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            circuit_name=dict(
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
            peering_type=dict(
                type='str',
                choices=['azure_public_peering',
                         'azure_private_peering',
                         'microsoft_peering']
            ),
            state=dict(
                type='str',
                choices=['disabled',
                         'enabled']
            ),
            azure_asn=dict(
                type='int'
            ),
            peer_asn=dict(
                type='int'
            ),
            primary_peer_address_prefix=dict(
                type='str'
            ),
            secondary_peer_address_prefix=dict(
                type='str'
            ),
            primary_azure_port=dict(
                type='str'
            ),
            secondary_azure_port=dict(
                type='str'
            ),
            shared_key=dict(
                type='str'
            ),
            vlan_id=dict(
                type='int'
            ),
            microsoft_peering_config=dict(
                type='dict'
            ),
            stats=dict(
                type='dict'
            ),
            gateway_manager_etag=dict(
                type='str'
            ),
            last_modified_by=dict(
                type='str'
            ),
            route_filter=dict(
                type='dict'
            ),
            ipv6_peering_config=dict(
                type='dict'
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
        self.circuit_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMExpressRouteCircuitPeerings, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "peering_type":
                    self.parameters["peering_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "state":
                    self.parameters["state"] = _snake_to_camel(kwargs[key], True)
                elif key == "azure_asn":
                    self.parameters["azure_asn"] = kwargs[key]
                elif key == "peer_asn":
                    self.parameters["peer_asn"] = kwargs[key]
                elif key == "primary_peer_address_prefix":
                    self.parameters["primary_peer_address_prefix"] = kwargs[key]
                elif key == "secondary_peer_address_prefix":
                    self.parameters["secondary_peer_address_prefix"] = kwargs[key]
                elif key == "primary_azure_port":
                    self.parameters["primary_azure_port"] = kwargs[key]
                elif key == "secondary_azure_port":
                    self.parameters["secondary_azure_port"] = kwargs[key]
                elif key == "shared_key":
                    self.parameters["shared_key"] = kwargs[key]
                elif key == "vlan_id":
                    self.parameters["vlan_id"] = kwargs[key]
                elif key == "microsoft_peering_config":
                    ev = kwargs[key]
                    if 'advertised_public_prefixes_state' in ev:
                        if ev['advertised_public_prefixes_state'] == 'not_configured':
                            ev['advertised_public_prefixes_state'] = 'NotConfigured'
                        elif ev['advertised_public_prefixes_state'] == 'configuring':
                            ev['advertised_public_prefixes_state'] = 'Configuring'
                        elif ev['advertised_public_prefixes_state'] == 'configured':
                            ev['advertised_public_prefixes_state'] = 'Configured'
                        elif ev['advertised_public_prefixes_state'] == 'validation_needed':
                            ev['advertised_public_prefixes_state'] = 'ValidationNeeded'
                    self.parameters["microsoft_peering_config"] = ev
                elif key == "stats":
                    self.parameters["stats"] = kwargs[key]
                elif key == "gateway_manager_etag":
                    self.parameters["gateway_manager_etag"] = kwargs[key]
                elif key == "last_modified_by":
                    self.parameters["last_modified_by"] = kwargs[key]
                elif key == "route_filter":
                    self.parameters["route_filter"] = kwargs[key]
                elif key == "ipv6_peering_config":
                    ev = kwargs[key]
                    if 'state' in ev:
                        if ev['state'] == 'disabled':
                            ev['state'] = 'Disabled'
                        elif ev['state'] == 'enabled':
                            ev['state'] = 'Enabled'
                    self.parameters["ipv6_peering_config"] = ev
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_expressroutecircuitpeering()

        if not old_response:
            self.log("Express Route Circuit Peering instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Express Route Circuit Peering instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Express Route Circuit Peering instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_expressroutecircuitpeering()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Express Route Circuit Peering instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_expressroutecircuitpeering()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_expressroutecircuitpeering():
                time.sleep(20)
        else:
            self.log("Express Route Circuit Peering instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_expressroutecircuitpeering(self):
        '''
        Creates or updates Express Route Circuit Peering with the specified configuration.

        :return: deserialized Express Route Circuit Peering instance state dictionary
        '''
        self.log("Creating / Updating the Express Route Circuit Peering instance {0}".format(self.name))

        try:
            response = self.mgmt_client.express_route_circuit_peerings.create_or_update(resource_group_name=self.resource_group,
                                                                                        circuit_name=self.circuit_name,
                                                                                        peering_name=self.name,
                                                                                        peering_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Express Route Circuit Peering instance.')
            self.fail("Error creating the Express Route Circuit Peering instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_expressroutecircuitpeering(self):
        '''
        Deletes specified Express Route Circuit Peering instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Express Route Circuit Peering instance {0}".format(self.name))
        try:
            response = self.mgmt_client.express_route_circuit_peerings.delete(resource_group_name=self.resource_group,
                                                                              circuit_name=self.circuit_name,
                                                                              peering_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Express Route Circuit Peering instance.')
            self.fail("Error deleting the Express Route Circuit Peering instance: {0}".format(str(e)))

        return True

    def get_expressroutecircuitpeering(self):
        '''
        Gets the properties of the specified Express Route Circuit Peering.

        :return: deserialized Express Route Circuit Peering instance state dictionary
        '''
        self.log("Checking if the Express Route Circuit Peering instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.express_route_circuit_peerings.get(resource_group_name=self.resource_group,
                                                                           circuit_name=self.circuit_name,
                                                                           peering_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Express Route Circuit Peering instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Express Route Circuit Peering instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
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
    AzureRMExpressRouteCircuitPeerings()


if __name__ == '__main__':
    main()

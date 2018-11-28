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
module: azure_rm_expressroutecircuit
version_added: "2.8"
short_description: Manage Azure Express Route Circuit instance.
description:
    - Create, update and delete instance of Azure Express Route Circuit.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the circuit.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The SKU.
        suboptions:
            name:
                description:
                    - The name of the SKU.
            tier:
                description:
                    - "The tier of the SKU. Possible values are 'C(standard)' and 'C(premium)'."
                choices:
                    - 'standard'
                    - 'premium'
            family:
                description:
                    - "The family of the SKU. Possible values are: 'C(unlimited_data)' and 'C(metered_data)'."
                choices:
                    - 'unlimited_data'
                    - 'metered_data'
    allow_classic_operations:
        description:
            - Allow classic operations
    circuit_provisioning_state:
        description:
            - The CircuitProvisioningState state of the resource.
    service_provider_provisioning_state:
        description:
            - "The ServiceProviderProvisioningState state of the resource. Possible values are 'C(not_provisioned)', 'C(provisioning)', 'C(provisioned)',
               and 'C(deprovisioning)'."
        choices:
            - 'not_provisioned'
            - 'provisioning'
            - 'provisioned'
            - 'deprovisioning'
    authorizations:
        description:
            - The list of authorizations.
        type: list
        suboptions:
            id:
                description:
                    - Resource ID.
            authorization_key:
                description:
                    - The authorization key.
            authorization_use_status:
                description:
                    - "AuthorizationUseStatus. Possible values are: 'C(available)' and 'C(in_use)'."
                choices:
                    - 'available'
                    - 'in_use'
            name:
                description:
                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    peerings:
        description:
            - The list of peerings.
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
                    - "The state of peering. Possible values are: 'Disabled' and 'Enabled'. Possible values include: 'Disabled', 'Enabled'"
                type: bool
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
                                    - "The state of peering. Possible values are: 'Disabled' and 'Enabled'. Possible values include: 'Disabled', 'Enabled'"
                                type: bool
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
                                            - "The state of peering. Possible values are: 'Disabled' and 'Enabled'. Possible values include: 'Disabled',
                                               'Enabled'"
                                        type: bool
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
                                            - "The state of peering. Possible values are: 'Disabled' and 'Enabled'. Possible values include: 'Disabled',
                                               'Enabled'"
                                        type: bool
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
                    state:
                        description:
                            - "The state of peering. Possible values are: 'Disabled' and 'Enabled'. Possible values include: 'Disabled', 'Enabled'"
                        type: bool
            name:
                description:
                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    service_key:
        description:
            - The ServiceKey.
    service_provider_notes:
        description:
            - The ServiceProviderNotes.
    service_provider_properties:
        description:
            - The ServiceProviderProperties.
        suboptions:
            service_provider_name:
                description:
                    - The serviceProviderName.
            peering_location:
                description:
                    - The peering location.
            bandwidth_in_mbps:
                description:
                    - The BandwidthInMbps.
    gateway_manager_etag:
        description:
            - The GatewayManager Etag.
    state:
      description:
        - Assert the state of the Express Route Circuit.
        - Use 'present' to create or update an Express Route Circuit and 'absent' to delete it.
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
  - name: Create (or update) Express Route Circuit
    azure_rm_expressroutecircuit:
      resource_group: NOT FOUND
      name: NOT FOUND
      location: eastus
      peerings:
        - state: state
          route_filter:
            peerings:
              - state: state
                ipv6_peering_config:
                  state: state
          ipv6_peering_config:
            route_filter:
              peerings:
                - state: state
            state: state
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


class AzureRMExpressRouteCircuit(AzureRMModuleBase):
    """Configuration class for an Azure RM Express Route Circuit resource"""

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
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    tier=dict(
                        type='str',
                        choices=['standard',
                                 'premium']
                    ),
                    family=dict(
                        type='str',
                        choices=['unlimited_data',
                                 'metered_data']
                    )
                )
            ),
            allow_classic_operations=dict(
                type='str'
            ),
            circuit_provisioning_state=dict(
                type='str'
            ),
            service_provider_provisioning_state=dict(
                type='str',
                choices=['not_provisioned',
                         'provisioning',
                         'provisioned',
                         'deprovisioning']
            ),
            authorizations=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    authorization_key=dict(
                        type='str'
                    ),
                    authorization_use_status=dict(
                        type='str',
                        choices=['available',
                                 'in_use']
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            peerings=dict(
                type='list',
                options=dict(
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
                        type='bool'
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
                        type='dict',
                        options=dict(
                            advertised_public_prefixes=dict(
                                type='list'
                            ),
                            advertised_communities=dict(
                                type='list'
                            ),
                            advertised_public_prefixes_state=dict(
                                type='str',
                                choices=['not_configured',
                                         'configuring',
                                         'configured',
                                         'validation_needed']
                            ),
                            legacy_mode=dict(
                                type='int'
                            ),
                            customer_asn=dict(
                                type='int'
                            ),
                            routing_registry_name=dict(
                                type='str'
                            )
                        )
                    ),
                    stats=dict(
                        type='dict',
                        options=dict(
                            primarybytes_in=dict(
                                type='int'
                            ),
                            primarybytes_out=dict(
                                type='int'
                            ),
                            secondarybytes_in=dict(
                                type='int'
                            ),
                            secondarybytes_out=dict(
                                type='int'
                            )
                        )
                    ),
                    gateway_manager_etag=dict(
                        type='str'
                    ),
                    last_modified_by=dict(
                        type='str'
                    ),
                    route_filter=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            ),
                            location=dict(
                                type='str'
                            ),
                            rules=dict(
                                type='list',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    access=dict(
                                        type='str',
                                        choices=['allow',
                                                 'deny']
                                    ),
                                    route_filter_rule_type=dict(
                                        type='str'
                                    ),
                                    communities=dict(
                                        type='list'
                                    ),
                                    name=dict(
                                        type='str'
                                    ),
                                    location=dict(
                                        type='str'
                                    )
                                )
                            ),
                            peerings=dict(
                                type='list',
                                options=dict(
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
                                        type='bool'
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
                                        type='dict',
                                        options=dict(
                                            advertised_public_prefixes=dict(
                                                type='list'
                                            ),
                                            advertised_communities=dict(
                                                type='list'
                                            ),
                                            advertised_public_prefixes_state=dict(
                                                type='str',
                                                choices=['not_configured',
                                                         'configuring',
                                                         'configured',
                                                         'validation_needed']
                                            ),
                                            legacy_mode=dict(
                                                type='int'
                                            ),
                                            customer_asn=dict(
                                                type='int'
                                            ),
                                            routing_registry_name=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    stats=dict(
                                        type='dict',
                                        options=dict(
                                            primarybytes_in=dict(
                                                type='int'
                                            ),
                                            primarybytes_out=dict(
                                                type='int'
                                            ),
                                            secondarybytes_in=dict(
                                                type='int'
                                            ),
                                            secondarybytes_out=dict(
                                                type='int'
                                            )
                                        )
                                    ),
                                    gateway_manager_etag=dict(
                                        type='str'
                                    ),
                                    last_modified_by=dict(
                                        type='str'
                                    ),
                                    route_filter=dict(
                                        type='dict',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            ),
                                            rules=dict(
                                                type='list'
                                            ),
                                            peerings=dict(
                                                type='list'
                                            )
                                        )
                                    ),
                                    ipv6_peering_config=dict(
                                        type='dict',
                                        options=dict(
                                            primary_peer_address_prefix=dict(
                                                type='str'
                                            ),
                                            secondary_peer_address_prefix=dict(
                                                type='str'
                                            ),
                                            microsoft_peering_config=dict(
                                                type='dict'
                                            ),
                                            route_filter=dict(
                                                type='dict'
                                            ),
                                            state=dict(
                                                type='bool'
                                            )
                                        )
                                    ),
                                    name=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    ipv6_peering_config=dict(
                        type='dict',
                        options=dict(
                            primary_peer_address_prefix=dict(
                                type='str'
                            ),
                            secondary_peer_address_prefix=dict(
                                type='str'
                            ),
                            microsoft_peering_config=dict(
                                type='dict',
                                options=dict(
                                    advertised_public_prefixes=dict(
                                        type='list'
                                    ),
                                    advertised_communities=dict(
                                        type='list'
                                    ),
                                    advertised_public_prefixes_state=dict(
                                        type='str',
                                        choices=['not_configured',
                                                 'configuring',
                                                 'configured',
                                                 'validation_needed']
                                    ),
                                    legacy_mode=dict(
                                        type='int'
                                    ),
                                    customer_asn=dict(
                                        type='int'
                                    ),
                                    routing_registry_name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            route_filter=dict(
                                type='dict',
                                options=dict(
                                    id=dict(
                                        type='str'
                                    ),
                                    location=dict(
                                        type='str'
                                    ),
                                    rules=dict(
                                        type='list',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            ),
                                            access=dict(
                                                type='str',
                                                choices=['allow',
                                                         'deny']
                                            ),
                                            route_filter_rule_type=dict(
                                                type='str'
                                            ),
                                            communities=dict(
                                                type='list'
                                            ),
                                            name=dict(
                                                type='str'
                                            ),
                                            location=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    peerings=dict(
                                        type='list',
                                        options=dict(
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
                                                type='bool'
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
                                            )
                                        )
                                    )
                                )
                            ),
                            state=dict(
                                type='bool'
                            )
                        )
                    ),
                    name=dict(
                        type='str'
                    )
                )
            ),
            service_key=dict(
                type='str'
            ),
            service_provider_notes=dict(
                type='str'
            ),
            service_provider_properties=dict(
                type='dict',
                options=dict(
                    service_provider_name=dict(
                        type='str'
                    ),
                    peering_location=dict(
                        type='str'
                    ),
                    bandwidth_in_mbps=dict(
                        type='int'
                    )
                )
            ),
            gateway_manager_etag=dict(
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

        super(AzureRMExpressRouteCircuit, self).__init__(derived_arg_spec=self.module_arg_spec,
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
        dict_camelize(self.parameters, ['sku', 'tier'], True)
        dict_camelize(self.parameters, ['sku', 'family'], True)
        dict_camelize(self.parameters, ['service_provider_provisioning_state'], True)
        dict_resource_id(self.parameters, ['authorizations', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['authorizations', 'authorization_use_status'], True)
        dict_resource_id(self.parameters, ['peerings', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['peerings', 'peering_type'], True)
        dict_map(self.parameters, ['peerings', 'state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.parameters, ['peerings', 'microsoft_peering_config', 'advertised_public_prefixes_state'], True)
        dict_resource_id(self.parameters, ['peerings', 'route_filter', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['peerings', 'route_filter', 'rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['peerings', 'route_filter', 'rules', 'access'], True)
        dict_resource_id(self.parameters, ['peerings', 'route_filter', 'peerings', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['peerings', 'route_filter', 'peerings', 'peering_type'], True)
        dict_map(self.parameters, ['peerings', 'route_filter', 'peerings', 'state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.parameters, ['peerings', 'route_filter', 'peerings', 'microsoft_peering_config', 'advertised_public_prefixes_state'], True)
        dict_resource_id(self.parameters, ['peerings', 'route_filter', 'peerings', 'route_filter', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_map(self.parameters, ['peerings', 'route_filter', 'peerings', 'ipv6_peering_config', 'state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.parameters, ['peerings', 'ipv6_peering_config', 'microsoft_peering_config', 'advertised_public_prefixes_state'], True)
        dict_resource_id(self.parameters, ['peerings', 'ipv6_peering_config', 'route_filter', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['peerings', 'ipv6_peering_config', 'route_filter', 'rules', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['peerings', 'ipv6_peering_config', 'route_filter', 'rules', 'access'], True)
        dict_resource_id(self.parameters, ['peerings', 'ipv6_peering_config', 'route_filter', 'peerings', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['peerings', 'ipv6_peering_config', 'route_filter', 'peerings', 'peering_type'], True)
        dict_map(self.parameters, ['peerings', 'ipv6_peering_config', 'route_filter', 'peerings', 'state'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.parameters, ['peerings', 'ipv6_peering_config', 'state'], {True: 'Enabled', False: 'Disabled'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_expressroutecircuit()

        if not old_response:
            self.log("Express Route Circuit instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Express Route Circuit instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Express Route Circuit instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_expressroutecircuit()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Express Route Circuit instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_expressroutecircuit()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Express Route Circuit instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_expressroutecircuit(self):
        '''
        Creates or updates Express Route Circuit with the specified configuration.

        :return: deserialized Express Route Circuit instance state dictionary
        '''
        self.log("Creating / Updating the Express Route Circuit instance {0}".format(self.name))

        try:
            response = self.mgmt_client.express_route_circuits.create_or_update(resource_group_name=self.resource_group,
                                                                                circuit_name=self.name,
                                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Express Route Circuit instance.')
            self.fail("Error creating the Express Route Circuit instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_expressroutecircuit(self):
        '''
        Deletes specified Express Route Circuit instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Express Route Circuit instance {0}".format(self.name))
        try:
            response = self.mgmt_client.express_route_circuits.delete(resource_group_name=self.resource_group,
                                                                      circuit_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Express Route Circuit instance.')
            self.fail("Error deleting the Express Route Circuit instance: {0}".format(str(e)))

        return True

    def get_expressroutecircuit(self):
        '''
        Gets the properties of the specified Express Route Circuit.

        :return: deserialized Express Route Circuit instance state dictionary
        '''
        self.log("Checking if the Express Route Circuit instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.express_route_circuits.get(resource_group_name=self.resource_group,
                                                                   circuit_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Express Route Circuit instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Express Route Circuit instance.')
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
    AzureRMExpressRouteCircuit()


if __name__ == '__main__':
    main()

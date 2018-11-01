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
short_description: Manage Express Route Circuit instance.
description:
    - Create, update and delete instance of Express Route Circuit.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    circuit_name:
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
            provisioning_state:
                description:
                    - "Gets the provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
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
            provisioning_state:
                description:
                    - "Gets the provisioning I(state) of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
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
                                required: True
                                choices:
                                    - 'allow'
                                    - 'deny'
                            route_filter_rule_type:
                                description:
                                    - "The rule type of the rule. Valid value is: 'Community'"
                                required: True
                            communities:
                                description:
                                    - "The collection for bgp community values to filter on. e.g. ['12076:5010','12076:5020']"
                                required: True
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
                            provisioning_state:
                                description:
                                    - "Gets the provisioning I(state) of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
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
                                        required: True
                                        choices:
                                            - 'allow'
                                            - 'deny'
                                    route_filter_rule_type:
                                        description:
                                            - "The rule type of the rule. Valid value is: 'Community'"
                                        required: True
                                    communities:
                                        description:
                                            - "The collection for bgp community values to filter on. e.g. ['12076:5010','12076:5020']"
                                        required: True
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
                                    provisioning_state:
                                        description:
                                            - "Gets the provisioning I(state) of the public IP resource. Possible values are: 'Updating', 'Deleting', and
                                               'Failed'."
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
                            - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                        choices:
                            - 'disabled'
                            - 'enabled'
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
    provisioning_state:
        description:
            - "Gets the C(provisioning) state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'."
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
      circuit_name: NOT FOUND
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


class AzureRMExpressRouteCircuits(AzureRMModuleBase):
    """Configuration class for an Azure RM Express Route Circuit resource"""

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
            id=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
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
                type='list'
            ),
            peerings=dict(
                type='list'
            ),
            service_key=dict(
                type='str'
            ),
            service_provider_notes=dict(
                type='str'
            ),
            service_provider_properties=dict(
                type='dict'
            ),
            provisioning_state=dict(
                type='str'
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
        self.circuit_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMExpressRouteCircuits, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "sku":
                    ev = kwargs[key]
                    if 'tier' in ev:
                        if ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                        elif ev['tier'] == 'premium':
                            ev['tier'] = 'Premium'
                    if 'family' in ev:
                        if ev['family'] == 'unlimited_data':
                            ev['family'] = 'UnlimitedData'
                        elif ev['family'] == 'metered_data':
                            ev['family'] = 'MeteredData'
                    self.parameters["sku"] = ev
                elif key == "allow_classic_operations":
                    self.parameters["allow_classic_operations"] = kwargs[key]
                elif key == "circuit_provisioning_state":
                    self.parameters["circuit_provisioning_state"] = kwargs[key]
                elif key == "service_provider_provisioning_state":
                    self.parameters["service_provider_provisioning_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "authorizations":
                    ev = kwargs[key]
                    if 'authorization_use_status' in ev:
                        if ev['authorization_use_status'] == 'available':
                            ev['authorization_use_status'] = 'Available'
                        elif ev['authorization_use_status'] == 'in_use':
                            ev['authorization_use_status'] = 'InUse'
                    self.parameters["authorizations"] = ev
                elif key == "peerings":
                    ev = kwargs[key]
                    if 'peering_type' in ev:
                        if ev['peering_type'] == 'azure_public_peering':
                            ev['peering_type'] = 'AzurePublicPeering'
                        elif ev['peering_type'] == 'azure_private_peering':
                            ev['peering_type'] = 'AzurePrivatePeering'
                        elif ev['peering_type'] == 'microsoft_peering':
                            ev['peering_type'] = 'MicrosoftPeering'
                    if 'state' in ev:
                        if ev['state'] == 'disabled':
                            ev['state'] = 'Disabled'
                        elif ev['state'] == 'enabled':
                            ev['state'] = 'Enabled'
                    self.parameters["peerings"] = ev
                elif key == "service_key":
                    self.parameters["service_key"] = kwargs[key]
                elif key == "service_provider_notes":
                    self.parameters["service_provider_notes"] = kwargs[key]
                elif key == "service_provider_properties":
                    self.parameters["service_provider_properties"] = kwargs[key]
                elif key == "provisioning_state":
                    self.parameters["provisioning_state"] = kwargs[key]
                elif key == "gateway_manager_etag":
                    self.parameters["gateway_manager_etag"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Express Route Circuit instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Express Route Circuit instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_expressroutecircuit()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Express Route Circuit instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_expressroutecircuit()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_expressroutecircuit():
                time.sleep(20)
        else:
            self.log("Express Route Circuit instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_expressroutecircuit(self):
        '''
        Creates or updates Express Route Circuit with the specified configuration.

        :return: deserialized Express Route Circuit instance state dictionary
        '''
        self.log("Creating / Updating the Express Route Circuit instance {0}".format(self.circuit_name))

        try:
            response = self.mgmt_client.express_route_circuits.create_or_update(resource_group_name=self.resource_group,
                                                                                circuit_name=self.circuit_name,
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
        self.log("Deleting the Express Route Circuit instance {0}".format(self.circuit_name))
        try:
            response = self.mgmt_client.express_route_circuits.delete(resource_group_name=self.resource_group,
                                                                      circuit_name=self.circuit_name)
        except CloudError as e:
            self.log('Error attempting to delete the Express Route Circuit instance.')
            self.fail("Error deleting the Express Route Circuit instance: {0}".format(str(e)))

        return True

    def get_expressroutecircuit(self):
        '''
        Gets the properties of the specified Express Route Circuit.

        :return: deserialized Express Route Circuit instance state dictionary
        '''
        self.log("Checking if the Express Route Circuit instance {0} is present".format(self.circuit_name))
        found = False
        try:
            response = self.mgmt_client.express_route_circuits.get(resource_group_name=self.resource_group,
                                                                   circuit_name=self.circuit_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Express Route Circuit instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Express Route Circuit instance.')
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
    AzureRMExpressRouteCircuits()


if __name__ == '__main__':
    main()

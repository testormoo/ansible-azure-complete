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
module: azure_rm_routefilter
version_added: "2.8"
short_description: Manage Route Filter instance.
description:
    - Create, update and delete instance of Route Filter.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the route filter.
        required: True
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
                            - "The state of peering. Possible values are: 'C(disabled)' and 'C(enabled)'."
                        choices:
                            - 'disabled'
                            - 'enabled'
            name:
                description:
                    - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    state:
      description:
        - Assert the state of the Route Filter.
        - Use 'present' to create or update an Route Filter and 'absent' to delete it.
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
  - name: Create (or update) Route Filter
    azure_rm_routefilter:
      resource_group: rg1
      name: filterName
      location: West US
      rules:
        - access: Allow
          route_filter_rule_type: Community
          communities:
            - [
  "12076:5030",
  "12076:5040"
]
          name: ruleName
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsofot.Network/routeFilters/filterName
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


class AzureRMRouteFilters(AzureRMModuleBase):
    """Configuration class for an Azure RM Route Filter resource"""

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
            rules=dict(
                type='list'
            ),
            peerings=dict(
                type='list'
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

        super(AzureRMRouteFilters, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "rules":
                    ev = kwargs[key]
                    if 'access' in ev:
                        if ev['access'] == 'allow':
                            ev['access'] = 'Allow'
                        elif ev['access'] == 'deny':
                            ev['access'] = 'Deny'
                    self.parameters["rules"] = ev
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

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_routefilter()

        if not old_response:
            self.log("Route Filter instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Route Filter instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Route Filter instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_routefilter()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Route Filter instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_routefilter()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_routefilter():
                time.sleep(20)
        else:
            self.log("Route Filter instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_routefilter(self):
        '''
        Creates or updates Route Filter with the specified configuration.

        :return: deserialized Route Filter instance state dictionary
        '''
        self.log("Creating / Updating the Route Filter instance {0}".format(self.name))

        try:
            response = self.mgmt_client.route_filters.create_or_update(resource_group_name=self.resource_group,
                                                                       route_filter_name=self.name,
                                                                       route_filter_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Route Filter instance.')
            self.fail("Error creating the Route Filter instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_routefilter(self):
        '''
        Deletes specified Route Filter instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Route Filter instance {0}".format(self.name))
        try:
            response = self.mgmt_client.route_filters.delete(resource_group_name=self.resource_group,
                                                             route_filter_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Route Filter instance.')
            self.fail("Error deleting the Route Filter instance: {0}".format(str(e)))

        return True

    def get_routefilter(self):
        '''
        Gets the properties of the specified Route Filter.

        :return: deserialized Route Filter instance state dictionary
        '''
        self.log("Checking if the Route Filter instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.route_filters.get(resource_group_name=self.resource_group,
                                                          route_filter_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Route Filter instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Route Filter instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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


def main():
    """Main execution"""
    AzureRMRouteFilters()


if __name__ == '__main__':
    main()

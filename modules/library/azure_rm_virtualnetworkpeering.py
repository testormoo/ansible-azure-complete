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
module: azure_rm_virtualnetworkpeering
version_added: "2.8"
short_description: Manage Virtual Network Peering instance.
description:
    - Create, update and delete instance of Virtual Network Peering.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    virtual_network_name:
        description:
            - The name of the virtual network.
        required: True
    virtual_network_peering_name:
        description:
            - The name of the peering.
        required: True
    id:
        description:
            - Resource ID.
    allow_virtual_network_access:
        description:
            - Whether the VMs in the linked virtual network space would be able to access all the VMs in local Virtual network space.
    allow_forwarded_traffic:
        description:
            - Whether the forwarded traffic from the VMs in the remote virtual network will be allowed/disallowed.
    allow_gateway_transit:
        description:
            - If gateway links can be used in remote virtual networking to link to this virtual network.
    use_remote_gateways:
        description:
            - "If remote gateways can be used on this virtual network. If the flag is set to true, and I(allow_gateway_transit) on remote peering is also
               true, virtual network will use gateways of remote virtual network for transit. Only one peering can have this flag set to true. This flag
               cannot be set if virtual network already has a gateway."
    remote_virtual_network:
        description:
            - "The reference of the remote virtual network. The remote virtual network can be in the same or different region (preview). See here to
               register for the preview and learn more (https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-create-peering)."
        suboptions:
            id:
                description:
                    - Resource ID.
    remote_address_space:
        description:
            - The reference of the remote virtual network address space.
        suboptions:
            address_prefixes:
                description:
                    - A list of address blocks reserved for this virtual network in CIDR notation.
                type: list
    peering_state:
        description:
            - "The status of the virtual network peering. Possible values are 'C(initiated)', 'C(connected)', and 'C(disconnected)'."
        choices:
            - 'initiated'
            - 'connected'
            - 'disconnected'
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
        - Assert the state of the Virtual Network Peering.
        - Use 'present' to create or update an Virtual Network Peering and 'absent' to delete it.
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
  - name: Create (or update) Virtual Network Peering
    azure_rm_virtualnetworkpeering:
      resource_group: peerTest
      virtual_network_name: vnet1
      virtual_network_peering_name: peer
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/peerTest/providers/Microsoft.Network/virtualNetworks/vnet1/virtualNetworkPeerings/peer
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


class AzureRMVirtualNetworkPeerings(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network Peering resource"""

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
            virtual_network_peering_name=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            allow_virtual_network_access=dict(
                type='str'
            ),
            allow_forwarded_traffic=dict(
                type='str'
            ),
            allow_gateway_transit=dict(
                type='str'
            ),
            use_remote_gateways=dict(
                type='str'
            ),
            remote_virtual_network=dict(
                type='dict'
            ),
            remote_address_space=dict(
                type='dict'
            ),
            peering_state=dict(
                type='str',
                choices=['initiated',
                         'connected',
                         'disconnected']
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
        self.virtual_network_peering_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualNetworkPeerings, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "allow_virtual_network_access":
                    self.parameters["allow_virtual_network_access"] = kwargs[key]
                elif key == "allow_forwarded_traffic":
                    self.parameters["allow_forwarded_traffic"] = kwargs[key]
                elif key == "allow_gateway_transit":
                    self.parameters["allow_gateway_transit"] = kwargs[key]
                elif key == "use_remote_gateways":
                    self.parameters["use_remote_gateways"] = kwargs[key]
                elif key == "remote_virtual_network":
                    self.parameters["remote_virtual_network"] = kwargs[key]
                elif key == "remote_address_space":
                    self.parameters["remote_address_space"] = kwargs[key]
                elif key == "peering_state":
                    self.parameters["peering_state"] = _snake_to_camel(kwargs[key], True)
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

        old_response = self.get_virtualnetworkpeering()

        if not old_response:
            self.log("Virtual Network Peering instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Network Peering instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Virtual Network Peering instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network Peering instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkpeering()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network Peering instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetworkpeering()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_virtualnetworkpeering():
                time.sleep(20)
        else:
            self.log("Virtual Network Peering instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_virtualnetworkpeering(self):
        '''
        Creates or updates Virtual Network Peering with the specified configuration.

        :return: deserialized Virtual Network Peering instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network Peering instance {0}".format(self.virtual_network_peering_name))

        try:
            response = self.mgmt_client.virtual_network_peerings.create_or_update(resource_group_name=self.resource_group,
                                                                                  virtual_network_name=self.virtual_network_name,
                                                                                  virtual_network_peering_name=self.virtual_network_peering_name,
                                                                                  virtual_network_peering_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Network Peering instance.')
            self.fail("Error creating the Virtual Network Peering instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetworkpeering(self):
        '''
        Deletes specified Virtual Network Peering instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Network Peering instance {0}".format(self.virtual_network_peering_name))
        try:
            response = self.mgmt_client.virtual_network_peerings.delete(resource_group_name=self.resource_group,
                                                                        virtual_network_name=self.virtual_network_name,
                                                                        virtual_network_peering_name=self.virtual_network_peering_name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network Peering instance.')
            self.fail("Error deleting the Virtual Network Peering instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkpeering(self):
        '''
        Gets the properties of the specified Virtual Network Peering.

        :return: deserialized Virtual Network Peering instance state dictionary
        '''
        self.log("Checking if the Virtual Network Peering instance {0} is present".format(self.virtual_network_peering_name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_peerings.get(resource_group_name=self.resource_group,
                                                                     virtual_network_name=self.virtual_network_name,
                                                                     virtual_network_peering_name=self.virtual_network_peering_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network Peering instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network Peering instance.')
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
    AzureRMVirtualNetworkPeerings()


if __name__ == '__main__':
    main()

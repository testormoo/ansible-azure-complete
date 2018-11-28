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
short_description: Manage Azure Virtual Network Peering instance.
description:
    - Create, update and delete instance of Azure Virtual Network Peering.

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
    name:
        description:
            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
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
      name: peer
      allow_virtual_network_access: True
      allow_forwarded_traffic: True
      allow_gateway_transit: False
      use_remote_gateways: False
      remote_virtual_network:
        id: /subscriptions/subid/resourceGroups/peerTest/providers/Microsoft.Network/virtualNetworks/vnet2
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


class AzureRMVirtualNetworkPeering(AzureRMModuleBase):
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
            name=dict(
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
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            remote_address_space=dict(
                type='dict',
                options=dict(
                    address_prefixes=dict(
                        type='list'
                    )
                )
            ),
            peering_state=dict(
                type='str',
                choices=['initiated',
                         'connected',
                         'disconnected']
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

        super(AzureRMVirtualNetworkPeering, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.virtual_network_peering_parameters[key] = kwargs[key]

        dict_resource_id(self.virtual_network_peering_parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.virtual_network_peering_parameters, ['remote_virtual_network', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.virtual_network_peering_parameters, ['peering_state'], True)

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
                if (not default_compare(self.virtual_network_peering_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network Peering instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkpeering()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network Peering instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetworkpeering()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Network Peering instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_virtualnetworkpeering(self):
        '''
        Creates or updates Virtual Network Peering with the specified configuration.

        :return: deserialized Virtual Network Peering instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network Peering instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_network_peerings.create_or_update(resource_group_name=self.resource_group,
                                                                                  virtual_network_name=self.virtual_network_name,
                                                                                  virtual_network_peering_name=self.name,
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
        self.log("Deleting the Virtual Network Peering instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_network_peerings.delete(resource_group_name=self.resource_group,
                                                                        virtual_network_name=self.virtual_network_name,
                                                                        virtual_network_peering_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network Peering instance.')
            self.fail("Error deleting the Virtual Network Peering instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkpeering(self):
        '''
        Gets the properties of the specified Virtual Network Peering.

        :return: deserialized Virtual Network Peering instance state dictionary
        '''
        self.log("Checking if the Virtual Network Peering instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_peerings.get(resource_group_name=self.resource_group,
                                                                     virtual_network_name=self.virtual_network_name,
                                                                     virtual_network_peering_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network Peering instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network Peering instance.')
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
    AzureRMVirtualNetworkPeering()


if __name__ == '__main__':
    main()

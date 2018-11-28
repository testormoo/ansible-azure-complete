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
module: azure_rm_route
version_added: "2.8"
short_description: Manage Azure Route instance.
description:
    - Create, update and delete instance of Azure Route.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    route_table_name:
        description:
            - The name of the route table.
        required: True
    name:
        description:
            - The name of the route.
        required: True
    id:
        description:
            - Resource ID.
    address_prefix:
        description:
            - The destination CIDR to which the route applies.
    next_hop_type:
        description:
            - "The type of Azure hop the packet should be sent to. Possible values are: 'C(virtual_network_gateway)', 'C(vnet_local)', 'C(internet)',
               'C(virtual_appliance)', and 'C(none)'."
        choices:
            - 'virtual_network_gateway'
            - 'vnet_local'
            - 'internet'
            - 'virtual_appliance'
            - 'none'
    next_hop_ip_address:
        description:
            - The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is C(virtual_appliance).
    name:
        description:
            - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    state:
      description:
        - Assert the state of the Route.
        - Use 'present' to create or update an Route and 'absent' to delete it.
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
  - name: Create (or update) Route
    azure_rm_route:
      resource_group: rg1
      route_table_name: testrt
      name: route1
      address_prefix: 10.0.3.0/24
      next_hop_type: VirtualNetworkGateway
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/routeTables/testrt/routes/route1
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


class AzureRMRoute(AzureRMModuleBase):
    """Configuration class for an Azure RM Route resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            route_table_name=dict(
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
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.route_table_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRoute, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.route_parameters[key] = kwargs[key]

        dict_resource_id(self.route_parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.route_parameters, ['next_hop_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_route()

        if not old_response:
            self.log("Route instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Route instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.route_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Route instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_route()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Route instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_route()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Route instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_route(self):
        '''
        Creates or updates Route with the specified configuration.

        :return: deserialized Route instance state dictionary
        '''
        self.log("Creating / Updating the Route instance {0}".format(self.name))

        try:
            response = self.mgmt_client.routes.create_or_update(resource_group_name=self.resource_group,
                                                                route_table_name=self.route_table_name,
                                                                route_name=self.name,
                                                                route_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Route instance.')
            self.fail("Error creating the Route instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_route(self):
        '''
        Deletes specified Route instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Route instance {0}".format(self.name))
        try:
            response = self.mgmt_client.routes.delete(resource_group_name=self.resource_group,
                                                      route_table_name=self.route_table_name,
                                                      route_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Route instance.')
            self.fail("Error deleting the Route instance: {0}".format(str(e)))

        return True

    def get_route(self):
        '''
        Gets the properties of the specified Route.

        :return: deserialized Route instance state dictionary
        '''
        self.log("Checking if the Route instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.routes.get(resource_group_name=self.resource_group,
                                                   route_table_name=self.route_table_name,
                                                   route_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Route instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Route instance.')
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
    AzureRMRoute()


if __name__ == '__main__':
    main()

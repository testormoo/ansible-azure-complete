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
module: azure_rm_routetable
version_added: "2.8"
short_description: Manage Azure Route Table instance.
description:
    - Create, update and delete instance of Azure Route Table.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the route table.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
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
                    - The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is C(virtual_appliance).
            name:
                description:
                    - The name of the resource that is unique within a resource group. This name can be used to access the resource.
    disable_bgp_route_propagation:
        description:
            - Gets or sets whether to disable the I(routes) learned by BGP on that route table. True means disable.
    state:
      description:
        - Assert the state of the Route Table.
        - Use 'present' to create or update an Route Table and 'absent' to delete it.
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
  - name: Create (or update) Route Table
    azure_rm_routetable:
      resource_group: rg1
      name: testrt
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/routeTables/testrt
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


class AzureRMRouteTable(AzureRMModuleBase):
    """Configuration class for an Azure RM Route Table resource"""

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

        super(AzureRMRouteTable, self).__init__(derived_arg_spec=self.module_arg_spec,
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
        dict_resource_id(self.parameters, ['routes', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.parameters, ['routes', 'next_hop_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_routetable()

        if not old_response:
            self.log("Route Table instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Route Table instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Route Table instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_routetable()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Route Table instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_routetable()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Route Table instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_routetable(self):
        '''
        Creates or updates Route Table with the specified configuration.

        :return: deserialized Route Table instance state dictionary
        '''
        self.log("Creating / Updating the Route Table instance {0}".format(self.name))

        try:
            response = self.mgmt_client.route_tables.create_or_update(resource_group_name=self.resource_group,
                                                                      route_table_name=self.name,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Route Table instance.')
            self.fail("Error creating the Route Table instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_routetable(self):
        '''
        Deletes specified Route Table instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Route Table instance {0}".format(self.name))
        try:
            response = self.mgmt_client.route_tables.delete(resource_group_name=self.resource_group,
                                                            route_table_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Route Table instance.')
            self.fail("Error deleting the Route Table instance: {0}".format(str(e)))

        return True

    def get_routetable(self):
        '''
        Gets the properties of the specified Route Table.

        :return: deserialized Route Table instance state dictionary
        '''
        self.log("Checking if the Route Table instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.route_tables.get(resource_group_name=self.resource_group,
                                                         route_table_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Route Table instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Route Table instance.')
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
            else:
                key = list(old[0])[0]
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
    AzureRMRouteTable()


if __name__ == '__main__':
    main()

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
module: azure_rm_frontdoorbackendpool
version_added: "2.8"
short_description: Manage Backend Pool instance.
description:
    - Create, update and delete instance of Backend Pool.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    name:
        description:
            - Name of the Backend Pool which is unique within the Front Door.
        required: True
    id:
        description:
            - Resource ID.
    backends:
        description:
            - The set of backends for this pool
        type: list
        suboptions:
            address:
                description:
                    - Location of the backend (IP address or FQDN)
            http_port:
                description:
                    - The HTTP TCP port number. Must be between 1 and 65535.
            https_port:
                description:
                    - The HTTPS TCP port number. Must be between 1 and 65535.
            enabled_state:
                description:
                    - "Whether to enable use of this backend. Permitted values are 'C(enabled)' or 'C(disabled)'."
                choices:
                    - 'enabled'
                    - 'disabled'
            priority:
                description:
                    - Priority to use for load balancing. Higher priorities will not be used for load balancing if any lower priority backend is healthy.
            weight:
                description:
                    - Weight of this endpoint for load balancing purposes.
            backend_host_header:
                description:
                    - The value to use as the host header sent to the backend. If blank or unspecified, this defaults to the incoming host.
    load_balancing_settings:
        description:
            - Load balancing settings for a backend pool
        suboptions:
            id:
                description:
                    - Resource ID.
    health_probe_settings:
        description:
            - L7 health probe settings for a backend pool
        suboptions:
            id:
                description:
                    - Resource ID.
    resource_state:
        description:
            - Resource status.
        choices:
            - 'creating'
            - 'enabling'
            - 'enabled'
            - 'disabling'
            - 'disabled'
            - 'deleting'
    name:
        description:
            - Resource name.
    state:
      description:
        - Assert the state of the Backend Pool.
        - Use 'present' to create or update an Backend Pool and 'absent' to delete it.
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
  - name: Create (or update) Backend Pool
    azure_rm_frontdoorbackendpool:
      resource_group: rg1
      front_door_name: frontDoor1
      name: backendPool1
      backends:
        - address: w3.contoso.com
          http_port: 80
          https_port: 443
          priority: 2
          weight: 1
      load_balancing_settings:
        id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/loadBalancingSettings/loadBalancingSettings1
      health_probe_settings:
        id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/healthProbeSettings/healthProbeSettings1
      name: backendPool1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/backendPools/backendPool1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.frontdoor import FrontDoorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMBackendPools(AzureRMModuleBase):
    """Configuration class for an Azure RM Backend Pool resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            front_door_name=dict(
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
            backends=dict(
                type='list'
            ),
            load_balancing_settings=dict(
                type='dict'
            ),
            health_probe_settings=dict(
                type='dict'
            ),
            resource_state=dict(
                type='str',
                choices=['creating',
                         'enabling',
                         'enabled',
                         'disabling',
                         'disabled',
                         'deleting']
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
        self.front_door_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBackendPools, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "backends":
                    ev = kwargs[key]
                    if 'enabled_state' in ev:
                        if ev['enabled_state'] == 'enabled':
                            ev['enabled_state'] = 'Enabled'
                        elif ev['enabled_state'] == 'disabled':
                            ev['enabled_state'] = 'Disabled'
                    self.parameters["backends"] = ev
                elif key == "load_balancing_settings":
                    self.parameters["load_balancing_settings"] = kwargs[key]
                elif key == "health_probe_settings":
                    self.parameters["health_probe_settings"] = kwargs[key]
                elif key == "resource_state":
                    self.parameters["resource_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_backendpool()

        if not old_response:
            self.log("Backend Pool instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Backend Pool instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Backend Pool instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_backendpool()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Backend Pool instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_backendpool()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_backendpool():
                time.sleep(20)
        else:
            self.log("Backend Pool instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_backendpool(self):
        '''
        Creates or updates Backend Pool with the specified configuration.

        :return: deserialized Backend Pool instance state dictionary
        '''
        self.log("Creating / Updating the Backend Pool instance {0}".format(self.name))

        try:
            response = self.mgmt_client.backend_pools.create_or_update(resource_group_name=self.resource_group,
                                                                       front_door_name=self.front_door_name,
                                                                       backend_pool_name=self.name,
                                                                       backend_pool_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Backend Pool instance.')
            self.fail("Error creating the Backend Pool instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_backendpool(self):
        '''
        Deletes specified Backend Pool instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Backend Pool instance {0}".format(self.name))
        try:
            response = self.mgmt_client.backend_pools.delete(resource_group_name=self.resource_group,
                                                             front_door_name=self.front_door_name,
                                                             backend_pool_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Backend Pool instance.')
            self.fail("Error deleting the Backend Pool instance: {0}".format(str(e)))

        return True

    def get_backendpool(self):
        '''
        Gets the properties of the specified Backend Pool.

        :return: deserialized Backend Pool instance state dictionary
        '''
        self.log("Checking if the Backend Pool instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.backend_pools.get(resource_group_name=self.resource_group,
                                                          front_door_name=self.front_door_name,
                                                          backend_pool_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Backend Pool instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Backend Pool instance.')
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMBackendPools()


if __name__ == '__main__':
    main()

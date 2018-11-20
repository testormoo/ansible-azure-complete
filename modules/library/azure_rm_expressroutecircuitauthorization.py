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
module: azure_rm_expressroutecircuitauthorization
version_added: "2.8"
short_description: Manage Express Route Circuit Authorization instance.
description:
    - Create, update and delete instance of Express Route Circuit Authorization.

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
            - The name of the authorization.
        required: True
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
    state:
      description:
        - Assert the state of the Express Route Circuit Authorization.
        - Use 'present' to create or update an Express Route Circuit Authorization and 'absent' to delete it.
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
  - name: Create (or update) Express Route Circuit Authorization
    azure_rm_expressroutecircuitauthorization:
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


class AzureRMExpressRouteCircuitAuthorizations(AzureRMModuleBase):
    """Configuration class for an Azure RM Express Route Circuit Authorization resource"""

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

        super(AzureRMExpressRouteCircuitAuthorizations, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "authorization_key":
                    self.parameters["authorization_key"] = kwargs[key]
                elif key == "authorization_use_status":
                    self.parameters["authorization_use_status"] = _snake_to_camel(kwargs[key], True)
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_expressroutecircuitauthorization()

        if not old_response:
            self.log("Express Route Circuit Authorization instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Express Route Circuit Authorization instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Express Route Circuit Authorization instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_expressroutecircuitauthorization()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Express Route Circuit Authorization instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_expressroutecircuitauthorization()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_expressroutecircuitauthorization():
                time.sleep(20)
        else:
            self.log("Express Route Circuit Authorization instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_expressroutecircuitauthorization(self):
        '''
        Creates or updates Express Route Circuit Authorization with the specified configuration.

        :return: deserialized Express Route Circuit Authorization instance state dictionary
        '''
        self.log("Creating / Updating the Express Route Circuit Authorization instance {0}".format(self.name))

        try:
            response = self.mgmt_client.express_route_circuit_authorizations.create_or_update(resource_group_name=self.resource_group,
                                                                                              circuit_name=self.circuit_name,
                                                                                              authorization_name=self.name,
                                                                                              authorization_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Express Route Circuit Authorization instance.')
            self.fail("Error creating the Express Route Circuit Authorization instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_expressroutecircuitauthorization(self):
        '''
        Deletes specified Express Route Circuit Authorization instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Express Route Circuit Authorization instance {0}".format(self.name))
        try:
            response = self.mgmt_client.express_route_circuit_authorizations.delete(resource_group_name=self.resource_group,
                                                                                    circuit_name=self.circuit_name,
                                                                                    authorization_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Express Route Circuit Authorization instance.')
            self.fail("Error deleting the Express Route Circuit Authorization instance: {0}".format(str(e)))

        return True

    def get_expressroutecircuitauthorization(self):
        '''
        Gets the properties of the specified Express Route Circuit Authorization.

        :return: deserialized Express Route Circuit Authorization instance state dictionary
        '''
        self.log("Checking if the Express Route Circuit Authorization instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.express_route_circuit_authorizations.get(resource_group_name=self.resource_group,
                                                                                 circuit_name=self.circuit_name,
                                                                                 authorization_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Express Route Circuit Authorization instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Express Route Circuit Authorization instance.')
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
    AzureRMExpressRouteCircuitAuthorizations()


if __name__ == '__main__':
    main()

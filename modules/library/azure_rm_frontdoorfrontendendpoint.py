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
module: azure_rm_frontdoorfrontendendpoint
version_added: "2.8"
short_description: Manage Frontend Endpoint instance.
description:
    - Create, update and delete instance of Frontend Endpoint.

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
            - Name of the Frontend endpoint which is unique within the Front Door.
        required: True
    id:
        description:
            - Resource ID.
    host_name:
        description:
            - The host name of the frontendEndpoint. Must be a domain name.
    session_affinity_enabled_state:
        description:
            - "Whether to allow session affinity on this host. Valid options are 'C(C(enabled))' or 'C(C(disabled))'."
        choices:
            - 'enabled'
            - 'disabled'
    session_affinity_ttl_seconds:
        description:
            - UNUSED. This field will be ignored. The TTL to use in seconds for session affinity, if applicable.
    web_application_firewall_policy_link:
        description:
            - Defines the Web Application Firewall policy for each host (if applicable)
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
        - Assert the state of the Frontend Endpoint.
        - Use 'present' to create or update an Frontend Endpoint and 'absent' to delete it.
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
  - name: Create (or update) Frontend Endpoint
    azure_rm_frontdoorfrontendendpoint:
      resource_group: rg1
      front_door_name: frontDoor1
      name: frontDoorEndpoint1
      host_name: www.contoso.com
      session_affinity_enabled_state: Enabled
      session_affinity_ttl_seconds: 60
      web_application_firewall_policy_link:
        id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoorWebApplicationFirewallPolicies/policy1
      name: frontendEndpoint1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/frontendEndpoints/frontendEndpoint1
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


class AzureRMFrontendEndpoints(AzureRMModuleBase):
    """Configuration class for an Azure RM Frontend Endpoint resource"""

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
            host_name=dict(
                type='str'
            ),
            session_affinity_enabled_state=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            session_affinity_ttl_seconds=dict(
                type='int'
            ),
            web_application_firewall_policy_link=dict(
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

        super(AzureRMFrontendEndpoints, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "host_name":
                    self.parameters["host_name"] = kwargs[key]
                elif key == "session_affinity_enabled_state":
                    self.parameters["session_affinity_enabled_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "session_affinity_ttl_seconds":
                    self.parameters["session_affinity_ttl_seconds"] = kwargs[key]
                elif key == "web_application_firewall_policy_link":
                    self.parameters["web_application_firewall_policy_link"] = kwargs[key]
                elif key == "resource_state":
                    self.parameters["resource_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_frontendendpoint()

        if not old_response:
            self.log("Frontend Endpoint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Frontend Endpoint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Frontend Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_frontendendpoint()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Frontend Endpoint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_frontendendpoint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_frontendendpoint():
                time.sleep(20)
        else:
            self.log("Frontend Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_frontendendpoint(self):
        '''
        Creates or updates Frontend Endpoint with the specified configuration.

        :return: deserialized Frontend Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Frontend Endpoint instance {0}".format(self.name))

        try:
            response = self.mgmt_client.frontend_endpoints.create_or_update(resource_group_name=self.resource_group,
                                                                            front_door_name=self.front_door_name,
                                                                            frontend_endpoint_name=self.name,
                                                                            frontend_endpoint_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Frontend Endpoint instance.')
            self.fail("Error creating the Frontend Endpoint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_frontendendpoint(self):
        '''
        Deletes specified Frontend Endpoint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Frontend Endpoint instance {0}".format(self.name))
        try:
            response = self.mgmt_client.frontend_endpoints.delete(resource_group_name=self.resource_group,
                                                                  front_door_name=self.front_door_name,
                                                                  frontend_endpoint_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Frontend Endpoint instance.')
            self.fail("Error deleting the Frontend Endpoint instance: {0}".format(str(e)))

        return True

    def get_frontendendpoint(self):
        '''
        Gets the properties of the specified Frontend Endpoint.

        :return: deserialized Frontend Endpoint instance state dictionary
        '''
        self.log("Checking if the Frontend Endpoint instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.frontend_endpoints.get(resource_group_name=self.resource_group,
                                                               front_door_name=self.front_door_name,
                                                               frontend_endpoint_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Frontend Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Frontend Endpoint instance.')
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
    AzureRMFrontendEndpoints()


if __name__ == '__main__':
    main()

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
module: azure_rm_frontdoorloadbalancingsetting
version_added: "2.8"
short_description: Manage Load Balancing Setting instance.
description:
    - Create, update and delete instance of Load Balancing Setting.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    load_balancing_settings_name:
        description:
            - Name of the load balancing settings which is unique within the Front Door.
        required: True
    id:
        description:
            - Resource ID.
    sample_size:
        description:
            - The number of samples to consider for load balancing decisions
    successful_samples_required:
        description:
            - The number of samples within the sample period that must succeed
    additional_latency_milliseconds:
        description:
            - The additional latency in milliseconds for probes to fall into the lowest latency bucket
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
        - Assert the state of the Load Balancing Setting.
        - Use 'present' to create or update an Load Balancing Setting and 'absent' to delete it.
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
  - name: Create (or update) Load Balancing Setting
    azure_rm_frontdoorloadbalancingsetting:
      resource_group: rg1
      front_door_name: frontDoor1
      load_balancing_settings_name: loadBalancingSettings1
      name: loadBalancingSettings1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/loadBalancingSettings/loadbalancingSettings1
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


class AzureRMLoadBalancingSettings(AzureRMModuleBase):
    """Configuration class for an Azure RM Load Balancing Setting resource"""

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
            load_balancing_settings_name=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            sample_size=dict(
                type='int'
            ),
            successful_samples_required=dict(
                type='int'
            ),
            additional_latency_milliseconds=dict(
                type='int'
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
        self.load_balancing_settings_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLoadBalancingSettings, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "sample_size":
                    self.parameters["sample_size"] = kwargs[key]
                elif key == "successful_samples_required":
                    self.parameters["successful_samples_required"] = kwargs[key]
                elif key == "additional_latency_milliseconds":
                    self.parameters["additional_latency_milliseconds"] = kwargs[key]
                elif key == "resource_state":
                    self.parameters["resource_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_loadbalancingsetting()

        if not old_response:
            self.log("Load Balancing Setting instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Load Balancing Setting instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Load Balancing Setting instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Load Balancing Setting instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_loadbalancingsetting()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Load Balancing Setting instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_loadbalancingsetting()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_loadbalancingsetting():
                time.sleep(20)
        else:
            self.log("Load Balancing Setting instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_loadbalancingsetting(self):
        '''
        Creates or updates Load Balancing Setting with the specified configuration.

        :return: deserialized Load Balancing Setting instance state dictionary
        '''
        self.log("Creating / Updating the Load Balancing Setting instance {0}".format(self.load_balancing_settings_name))

        try:
            response = self.mgmt_client.load_balancing_settings.create_or_update(resource_group_name=self.resource_group,
                                                                                 front_door_name=self.front_door_name,
                                                                                 load_balancing_settings_name=self.load_balancing_settings_name,
                                                                                 load_balancing_settings_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Load Balancing Setting instance.')
            self.fail("Error creating the Load Balancing Setting instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_loadbalancingsetting(self):
        '''
        Deletes specified Load Balancing Setting instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Load Balancing Setting instance {0}".format(self.load_balancing_settings_name))
        try:
            response = self.mgmt_client.load_balancing_settings.delete(resource_group_name=self.resource_group,
                                                                       front_door_name=self.front_door_name,
                                                                       load_balancing_settings_name=self.load_balancing_settings_name)
        except CloudError as e:
            self.log('Error attempting to delete the Load Balancing Setting instance.')
            self.fail("Error deleting the Load Balancing Setting instance: {0}".format(str(e)))

        return True

    def get_loadbalancingsetting(self):
        '''
        Gets the properties of the specified Load Balancing Setting.

        :return: deserialized Load Balancing Setting instance state dictionary
        '''
        self.log("Checking if the Load Balancing Setting instance {0} is present".format(self.load_balancing_settings_name))
        found = False
        try:
            response = self.mgmt_client.load_balancing_settings.get(resource_group_name=self.resource_group,
                                                                    front_door_name=self.front_door_name,
                                                                    load_balancing_settings_name=self.load_balancing_settings_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Load Balancing Setting instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Load Balancing Setting instance.')
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
    AzureRMLoadBalancingSettings()


if __name__ == '__main__':
    main()

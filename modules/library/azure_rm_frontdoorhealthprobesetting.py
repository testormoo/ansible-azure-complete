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
module: azure_rm_frontdoorhealthprobesetting
version_added: "2.8"
short_description: Manage Health Probe Setting instance.
description:
    - Create, update and delete instance of Health Probe Setting.

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
            - Name of the health probe settings which is unique within the Front Door.
        required: True
    id:
        description:
            - Resource ID.
    path:
        description:
            - The path to use for the health probe. Default is /
    protocol:
        description:
            - Protocol scheme to use for this probe.
        choices:
            - 'http'
            - 'https'
    interval_in_seconds:
        description:
            - The number of seconds between health probes.
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
        - Assert the state of the Health Probe Setting.
        - Use 'present' to create or update an Health Probe Setting and 'absent' to delete it.
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
  - name: Create (or update) Health Probe Setting
    azure_rm_frontdoorhealthprobesetting:
      resource_group: rg1
      front_door_name: frontDoor1
      name: healthProbeSettings1
      path: /
      protocol: Http
      interval_in_seconds: 120
      name: healthProbeSettings1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/healthProbeSettings/healthProbeSettings1
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


class AzureRMHealthProbeSettings(AzureRMModuleBase):
    """Configuration class for an Azure RM Health Probe Setting resource"""

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
            path=dict(
                type='str'
            ),
            protocol=dict(
                type='str',
                choices=['http',
                         'https']
            ),
            interval_in_seconds=dict(
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMHealthProbeSettings, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "path":
                    self.parameters["path"] = kwargs[key]
                elif key == "protocol":
                    self.parameters["protocol"] = _snake_to_camel(kwargs[key], True)
                elif key == "interval_in_seconds":
                    self.parameters["interval_in_seconds"] = kwargs[key]
                elif key == "resource_state":
                    self.parameters["resource_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_healthprobesetting()

        if not old_response:
            self.log("Health Probe Setting instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Health Probe Setting instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Health Probe Setting instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_healthprobesetting()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Health Probe Setting instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_healthprobesetting()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_healthprobesetting():
                time.sleep(20)
        else:
            self.log("Health Probe Setting instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_healthprobesetting(self):
        '''
        Creates or updates Health Probe Setting with the specified configuration.

        :return: deserialized Health Probe Setting instance state dictionary
        '''
        self.log("Creating / Updating the Health Probe Setting instance {0}".format(self.name))

        try:
            response = self.mgmt_client.health_probe_settings.create_or_update(resource_group_name=self.resource_group,
                                                                               front_door_name=self.front_door_name,
                                                                               health_probe_settings_name=self.name,
                                                                               health_probe_settings_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Health Probe Setting instance.')
            self.fail("Error creating the Health Probe Setting instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_healthprobesetting(self):
        '''
        Deletes specified Health Probe Setting instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Health Probe Setting instance {0}".format(self.name))
        try:
            response = self.mgmt_client.health_probe_settings.delete(resource_group_name=self.resource_group,
                                                                     front_door_name=self.front_door_name,
                                                                     health_probe_settings_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Health Probe Setting instance.')
            self.fail("Error deleting the Health Probe Setting instance: {0}".format(str(e)))

        return True

    def get_healthprobesetting(self):
        '''
        Gets the properties of the specified Health Probe Setting.

        :return: deserialized Health Probe Setting instance state dictionary
        '''
        self.log("Checking if the Health Probe Setting instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.health_probe_settings.get(resource_group_name=self.resource_group,
                                                                  front_door_name=self.front_door_name,
                                                                  health_probe_settings_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Health Probe Setting instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Health Probe Setting instance.')
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
    AzureRMHealthProbeSettings()


if __name__ == '__main__':
    main()

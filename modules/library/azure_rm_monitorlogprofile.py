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
module: azure_rm_monitorlogprofile
version_added: "2.8"
short_description: Manage Azure Log Profile instance.
description:
    - Create, update and delete instance of Azure Log Profile.

options:
    name:
        description:
            - The name of the log profile.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    storage_account_id:
        description:
            - the resource id of the storage account to which you would like to send the Activity Log.
    service_bus_rule_id:
        description:
            - "The service bus rule ID of the service bus namespace in which you would like to have Event Hubs created for streaming the Activity Log. The
               rule ID is of the format: '{service bus resource ID}/authorizationrules/{key name}'."
    locations:
        description:
            - "List of regions for which Activity Log events should be stored or streamed. It is a comma separated list of valid ARM locations including the
               'global' location."
            - Required when C(state) is I(present).
        type: list
    categories:
        description:
            - "the categories of the logs. These categories are created as is convenient to the user. Some values are: 'Write', 'Delete', and/or 'Action.'"
            - Required when C(state) is I(present).
        type: list
    retention_policy:
        description:
            - the retention policy for the events in the log.
            - Required when C(state) is I(present).
        suboptions:
            enabled:
                description:
                    - a value indicating whether the retention policy is enabled.
                    - Required when C(state) is I(present).
            days:
                description:
                    - the number of days for the retention in days. A value of 0 will retain the events indefinitely.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Log Profile.
        - Use 'present' to create or update an Log Profile and 'absent' to delete it.
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
  - name: Create (or update) Log Profile
    azure_rm_monitorlogprofile:
      name: Rac46PostSwapRG
      location: eastus
      storage_account_id: /subscriptions/df602c9c-7aa0-407d-a6fb-eb20c8bd1192/resourceGroups/JohnKemTest/providers/Microsoft.Storage/storageAccounts/johnkemtest8162
      locations:
        - [
  "global"
]
      categories:
        - [
  "Write",
  "Delete",
  "Action"
]
      retention_policy:
        enabled: True
        days: 3
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: /subscriptions/df602c9c-7aa0-407d-a6fb-eb20c8bd1192/providers/microsoft.insights/logprofiles/default
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMLogProfile(AzureRMModuleBase):
    """Configuration class for an Azure RM Log Profile resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            storage_account_id=dict(
                type='str'
            ),
            service_bus_rule_id=dict(
                type='str'
            ),
            locations=dict(
                type='list'
            ),
            categories=dict(
                type='list'
            ),
            retention_policy=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLogProfile, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_logprofile()

        if not old_response:
            self.log("Log Profile instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Log Profile instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Log Profile instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_logprofile()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Log Profile instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_logprofile()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_logprofile():
                time.sleep(20)
        else:
            self.log("Log Profile instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_logprofile(self):
        '''
        Creates or updates Log Profile with the specified configuration.

        :return: deserialized Log Profile instance state dictionary
        '''
        self.log("Creating / Updating the Log Profile instance {0}".format(self.name))

        try:
            response = self.mgmt_client.log_profiles.create_or_update(log_profile_name=self.name,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Log Profile instance.')
            self.fail("Error creating the Log Profile instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_logprofile(self):
        '''
        Deletes specified Log Profile instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Log Profile instance {0}".format(self.name))
        try:
            response = self.mgmt_client.log_profiles.delete(log_profile_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Log Profile instance.')
            self.fail("Error deleting the Log Profile instance: {0}".format(str(e)))

        return True

    def get_logprofile(self):
        '''
        Gets the properties of the specified Log Profile.

        :return: deserialized Log Profile instance state dictionary
        '''
        self.log("Checking if the Log Profile instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.log_profiles.get(log_profile_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Log Profile instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Log Profile instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMLogProfile()


if __name__ == '__main__':
    main()

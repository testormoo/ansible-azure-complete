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
module: azure_rm_automationwatcher
version_added: "2.8"
short_description: Manage Watcher instance.
description:
    - Create, update and delete instance of Watcher.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    name:
        description:
            - The watcher name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    execution_frequency_in_seconds:
        description:
            - Gets or sets the frequency at which the watcher is invoked.
    script_name:
        description:
            - Gets or sets the name of the script the watcher is attached to, i.e. the name of an existing runbook.
    script_parameters:
        description:
            - Gets or sets the parameters of the script.
    script_run_on:
        description:
            - Gets or sets the name of the hybrid worker group the watcher will run on.
    description:
        description:
            - Gets or sets the description.
    state:
      description:
        - Assert the state of the Watcher.
        - Use 'present' to create or update an Watcher and 'absent' to delete it.
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
  - name: Create (or update) Watcher
    azure_rm_automationwatcher:
      resource_group: rg
      automation_account_name: MyTestAutomationAccount
      name: MyTestWatcher
      location: eastus
      execution_frequency_in_seconds: 60
      script_name: MyTestWatcherRunbook
      script_run_on: MyTestHybridWorkerGroup
      description: This is a test watcher.
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subId/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/MyTestAutomationAccount/watchers/MyTestWatcher
status:
    description:
        - Gets the current status of the watcher.
    returned: always
    type: str
    sample: New
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWatcher(AzureRMModuleBase):
    """Configuration class for an Azure RM Watcher resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            execution_frequency_in_seconds=dict(
                type='int'
            ),
            script_name=dict(
                type='str'
            ),
            script_parameters=dict(
                type='dict'
            ),
            script_run_on=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWatcher, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "execution_frequency_in_seconds":
                    self.parameters["execution_frequency_in_seconds"] = kwargs[key]
                elif key == "script_name":
                    self.parameters["script_name"] = kwargs[key]
                elif key == "script_parameters":
                    self.parameters["script_parameters"] = kwargs[key]
                elif key == "script_run_on":
                    self.parameters["script_run_on"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_watcher()

        if not old_response:
            self.log("Watcher instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Watcher instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Watcher instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_watcher()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Watcher instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_watcher()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_watcher():
                time.sleep(20)
        else:
            self.log("Watcher instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_watcher(self):
        '''
        Creates or updates Watcher with the specified configuration.

        :return: deserialized Watcher instance state dictionary
        '''
        self.log("Creating / Updating the Watcher instance {0}".format(self.name))

        try:
            response = self.mgmt_client.watcher.create_or_update(resource_group_name=self.resource_group,
                                                                 automation_account_name=self.automation_account_name,
                                                                 watcher_name=self.name,
                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Watcher instance.')
            self.fail("Error creating the Watcher instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_watcher(self):
        '''
        Deletes specified Watcher instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Watcher instance {0}".format(self.name))
        try:
            response = self.mgmt_client.watcher.delete(resource_group_name=self.resource_group,
                                                       automation_account_name=self.automation_account_name,
                                                       watcher_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Watcher instance.')
            self.fail("Error deleting the Watcher instance: {0}".format(str(e)))

        return True

    def get_watcher(self):
        '''
        Gets the properties of the specified Watcher.

        :return: deserialized Watcher instance state dictionary
        '''
        self.log("Checking if the Watcher instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.watcher.get(resource_group_name=self.resource_group,
                                                    automation_account_name=self.automation_account_name,
                                                    watcher_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Watcher instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Watcher instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
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


def main():
    """Main execution"""
    AzureRMWatcher()


if __name__ == '__main__':
    main()

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
module: azure_rm_automationtestjob
version_added: "2.8"
short_description: Manage Azure Test Job instance.
description:
    - Create, update and delete instance of Azure Test Job.

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
            - The parameters supplied to the create test job operation.
        required: True
    run_on:
        description:
            - Gets or sets the runOn which specifies the group name where the job is to be executed.
    state:
      description:
        - Assert the state of the Test Job.
        - Use 'present' to create or update an Test Job and 'absent' to delete it.
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
  - name: Create (or update) Test Job
    azure_rm_automationtestjob:
      resource_group: mygroup
      automation_account_name: ContoseAutomationAccount
      name: Get-AzureVMTutorial
      run_on: NOT FOUND
'''

RETURN = '''
status:
    description:
        - Gets or sets the status of the test job.
    returned: always
    type: str
    sample: status
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMTestJob(AzureRMModuleBase):
    """Configuration class for an Azure RM Test Job resource"""

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
            run_on=dict(
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
        self.run_on = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMTestJob, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_testjob()

        if not old_response:
            self.log("Test Job instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Test Job instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Test Job instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_testjob()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Test Job instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_testjob()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Test Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'status': response.get('status', None)
                })
        return self.results

    def create_update_testjob(self):
        '''
        Creates or updates Test Job with the specified configuration.

        :return: deserialized Test Job instance state dictionary
        '''
        self.log("Creating / Updating the Test Job instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.test_job.create(resource_group_name=self.resource_group,
                                                            automation_account_name=self.automation_account_name,
                                                            runbook_name=self.name)
            else:
                response = self.mgmt_client.test_job.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Test Job instance.')
            self.fail("Error creating the Test Job instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_testjob(self):
        '''
        Deletes specified Test Job instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Test Job instance {0}".format(self.name))
        try:
            response = self.mgmt_client.test_job.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Test Job instance.')
            self.fail("Error deleting the Test Job instance: {0}".format(str(e)))

        return True

    def get_testjob(self):
        '''
        Gets the properties of the specified Test Job.

        :return: deserialized Test Job instance state dictionary
        '''
        self.log("Checking if the Test Job instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.test_job.get(resource_group_name=self.resource_group,
                                                     automation_account_name=self.automation_account_name,
                                                     runbook_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Test Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Test Job instance.')
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
    AzureRMTestJob()


if __name__ == '__main__':
    main()

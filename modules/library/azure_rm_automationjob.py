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
module: azure_rm_automationjob
version_added: "2.8"
short_description: Manage Job instance.
description:
    - Create, update and delete instance of Job.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    job_name:
        description:
            - The job name.
        required: True
    runbook:
        description:
            - Gets or sets the runbook.
        suboptions:
            name:
                description:
                    - Gets or sets the name of the runbook.
    parameters:
        description:
            - Gets or sets the parameters of the job.
    run_on:
        description:
            - Gets or sets the runOn which specifies the group name where the job is to be executed.
    client_request_id:
        description:
            - Identifies this specific client request.
    state:
      description:
        - Assert the state of the Job.
        - Use 'present' to create or update an Job and 'absent' to delete it.
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
  - name: Create (or update) Job
    azure_rm_automationjob:
      resource_group: mygroup
      automation_account_name: ContoseAutomationAccount
      job_name: foo
      client_request_id: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: id
status:
    description:
        - "Gets or sets the status of the job. Possible values include: 'New', 'Activating', 'Running', 'Completed', 'Failed', 'Stopped', 'Blocked',
           'Suspended', 'Disconnected', 'Suspending', 'Stopping', 'Resuming', 'Removing'"
    returned: always
    type: str
    sample: status
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


class AzureRMJob(AzureRMModuleBase):
    """Configuration class for an Azure RM Job resource"""

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
            job_name=dict(
                type='str',
                required=True
            ),
            runbook=dict(
                type='dict'
            ),
            parameters=dict(
                type='dict'
            ),
            run_on=dict(
                type='str'
            ),
            client_request_id=dict(
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
        self.job_name = None
        self.parameters = dict()
        self.client_request_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJob, self).__init__(derived_arg_spec=self.module_arg_spec,
                                         supports_check_mode=True,
                                         supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "runbook":
                    self.parameters["runbook"] = kwargs[key]
                elif key == "parameters":
                    self.parameters["parameters"] = kwargs[key]
                elif key == "run_on":
                    self.parameters["run_on"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_job()

        if not old_response:
            self.log("Job instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Job instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_job()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_job()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_job():
                time.sleep(20)
        else:
            self.log("Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_job(self):
        '''
        Creates or updates Job with the specified configuration.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Creating / Updating the Job instance {0}".format(self.))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.job.create(resource_group_name=self.resource_group,
                                                       automation_account_name=self.automation_account_name,
                                                       job_name=self.job_name,
                                                       parameters=self.parameters)
            else:
                response = self.mgmt_client.job.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job instance.')
            self.fail("Error creating the Job instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_job(self):
        '''
        Deletes specified Job instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job instance {0}".format(self.))
        try:
            response = self.mgmt_client.job.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Job instance.')
            self.fail("Error deleting the Job instance: {0}".format(str(e)))

        return True

    def get_job(self):
        '''
        Gets the properties of the specified Job.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Checking if the Job instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.job.get(resource_group_name=self.resource_group,
                                                automation_account_name=self.automation_account_name,
                                                job_name=self.job_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMJob()


if __name__ == '__main__':
    main()
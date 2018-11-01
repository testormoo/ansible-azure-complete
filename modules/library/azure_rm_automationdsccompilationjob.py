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
module: azure_rm_automationdsccompilationjob
version_added: "2.8"
short_description: Manage Dsc Compilation Job instance.
description:
    - Create, update and delete instance of Dsc Compilation Job.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    compilation_job_name:
        description:
            - The the DSC I(configuration) Id.
        required: True
    configuration:
        description:
            - Gets or sets the configuration.
        required: True
        suboptions:
            name:
                description:
                    - Gets or sets the name of the Dsc configuration.
    parameters:
        description:
            - Gets or sets the parameters of the job.
    increment_node_configuration_build:
        description:
            - If a new build version of NodeConfiguration is required.
    name:
        description:
            - Gets or sets name of the resource.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
      description:
        - Assert the state of the Dsc Compilation Job.
        - Use 'present' to create or update an Dsc Compilation Job and 'absent' to delete it.
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
  - name: Create (or update) Dsc Compilation Job
    azure_rm_automationdsccompilationjob:
      resource_group: rg
      automation_account_name: myAutomationAccount33
      compilation_job_name: TestCompilationJob
      location: eastus
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


class AzureRMDscCompilationJob(AzureRMModuleBase):
    """Configuration class for an Azure RM Dsc Compilation Job resource"""

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
            compilation_job_name=dict(
                type='str',
                required=True
            ),
            configuration=dict(
                type='dict',
                required=True
            ),
            parameters=dict(
                type='dict'
            ),
            increment_node_configuration_build=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            location=dict(
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
        self.compilation_job_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDscCompilationJob, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "configuration":
                    self.parameters["configuration"] = kwargs[key]
                elif key == "parameters":
                    self.parameters["parameters"] = kwargs[key]
                elif key == "increment_node_configuration_build":
                    self.parameters["increment_node_configuration_build"] = kwargs[key]
                elif key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_dsccompilationjob()

        if not old_response:
            self.log("Dsc Compilation Job instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Dsc Compilation Job instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Dsc Compilation Job instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dsc Compilation Job instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dsccompilationjob()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dsc Compilation Job instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dsccompilationjob()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_dsccompilationjob():
                time.sleep(20)
        else:
            self.log("Dsc Compilation Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_dsccompilationjob(self):
        '''
        Creates or updates Dsc Compilation Job with the specified configuration.

        :return: deserialized Dsc Compilation Job instance state dictionary
        '''
        self.log("Creating / Updating the Dsc Compilation Job instance {0}".format(self.compilation_job_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.dsc_compilation_job.create(resource_group_name=self.resource_group,
                                                                       automation_account_name=self.automation_account_name,
                                                                       compilation_job_name=self.compilation_job_name,
                                                                       parameters=self.parameters)
            else:
                response = self.mgmt_client.dsc_compilation_job.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Dsc Compilation Job instance.')
            self.fail("Error creating the Dsc Compilation Job instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_dsccompilationjob(self):
        '''
        Deletes specified Dsc Compilation Job instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Dsc Compilation Job instance {0}".format(self.compilation_job_name))
        try:
            response = self.mgmt_client.dsc_compilation_job.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Dsc Compilation Job instance.')
            self.fail("Error deleting the Dsc Compilation Job instance: {0}".format(str(e)))

        return True

    def get_dsccompilationjob(self):
        '''
        Gets the properties of the specified Dsc Compilation Job.

        :return: deserialized Dsc Compilation Job instance state dictionary
        '''
        self.log("Checking if the Dsc Compilation Job instance {0} is present".format(self.compilation_job_name))
        found = False
        try:
            response = self.mgmt_client.dsc_compilation_job.get(resource_group_name=self.resource_group,
                                                                automation_account_name=self.automation_account_name,
                                                                compilation_job_name=self.compilation_job_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Dsc Compilation Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Dsc Compilation Job instance.')
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
    AzureRMDscCompilationJob()


if __name__ == '__main__':
    main()

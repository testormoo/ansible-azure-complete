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
module: azure_rm_automationsourcecontrolsyncjob
version_added: "2.8"
short_description: Manage Source Control Sync Job instance.
description:
    - Create, update and delete instance of Source Control Sync Job.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    source_control_name:
        description:
            - The source control name.
        required: True
    source_control_sync_job_id:
        description:
            - The source control sync job id.
        required: True
    commit_id:
        description:
            - The commit id of the source control sync job. If not syncing to a commitId, enter an empty string.
        required: True
    state:
      description:
        - Assert the state of the Source Control Sync Job.
        - Use 'present' to create or update an Source Control Sync Job and 'absent' to delete it.
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
  - name: Create (or update) Source Control Sync Job
    azure_rm_automationsourcecontrolsyncjob:
      resource_group: rg
      automation_account_name: myAutomationAccount33
      source_control_name: MySourceControl
      source_control_sync_job_id: ce6fe3e3-9db3-4096-a6b4-82bfb4c10a9a
      commit_id: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource id.
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
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSourceControlSyncJob(AzureRMModuleBase):
    """Configuration class for an Azure RM Source Control Sync Job resource"""

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
            source_control_name=dict(
                type='str',
                required=True
            ),
            source_control_sync_job_id=dict(
                type='str',
                required=True
            ),
            commit_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.source_control_name = None
        self.source_control_sync_job_id = None
        self.commit_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSourceControlSyncJob, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_sourcecontrolsyncjob()

        if not old_response:
            self.log("Source Control Sync Job instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Source Control Sync Job instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Source Control Sync Job instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Source Control Sync Job instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_sourcecontrolsyncjob()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Source Control Sync Job instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sourcecontrolsyncjob()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_sourcecontrolsyncjob():
                time.sleep(20)
        else:
            self.log("Source Control Sync Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_sourcecontrolsyncjob(self):
        '''
        Creates or updates Source Control Sync Job with the specified configuration.

        :return: deserialized Source Control Sync Job instance state dictionary
        '''
        self.log("Creating / Updating the Source Control Sync Job instance {0}".format(self.source_control_sync_job_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.source_control_sync_job.create(resource_group_name=self.resource_group,
                                                                           automation_account_name=self.automation_account_name,
                                                                           source_control_name=self.source_control_name,
                                                                           source_control_sync_job_id=self.source_control_sync_job_id,
                                                                           commit_id=self.commit_id)
            else:
                response = self.mgmt_client.source_control_sync_job.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Source Control Sync Job instance.')
            self.fail("Error creating the Source Control Sync Job instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_sourcecontrolsyncjob(self):
        '''
        Deletes specified Source Control Sync Job instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Source Control Sync Job instance {0}".format(self.source_control_sync_job_id))
        try:
            response = self.mgmt_client.source_control_sync_job.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Source Control Sync Job instance.')
            self.fail("Error deleting the Source Control Sync Job instance: {0}".format(str(e)))

        return True

    def get_sourcecontrolsyncjob(self):
        '''
        Gets the properties of the specified Source Control Sync Job.

        :return: deserialized Source Control Sync Job instance state dictionary
        '''
        self.log("Checking if the Source Control Sync Job instance {0} is present".format(self.source_control_sync_job_id))
        found = False
        try:
            response = self.mgmt_client.source_control_sync_job.get(resource_group_name=self.resource_group,
                                                                    automation_account_name=self.automation_account_name,
                                                                    source_control_name=self.source_control_name,
                                                                    source_control_sync_job_id=self.source_control_sync_job_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Source Control Sync Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Source Control Sync Job instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMSourceControlSyncJob()


if __name__ == '__main__':
    main()

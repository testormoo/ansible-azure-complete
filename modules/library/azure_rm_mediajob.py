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
module: azure_rm_mediajob
version_added: "2.8"
short_description: Manage Job instance.
description:
    - Create, update and delete instance of Job.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    transform_name:
        description:
            - The Transform name.
        required: True
    job_name:
        description:
            - The Job name.
        required: True
    description:
        description:
            - Optional customer supplied description of the Job.
    input:
        description:
            - The inputs for the Job.
        required: True
        suboptions:
            odatatype:
                description:
                    - Constant filled by server.
                required: True
    outputs:
        description:
            - The outputs for the Job.
        required: True
        type: list
        suboptions:
            label:
                description:
                    - "A label that is assigned to a JobOutput in order to help uniquely identify it. This is useful when your Transform has more than one
                       TransformOutput, whereby your Job has more than one JobOutput. In such cases, when you submit the Job, you will add two or more
                       JobOutputs, in the same order as TransformOutputs in the Transform. Subsequently, when you retrieve the Job, either through events
                       or on a GET request, you can use the label to easily identify the JobOutput. If a label is not provided, a default value of
                       '{presetName}_{outputIndex}' will be used, where the preset name is the name of the preset in the corresponding TransformOutput and
                       the output index is the relative index of the this JobOutput within the Job. Note that this index is the same as the relative index
                       of the corresponding TransformOutput within its Transform."
            odatatype:
                description:
                    - Constant filled by server.
                required: True
    priority:
        description:
            - "Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is
               C(normal)."
        choices:
            - 'low'
            - 'normal'
            - 'high'
    correlation_data:
        description:
            - Customer provided correlation data that will be returned in Job and JobOutput state events.
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
    azure_rm_mediajob:
      resource_group: contosoresources
      account_name: contosomedia
      transform_name: exampleTransform
      job_name: job1
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contosoresources/providers/Microsoft.Media/mediaservices/contosomedia/transfo
            rms/exampleTransform/jobs/job1"
state:
    description:
        - "The current state of the job. Possible values include: 'Canceled', 'Canceling', 'Error', 'Finished', 'Processing', 'Queued', 'Scheduled'"
    returned: always
    type: str
    sample: Queued
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMJobs(AzureRMModuleBase):
    """Configuration class for an Azure RM Job resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            transform_name=dict(
                type='str',
                required=True
            ),
            job_name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            input=dict(
                type='dict',
                required=True
            ),
            outputs=dict(
                type='list',
                required=True
            ),
            priority=dict(
                type='str',
                choices=['low',
                         'normal',
                         'high']
            ),
            correlation_data=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.transform_name = None
        self.job_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobs, self).__init__(derived_arg_spec=self.module_arg_spec,
                                          supports_check_mode=True,
                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "input":
                    self.parameters["input"] = kwargs[key]
                elif key == "outputs":
                    self.parameters["outputs"] = kwargs[key]
                elif key == "priority":
                    self.parameters["priority"] = _snake_to_camel(kwargs[key], True)
                elif key == "correlation_data":
                    self.parameters["correlation_data"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
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
        self.log("Creating / Updating the Job instance {0}".format(self.job_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.jobs.create(resource_group_name=self.resource_group,
                                                        account_name=self.account_name,
                                                        transform_name=self.transform_name,
                                                        job_name=self.job_name,
                                                        parameters=self.parameters)
            else:
                response = self.mgmt_client.jobs.update(resource_group_name=self.resource_group,
                                                        account_name=self.account_name,
                                                        transform_name=self.transform_name,
                                                        job_name=self.job_name,
                                                        parameters=self.parameters)
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
        self.log("Deleting the Job instance {0}".format(self.job_name))
        try:
            response = self.mgmt_client.jobs.delete(resource_group_name=self.resource_group,
                                                    account_name=self.account_name,
                                                    transform_name=self.transform_name,
                                                    job_name=self.job_name)
        except CloudError as e:
            self.log('Error attempting to delete the Job instance.')
            self.fail("Error deleting the Job instance: {0}".format(str(e)))

        return True

    def get_job(self):
        '''
        Gets the properties of the specified Job.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Checking if the Job instance {0} is present".format(self.job_name))
        found = False
        try:
            response = self.mgmt_client.jobs.get(resource_group_name=self.resource_group,
                                                 account_name=self.account_name,
                                                 transform_name=self.transform_name,
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
            'state': d.get('state', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMJobs()


if __name__ == '__main__':
    main()

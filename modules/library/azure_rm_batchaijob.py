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
module: azure_rm_batchaijob
version_added: "2.8"
short_description: Manage Job instance.
description:
    - Create, update and delete instance of Job.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    job_name:
        description:
            - "The name of the job within the specified resource group. Job names can only contain a combination of alphanumeric characters along with dash
               (-) and underscore (_). The name must be from 1 through 64 characters long."
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    experiment_name:
        description:
            - Describe the experiment information of the job
    priority:
        description:
            - "Priority associated with the job. Priority values can range from -1000 to 1000, with -1000 being the lowest priority and 1000 being the
               highest priority. The default value is 0."
    cluster:
        description:
        required: True
        suboptions:
            id:
                description:
                    - The ID of the resource
                required: True
    node_count:
        description:
            - The job will be gang scheduled on that many compute nodes
        required: True
    container_settings:
        description:
            - "If the container was downloaded as part of I(cluster) setup then the same container image will be used. If not provided, the job will run on
               the VM."
        suboptions:
            image_source_registry:
                description:
                required: True
                suboptions:
                    server_url:
                        description:
                    image:
                        description:
                        required: True
                    credentials:
                        description:
                        suboptions:
                            username:
                                description:
                                required: True
                            password:
                                description:
                                    - One of password or I(password_secret_reference) must be specified.
                            password_secret_reference:
                                description:
                                    - "Users can store their secrets in Azure KeyVault and pass it to the Batch AI Service to integrate with KeyVault. One
                                       of I(password) or passwordSecretReference must be specified."
                                suboptions:
                                    source_vault:
                                        description:
                                        required: True
                                    secret_url:
                                        description:
                                        required: True
    cntk_settings:
        description:
        suboptions:
            language_type:
                description:
                    - "Valid values are 'BrainScript' or 'Python'."
            config_file_path:
                description:
                    - "This property can be specified only if the I(language_type) is 'BrainScript'."
            python_script_file_path:
                description:
                    - "This property can be specified only if the I(language_type) is 'Python'."
            python_interpreter_path:
                description:
                    - "This property can be specified only if the I(language_type) is 'Python'."
            command_line_args:
                description:
            process_count:
                description:
                    - The default value for this property is equal to nodeCount property
    tensor_flow_settings:
        description:
        suboptions:
            python_script_file_path:
                description:
                required: True
            python_interpreter_path:
                description:
            master_command_line_args:
                description:
                required: True
            worker_command_line_args:
                description:
                    - This property is optional for single machine training.
            parameter_server_command_line_args:
                description:
                    - This property is optional for single machine training.
            worker_count:
                description:
                    - "If specified, the value must be less than or equal to (nodeCount * numberOfGPUs per VM). If not specified, the default value is equal
                       to nodeCount. This property can be specified only for distributed TensorFlow training"
            parameter_server_count:
                description:
                    - "If specified, the value must be less than or equal to nodeCount. If not specified, the default value is equal to 1 for distributed
                       TensorFlow training (This property is not applicable for single machine training). This property can be specified only for
                       distributed TensorFlow training."
    caffe_settings:
        description:
        suboptions:
            config_file_path:
                description:
                    - This property cannot be specified if I(python_script_file_path) is specified.
            python_script_file_path:
                description:
                    - This property cannot be specified if I(config_file_path) is specified.
            python_interpreter_path:
                description:
                    - This property can be specified only if the I(python_script_file_path) is specified.
            command_line_args:
                description:
            process_count:
                description:
                    - The default value for this property is equal to nodeCount property
    caffe2_settings:
        description:
        suboptions:
            python_script_file_path:
                description:
                required: True
            python_interpreter_path:
                description:
            command_line_args:
                description:
    chainer_settings:
        description:
        suboptions:
            python_script_file_path:
                description:
                required: True
            python_interpreter_path:
                description:
            command_line_args:
                description:
            process_count:
                description:
                    - The default value for this property is equal to nodeCount property
    custom_toolkit_settings:
        description:
        suboptions:
            command_line:
                description:
    job_preparation:
        description:
            - The specified actions will run on all the nodes that are part of the job
        suboptions:
            command_line:
                description:
                    - "If containerSettings is specified on the job, this commandLine will be executed in the same container as job. Otherwise it will be
                       executed on the node."
                required: True
    std_out_err_path_prefix:
        description:
            - The path where the Batch AI service will upload stdout and stderror of the job.
        required: True
    input_directories:
        description:
        type: list
        suboptions:
            id:
                description:
                    - "It will be available for the job as an environment variable under AZ_BATCHAI_INPUT_id. The service will also provide the following
                       environment variable: AZ_BATCHAI_PREV_OUTPUT_Name. The value of the variable will be populated if the job is being retried after a
                       previous failure, otherwise it will be set to nothing."
                required: True
            path:
                description:
                required: True
    output_directories:
        description:
        type: list
        suboptions:
            id:
                description:
                    - It will be available for the job as an environment variable under AZ_BATCHAI_OUTPUT_id.
                required: True
            path_prefix:
                description:
                    - "NOTE: This is an absolute path to prefix. E.g. $AZ_BATCHAI_MOUNT_ROOT/MyNFS/MyLogs."
                required: True
            path_suffix:
                description:
                    - The suffix path where the output directory will be created.
            type:
                description:
                    - "Default value is C(custom). The possible values are C(model), C(logs), C(summary), and C(custom). Users can use multiple enums for a
                       single directory. Eg. outPutType='C(model),C(logs), C(summary)'."
                choices:
                    - 'model'
                    - 'logs'
                    - 'summary'
                    - 'custom'
            create_new:
                description:
                    - Default is true. If false, then the directory is not created and can be any directory path that the user specifies.
    environment_variables:
        description:
            - "Batch AI service sets the following environment variables for all jobs: AZ_BATCHAI_INPUT_id, AZ_BATCHAI_OUTPUT_id,
               AZ_BATCHAI_NUM_GPUS_PER_NODE. For distributed TensorFlow jobs, following additional environment variables are set by the Batch AI Service:
               AZ_BATCHAI_PS_HOSTS, AZ_BATCHAI_WORKER_HOSTS"
        type: list
        suboptions:
            name:
                description:
                required: True
            value:
                description:
    constraints:
        description:
            - Constraints associated with the Job.
        suboptions:
            max_wall_clock_time:
                description:
                    - Default Value = 1 week.
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
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Job
    azure_rm_batchaijob:
      resource_group: demo_resource_group
      job_name: demo_job
      location: eastus
'''

RETURN = '''
id:
    description:
        - The ID of the resource
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.BatchAI/jobs/demo_job
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.batchai import BatchAIManagementClient
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
            job_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            experiment_name=dict(
                type='str'
            ),
            priority=dict(
                type='int'
            ),
            cluster=dict(
                type='dict',
                required=True
            ),
            node_count=dict(
                type='int',
                required=True
            ),
            container_settings=dict(
                type='dict'
            ),
            cntk_settings=dict(
                type='dict'
            ),
            tensor_flow_settings=dict(
                type='dict'
            ),
            caffe_settings=dict(
                type='dict'
            ),
            caffe2_settings=dict(
                type='dict'
            ),
            chainer_settings=dict(
                type='dict'
            ),
            custom_toolkit_settings=dict(
                type='dict'
            ),
            job_preparation=dict(
                type='dict'
            ),
            std_out_err_path_prefix=dict(
                type='str',
                required=True
            ),
            input_directories=dict(
                type='list'
            ),
            output_directories=dict(
                type='list'
            ),
            environment_variables=dict(
                type='list'
            ),
            constraints=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.job_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobs, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "experiment_name":
                    self.parameters["experiment_name"] = kwargs[key]
                elif key == "priority":
                    self.parameters["priority"] = kwargs[key]
                elif key == "cluster":
                    self.parameters["cluster"] = kwargs[key]
                elif key == "node_count":
                    self.parameters["node_count"] = kwargs[key]
                elif key == "container_settings":
                    self.parameters["container_settings"] = kwargs[key]
                elif key == "cntk_settings":
                    self.parameters["cntk_settings"] = kwargs[key]
                elif key == "tensor_flow_settings":
                    self.parameters["tensor_flow_settings"] = kwargs[key]
                elif key == "caffe_settings":
                    self.parameters["caffe_settings"] = kwargs[key]
                elif key == "caffe2_settings":
                    self.parameters["caffe2_settings"] = kwargs[key]
                elif key == "chainer_settings":
                    self.parameters["chainer_settings"] = kwargs[key]
                elif key == "custom_toolkit_settings":
                    self.parameters["custom_toolkit_settings"] = kwargs[key]
                elif key == "job_preparation":
                    self.parameters["job_preparation"] = kwargs[key]
                elif key == "std_out_err_path_prefix":
                    self.parameters["std_out_err_path_prefix"] = kwargs[key]
                elif key == "input_directories":
                    self.parameters["input_directories"] = kwargs[key]
                elif key == "output_directories":
                    self.parameters["output_directories"] = kwargs[key]
                elif key == "environment_variables":
                    self.parameters["environment_variables"] = kwargs[key]
                elif key == "constraints":
                    self.parameters["constraints"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BatchAIManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

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
                                                        job_name=self.job_name,
                                                        parameters=self.parameters)
            else:
                response = self.mgmt_client.jobs.update()
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
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMJobs()


if __name__ == '__main__':
    main()

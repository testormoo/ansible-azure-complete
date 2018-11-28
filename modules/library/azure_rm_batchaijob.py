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
short_description: Manage Azure Job instance.
description:
    - Create, update and delete instance of Azure Job.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
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
            - Required when C(state) is I(present).
        suboptions:
            id:
                description:
                    - The ID of the resource
                    - Required when C(state) is I(present).
    node_count:
        description:
            - The job will be gang scheduled on that many compute nodes
            - Required when C(state) is I(present).
    container_settings:
        description:
            - "If the container was downloaded as part of I(cluster) setup then the same container image will be used. If not provided, the job will run on
               the VM."
        suboptions:
            image_source_registry:
                description:
                    - Required when C(state) is I(present).
                suboptions:
                    server_url:
                        description:
                    image:
                        description:
                            - Required when C(state) is I(present).
                    credentials:
                        description:
                        suboptions:
                            username:
                                description:
                                    - Required when C(state) is I(present).
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
                                            - Required when C(state) is I(present).
                                    secret_url:
                                        description:
                                            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
            python_interpreter_path:
                description:
            master_command_line_args:
                description:
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
            python_interpreter_path:
                description:
            command_line_args:
                description:
    chainer_settings:
        description:
        suboptions:
            python_script_file_path:
                description:
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
    std_out_err_path_prefix:
        description:
            - The path where the Batch AI service will upload stdout and stderror of the job.
            - Required when C(state) is I(present).
    input_directories:
        description:
        type: list
        suboptions:
            id:
                description:
                    - "It will be available for the job as an environment variable under AZ_BATCHAI_INPUT_id. The service will also provide the following
                       environment variable: AZ_BATCHAI_PREV_OUTPUT_Name. The value of the variable will be populated if the job is being retried after a
                       previous failure, otherwise it will be set to nothing."
                    - Required when C(state) is I(present).
            path:
                description:
                    - Required when C(state) is I(present).
    output_directories:
        description:
        type: list
        suboptions:
            id:
                description:
                    - It will be available for the job as an environment variable under AZ_BATCHAI_OUTPUT_id.
                    - Required when C(state) is I(present).
            path_prefix:
                description:
                    - "NOTE: This is an absolute path to prefix. E.g. $AZ_BATCHAI_MOUNT_ROOT/MyNFS/MyLogs."
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
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
      name: demo_job
      location: eastus
      priority: 0
      cluster:
        id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.BatchAI/clusters/demo_cluster
      node_count: 1
      container_settings:
        image_source_registry:
          image: ubuntu
      custom_toolkit_settings:
        command_line: echo hi | tee $AZ_BATCHAI_OUTPUT_OUTPUTS/hi.txt
      std_out_err_path_prefix: $AZ_BATCHAI_MOUNT_ROOT/azfiles
      input_directories:
        - id: INPUT
          path: $AZ_BATCHAI_MOUNT_ROOT/azfiles/input
      output_directories:
        - id: OUTPUTS
          path_prefix: $AZ_BATCHAI_MOUNT_ROOT/azfiles/
          path_suffix: files
          type: custom
          create_new: True
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMJob(AzureRMModuleBase):
    """Configuration class for an Azure RM Job resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
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
            experiment_name=dict(
                type='str'
            ),
            priority=dict(
                type='int'
            ),
            cluster=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            node_count=dict(
                type='int'
            ),
            container_settings=dict(
                type='dict',
                options=dict(
                    image_source_registry=dict(
                        type='dict',
                        options=dict(
                            server_url=dict(
                                type='str'
                            ),
                            image=dict(
                                type='str'
                            ),
                            credentials=dict(
                                type='dict',
                                options=dict(
                                    username=dict(
                                        type='str'
                                    ),
                                    password=dict(
                                        type='str',
                                        no_log=True
                                    ),
                                    password_secret_reference=dict(
                                        type='dict',
                                        no_log=True,
                                        options=dict(
                                            source_vault=dict(
                                                type='dict'
                                            ),
                                            secret_url=dict(
                                                type='str'
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            cntk_settings=dict(
                type='dict',
                options=dict(
                    language_type=dict(
                        type='str'
                    ),
                    config_file_path=dict(
                        type='str'
                    ),
                    python_script_file_path=dict(
                        type='str'
                    ),
                    python_interpreter_path=dict(
                        type='str'
                    ),
                    command_line_args=dict(
                        type='str'
                    ),
                    process_count=dict(
                        type='int'
                    )
                )
            ),
            tensor_flow_settings=dict(
                type='dict',
                options=dict(
                    python_script_file_path=dict(
                        type='str'
                    ),
                    python_interpreter_path=dict(
                        type='str'
                    ),
                    master_command_line_args=dict(
                        type='str'
                    ),
                    worker_command_line_args=dict(
                        type='str'
                    ),
                    parameter_server_command_line_args=dict(
                        type='str'
                    ),
                    worker_count=dict(
                        type='int'
                    ),
                    parameter_server_count=dict(
                        type='int'
                    )
                )
            ),
            caffe_settings=dict(
                type='dict',
                options=dict(
                    config_file_path=dict(
                        type='str'
                    ),
                    python_script_file_path=dict(
                        type='str'
                    ),
                    python_interpreter_path=dict(
                        type='str'
                    ),
                    command_line_args=dict(
                        type='str'
                    ),
                    process_count=dict(
                        type='int'
                    )
                )
            ),
            caffe2_settings=dict(
                type='dict',
                options=dict(
                    python_script_file_path=dict(
                        type='str'
                    ),
                    python_interpreter_path=dict(
                        type='str'
                    ),
                    command_line_args=dict(
                        type='str'
                    )
                )
            ),
            chainer_settings=dict(
                type='dict',
                options=dict(
                    python_script_file_path=dict(
                        type='str'
                    ),
                    python_interpreter_path=dict(
                        type='str'
                    ),
                    command_line_args=dict(
                        type='str'
                    ),
                    process_count=dict(
                        type='int'
                    )
                )
            ),
            custom_toolkit_settings=dict(
                type='dict',
                options=dict(
                    command_line=dict(
                        type='str'
                    )
                )
            ),
            job_preparation=dict(
                type='dict',
                options=dict(
                    command_line=dict(
                        type='str'
                    )
                )
            ),
            std_out_err_path_prefix=dict(
                type='str'
            ),
            input_directories=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    path=dict(
                        type='str'
                    )
                )
            ),
            output_directories=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    path_prefix=dict(
                        type='str'
                    ),
                    path_suffix=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str',
                        choices=['model',
                                 'logs',
                                 'summary',
                                 'custom']
                    ),
                    create_new=dict(
                        type='str'
                    )
                )
            ),
            environment_variables=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            constraints=dict(
                type='dict',
                options=dict(
                    max_wall_clock_time=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJob, self).__init__(derived_arg_spec=self.module_arg_spec,
                                         supports_check_mode=True,
                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['cluster', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['input_directories', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['output_directories', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_job()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_job()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_job(self):
        '''
        Creates or updates Job with the specified configuration.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Creating / Updating the Job instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.jobs.create(resource_group_name=self.resource_group,
                                                        job_name=self.name,
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
        self.log("Deleting the Job instance {0}".format(self.name))
        try:
            response = self.mgmt_client.jobs.delete(resource_group_name=self.resource_group,
                                                    job_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Job instance.')
            self.fail("Error deleting the Job instance: {0}".format(str(e)))

        return True

    def get_job(self):
        '''
        Gets the properties of the specified Job.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Checking if the Job instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.jobs.get(resource_group_name=self.resource_group,
                                                 job_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job instance.')
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMJob()


if __name__ == '__main__':
    main()

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
module: azure_rm_batchaicluster
version_added: "2.8"
short_description: Manage Azure Cluster instance.
description:
    - Create, update and delete instance of Azure Cluster.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - "The name of the cluster within the specified resource group. Cluster names can only contain a combination of alphanumeric characters along
               with dash (-) and underscore (_). The name must be from 1 through 64 characters long."
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    vm_size:
        description:
            - "All virtual machines in a cluster are the same size. For information about available VM sizes for clusters using images from the Virtual
               Machines Marketplace (see Sizes for Virtual Machines (Linux) or Sizes for Virtual Machines (Windows). Batch AI service supports all Azure VM
               sizes except STANDARD_A0 and those with premium storage (STANDARD_GS, STANDARD_DS, and STANDARD_DSV2 series)."
            - Required when C(state) is I(present).
    vm_priority:
        description:
            - Default is C(dedicated).
        choices:
            - 'dedicated'
            - 'lowpriority'
    scale_settings:
        description:
        suboptions:
            manual:
                description:
                suboptions:
                    target_node_count:
                        description:
                            - Default is 0. If autoScaleSettings are not specified, then the Cluster starts with this target.
                            - Required when C(state) is I(present).
                    node_deallocation_option:
                        description:
                            - The default value is C(requeue).
                        choices:
                            - 'requeue'
                            - 'terminate'
                            - 'waitforjobcompletion'
                            - 'unknown'
            auto_scale:
                description:
                suboptions:
                    minimum_node_count:
                        description:
                            - Required when C(state) is I(present).
                    maximum_node_count:
                        description:
                            - Required when C(state) is I(present).
                    initial_node_count:
                        description:
    virtual_machine_configuration:
        description:
        suboptions:
            image_reference:
                description:
                suboptions:
                    publisher:
                        description:
                            - Required when C(state) is I(present).
                    offer:
                        description:
                            - Required when C(state) is I(present).
                    sku:
                        description:
                            - Required when C(state) is I(present).
                    version:
                        description:
    node_setup:
        description:
        suboptions:
            setup_task:
                description:
                suboptions:
                    command_line:
                        description:
                            - Required when C(state) is I(present).
                    environment_variables:
                        description:
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Required when C(state) is I(present).
                            value:
                                description:
                    run_elevated:
                        description:
                    std_out_err_path_prefix:
                        description:
                            - The path where the Batch AI service will upload the stdout and stderror of setup task.
                            - Required when C(state) is I(present).
            mount_volumes:
                description:
                suboptions:
                    azure_file_shares:
                        description:
                            - References to Azure File Shares that are to be mounted to the cluster nodes.
                        type: list
                        suboptions:
                            account_name:
                                description:
                                    - Required when C(state) is I(present).
                            azure_file_url:
                                description:
                                    - Required when C(state) is I(present).
                            credentials:
                                description:
                                    - Required when C(state) is I(present).
                                suboptions:
                                    account_key:
                                        description:
                                            - One of accountKey or I(account_key_secret_reference) must be specified.
                                    account_key_secret_reference:
                                        description:
                                            - "Users can store their secrets in Azure KeyVault and pass it to the Batch AI Service to integrate with
                                               KeyVault. One of I(account_key) or accountKeySecretReference must be specified."
                            relative_mount_path:
                                description:
                                    - Note that all file shares will be mounted under $AZ_BATCHAI_MOUNT_ROOT location.
                                    - Required when C(state) is I(present).
                            file_mode:
                                description:
                                    - Default value is 0777. Valid only if OS is linux.
                            directory_mode:
                                description:
                                    - Default value is 0777. Valid only if OS is linux.
                    azure_blob_file_systems:
                        description:
                            - References to Azure Blob FUSE that are to be mounted to the cluster nodes.
                        type: list
                        suboptions:
                            account_name:
                                description:
                                    - Required when C(state) is I(present).
                            container_name:
                                description:
                                    - Required when C(state) is I(present).
                            credentials:
                                description:
                                    - Required when C(state) is I(present).
                                suboptions:
                                    account_key:
                                        description:
                                            - One of accountKey or I(account_key_secret_reference) must be specified.
                                    account_key_secret_reference:
                                        description:
                                            - "Users can store their secrets in Azure KeyVault and pass it to the Batch AI Service to integrate with
                                               KeyVault. One of I(account_key) or accountKeySecretReference must be specified."
                            relative_mount_path:
                                description:
                                    - Note that all blob file systems will be mounted under $AZ_BATCHAI_MOUNT_ROOT location.
                                    - Required when C(state) is I(present).
                            mount_options:
                                description:
                    file_servers:
                        description:
                        type: list
                        suboptions:
                            file_server:
                                description:
                                    - Required when C(state) is I(present).
                                suboptions:
                                    id:
                                        description:
                                            - The ID of the resource
                                            - Required when C(state) is I(present).
                            source_directory:
                                description:
                                    - If this property is not specified, the entire File Server will be mounted.
                            relative_mount_path:
                                description:
                                    - Note that all file shares will be mounted under $AZ_BATCHAI_MOUNT_ROOT location.
                                    - Required when C(state) is I(present).
                            mount_options:
                                description:
                    unmanaged_file_systems:
                        description:
                        type: list
                        suboptions:
                            mount_command:
                                description:
                                    - Required when C(state) is I(present).
                            relative_mount_path:
                                description:
                                    - Note that all file shares will be mounted under $AZ_BATCHAI_MOUNT_ROOT location.
                                    - Required when C(state) is I(present).
    user_account_settings:
        description:
            - Required when C(state) is I(present).
        suboptions:
            admin_user_name:
                description:
                    - Required when C(state) is I(present).
            admin_user_ssh_public_key:
                description:
            admin_user_password:
                description:
    subnet:
        description:
        suboptions:
            id:
                description:
                    - The ID of the resource
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Cluster.
        - Use 'present' to create or update an Cluster and 'absent' to delete it.
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
  - name: Create (or update) Cluster
    azure_rm_batchaicluster:
      resource_group: demo_resource_group
      name: demo_cluster
      location: eastus
      vm_size: STANDARD_NC6
      vm_priority: dedicated
      scale_settings:
        manual:
          target_node_count: 1
          node_deallocation_option: requeue
      node_setup:
        mount_volumes:
          azure_file_shares:
            - account_name: storage_account_name
              azure_file_url: https://storage_account_name.file.core.windows.net/azure_file_share_name
              credentials:
                account_key: 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000==
              relative_mount_path: azfiles
              file_mode: 0777
              directory_mode: 0777
          file_servers:
            - file_server:
                id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.BatchAI/fileservers/fileservercedd134b
              relative_mount_path: nfs
              mount_options: rw
      user_account_settings:
        admin_user_name: admin_user_name
        admin_user_ssh_public_key: ssh-rsa AAAAB3NzaC1yc...
        admin_user_password: admin_user_password
'''

RETURN = '''
id:
    description:
        - The ID of the resource
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/demo_resource_group/providers/Microsoft.BatchAI/clusters/demo_cluster
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


class AzureRMCluster(AzureRMModuleBase):
    """Configuration class for an Azure RM Cluster resource"""

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
            vm_size=dict(
                type='str'
            ),
            vm_priority=dict(
                type='str',
                choices=['dedicated',
                         'lowpriority']
            ),
            scale_settings=dict(
                type='dict',
                options=dict(
                    manual=dict(
                        type='dict',
                        options=dict(
                            target_node_count=dict(
                                type='int'
                            ),
                            node_deallocation_option=dict(
                                type='str',
                                choices=['requeue',
                                         'terminate',
                                         'waitforjobcompletion',
                                         'unknown']
                            )
                        )
                    ),
                    auto_scale=dict(
                        type='dict',
                        options=dict(
                            minimum_node_count=dict(
                                type='int'
                            ),
                            maximum_node_count=dict(
                                type='int'
                            ),
                            initial_node_count=dict(
                                type='int'
                            )
                        )
                    )
                )
            ),
            virtual_machine_configuration=dict(
                type='dict',
                options=dict(
                    image_reference=dict(
                        type='dict',
                        options=dict(
                            publisher=dict(
                                type='str'
                            ),
                            offer=dict(
                                type='str'
                            ),
                            sku=dict(
                                type='str'
                            ),
                            version=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            node_setup=dict(
                type='dict',
                options=dict(
                    setup_task=dict(
                        type='dict',
                        options=dict(
                            command_line=dict(
                                type='str'
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
                            run_elevated=dict(
                                type='str'
                            ),
                            std_out_err_path_prefix=dict(
                                type='str'
                            )
                        )
                    ),
                    mount_volumes=dict(
                        type='dict',
                        options=dict(
                            azure_file_shares=dict(
                                type='list',
                                options=dict(
                                    account_name=dict(
                                        type='str'
                                    ),
                                    azure_file_url=dict(
                                        type='str'
                                    ),
                                    credentials=dict(
                                        type='dict',
                                        options=dict(
                                            account_key=dict(
                                                type='str'
                                            ),
                                            account_key_secret_reference=dict(
                                                type='dict'
                                            )
                                        )
                                    ),
                                    relative_mount_path=dict(
                                        type='str'
                                    ),
                                    file_mode=dict(
                                        type='str'
                                    ),
                                    directory_mode=dict(
                                        type='str'
                                    )
                                )
                            ),
                            azure_blob_file_systems=dict(
                                type='list',
                                options=dict(
                                    account_name=dict(
                                        type='str'
                                    ),
                                    container_name=dict(
                                        type='str'
                                    ),
                                    credentials=dict(
                                        type='dict',
                                        options=dict(
                                            account_key=dict(
                                                type='str'
                                            ),
                                            account_key_secret_reference=dict(
                                                type='dict'
                                            )
                                        )
                                    ),
                                    relative_mount_path=dict(
                                        type='str'
                                    ),
                                    mount_options=dict(
                                        type='str'
                                    )
                                )
                            ),
                            file_servers=dict(
                                type='list',
                                options=dict(
                                    file_server=dict(
                                        type='dict',
                                        options=dict(
                                            id=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    source_directory=dict(
                                        type='str'
                                    ),
                                    relative_mount_path=dict(
                                        type='str'
                                    ),
                                    mount_options=dict(
                                        type='str'
                                    )
                                )
                            ),
                            unmanaged_file_systems=dict(
                                type='list',
                                options=dict(
                                    mount_command=dict(
                                        type='str'
                                    ),
                                    relative_mount_path=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            user_account_settings=dict(
                type='dict',
                options=dict(
                    admin_user_name=dict(
                        type='str'
                    ),
                    admin_user_ssh_public_key=dict(
                        type='str'
                    ),
                    admin_user_password=dict(
                        type='str',
                        no_log=True
                    )
                )
            ),
            subnet=dict(
                type='dict',
                options=dict(
                    id=dict(
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

        super(AzureRMCluster, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['node_setup', 'mount_volumes', 'file_servers', 'file_server', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.parameters, ['subnet', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BatchAIManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_cluster()

        if not old_response:
            self.log("Cluster instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Cluster instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Cluster instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_cluster()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Cluster instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_cluster()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Cluster instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_cluster(self):
        '''
        Creates or updates Cluster with the specified configuration.

        :return: deserialized Cluster instance state dictionary
        '''
        self.log("Creating / Updating the Cluster instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.clusters.create(resource_group_name=self.resource_group,
                                                            cluster_name=self.name,
                                                            parameters=self.parameters)
            else:
                response = self.mgmt_client.clusters.update(resource_group_name=self.resource_group,
                                                            cluster_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Cluster instance.')
            self.fail("Error creating the Cluster instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_cluster(self):
        '''
        Deletes specified Cluster instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Cluster instance {0}".format(self.name))
        try:
            response = self.mgmt_client.clusters.delete(resource_group_name=self.resource_group,
                                                        cluster_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Cluster instance.')
            self.fail("Error deleting the Cluster instance: {0}".format(str(e)))

        return True

    def get_cluster(self):
        '''
        Gets the properties of the specified Cluster.

        :return: deserialized Cluster instance state dictionary
        '''
        self.log("Checking if the Cluster instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.clusters.get(resource_group_name=self.resource_group,
                                                     cluster_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Cluster instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Cluster instance.')
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
            else:
                key = list(old[0])[0]
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
    AzureRMCluster()


if __name__ == '__main__':
    main()

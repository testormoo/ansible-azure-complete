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
short_description: Manage Cluster instance.
description:
    - Create, update and delete instance of Cluster.

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


class AzureRMClusters(AzureRMModuleBase):
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
                type='dict'
            ),
            virtual_machine_configuration=dict(
                type='dict'
            ),
            node_setup=dict(
                type='dict'
            ),
            user_account_settings=dict(
                type='dict'
            ),
            subnet=dict(
                type='dict'
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

        super(AzureRMClusters, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "vm_size":
                    self.parameters["vm_size"] = kwargs[key]
                elif key == "vm_priority":
                    self.parameters["vm_priority"] = kwargs[key]
                elif key == "scale_settings":
                    self.parameters["scale_settings"] = kwargs[key]
                elif key == "virtual_machine_configuration":
                    self.parameters["virtual_machine_configuration"] = kwargs[key]
                elif key == "node_setup":
                    self.parameters["node_setup"] = kwargs[key]
                elif key == "user_account_settings":
                    self.parameters["user_account_settings"] = kwargs[key]
                elif key == "subnet":
                    self.parameters["subnet"] = kwargs[key]

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
                if (not default_compare(self.parameters, old_response, '')):
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
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_cluster():
                time.sleep(20)
        else:
            self.log("Cluster instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
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

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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
    AzureRMClusters()


if __name__ == '__main__':
    main()

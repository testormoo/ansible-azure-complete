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
module: azure_rm_machinelearningcomputeoperationalizationcluster
version_added: "2.8"
short_description: Manage Operationalization Cluster instance.
description:
    - Create, update and delete instance of Operationalization Cluster.

options:
    resource_group:
        description:
            - Name of the resource group in which the cluster is located.
        required: True
    cluster_name:
        description:
            - The name of the cluster.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    description:
        description:
            - The description of the cluster.
    cluster_type:
        description:
            - The cluster type.
        required: True
        choices:
            - 'acs'
            - 'local'
    storage_account:
        description:
            - Storage Account properties.
        suboptions:
            resource_id:
                description:
                    - "ARM resource ID of the Azure Storage Account to store CLI specific files. If not provided one will be created. This cannot be changed
                       once the cluster is created."
    container_registry:
        description:
            - Container Registry properties.
        suboptions:
            resource_id:
                description:
                    - "ARM resource ID of the Azure Container Registry used to store Docker images for web services in the cluster. If not provided one will
                       be created. This cannot be changed once the cluster is created."
    container_service:
        description:
            - Parameters for the Azure Container Service cluster.
        suboptions:
            orchestrator_type:
                description:
                    - Type of orchestrator. It cannot be changed once the cluster is created.
                required: True
                choices:
                    - 'kubernetes'
                    - 'none'
            orchestrator_properties:
                description:
                    - Orchestrator specific properties
                suboptions:
                    service_principal:
                        description:
                            - The Azure Service Principal used by Kubernetes
                        suboptions:
                            client_id:
                                description:
                                    - The service principal client ID
                                required: True
                            secret:
                                description:
                                    - "The service principal secret. This is not returned in response of GET/PUT on the resource. To see this please call
                                       listKeys."
                                required: True
            system_services:
                description:
                    - The system services deployed to the cluster
                type: list
                suboptions:
                    system_service_type:
                        description:
                            - The system service type.
                        required: True
                        choices:
                            - 'none'
                            - 'scoring_front_end'
                            - 'batch_front_end'
            master_count:
                description:
                    - The number of master nodes in the container service.
            agent_count:
                description:
                    - The number of agent nodes in the Container Service. This can be changed to scale the cluster.
            agent_vm_size:
                description:
                    - "The Azure VM size of the agent VM nodes. This cannot be changed once the cluster is created. This list is non exhaustive; refer to
                       https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes for the possible VM sizes."
                choices:
                    - 'standard_a0'
                    - 'standard_a1'
                    - 'standard_a2'
                    - 'standard_a3'
                    - 'standard_a4'
                    - 'standard_a5'
                    - 'standard_a6'
                    - 'standard_a7'
                    - 'standard_a8'
                    - 'standard_a9'
                    - 'standard_a10'
                    - 'standard_a11'
                    - 'standard_d1'
                    - 'standard_d2'
                    - 'standard_d3'
                    - 'standard_d4'
                    - 'standard_d11'
                    - 'standard_d12'
                    - 'standard_d13'
                    - 'standard_d14'
                    - 'standard_d1_v2'
                    - 'standard_d2_v2'
                    - 'standard_d3_v2'
                    - 'standard_d4_v2'
                    - 'standard_d5_v2'
                    - 'standard_d11_v2'
                    - 'standard_d12_v2'
                    - 'standard_d13_v2'
                    - 'standard_d14_v2'
                    - 'standard_g1'
                    - 'standard_g2'
                    - 'standard_g3'
                    - 'standard_g4'
                    - 'standard_g5'
                    - 'standard_ds1'
                    - 'standard_ds2'
                    - 'standard_ds3'
                    - 'standard_ds4'
                    - 'standard_ds11'
                    - 'standard_ds12'
                    - 'standard_ds13'
                    - 'standard_ds14'
                    - 'standard_gs1'
                    - 'standard_gs2'
                    - 'standard_gs3'
                    - 'standard_gs4'
                    - 'standard_gs5'
    app_insights:
        description:
            - AppInsights configuration.
        suboptions:
            resource_id:
                description:
                    - ARM resource ID of the App Insights.
    global_service_configuration:
        description:
            - Contains global configuration for the web services in the cluster.
        suboptions:
            additional_properties:
                description:
                    - Unmatched properties from the message are deserialized this collection
            etag:
                description:
                    - The configuartion ETag for updates.
            ssl:
                description:
                    - The SSL configuration properties
                suboptions:
                    status:
                        description:
                            - SSL status. Allowed values are C(enabled) and C(disabled).
                        choices:
                            - 'enabled'
                            - 'disabled'
                    cert:
                        description:
                            - The SSL cert data in PEM format.
                    key:
                        description:
                            - The SSL key data in PEM format. This is not returned in response of GET/PUT on the resource. To see this please call listKeys API.
                    cname:
                        description:
                            - The CName of the certificate.
            service_auth:
                description:
                    - Optional global authorization keys for all user services deployed in cluster. These are used if the service does not have auth keys.
                suboptions:
                    primary_auth_key_hash:
                        description:
                            - The primary auth key hash. This is not returned in response of GET/PUT on the resource.. To see this please call listKeys API.
                        required: True
                    secondary_auth_key_hash:
                        description:
                            - The secondary auth key hash. This is not returned in response of GET/PUT on the resource.. To see this please call listKeys API.
                        required: True
            auto_scale:
                description:
                    - The auto-scale configuration
                suboptions:
                    status:
                        description:
                            - If auto-scale is C(enabled) for all services. Each service can turn it off individually.
                        choices:
                            - 'enabled'
                            - 'disabled'
                    min_replicas:
                        description:
                            - The minimum number of replicas for each service.
                    max_replicas:
                        description:
                            - The maximum number of replicas for each service.
                    target_utilization:
                        description:
                            - The target utilization.
                    refresh_period_in_seconds:
                        description:
                            - Refresh period in seconds.
    state:
      description:
        - Assert the state of the Operationalization Cluster.
        - Use 'present' to create or update an Operationalization Cluster and 'absent' to delete it.
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
  - name: Create (or update) Operationalization Cluster
    azure_rm_machinelearningcomputeoperationalizationcluster:
      resource_group: myResourceGroup
      cluster_name: myCluster
      location: eastus
'''

RETURN = '''
id:
    description:
        - Specifies the resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.MachineLearningCompute/operationalization
            Clusters/myCluster"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.machinelearningcompute import MachineLearningComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOperationalizationClusters(AzureRMModuleBase):
    """Configuration class for an Azure RM Operationalization Cluster resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            cluster_type=dict(
                type='str',
                choices=['acs',
                         'local'],
                required=True
            ),
            storage_account=dict(
                type='dict'
            ),
            container_registry=dict(
                type='dict'
            ),
            container_service=dict(
                type='dict'
            ),
            app_insights=dict(
                type='dict'
            ),
            global_service_configuration=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.cluster_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMOperationalizationClusters, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "cluster_type":
                    ev = kwargs[key]
                    if ev == 'acs':
                        ev = 'ACS'
                    self.parameters["cluster_type"] = _snake_to_camel(ev, True)
                elif key == "storage_account":
                    self.parameters["storage_account"] = kwargs[key]
                elif key == "container_registry":
                    self.parameters["container_registry"] = kwargs[key]
                elif key == "container_service":
                    ev = kwargs[key]
                    if 'orchestrator_type' in ev:
                        if ev['orchestrator_type'] == 'kubernetes':
                            ev['orchestrator_type'] = 'Kubernetes'
                        elif ev['orchestrator_type'] == 'none':
                            ev['orchestrator_type'] = 'None'
                    if 'agent_vm_size' in ev:
                        if ev['agent_vm_size'] == 'standard_a0':
                            ev['agent_vm_size'] = 'Standard_A0'
                        elif ev['agent_vm_size'] == 'standard_a1':
                            ev['agent_vm_size'] = 'Standard_A1'
                        elif ev['agent_vm_size'] == 'standard_a2':
                            ev['agent_vm_size'] = 'Standard_A2'
                        elif ev['agent_vm_size'] == 'standard_a3':
                            ev['agent_vm_size'] = 'Standard_A3'
                        elif ev['agent_vm_size'] == 'standard_a4':
                            ev['agent_vm_size'] = 'Standard_A4'
                        elif ev['agent_vm_size'] == 'standard_a5':
                            ev['agent_vm_size'] = 'Standard_A5'
                        elif ev['agent_vm_size'] == 'standard_a6':
                            ev['agent_vm_size'] = 'Standard_A6'
                        elif ev['agent_vm_size'] == 'standard_a7':
                            ev['agent_vm_size'] = 'Standard_A7'
                        elif ev['agent_vm_size'] == 'standard_a8':
                            ev['agent_vm_size'] = 'Standard_A8'
                        elif ev['agent_vm_size'] == 'standard_a9':
                            ev['agent_vm_size'] = 'Standard_A9'
                        elif ev['agent_vm_size'] == 'standard_a10':
                            ev['agent_vm_size'] = 'Standard_A10'
                        elif ev['agent_vm_size'] == 'standard_a11':
                            ev['agent_vm_size'] = 'Standard_A11'
                        elif ev['agent_vm_size'] == 'standard_d1':
                            ev['agent_vm_size'] = 'Standard_D1'
                        elif ev['agent_vm_size'] == 'standard_d2':
                            ev['agent_vm_size'] = 'Standard_D2'
                        elif ev['agent_vm_size'] == 'standard_d3':
                            ev['agent_vm_size'] = 'Standard_D3'
                        elif ev['agent_vm_size'] == 'standard_d4':
                            ev['agent_vm_size'] = 'Standard_D4'
                        elif ev['agent_vm_size'] == 'standard_d11':
                            ev['agent_vm_size'] = 'Standard_D11'
                        elif ev['agent_vm_size'] == 'standard_d12':
                            ev['agent_vm_size'] = 'Standard_D12'
                        elif ev['agent_vm_size'] == 'standard_d13':
                            ev['agent_vm_size'] = 'Standard_D13'
                        elif ev['agent_vm_size'] == 'standard_d14':
                            ev['agent_vm_size'] = 'Standard_D14'
                        elif ev['agent_vm_size'] == 'standard_d1_v2':
                            ev['agent_vm_size'] = 'Standard_D1_v2'
                        elif ev['agent_vm_size'] == 'standard_d2_v2':
                            ev['agent_vm_size'] = 'Standard_D2_v2'
                        elif ev['agent_vm_size'] == 'standard_d3_v2':
                            ev['agent_vm_size'] = 'Standard_D3_v2'
                        elif ev['agent_vm_size'] == 'standard_d4_v2':
                            ev['agent_vm_size'] = 'Standard_D4_v2'
                        elif ev['agent_vm_size'] == 'standard_d5_v2':
                            ev['agent_vm_size'] = 'Standard_D5_v2'
                        elif ev['agent_vm_size'] == 'standard_d11_v2':
                            ev['agent_vm_size'] = 'Standard_D11_v2'
                        elif ev['agent_vm_size'] == 'standard_d12_v2':
                            ev['agent_vm_size'] = 'Standard_D12_v2'
                        elif ev['agent_vm_size'] == 'standard_d13_v2':
                            ev['agent_vm_size'] = 'Standard_D13_v2'
                        elif ev['agent_vm_size'] == 'standard_d14_v2':
                            ev['agent_vm_size'] = 'Standard_D14_v2'
                        elif ev['agent_vm_size'] == 'standard_g1':
                            ev['agent_vm_size'] = 'Standard_G1'
                        elif ev['agent_vm_size'] == 'standard_g2':
                            ev['agent_vm_size'] = 'Standard_G2'
                        elif ev['agent_vm_size'] == 'standard_g3':
                            ev['agent_vm_size'] = 'Standard_G3'
                        elif ev['agent_vm_size'] == 'standard_g4':
                            ev['agent_vm_size'] = 'Standard_G4'
                        elif ev['agent_vm_size'] == 'standard_g5':
                            ev['agent_vm_size'] = 'Standard_G5'
                        elif ev['agent_vm_size'] == 'standard_ds1':
                            ev['agent_vm_size'] = 'Standard_DS1'
                        elif ev['agent_vm_size'] == 'standard_ds2':
                            ev['agent_vm_size'] = 'Standard_DS2'
                        elif ev['agent_vm_size'] == 'standard_ds3':
                            ev['agent_vm_size'] = 'Standard_DS3'
                        elif ev['agent_vm_size'] == 'standard_ds4':
                            ev['agent_vm_size'] = 'Standard_DS4'
                        elif ev['agent_vm_size'] == 'standard_ds11':
                            ev['agent_vm_size'] = 'Standard_DS11'
                        elif ev['agent_vm_size'] == 'standard_ds12':
                            ev['agent_vm_size'] = 'Standard_DS12'
                        elif ev['agent_vm_size'] == 'standard_ds13':
                            ev['agent_vm_size'] = 'Standard_DS13'
                        elif ev['agent_vm_size'] == 'standard_ds14':
                            ev['agent_vm_size'] = 'Standard_DS14'
                        elif ev['agent_vm_size'] == 'standard_gs1':
                            ev['agent_vm_size'] = 'Standard_GS1'
                        elif ev['agent_vm_size'] == 'standard_gs2':
                            ev['agent_vm_size'] = 'Standard_GS2'
                        elif ev['agent_vm_size'] == 'standard_gs3':
                            ev['agent_vm_size'] = 'Standard_GS3'
                        elif ev['agent_vm_size'] == 'standard_gs4':
                            ev['agent_vm_size'] = 'Standard_GS4'
                        elif ev['agent_vm_size'] == 'standard_gs5':
                            ev['agent_vm_size'] = 'Standard_GS5'
                    self.parameters["container_service"] = ev
                elif key == "app_insights":
                    self.parameters["app_insights"] = kwargs[key]
                elif key == "global_service_configuration":
                    self.parameters["global_service_configuration"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MachineLearningComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_operationalizationcluster()

        if not old_response:
            self.log("Operationalization Cluster instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Operationalization Cluster instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Operationalization Cluster instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Operationalization Cluster instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_operationalizationcluster()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Operationalization Cluster instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_operationalizationcluster()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_operationalizationcluster():
                time.sleep(20)
        else:
            self.log("Operationalization Cluster instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_operationalizationcluster(self):
        '''
        Creates or updates Operationalization Cluster with the specified configuration.

        :return: deserialized Operationalization Cluster instance state dictionary
        '''
        self.log("Creating / Updating the Operationalization Cluster instance {0}".format(self.cluster_name))

        try:
            response = self.mgmt_client.operationalization_clusters.create_or_update(resource_group_name=self.resource_group,
                                                                                     cluster_name=self.cluster_name,
                                                                                     parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Operationalization Cluster instance.')
            self.fail("Error creating the Operationalization Cluster instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_operationalizationcluster(self):
        '''
        Deletes specified Operationalization Cluster instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Operationalization Cluster instance {0}".format(self.cluster_name))
        try:
            response = self.mgmt_client.operationalization_clusters.delete(resource_group_name=self.resource_group,
                                                                           cluster_name=self.cluster_name)
        except CloudError as e:
            self.log('Error attempting to delete the Operationalization Cluster instance.')
            self.fail("Error deleting the Operationalization Cluster instance: {0}".format(str(e)))

        return True

    def get_operationalizationcluster(self):
        '''
        Gets the properties of the specified Operationalization Cluster.

        :return: deserialized Operationalization Cluster instance state dictionary
        '''
        self.log("Checking if the Operationalization Cluster instance {0} is present".format(self.cluster_name))
        found = False
        try:
            response = self.mgmt_client.operationalization_clusters.get(resource_group_name=self.resource_group,
                                                                        cluster_name=self.cluster_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Operationalization Cluster instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Operationalization Cluster instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMOperationalizationClusters()


if __name__ == '__main__':
    main()

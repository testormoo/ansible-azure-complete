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
short_description: Manage Azure Operationalization Cluster instance.
description:
    - Create, update and delete instance of Azure Operationalization Cluster.

options:
    resource_group:
        description:
            - Name of the resource group in which the cluster is located.
        required: True
    name:
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
            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
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
                                    - Required when C(state) is I(present).
                            secret:
                                description:
                                    - "The service principal secret. This is not returned in response of GET/PUT on the resource. To see this please call
                                       listKeys."
                                    - Required when C(state) is I(present).
            system_services:
                description:
                    - The system services deployed to the cluster
                type: list
                suboptions:
                    system_service_type:
                        description:
                            - The system service type.
                            - Required when C(state) is I(present).
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
            ssl:
                description:
                    - The SSL configuration properties
                suboptions:
                    status:
                        description:
                            - "SSL status. Allowed values are Enabled and Disabled. Possible values include: 'Enabled', 'Disabled'"
                        type: bool
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
                            - Required when C(state) is I(present).
                    secondary_auth_key_hash:
                        description:
                            - The secondary auth key hash. This is not returned in response of GET/PUT on the resource.. To see this please call listKeys API.
                            - Required when C(state) is I(present).
            auto_scale:
                description:
                    - The auto-scale configuration
                suboptions:
                    status:
                        description:
                            - "If auto-scale is enabled for all services. Each service can turn it off individually. Possible values include: 'Enabled',
                               'Disabled'"
                        type: bool
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
      name: myCluster
      location: eastus
      description: My Operationalization Cluster
      cluster_type: ACS
      container_service:
        orchestrator_type: Kubernetes
        orchestrator_properties:
          service_principal:
            client_id: abcdefghijklmnopqrt
            secret: uiuiwueiwuewiue
      global_service_configuration:
        ssl:
          status: status
          cert: afjdklq2131casfakld=
          key: flksdafkldsajf=
          cname: foo.bar.com
        auto_scale:
          status: status
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


class AzureRMOperationalizationCluster(AzureRMModuleBase):
    """Configuration class for an Azure RM Operationalization Cluster resource"""

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
            description=dict(
                type='str'
            ),
            cluster_type=dict(
                type='str',
                choices=['acs',
                         'local']
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMOperationalizationCluster, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                supports_check_mode=True,
                                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['cluster_type'], True)
        dict_map(self.parameters, ['cluster_type'], ''acs': 'ACS'')
        dict_camelize(self.parameters, ['container_service', 'orchestrator_type'], True)
        dict_camelize(self.parameters, ['container_service', 'system_services', 'system_service_type'], True)
        dict_camelize(self.parameters, ['container_service', 'agent_vm_size'], True)
        dict_map(self.parameters, ['container_service', 'agent_vm_size'], ''standard_a0': 'Standard_A0', 'standard_a1': 'Standard_A1', 'standard_a2': 'Standard_A2', 'standard_a3': 'Standard_A3', 'standard_a4': 'Standard_A4', 'standard_a5': 'Standard_A5', 'standard_a6': 'Standard_A6', 'standard_a7': 'Standard_A7', 'standard_a8': 'Standard_A8', 'standard_a9': 'Standard_A9', 'standard_a10': 'Standard_A10', 'standard_a11': 'Standard_A11', 'standard_d1': 'Standard_D1', 'standard_d2': 'Standard_D2', 'standard_d3': 'Standard_D3', 'standard_d4': 'Standard_D4', 'standard_d11': 'Standard_D11', 'standard_d12': 'Standard_D12', 'standard_d13': 'Standard_D13', 'standard_d14': 'Standard_D14', 'standard_d1_v2': 'Standard_D1_v2', 'standard_d2_v2': 'Standard_D2_v2', 'standard_d3_v2': 'Standard_D3_v2', 'standard_d4_v2': 'Standard_D4_v2', 'standard_d5_v2': 'Standard_D5_v2', 'standard_d11_v2': 'Standard_D11_v2', 'standard_d12_v2': 'Standard_D12_v2', 'standard_d13_v2': 'Standard_D13_v2', 'standard_d14_v2': 'Standard_D14_v2', 'standard_g1': 'Standard_G1', 'standard_g2': 'Standard_G2', 'standard_g3': 'Standard_G3', 'standard_g4': 'Standard_G4', 'standard_g5': 'Standard_G5', 'standard_ds1': 'Standard_DS1', 'standard_ds2': 'Standard_DS2', 'standard_ds3': 'Standard_DS3', 'standard_ds4': 'Standard_DS4', 'standard_ds11': 'Standard_DS11', 'standard_ds12': 'Standard_DS12', 'standard_ds13': 'Standard_DS13', 'standard_ds14': 'Standard_DS14', 'standard_gs1': 'Standard_GS1', 'standard_gs2': 'Standard_GS2', 'standard_gs3': 'Standard_GS3', 'standard_gs4': 'Standard_GS4', 'standard_gs5': 'Standard_GS5'')
        dict_map(self.parameters, ['global_service_configuration', 'ssl', 'status'], '{True: 'Enabled', False: 'Disabled'}')
        dict_map(self.parameters, ['global_service_configuration', 'auto_scale', 'status'], '{True: 'Enabled', False: 'Disabled'}')

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Operationalization Cluster instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_operationalizationcluster()

            self.results['changed'] = True
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
            self.results.update(self.format_response(response))
        return self.results

    def create_update_operationalizationcluster(self):
        '''
        Creates or updates Operationalization Cluster with the specified configuration.

        :return: deserialized Operationalization Cluster instance state dictionary
        '''
        self.log("Creating / Updating the Operationalization Cluster instance {0}".format(self.name))

        try:
            response = self.mgmt_client.operationalization_clusters.create_or_update(resource_group_name=self.resource_group,
                                                                                     cluster_name=self.name,
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
        self.log("Deleting the Operationalization Cluster instance {0}".format(self.name))
        try:
            response = self.mgmt_client.operationalization_clusters.delete(resource_group_name=self.resource_group,
                                                                           cluster_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Operationalization Cluster instance.')
            self.fail("Error deleting the Operationalization Cluster instance: {0}".format(str(e)))

        return True

    def get_operationalizationcluster(self):
        '''
        Gets the properties of the specified Operationalization Cluster.

        :return: deserialized Operationalization Cluster instance state dictionary
        '''
        self.log("Checking if the Operationalization Cluster instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.operationalization_clusters.get(resource_group_name=self.resource_group,
                                                                        cluster_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Operationalization Cluster instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Operationalization Cluster instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


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


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMOperationalizationCluster()


if __name__ == '__main__':
    main()

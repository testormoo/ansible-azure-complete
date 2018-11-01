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
module: azure_rm_computecontainerservice
version_added: "2.8"
short_description: Manage Container Service instance.
description:
    - Create, update and delete instance of Container Service.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    container_service_name:
        description:
            - The name of the container service in the specified subscription and resource group.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    orchestrator_profile:
        description:
            - Properties of the orchestrator.
        suboptions:
            orchestrator_type:
                description:
                    - The orchestrator to use to manage container service cluster resources. Valid values are C(swarm), C(dcos), and C(custom).
                required: True
                choices:
                    - 'swarm'
                    - 'dcos'
                    - 'custom'
                    - 'kubernetes'
    custom_profile:
        description:
            - Properties for custom clusters.
        suboptions:
            orchestrator:
                description:
                    - The name of the custom orchestrator to use.
                required: True
    service_principal_profile:
        description:
            - Properties for cluster service principals.
        suboptions:
            client_id:
                description:
                    - The ID for the service principal.
                required: True
            secret:
                description:
                    - The secret password associated with the service principal.
                required: True
    master_profile:
        description:
            - Properties of master agents.
        required: True
        suboptions:
            count:
                description:
                    - Number of masters (VMs) in the container service cluster. Allowed values are 1, 3, and 5. The default value is 1.
            dns_prefix:
                description:
                    - DNS prefix to be used to create the FQDN for master.
                required: True
    agent_pool_profiles:
        description:
            - Properties of the agent pool.
        required: True
        type: list
        suboptions:
            name:
                description:
                    - Unique name of the agent pool profile in the context of the subscription and resource group.
                required: True
            count:
                description:
                    - Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1.
                required: True
            vm_size:
                description:
                    - Size of agent VMs.
                required: True
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
            dns_prefix:
                description:
                    - DNS prefix to be used to create the FQDN for the agent pool.
                required: True
    windows_profile:
        description:
            - Properties of Windows VMs.
        suboptions:
            admin_username:
                description:
                    - The administrator username to use for Windows VMs.
                required: True
            admin_password:
                description:
                    - The administrator password to use for Windows VMs.
                required: True
    linux_profile:
        description:
            - Properties of Linux VMs.
        required: True
        suboptions:
            admin_username:
                description:
                    - The administrator username to use for Linux VMs.
                required: True
            ssh:
                description:
                    - The ssh key configuration for Linux VMs.
                required: True
                suboptions:
                    public_keys:
                        description:
                            - the list of SSH public keys used to authenticate with Linux-based VMs.
                        required: True
                        type: list
                        suboptions:
                            key_data:
                                description:
                                    - "Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or
                                       without headers."
                                required: True
    diagnostics_profile:
        description:
            - Properties of the diagnostic agent.
        suboptions:
            vm_diagnostics:
                description:
                    - Profile for the container service VM diagnostic agent.
                required: True
                suboptions:
                    enabled:
                        description:
                            - Whether the VM diagnostic agent is provisioned on the VM.
                        required: True
    state:
      description:
        - Assert the state of the Container Service.
        - Use 'present' to create or update an Container Service and 'absent' to delete it.
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
  - name: Create (or update) Container Service
    azure_rm_computecontainerservice:
      resource_group: rg1
      container_service_name: acs1
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/subid1/resourceGroups/rg1/providers/Microsoft.ContainerService/containerServices/acs1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMContainerServices(AzureRMModuleBase):
    """Configuration class for an Azure RM Container Service resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            container_service_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            orchestrator_profile=dict(
                type='dict'
            ),
            custom_profile=dict(
                type='dict'
            ),
            service_principal_profile=dict(
                type='dict'
            ),
            master_profile=dict(
                type='dict',
                required=True
            ),
            agent_pool_profiles=dict(
                type='list',
                required=True
            ),
            windows_profile=dict(
                type='dict'
            ),
            linux_profile=dict(
                type='dict',
                required=True
            ),
            diagnostics_profile=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.container_service_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMContainerServices, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "orchestrator_profile":
                    ev = kwargs[key]
                    if 'orchestrator_type' in ev:
                        if ev['orchestrator_type'] == 'swarm':
                            ev['orchestrator_type'] = 'Swarm'
                        elif ev['orchestrator_type'] == 'dcos':
                            ev['orchestrator_type'] = 'DCOS'
                        elif ev['orchestrator_type'] == 'custom':
                            ev['orchestrator_type'] = 'Custom'
                        elif ev['orchestrator_type'] == 'kubernetes':
                            ev['orchestrator_type'] = 'Kubernetes'
                    self.parameters["orchestrator_profile"] = ev
                elif key == "custom_profile":
                    self.parameters["custom_profile"] = kwargs[key]
                elif key == "service_principal_profile":
                    self.parameters["service_principal_profile"] = kwargs[key]
                elif key == "master_profile":
                    self.parameters["master_profile"] = kwargs[key]
                elif key == "agent_pool_profiles":
                    ev = kwargs[key]
                    if 'vm_size' in ev:
                        if ev['vm_size'] == 'standard_a0':
                            ev['vm_size'] = 'Standard_A0'
                        elif ev['vm_size'] == 'standard_a1':
                            ev['vm_size'] = 'Standard_A1'
                        elif ev['vm_size'] == 'standard_a2':
                            ev['vm_size'] = 'Standard_A2'
                        elif ev['vm_size'] == 'standard_a3':
                            ev['vm_size'] = 'Standard_A3'
                        elif ev['vm_size'] == 'standard_a4':
                            ev['vm_size'] = 'Standard_A4'
                        elif ev['vm_size'] == 'standard_a5':
                            ev['vm_size'] = 'Standard_A5'
                        elif ev['vm_size'] == 'standard_a6':
                            ev['vm_size'] = 'Standard_A6'
                        elif ev['vm_size'] == 'standard_a7':
                            ev['vm_size'] = 'Standard_A7'
                        elif ev['vm_size'] == 'standard_a8':
                            ev['vm_size'] = 'Standard_A8'
                        elif ev['vm_size'] == 'standard_a9':
                            ev['vm_size'] = 'Standard_A9'
                        elif ev['vm_size'] == 'standard_a10':
                            ev['vm_size'] = 'Standard_A10'
                        elif ev['vm_size'] == 'standard_a11':
                            ev['vm_size'] = 'Standard_A11'
                        elif ev['vm_size'] == 'standard_d1':
                            ev['vm_size'] = 'Standard_D1'
                        elif ev['vm_size'] == 'standard_d2':
                            ev['vm_size'] = 'Standard_D2'
                        elif ev['vm_size'] == 'standard_d3':
                            ev['vm_size'] = 'Standard_D3'
                        elif ev['vm_size'] == 'standard_d4':
                            ev['vm_size'] = 'Standard_D4'
                        elif ev['vm_size'] == 'standard_d11':
                            ev['vm_size'] = 'Standard_D11'
                        elif ev['vm_size'] == 'standard_d12':
                            ev['vm_size'] = 'Standard_D12'
                        elif ev['vm_size'] == 'standard_d13':
                            ev['vm_size'] = 'Standard_D13'
                        elif ev['vm_size'] == 'standard_d14':
                            ev['vm_size'] = 'Standard_D14'
                        elif ev['vm_size'] == 'standard_d1_v2':
                            ev['vm_size'] = 'Standard_D1_v2'
                        elif ev['vm_size'] == 'standard_d2_v2':
                            ev['vm_size'] = 'Standard_D2_v2'
                        elif ev['vm_size'] == 'standard_d3_v2':
                            ev['vm_size'] = 'Standard_D3_v2'
                        elif ev['vm_size'] == 'standard_d4_v2':
                            ev['vm_size'] = 'Standard_D4_v2'
                        elif ev['vm_size'] == 'standard_d5_v2':
                            ev['vm_size'] = 'Standard_D5_v2'
                        elif ev['vm_size'] == 'standard_d11_v2':
                            ev['vm_size'] = 'Standard_D11_v2'
                        elif ev['vm_size'] == 'standard_d12_v2':
                            ev['vm_size'] = 'Standard_D12_v2'
                        elif ev['vm_size'] == 'standard_d13_v2':
                            ev['vm_size'] = 'Standard_D13_v2'
                        elif ev['vm_size'] == 'standard_d14_v2':
                            ev['vm_size'] = 'Standard_D14_v2'
                        elif ev['vm_size'] == 'standard_g1':
                            ev['vm_size'] = 'Standard_G1'
                        elif ev['vm_size'] == 'standard_g2':
                            ev['vm_size'] = 'Standard_G2'
                        elif ev['vm_size'] == 'standard_g3':
                            ev['vm_size'] = 'Standard_G3'
                        elif ev['vm_size'] == 'standard_g4':
                            ev['vm_size'] = 'Standard_G4'
                        elif ev['vm_size'] == 'standard_g5':
                            ev['vm_size'] = 'Standard_G5'
                        elif ev['vm_size'] == 'standard_ds1':
                            ev['vm_size'] = 'Standard_DS1'
                        elif ev['vm_size'] == 'standard_ds2':
                            ev['vm_size'] = 'Standard_DS2'
                        elif ev['vm_size'] == 'standard_ds3':
                            ev['vm_size'] = 'Standard_DS3'
                        elif ev['vm_size'] == 'standard_ds4':
                            ev['vm_size'] = 'Standard_DS4'
                        elif ev['vm_size'] == 'standard_ds11':
                            ev['vm_size'] = 'Standard_DS11'
                        elif ev['vm_size'] == 'standard_ds12':
                            ev['vm_size'] = 'Standard_DS12'
                        elif ev['vm_size'] == 'standard_ds13':
                            ev['vm_size'] = 'Standard_DS13'
                        elif ev['vm_size'] == 'standard_ds14':
                            ev['vm_size'] = 'Standard_DS14'
                        elif ev['vm_size'] == 'standard_gs1':
                            ev['vm_size'] = 'Standard_GS1'
                        elif ev['vm_size'] == 'standard_gs2':
                            ev['vm_size'] = 'Standard_GS2'
                        elif ev['vm_size'] == 'standard_gs3':
                            ev['vm_size'] = 'Standard_GS3'
                        elif ev['vm_size'] == 'standard_gs4':
                            ev['vm_size'] = 'Standard_GS4'
                        elif ev['vm_size'] == 'standard_gs5':
                            ev['vm_size'] = 'Standard_GS5'
                    self.parameters["agent_pool_profiles"] = ev
                elif key == "windows_profile":
                    self.parameters["windows_profile"] = kwargs[key]
                elif key == "linux_profile":
                    self.parameters["linux_profile"] = kwargs[key]
                elif key == "diagnostics_profile":
                    self.parameters["diagnostics_profile"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_containerservice()

        if not old_response:
            self.log("Container Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Container Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Container Service instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Container Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_containerservice()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Container Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_containerservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_containerservice():
                time.sleep(20)
        else:
            self.log("Container Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_containerservice(self):
        '''
        Creates or updates Container Service with the specified configuration.

        :return: deserialized Container Service instance state dictionary
        '''
        self.log("Creating / Updating the Container Service instance {0}".format(self.container_service_name))

        try:
            response = self.mgmt_client.container_services.create_or_update(resource_group_name=self.resource_group,
                                                                            container_service_name=self.container_service_name,
                                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Container Service instance.')
            self.fail("Error creating the Container Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_containerservice(self):
        '''
        Deletes specified Container Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Container Service instance {0}".format(self.container_service_name))
        try:
            response = self.mgmt_client.container_services.delete(resource_group_name=self.resource_group,
                                                                  container_service_name=self.container_service_name)
        except CloudError as e:
            self.log('Error attempting to delete the Container Service instance.')
            self.fail("Error deleting the Container Service instance: {0}".format(str(e)))

        return True

    def get_containerservice(self):
        '''
        Gets the properties of the specified Container Service.

        :return: deserialized Container Service instance state dictionary
        '''
        self.log("Checking if the Container Service instance {0} is present".format(self.container_service_name))
        found = False
        try:
            response = self.mgmt_client.container_services.get(resource_group_name=self.resource_group,
                                                               container_service_name=self.container_service_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Container Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Container Service instance.')
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
    AzureRMContainerServices()


if __name__ == '__main__':
    main()

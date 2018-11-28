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
short_description: Manage Azure Container Service instance.
description:
    - Create, update and delete instance of Azure Container Service.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
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
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
    service_principal_profile:
        description:
            - Properties for cluster service principals.
        suboptions:
            client_id:
                description:
                    - The ID for the service principal.
                    - Required when C(state) is I(present).
            secret:
                description:
                    - The secret password associated with the service principal.
                    - Required when C(state) is I(present).
    master_profile:
        description:
            - Properties of master agents.
            - Required when C(state) is I(present).
        suboptions:
            count:
                description:
                    - Number of masters (VMs) in the container service cluster. Allowed values are 1, 3, and 5. The default value is 1.
            dns_prefix:
                description:
                    - DNS prefix to be used to create the FQDN for master.
                    - Required when C(state) is I(present).
    agent_pool_profiles:
        description:
            - Properties of the agent pool.
            - Required when C(state) is I(present).
        type: list
        suboptions:
            name:
                description:
                    - Unique name of the agent pool profile in the context of the subscription and resource group.
                    - Required when C(state) is I(present).
            count:
                description:
                    - Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1.
                    - Required when C(state) is I(present).
            vm_size:
                description:
                    - Size of agent VMs.
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
    windows_profile:
        description:
            - Properties of Windows VMs.
        suboptions:
            admin_username:
                description:
                    - The administrator username to use for Windows VMs.
                    - Required when C(state) is I(present).
            admin_password:
                description:
                    - The administrator password to use for Windows VMs.
                    - Required when C(state) is I(present).
    linux_profile:
        description:
            - Properties of Linux VMs.
            - Required when C(state) is I(present).
        suboptions:
            admin_username:
                description:
                    - The administrator username to use for Linux VMs.
                    - Required when C(state) is I(present).
            ssh:
                description:
                    - The ssh key configuration for Linux VMs.
                    - Required when C(state) is I(present).
                suboptions:
                    public_keys:
                        description:
                            - the list of SSH public keys used to authenticate with Linux-based VMs.
                            - Required when C(state) is I(present).
                        type: list
                        suboptions:
                            key_data:
                                description:
                                    - "Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or
                                       without headers."
                                    - Required when C(state) is I(present).
    diagnostics_profile:
        description:
            - Properties of the diagnostic agent.
        suboptions:
            vm_diagnostics:
                description:
                    - Profile for the container service VM diagnostic agent.
                    - Required when C(state) is I(present).
                suboptions:
                    enabled:
                        description:
                            - Whether the VM diagnostic agent is provisioned on the VM.
                            - Required when C(state) is I(present).
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
      name: acs1
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMContainerService(AzureRMModuleBase):
    """Configuration class for an Azure RM Container Service resource"""

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
            orchestrator_profile=dict(
                type='dict'
                options=dict(
                    orchestrator_type=dict(
                        type='str',
                        choices=['swarm',
                                 'dcos',
                                 'custom',
                                 'kubernetes']
                    )
                )
            ),
            custom_profile=dict(
                type='dict'
                options=dict(
                    orchestrator=dict(
                        type='str'
                    )
                )
            ),
            service_principal_profile=dict(
                type='dict'
                options=dict(
                    client_id=dict(
                        type='str'
                    ),
                    secret=dict(
                        type='str'
                    )
                )
            ),
            master_profile=dict(
                type='dict'
                options=dict(
                    count=dict(
                        type='int'
                    ),
                    dns_prefix=dict(
                        type='str'
                    )
                )
            ),
            agent_pool_profiles=dict(
                type='list'
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    count=dict(
                        type='int'
                    ),
                    vm_size=dict(
                        type='str',
                        choices=['standard_a0',
                                 'standard_a1',
                                 'standard_a2',
                                 'standard_a3',
                                 'standard_a4',
                                 'standard_a5',
                                 'standard_a6',
                                 'standard_a7',
                                 'standard_a8',
                                 'standard_a9',
                                 'standard_a10',
                                 'standard_a11',
                                 'standard_d1',
                                 'standard_d2',
                                 'standard_d3',
                                 'standard_d4',
                                 'standard_d11',
                                 'standard_d12',
                                 'standard_d13',
                                 'standard_d14',
                                 'standard_d1_v2',
                                 'standard_d2_v2',
                                 'standard_d3_v2',
                                 'standard_d4_v2',
                                 'standard_d5_v2',
                                 'standard_d11_v2',
                                 'standard_d12_v2',
                                 'standard_d13_v2',
                                 'standard_d14_v2',
                                 'standard_g1',
                                 'standard_g2',
                                 'standard_g3',
                                 'standard_g4',
                                 'standard_g5',
                                 'standard_ds1',
                                 'standard_ds2',
                                 'standard_ds3',
                                 'standard_ds4',
                                 'standard_ds11',
                                 'standard_ds12',
                                 'standard_ds13',
                                 'standard_ds14',
                                 'standard_gs1',
                                 'standard_gs2',
                                 'standard_gs3',
                                 'standard_gs4',
                                 'standard_gs5']
                    ),
                    dns_prefix=dict(
                        type='str'
                    )
                )
            ),
            windows_profile=dict(
                type='dict'
                options=dict(
                    admin_username=dict(
                        type='str'
                    ),
                    admin_password=dict(
                        type='str',
                        no_log=True
                    )
                )
            ),
            linux_profile=dict(
                type='dict'
                options=dict(
                    admin_username=dict(
                        type='str'
                    ),
                    ssh=dict(
                        type='dict'
                        options=dict(
                            public_keys=dict(
                                type='list'
                                options=dict(
                                    key_data=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            diagnostics_profile=dict(
                type='dict'
                options=dict(
                    vm_diagnostics=dict(
                        type='dict'
                        options=dict(
                            enabled=dict(
                                type='str'
                            )
                        )
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

        super(AzureRMContainerService, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['orchestrator_profile', 'orchestrator_type'], True)
        dict_map(self.parameters, ['orchestrator_profile', 'orchestrator_type'], {'dcos': 'DCOS'})
        dict_camelize(self.parameters, ['agent_pool_profiles', 'vm_size'], True)
        dict_map(self.parameters, ['agent_pool_profiles', 'vm_size'], {'standard_a0': 'Standard_A0', 'standard_a1': 'Standard_A1', 'standard_a2': 'Standard_A2', 'standard_a3': 'Standard_A3', 'standard_a4': 'Standard_A4', 'standard_a5': 'Standard_A5', 'standard_a6': 'Standard_A6', 'standard_a7': 'Standard_A7', 'standard_a8': 'Standard_A8', 'standard_a9': 'Standard_A9', 'standard_a10': 'Standard_A10', 'standard_a11': 'Standard_A11', 'standard_d1': 'Standard_D1', 'standard_d2': 'Standard_D2', 'standard_d3': 'Standard_D3', 'standard_d4': 'Standard_D4', 'standard_d11': 'Standard_D11', 'standard_d12': 'Standard_D12', 'standard_d13': 'Standard_D13', 'standard_d14': 'Standard_D14', 'standard_d1_v2': 'Standard_D1_v2', 'standard_d2_v2': 'Standard_D2_v2', 'standard_d3_v2': 'Standard_D3_v2', 'standard_d4_v2': 'Standard_D4_v2', 'standard_d5_v2': 'Standard_D5_v2', 'standard_d11_v2': 'Standard_D11_v2', 'standard_d12_v2': 'Standard_D12_v2', 'standard_d13_v2': 'Standard_D13_v2', 'standard_d14_v2': 'Standard_D14_v2', 'standard_g1': 'Standard_G1', 'standard_g2': 'Standard_G2', 'standard_g3': 'Standard_G3', 'standard_g4': 'Standard_G4', 'standard_g5': 'Standard_G5', 'standard_ds1': 'Standard_DS1', 'standard_ds2': 'Standard_DS2', 'standard_ds3': 'Standard_DS3', 'standard_ds4': 'Standard_DS4', 'standard_ds11': 'Standard_DS11', 'standard_ds12': 'Standard_DS12', 'standard_ds13': 'Standard_DS13', 'standard_ds14': 'Standard_DS14', 'standard_gs1': 'Standard_GS1', 'standard_gs2': 'Standard_GS2', 'standard_gs3': 'Standard_GS3', 'standard_gs4': 'Standard_GS4', 'standard_gs5': 'Standard_GS5'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Container Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_containerservice()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Container Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_containerservice()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Container Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_containerservice(self):
        '''
        Creates or updates Container Service with the specified configuration.

        :return: deserialized Container Service instance state dictionary
        '''
        self.log("Creating / Updating the Container Service instance {0}".format(self.name))

        try:
            response = self.mgmt_client.container_services.create_or_update(resource_group_name=self.resource_group,
                                                                            container_service_name=self.name,
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
        self.log("Deleting the Container Service instance {0}".format(self.name))
        try:
            response = self.mgmt_client.container_services.delete(resource_group_name=self.resource_group,
                                                                  container_service_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Container Service instance.')
            self.fail("Error deleting the Container Service instance: {0}".format(str(e)))

        return True

    def get_containerservice(self):
        '''
        Gets the properties of the specified Container Service.

        :return: deserialized Container Service instance state dictionary
        '''
        self.log("Checking if the Container Service instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.container_services.get(resource_group_name=self.resource_group,
                                                               container_service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Container Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Container Service instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMContainerService()


if __name__ == '__main__':
    main()

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
module: azure_rm_containerservicemanagedcluster
version_added: "2.8"
short_description: Manage Managed Cluster instance.
description:
    - Create, update and delete instance of Managed Cluster.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the managed cluster resource.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    kubernetes_version:
        description:
            - Version of Kubernetes specified when creating the managed cluster.
    dns_prefix:
        description:
            - DNS prefix specified when creating the managed cluster.
    agent_pool_profiles:
        description:
            - Properties of the agent pool.
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
                    - 'standard_a1'
                    - 'standard_a10'
                    - 'standard_a11'
                    - 'standard_a1_v2'
                    - 'standard_a2'
                    - 'standard_a2_v2'
                    - 'standard_a2m_v2'
                    - 'standard_a3'
                    - 'standard_a4'
                    - 'standard_a4_v2'
                    - 'standard_a4m_v2'
                    - 'standard_a5'
                    - 'standard_a6'
                    - 'standard_a7'
                    - 'standard_a8'
                    - 'standard_a8_v2'
                    - 'standard_a8m_v2'
                    - 'standard_a9'
                    - 'standard_b2ms'
                    - 'standard_b2s'
                    - 'standard_b4ms'
                    - 'standard_b8ms'
                    - 'standard_d1'
                    - 'standard_d11'
                    - 'standard_d11_v2'
                    - 'standard_d11_v2_promo'
                    - 'standard_d12'
                    - 'standard_d12_v2'
                    - 'standard_d12_v2_promo'
                    - 'standard_d13'
                    - 'standard_d13_v2'
                    - 'standard_d13_v2_promo'
                    - 'standard_d14'
                    - 'standard_d14_v2'
                    - 'standard_d14_v2_promo'
                    - 'standard_d15_v2'
                    - 'standard_d16_v3'
                    - 'standard_d16s_v3'
                    - 'standard_d1_v2'
                    - 'standard_d2'
                    - 'standard_d2_v2'
                    - 'standard_d2_v2_promo'
                    - 'standard_d2_v3'
                    - 'standard_d2s_v3'
                    - 'standard_d3'
                    - 'standard_d32_v3'
                    - 'standard_d32s_v3'
                    - 'standard_d3_v2'
                    - 'standard_d3_v2_promo'
                    - 'standard_d4'
                    - 'standard_d4_v2'
                    - 'standard_d4_v2_promo'
                    - 'standard_d4_v3'
                    - 'standard_d4s_v3'
                    - 'standard_d5_v2'
                    - 'standard_d5_v2_promo'
                    - 'standard_d64_v3'
                    - 'standard_d64s_v3'
                    - 'standard_d8_v3'
                    - 'standard_d8s_v3'
                    - 'standard_ds1'
                    - 'standard_ds11'
                    - 'standard_ds11_v2'
                    - 'standard_ds11_v2_promo'
                    - 'standard_ds12'
                    - 'standard_ds12_v2'
                    - 'standard_ds12_v2_promo'
                    - 'standard_ds13'
                    - 'standard_ds13-2_v2'
                    - 'standard_ds13-4_v2'
                    - 'standard_ds13_v2'
                    - 'standard_ds13_v2_promo'
                    - 'standard_ds14'
                    - 'standard_ds14-4_v2'
                    - 'standard_ds14-8_v2'
                    - 'standard_ds14_v2'
                    - 'standard_ds14_v2_promo'
                    - 'standard_ds15_v2'
                    - 'standard_ds1_v2'
                    - 'standard_ds2'
                    - 'standard_ds2_v2'
                    - 'standard_ds2_v2_promo'
                    - 'standard_ds3'
                    - 'standard_ds3_v2'
                    - 'standard_ds3_v2_promo'
                    - 'standard_ds4'
                    - 'standard_ds4_v2'
                    - 'standard_ds4_v2_promo'
                    - 'standard_ds5_v2'
                    - 'standard_ds5_v2_promo'
                    - 'standard_e16_v3'
                    - 'standard_e16s_v3'
                    - 'standard_e2_v3'
                    - 'standard_e2s_v3'
                    - 'standard_e32-16s_v3'
                    - 'standard_e32-8s_v3'
                    - 'standard_e32_v3'
                    - 'standard_e32s_v3'
                    - 'standard_e4_v3'
                    - 'standard_e4s_v3'
                    - 'standard_e64-16s_v3'
                    - 'standard_e64-32s_v3'
                    - 'standard_e64_v3'
                    - 'standard_e64s_v3'
                    - 'standard_e8_v3'
                    - 'standard_e8s_v3'
                    - 'standard_f1'
                    - 'standard_f16'
                    - 'standard_f16s'
                    - 'standard_f16s_v2'
                    - 'standard_f1s'
                    - 'standard_f2'
                    - 'standard_f2s'
                    - 'standard_f2s_v2'
                    - 'standard_f32s_v2'
                    - 'standard_f4'
                    - 'standard_f4s'
                    - 'standard_f4s_v2'
                    - 'standard_f64s_v2'
                    - 'standard_f72s_v2'
                    - 'standard_f8'
                    - 'standard_f8s'
                    - 'standard_f8s_v2'
                    - 'standard_g1'
                    - 'standard_g2'
                    - 'standard_g3'
                    - 'standard_g4'
                    - 'standard_g5'
                    - 'standard_gs1'
                    - 'standard_gs2'
                    - 'standard_gs3'
                    - 'standard_gs4'
                    - 'standard_gs4-4'
                    - 'standard_gs4-8'
                    - 'standard_gs5'
                    - 'standard_gs5-16'
                    - 'standard_gs5-8'
                    - 'standard_h16'
                    - 'standard_h16m'
                    - 'standard_h16mr'
                    - 'standard_h16r'
                    - 'standard_h8'
                    - 'standard_h8m'
                    - 'standard_l16s'
                    - 'standard_l32s'
                    - 'standard_l4s'
                    - 'standard_l8s'
                    - 'standard_m128-32ms'
                    - 'standard_m128-64ms'
                    - 'standard_m128ms'
                    - 'standard_m128s'
                    - 'standard_m64-16ms'
                    - 'standard_m64-32ms'
                    - 'standard_m64ms'
                    - 'standard_m64s'
                    - 'standard_nc12'
                    - 'standard_nc12s_v2'
                    - 'standard_nc12s_v3'
                    - 'standard_nc24'
                    - 'standard_nc24r'
                    - 'standard_nc24rs_v2'
                    - 'standard_nc24rs_v3'
                    - 'standard_nc24s_v2'
                    - 'standard_nc24s_v3'
                    - 'standard_nc6'
                    - 'standard_nc6s_v2'
                    - 'standard_nc6s_v3'
                    - 'standard_nd12s'
                    - 'standard_nd24rs'
                    - 'standard_nd24s'
                    - 'standard_nd6s'
                    - 'standard_nv12'
                    - 'standard_nv24'
                    - 'standard_nv6'
            os_disk_size_gb:
                description:
                    - "OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply
                       the default osDisk size according to the I(vm_size) specified."
            vnet_subnet_id:
                description:
                    - "VNet SubnetID specifies the vnet's subnet identifier."
            max_pods:
                description:
                    - Maximum number of pods that can run on a node.
            os_type:
                description:
                    - OsType to be used to specify os I(type). Choose from C(linux) and C(windows). Default to C(linux).
                choices:
                    - 'linux'
                    - 'windows'
            max_count:
                description:
                    - Maximum number of nodes for auto-scaling
            min_count:
                description:
                    - Minimum number of nodes for auto-scaling
            enable_auto_scaling:
                description:
                    - Whether to enable auto-scaler
            type:
                description:
                    - AgentPoolType represents types of agentpool.
                choices:
                    - 'virtual_machine_scale_sets'
                    - 'availability_set'
    linux_profile:
        description:
            - Profile for Linux VMs in the container service cluster.
        suboptions:
            admin_username:
                description:
                    - The administrator username to use for Linux VMs.
                    - Required when C(state) is I(present).
            ssh:
                description:
                    - SSH configuration for Linux-based VMs running on Azure.
                    - Required when C(state) is I(present).
                suboptions:
                    public_keys:
                        description:
                            - The list of SSH public keys used to authenticate with Linux-based VMs. Only expect one key specified.
                            - Required when C(state) is I(present).
                        type: list
                        suboptions:
                            key_data:
                                description:
                                    - "Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or
                                       without headers."
                                    - Required when C(state) is I(present).
    service_principal_profile:
        description:
            - Information about a service principal identity for the cluster to use for manipulating Azure APIs.
        suboptions:
            client_id:
                description:
                    - The ID for the service principal.
                    - Required when C(state) is I(present).
            secret:
                description:
                    - The secret password associated with the service principal in plain text.
    addon_profiles:
        description:
            - Profile of managed cluster add-on.
    enable_rbac:
        description:
            - Whether to enable Kubernetes Role-Based Access Control.
    network_profile:
        description:
            - Profile of network configuration.
        suboptions:
            network_plugin:
                description:
                    - Network plugin used for building Kubernetes network.
                choices:
                    - 'azure'
                    - 'kubenet'
            network_policy:
                description:
                    - Network policy used for building Kubernetes network.
                choices:
                    - 'calico'
            pod_cidr:
                description:
                    - A CIDR notation IP range from which to assign pod IPs when C(kubenet) is used.
            service_cidr:
                description:
                    - A CIDR notation IP range from which to assign service cluster IPs. It must not overlap with any Subnet IP ranges.
            dns_service_ip:
                description:
                    - An IP address assigned to the Kubernetes DNS service. It must be within the Kubernetes service address range specified in I(service_cidr).
            docker_bridge_cidr:
                description:
                    - "A CIDR notation IP range assigned to the Docker bridge network. It must not overlap with any Subnet IP ranges or the Kubernetes
                       service address range."
    aad_profile:
        description:
            - Profile of Azure Active Directory configuration.
        suboptions:
            client_app_id:
                description:
                    - The client AAD application ID.
                    - Required when C(state) is I(present).
            server_app_id:
                description:
                    - The server AAD application ID.
                    - Required when C(state) is I(present).
            server_app_secret:
                description:
                    - The server AAD application secret.
            tenant_id:
                description:
                    - The AAD tenant ID to use for authentication. If not specified, will use the tenant of the deployment subscription.
    state:
      description:
        - Assert the state of the Managed Cluster.
        - Use 'present' to create or update an Managed Cluster and 'absent' to delete it.
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
  - name: Create (or update) Managed Cluster
    azure_rm_containerservicemanagedcluster:
      resource_group: rg1
      name: clustername1
      location: eastus
      dns_prefix: dnsprefix1
      agent_pool_profiles:
        - name: nodepool1
          count: 3
          vm_size: Standard_DS1_v2
          os_type: Linux
      linux_profile:
        admin_username: azureuser
        ssh:
          public_keys:
            - key_data: keydata
      service_principal_profile:
        client_id: clientid
        secret: secret
      addon_profiles: {}
      enable_rbac: False
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/subid1/resourcegroups/rg1/providers/Microsoft.ContainerService/managedClusters/clustername1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.containerservice import ContainerServiceClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagedClusters(AzureRMModuleBase):
    """Configuration class for an Azure RM Managed Cluster resource"""

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
            kubernetes_version=dict(
                type='str'
            ),
            dns_prefix=dict(
                type='str'
            ),
            agent_pool_profiles=dict(
                type='list'
            ),
            linux_profile=dict(
                type='dict'
            ),
            service_principal_profile=dict(
                type='dict'
            ),
            addon_profiles=dict(
                type='dict'
            ),
            enable_rbac=dict(
                type='str'
            ),
            network_profile=dict(
                type='dict'
            ),
            aad_profile=dict(
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

        super(AzureRMManagedClusters, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "kubernetes_version":
                    self.parameters["kubernetes_version"] = kwargs[key]
                elif key == "dns_prefix":
                    self.parameters["dns_prefix"] = kwargs[key]
                elif key == "agent_pool_profiles":
                    ev = kwargs[key]
                    if 'vm_size' in ev:
                        if ev['vm_size'] == 'standard_a1':
                            ev['vm_size'] = 'Standard_A1'
                        elif ev['vm_size'] == 'standard_a10':
                            ev['vm_size'] = 'Standard_A10'
                        elif ev['vm_size'] == 'standard_a11':
                            ev['vm_size'] = 'Standard_A11'
                        elif ev['vm_size'] == 'standard_a1_v2':
                            ev['vm_size'] = 'Standard_A1_v2'
                        elif ev['vm_size'] == 'standard_a2':
                            ev['vm_size'] = 'Standard_A2'
                        elif ev['vm_size'] == 'standard_a2_v2':
                            ev['vm_size'] = 'Standard_A2_v2'
                        elif ev['vm_size'] == 'standard_a2m_v2':
                            ev['vm_size'] = 'Standard_A2m_v2'
                        elif ev['vm_size'] == 'standard_a3':
                            ev['vm_size'] = 'Standard_A3'
                        elif ev['vm_size'] == 'standard_a4':
                            ev['vm_size'] = 'Standard_A4'
                        elif ev['vm_size'] == 'standard_a4_v2':
                            ev['vm_size'] = 'Standard_A4_v2'
                        elif ev['vm_size'] == 'standard_a4m_v2':
                            ev['vm_size'] = 'Standard_A4m_v2'
                        elif ev['vm_size'] == 'standard_a5':
                            ev['vm_size'] = 'Standard_A5'
                        elif ev['vm_size'] == 'standard_a6':
                            ev['vm_size'] = 'Standard_A6'
                        elif ev['vm_size'] == 'standard_a7':
                            ev['vm_size'] = 'Standard_A7'
                        elif ev['vm_size'] == 'standard_a8':
                            ev['vm_size'] = 'Standard_A8'
                        elif ev['vm_size'] == 'standard_a8_v2':
                            ev['vm_size'] = 'Standard_A8_v2'
                        elif ev['vm_size'] == 'standard_a8m_v2':
                            ev['vm_size'] = 'Standard_A8m_v2'
                        elif ev['vm_size'] == 'standard_a9':
                            ev['vm_size'] = 'Standard_A9'
                        elif ev['vm_size'] == 'standard_b2ms':
                            ev['vm_size'] = 'Standard_B2ms'
                        elif ev['vm_size'] == 'standard_b2s':
                            ev['vm_size'] = 'Standard_B2s'
                        elif ev['vm_size'] == 'standard_b4ms':
                            ev['vm_size'] = 'Standard_B4ms'
                        elif ev['vm_size'] == 'standard_b8ms':
                            ev['vm_size'] = 'Standard_B8ms'
                        elif ev['vm_size'] == 'standard_d1':
                            ev['vm_size'] = 'Standard_D1'
                        elif ev['vm_size'] == 'standard_d11':
                            ev['vm_size'] = 'Standard_D11'
                        elif ev['vm_size'] == 'standard_d11_v2':
                            ev['vm_size'] = 'Standard_D11_v2'
                        elif ev['vm_size'] == 'standard_d11_v2_promo':
                            ev['vm_size'] = 'Standard_D11_v2_Promo'
                        elif ev['vm_size'] == 'standard_d12':
                            ev['vm_size'] = 'Standard_D12'
                        elif ev['vm_size'] == 'standard_d12_v2':
                            ev['vm_size'] = 'Standard_D12_v2'
                        elif ev['vm_size'] == 'standard_d12_v2_promo':
                            ev['vm_size'] = 'Standard_D12_v2_Promo'
                        elif ev['vm_size'] == 'standard_d13':
                            ev['vm_size'] = 'Standard_D13'
                        elif ev['vm_size'] == 'standard_d13_v2':
                            ev['vm_size'] = 'Standard_D13_v2'
                        elif ev['vm_size'] == 'standard_d13_v2_promo':
                            ev['vm_size'] = 'Standard_D13_v2_Promo'
                        elif ev['vm_size'] == 'standard_d14':
                            ev['vm_size'] = 'Standard_D14'
                        elif ev['vm_size'] == 'standard_d14_v2':
                            ev['vm_size'] = 'Standard_D14_v2'
                        elif ev['vm_size'] == 'standard_d14_v2_promo':
                            ev['vm_size'] = 'Standard_D14_v2_Promo'
                        elif ev['vm_size'] == 'standard_d15_v2':
                            ev['vm_size'] = 'Standard_D15_v2'
                        elif ev['vm_size'] == 'standard_d16_v3':
                            ev['vm_size'] = 'Standard_D16_v3'
                        elif ev['vm_size'] == 'standard_d16s_v3':
                            ev['vm_size'] = 'Standard_D16s_v3'
                        elif ev['vm_size'] == 'standard_d1_v2':
                            ev['vm_size'] = 'Standard_D1_v2'
                        elif ev['vm_size'] == 'standard_d2':
                            ev['vm_size'] = 'Standard_D2'
                        elif ev['vm_size'] == 'standard_d2_v2':
                            ev['vm_size'] = 'Standard_D2_v2'
                        elif ev['vm_size'] == 'standard_d2_v2_promo':
                            ev['vm_size'] = 'Standard_D2_v2_Promo'
                        elif ev['vm_size'] == 'standard_d2_v3':
                            ev['vm_size'] = 'Standard_D2_v3'
                        elif ev['vm_size'] == 'standard_d2s_v3':
                            ev['vm_size'] = 'Standard_D2s_v3'
                        elif ev['vm_size'] == 'standard_d3':
                            ev['vm_size'] = 'Standard_D3'
                        elif ev['vm_size'] == 'standard_d32_v3':
                            ev['vm_size'] = 'Standard_D32_v3'
                        elif ev['vm_size'] == 'standard_d32s_v3':
                            ev['vm_size'] = 'Standard_D32s_v3'
                        elif ev['vm_size'] == 'standard_d3_v2':
                            ev['vm_size'] = 'Standard_D3_v2'
                        elif ev['vm_size'] == 'standard_d3_v2_promo':
                            ev['vm_size'] = 'Standard_D3_v2_Promo'
                        elif ev['vm_size'] == 'standard_d4':
                            ev['vm_size'] = 'Standard_D4'
                        elif ev['vm_size'] == 'standard_d4_v2':
                            ev['vm_size'] = 'Standard_D4_v2'
                        elif ev['vm_size'] == 'standard_d4_v2_promo':
                            ev['vm_size'] = 'Standard_D4_v2_Promo'
                        elif ev['vm_size'] == 'standard_d4_v3':
                            ev['vm_size'] = 'Standard_D4_v3'
                        elif ev['vm_size'] == 'standard_d4s_v3':
                            ev['vm_size'] = 'Standard_D4s_v3'
                        elif ev['vm_size'] == 'standard_d5_v2':
                            ev['vm_size'] = 'Standard_D5_v2'
                        elif ev['vm_size'] == 'standard_d5_v2_promo':
                            ev['vm_size'] = 'Standard_D5_v2_Promo'
                        elif ev['vm_size'] == 'standard_d64_v3':
                            ev['vm_size'] = 'Standard_D64_v3'
                        elif ev['vm_size'] == 'standard_d64s_v3':
                            ev['vm_size'] = 'Standard_D64s_v3'
                        elif ev['vm_size'] == 'standard_d8_v3':
                            ev['vm_size'] = 'Standard_D8_v3'
                        elif ev['vm_size'] == 'standard_d8s_v3':
                            ev['vm_size'] = 'Standard_D8s_v3'
                        elif ev['vm_size'] == 'standard_ds1':
                            ev['vm_size'] = 'Standard_DS1'
                        elif ev['vm_size'] == 'standard_ds11':
                            ev['vm_size'] = 'Standard_DS11'
                        elif ev['vm_size'] == 'standard_ds11_v2':
                            ev['vm_size'] = 'Standard_DS11_v2'
                        elif ev['vm_size'] == 'standard_ds11_v2_promo':
                            ev['vm_size'] = 'Standard_DS11_v2_Promo'
                        elif ev['vm_size'] == 'standard_ds12':
                            ev['vm_size'] = 'Standard_DS12'
                        elif ev['vm_size'] == 'standard_ds12_v2':
                            ev['vm_size'] = 'Standard_DS12_v2'
                        elif ev['vm_size'] == 'standard_ds12_v2_promo':
                            ev['vm_size'] = 'Standard_DS12_v2_Promo'
                        elif ev['vm_size'] == 'standard_ds13':
                            ev['vm_size'] = 'Standard_DS13'
                        elif ev['vm_size'] == 'standard_ds13-2_v2':
                            ev['vm_size'] = 'Standard_DS13-2_v2'
                        elif ev['vm_size'] == 'standard_ds13-4_v2':
                            ev['vm_size'] = 'Standard_DS13-4_v2'
                        elif ev['vm_size'] == 'standard_ds13_v2':
                            ev['vm_size'] = 'Standard_DS13_v2'
                        elif ev['vm_size'] == 'standard_ds13_v2_promo':
                            ev['vm_size'] = 'Standard_DS13_v2_Promo'
                        elif ev['vm_size'] == 'standard_ds14':
                            ev['vm_size'] = 'Standard_DS14'
                        elif ev['vm_size'] == 'standard_ds14-4_v2':
                            ev['vm_size'] = 'Standard_DS14-4_v2'
                        elif ev['vm_size'] == 'standard_ds14-8_v2':
                            ev['vm_size'] = 'Standard_DS14-8_v2'
                        elif ev['vm_size'] == 'standard_ds14_v2':
                            ev['vm_size'] = 'Standard_DS14_v2'
                        elif ev['vm_size'] == 'standard_ds14_v2_promo':
                            ev['vm_size'] = 'Standard_DS14_v2_Promo'
                        elif ev['vm_size'] == 'standard_ds15_v2':
                            ev['vm_size'] = 'Standard_DS15_v2'
                        elif ev['vm_size'] == 'standard_ds1_v2':
                            ev['vm_size'] = 'Standard_DS1_v2'
                        elif ev['vm_size'] == 'standard_ds2':
                            ev['vm_size'] = 'Standard_DS2'
                        elif ev['vm_size'] == 'standard_ds2_v2':
                            ev['vm_size'] = 'Standard_DS2_v2'
                        elif ev['vm_size'] == 'standard_ds2_v2_promo':
                            ev['vm_size'] = 'Standard_DS2_v2_Promo'
                        elif ev['vm_size'] == 'standard_ds3':
                            ev['vm_size'] = 'Standard_DS3'
                        elif ev['vm_size'] == 'standard_ds3_v2':
                            ev['vm_size'] = 'Standard_DS3_v2'
                        elif ev['vm_size'] == 'standard_ds3_v2_promo':
                            ev['vm_size'] = 'Standard_DS3_v2_Promo'
                        elif ev['vm_size'] == 'standard_ds4':
                            ev['vm_size'] = 'Standard_DS4'
                        elif ev['vm_size'] == 'standard_ds4_v2':
                            ev['vm_size'] = 'Standard_DS4_v2'
                        elif ev['vm_size'] == 'standard_ds4_v2_promo':
                            ev['vm_size'] = 'Standard_DS4_v2_Promo'
                        elif ev['vm_size'] == 'standard_ds5_v2':
                            ev['vm_size'] = 'Standard_DS5_v2'
                        elif ev['vm_size'] == 'standard_ds5_v2_promo':
                            ev['vm_size'] = 'Standard_DS5_v2_Promo'
                        elif ev['vm_size'] == 'standard_e16_v3':
                            ev['vm_size'] = 'Standard_E16_v3'
                        elif ev['vm_size'] == 'standard_e16s_v3':
                            ev['vm_size'] = 'Standard_E16s_v3'
                        elif ev['vm_size'] == 'standard_e2_v3':
                            ev['vm_size'] = 'Standard_E2_v3'
                        elif ev['vm_size'] == 'standard_e2s_v3':
                            ev['vm_size'] = 'Standard_E2s_v3'
                        elif ev['vm_size'] == 'standard_e32-16s_v3':
                            ev['vm_size'] = 'Standard_E32-16s_v3'
                        elif ev['vm_size'] == 'standard_e32-8s_v3':
                            ev['vm_size'] = 'Standard_E32-8s_v3'
                        elif ev['vm_size'] == 'standard_e32_v3':
                            ev['vm_size'] = 'Standard_E32_v3'
                        elif ev['vm_size'] == 'standard_e32s_v3':
                            ev['vm_size'] = 'Standard_E32s_v3'
                        elif ev['vm_size'] == 'standard_e4_v3':
                            ev['vm_size'] = 'Standard_E4_v3'
                        elif ev['vm_size'] == 'standard_e4s_v3':
                            ev['vm_size'] = 'Standard_E4s_v3'
                        elif ev['vm_size'] == 'standard_e64-16s_v3':
                            ev['vm_size'] = 'Standard_E64-16s_v3'
                        elif ev['vm_size'] == 'standard_e64-32s_v3':
                            ev['vm_size'] = 'Standard_E64-32s_v3'
                        elif ev['vm_size'] == 'standard_e64_v3':
                            ev['vm_size'] = 'Standard_E64_v3'
                        elif ev['vm_size'] == 'standard_e64s_v3':
                            ev['vm_size'] = 'Standard_E64s_v3'
                        elif ev['vm_size'] == 'standard_e8_v3':
                            ev['vm_size'] = 'Standard_E8_v3'
                        elif ev['vm_size'] == 'standard_e8s_v3':
                            ev['vm_size'] = 'Standard_E8s_v3'
                        elif ev['vm_size'] == 'standard_f1':
                            ev['vm_size'] = 'Standard_F1'
                        elif ev['vm_size'] == 'standard_f16':
                            ev['vm_size'] = 'Standard_F16'
                        elif ev['vm_size'] == 'standard_f16s':
                            ev['vm_size'] = 'Standard_F16s'
                        elif ev['vm_size'] == 'standard_f16s_v2':
                            ev['vm_size'] = 'Standard_F16s_v2'
                        elif ev['vm_size'] == 'standard_f1s':
                            ev['vm_size'] = 'Standard_F1s'
                        elif ev['vm_size'] == 'standard_f2':
                            ev['vm_size'] = 'Standard_F2'
                        elif ev['vm_size'] == 'standard_f2s':
                            ev['vm_size'] = 'Standard_F2s'
                        elif ev['vm_size'] == 'standard_f2s_v2':
                            ev['vm_size'] = 'Standard_F2s_v2'
                        elif ev['vm_size'] == 'standard_f32s_v2':
                            ev['vm_size'] = 'Standard_F32s_v2'
                        elif ev['vm_size'] == 'standard_f4':
                            ev['vm_size'] = 'Standard_F4'
                        elif ev['vm_size'] == 'standard_f4s':
                            ev['vm_size'] = 'Standard_F4s'
                        elif ev['vm_size'] == 'standard_f4s_v2':
                            ev['vm_size'] = 'Standard_F4s_v2'
                        elif ev['vm_size'] == 'standard_f64s_v2':
                            ev['vm_size'] = 'Standard_F64s_v2'
                        elif ev['vm_size'] == 'standard_f72s_v2':
                            ev['vm_size'] = 'Standard_F72s_v2'
                        elif ev['vm_size'] == 'standard_f8':
                            ev['vm_size'] = 'Standard_F8'
                        elif ev['vm_size'] == 'standard_f8s':
                            ev['vm_size'] = 'Standard_F8s'
                        elif ev['vm_size'] == 'standard_f8s_v2':
                            ev['vm_size'] = 'Standard_F8s_v2'
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
                        elif ev['vm_size'] == 'standard_gs1':
                            ev['vm_size'] = 'Standard_GS1'
                        elif ev['vm_size'] == 'standard_gs2':
                            ev['vm_size'] = 'Standard_GS2'
                        elif ev['vm_size'] == 'standard_gs3':
                            ev['vm_size'] = 'Standard_GS3'
                        elif ev['vm_size'] == 'standard_gs4':
                            ev['vm_size'] = 'Standard_GS4'
                        elif ev['vm_size'] == 'standard_gs4-4':
                            ev['vm_size'] = 'Standard_GS4-4'
                        elif ev['vm_size'] == 'standard_gs4-8':
                            ev['vm_size'] = 'Standard_GS4-8'
                        elif ev['vm_size'] == 'standard_gs5':
                            ev['vm_size'] = 'Standard_GS5'
                        elif ev['vm_size'] == 'standard_gs5-16':
                            ev['vm_size'] = 'Standard_GS5-16'
                        elif ev['vm_size'] == 'standard_gs5-8':
                            ev['vm_size'] = 'Standard_GS5-8'
                        elif ev['vm_size'] == 'standard_h16':
                            ev['vm_size'] = 'Standard_H16'
                        elif ev['vm_size'] == 'standard_h16m':
                            ev['vm_size'] = 'Standard_H16m'
                        elif ev['vm_size'] == 'standard_h16mr':
                            ev['vm_size'] = 'Standard_H16mr'
                        elif ev['vm_size'] == 'standard_h16r':
                            ev['vm_size'] = 'Standard_H16r'
                        elif ev['vm_size'] == 'standard_h8':
                            ev['vm_size'] = 'Standard_H8'
                        elif ev['vm_size'] == 'standard_h8m':
                            ev['vm_size'] = 'Standard_H8m'
                        elif ev['vm_size'] == 'standard_l16s':
                            ev['vm_size'] = 'Standard_L16s'
                        elif ev['vm_size'] == 'standard_l32s':
                            ev['vm_size'] = 'Standard_L32s'
                        elif ev['vm_size'] == 'standard_l4s':
                            ev['vm_size'] = 'Standard_L4s'
                        elif ev['vm_size'] == 'standard_l8s':
                            ev['vm_size'] = 'Standard_L8s'
                        elif ev['vm_size'] == 'standard_m128-32ms':
                            ev['vm_size'] = 'Standard_M128-32ms'
                        elif ev['vm_size'] == 'standard_m128-64ms':
                            ev['vm_size'] = 'Standard_M128-64ms'
                        elif ev['vm_size'] == 'standard_m128ms':
                            ev['vm_size'] = 'Standard_M128ms'
                        elif ev['vm_size'] == 'standard_m128s':
                            ev['vm_size'] = 'Standard_M128s'
                        elif ev['vm_size'] == 'standard_m64-16ms':
                            ev['vm_size'] = 'Standard_M64-16ms'
                        elif ev['vm_size'] == 'standard_m64-32ms':
                            ev['vm_size'] = 'Standard_M64-32ms'
                        elif ev['vm_size'] == 'standard_m64ms':
                            ev['vm_size'] = 'Standard_M64ms'
                        elif ev['vm_size'] == 'standard_m64s':
                            ev['vm_size'] = 'Standard_M64s'
                        elif ev['vm_size'] == 'standard_nc12':
                            ev['vm_size'] = 'Standard_NC12'
                        elif ev['vm_size'] == 'standard_nc12s_v2':
                            ev['vm_size'] = 'Standard_NC12s_v2'
                        elif ev['vm_size'] == 'standard_nc12s_v3':
                            ev['vm_size'] = 'Standard_NC12s_v3'
                        elif ev['vm_size'] == 'standard_nc24':
                            ev['vm_size'] = 'Standard_NC24'
                        elif ev['vm_size'] == 'standard_nc24r':
                            ev['vm_size'] = 'Standard_NC24r'
                        elif ev['vm_size'] == 'standard_nc24rs_v2':
                            ev['vm_size'] = 'Standard_NC24rs_v2'
                        elif ev['vm_size'] == 'standard_nc24rs_v3':
                            ev['vm_size'] = 'Standard_NC24rs_v3'
                        elif ev['vm_size'] == 'standard_nc24s_v2':
                            ev['vm_size'] = 'Standard_NC24s_v2'
                        elif ev['vm_size'] == 'standard_nc24s_v3':
                            ev['vm_size'] = 'Standard_NC24s_v3'
                        elif ev['vm_size'] == 'standard_nc6':
                            ev['vm_size'] = 'Standard_NC6'
                        elif ev['vm_size'] == 'standard_nc6s_v2':
                            ev['vm_size'] = 'Standard_NC6s_v2'
                        elif ev['vm_size'] == 'standard_nc6s_v3':
                            ev['vm_size'] = 'Standard_NC6s_v3'
                        elif ev['vm_size'] == 'standard_nd12s':
                            ev['vm_size'] = 'Standard_ND12s'
                        elif ev['vm_size'] == 'standard_nd24rs':
                            ev['vm_size'] = 'Standard_ND24rs'
                        elif ev['vm_size'] == 'standard_nd24s':
                            ev['vm_size'] = 'Standard_ND24s'
                        elif ev['vm_size'] == 'standard_nd6s':
                            ev['vm_size'] = 'Standard_ND6s'
                        elif ev['vm_size'] == 'standard_nv12':
                            ev['vm_size'] = 'Standard_NV12'
                        elif ev['vm_size'] == 'standard_nv24':
                            ev['vm_size'] = 'Standard_NV24'
                        elif ev['vm_size'] == 'standard_nv6':
                            ev['vm_size'] = 'Standard_NV6'
                    if 'os_type' in ev:
                        if ev['os_type'] == 'linux':
                            ev['os_type'] = 'Linux'
                        elif ev['os_type'] == 'windows':
                            ev['os_type'] = 'Windows'
                    if 'type' in ev:
                        if ev['type'] == 'virtual_machine_scale_sets':
                            ev['type'] = 'VirtualMachineScaleSets'
                        elif ev['type'] == 'availability_set':
                            ev['type'] = 'AvailabilitySet'
                    self.parameters["agent_pool_profiles"] = ev
                elif key == "linux_profile":
                    self.parameters["linux_profile"] = kwargs[key]
                elif key == "service_principal_profile":
                    self.parameters["service_principal_profile"] = kwargs[key]
                elif key == "addon_profiles":
                    self.parameters["addon_profiles"] = kwargs[key]
                elif key == "enable_rbac":
                    self.parameters["enable_rbac"] = kwargs[key]
                elif key == "network_profile":
                    self.parameters["network_profile"] = kwargs[key]
                elif key == "aad_profile":
                    self.parameters["aad_profile"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ContainerServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_managedcluster()

        if not old_response:
            self.log("Managed Cluster instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Managed Cluster instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Managed Cluster instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managedcluster()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Managed Cluster instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managedcluster()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_managedcluster():
                time.sleep(20)
        else:
            self.log("Managed Cluster instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_managedcluster(self):
        '''
        Creates or updates Managed Cluster with the specified configuration.

        :return: deserialized Managed Cluster instance state dictionary
        '''
        self.log("Creating / Updating the Managed Cluster instance {0}".format(self.name))

        try:
            response = self.mgmt_client.managed_clusters.create_or_update(resource_group_name=self.resource_group,
                                                                          resource_name=self.name,
                                                                          parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Managed Cluster instance.')
            self.fail("Error creating the Managed Cluster instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_managedcluster(self):
        '''
        Deletes specified Managed Cluster instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Managed Cluster instance {0}".format(self.name))
        try:
            response = self.mgmt_client.managed_clusters.delete(resource_group_name=self.resource_group,
                                                                resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Managed Cluster instance.')
            self.fail("Error deleting the Managed Cluster instance: {0}".format(str(e)))

        return True

    def get_managedcluster(self):
        '''
        Gets the properties of the specified Managed Cluster.

        :return: deserialized Managed Cluster instance state dictionary
        '''
        self.log("Checking if the Managed Cluster instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.managed_clusters.get(resource_group_name=self.resource_group,
                                                             resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Managed Cluster instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Managed Cluster instance.')
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
    AzureRMManagedClusters()


if __name__ == '__main__':
    main()

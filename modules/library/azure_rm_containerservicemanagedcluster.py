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
short_description: Manage Azure Managed Cluster instance.
description:
    - Create, update and delete instance of Azure Managed Cluster.

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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMManagedCluster(AzureRMModuleBase):
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
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    count=dict(
                        type='int'
                    ),
                    vm_size=dict(
                        type='str',
                        choices=['standard_a1',
                                 'standard_a10',
                                 'standard_a11',
                                 'standard_a1_v2',
                                 'standard_a2',
                                 'standard_a2_v2',
                                 'standard_a2m_v2',
                                 'standard_a3',
                                 'standard_a4',
                                 'standard_a4_v2',
                                 'standard_a4m_v2',
                                 'standard_a5',
                                 'standard_a6',
                                 'standard_a7',
                                 'standard_a8',
                                 'standard_a8_v2',
                                 'standard_a8m_v2',
                                 'standard_a9',
                                 'standard_b2ms',
                                 'standard_b2s',
                                 'standard_b4ms',
                                 'standard_b8ms',
                                 'standard_d1',
                                 'standard_d11',
                                 'standard_d11_v2',
                                 'standard_d11_v2_promo',
                                 'standard_d12',
                                 'standard_d12_v2',
                                 'standard_d12_v2_promo',
                                 'standard_d13',
                                 'standard_d13_v2',
                                 'standard_d13_v2_promo',
                                 'standard_d14',
                                 'standard_d14_v2',
                                 'standard_d14_v2_promo',
                                 'standard_d15_v2',
                                 'standard_d16_v3',
                                 'standard_d16s_v3',
                                 'standard_d1_v2',
                                 'standard_d2',
                                 'standard_d2_v2',
                                 'standard_d2_v2_promo',
                                 'standard_d2_v3',
                                 'standard_d2s_v3',
                                 'standard_d3',
                                 'standard_d32_v3',
                                 'standard_d32s_v3',
                                 'standard_d3_v2',
                                 'standard_d3_v2_promo',
                                 'standard_d4',
                                 'standard_d4_v2',
                                 'standard_d4_v2_promo',
                                 'standard_d4_v3',
                                 'standard_d4s_v3',
                                 'standard_d5_v2',
                                 'standard_d5_v2_promo',
                                 'standard_d64_v3',
                                 'standard_d64s_v3',
                                 'standard_d8_v3',
                                 'standard_d8s_v3',
                                 'standard_ds1',
                                 'standard_ds11',
                                 'standard_ds11_v2',
                                 'standard_ds11_v2_promo',
                                 'standard_ds12',
                                 'standard_ds12_v2',
                                 'standard_ds12_v2_promo',
                                 'standard_ds13',
                                 'standard_ds13-2_v2',
                                 'standard_ds13-4_v2',
                                 'standard_ds13_v2',
                                 'standard_ds13_v2_promo',
                                 'standard_ds14',
                                 'standard_ds14-4_v2',
                                 'standard_ds14-8_v2',
                                 'standard_ds14_v2',
                                 'standard_ds14_v2_promo',
                                 'standard_ds15_v2',
                                 'standard_ds1_v2',
                                 'standard_ds2',
                                 'standard_ds2_v2',
                                 'standard_ds2_v2_promo',
                                 'standard_ds3',
                                 'standard_ds3_v2',
                                 'standard_ds3_v2_promo',
                                 'standard_ds4',
                                 'standard_ds4_v2',
                                 'standard_ds4_v2_promo',
                                 'standard_ds5_v2',
                                 'standard_ds5_v2_promo',
                                 'standard_e16_v3',
                                 'standard_e16s_v3',
                                 'standard_e2_v3',
                                 'standard_e2s_v3',
                                 'standard_e32-16s_v3',
                                 'standard_e32-8s_v3',
                                 'standard_e32_v3',
                                 'standard_e32s_v3',
                                 'standard_e4_v3',
                                 'standard_e4s_v3',
                                 'standard_e64-16s_v3',
                                 'standard_e64-32s_v3',
                                 'standard_e64_v3',
                                 'standard_e64s_v3',
                                 'standard_e8_v3',
                                 'standard_e8s_v3',
                                 'standard_f1',
                                 'standard_f16',
                                 'standard_f16s',
                                 'standard_f16s_v2',
                                 'standard_f1s',
                                 'standard_f2',
                                 'standard_f2s',
                                 'standard_f2s_v2',
                                 'standard_f32s_v2',
                                 'standard_f4',
                                 'standard_f4s',
                                 'standard_f4s_v2',
                                 'standard_f64s_v2',
                                 'standard_f72s_v2',
                                 'standard_f8',
                                 'standard_f8s',
                                 'standard_f8s_v2',
                                 'standard_g1',
                                 'standard_g2',
                                 'standard_g3',
                                 'standard_g4',
                                 'standard_g5',
                                 'standard_gs1',
                                 'standard_gs2',
                                 'standard_gs3',
                                 'standard_gs4',
                                 'standard_gs4-4',
                                 'standard_gs4-8',
                                 'standard_gs5',
                                 'standard_gs5-16',
                                 'standard_gs5-8',
                                 'standard_h16',
                                 'standard_h16m',
                                 'standard_h16mr',
                                 'standard_h16r',
                                 'standard_h8',
                                 'standard_h8m',
                                 'standard_l16s',
                                 'standard_l32s',
                                 'standard_l4s',
                                 'standard_l8s',
                                 'standard_m128-32ms',
                                 'standard_m128-64ms',
                                 'standard_m128ms',
                                 'standard_m128s',
                                 'standard_m64-16ms',
                                 'standard_m64-32ms',
                                 'standard_m64ms',
                                 'standard_m64s',
                                 'standard_nc12',
                                 'standard_nc12s_v2',
                                 'standard_nc12s_v3',
                                 'standard_nc24',
                                 'standard_nc24r',
                                 'standard_nc24rs_v2',
                                 'standard_nc24rs_v3',
                                 'standard_nc24s_v2',
                                 'standard_nc24s_v3',
                                 'standard_nc6',
                                 'standard_nc6s_v2',
                                 'standard_nc6s_v3',
                                 'standard_nd12s',
                                 'standard_nd24rs',
                                 'standard_nd24s',
                                 'standard_nd6s',
                                 'standard_nv12',
                                 'standard_nv24',
                                 'standard_nv6']
                    ),
                    os_disk_size_gb=dict(
                        type='int'
                    ),
                    vnet_subnet_id=dict(
                        type='str'
                    ),
                    max_pods=dict(
                        type='int'
                    ),
                    os_type=dict(
                        type='str',
                        choices=['linux',
                                 'windows']
                    ),
                    max_count=dict(
                        type='int'
                    ),
                    min_count=dict(
                        type='int'
                    ),
                    enable_auto_scaling=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str',
                        choices=['virtual_machine_scale_sets',
                                 'availability_set']
                    )
                )
            ),
            linux_profile=dict(
                type='dict',
                options=dict(
                    admin_username=dict(
                        type='str'
                    ),
                    ssh=dict(
                        type='dict',
                        options=dict(
                            public_keys=dict(
                                type='list',
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
            service_principal_profile=dict(
                type='dict',
                options=dict(
                    client_id=dict(
                        type='str'
                    ),
                    secret=dict(
                        type='str'
                    )
                )
            ),
            addon_profiles=dict(
                type='dict'
            ),
            enable_rbac=dict(
                type='str'
            ),
            network_profile=dict(
                type='dict',
                options=dict(
                    network_plugin=dict(
                        type='str',
                        choices=['azure',
                                 'kubenet']
                    ),
                    network_policy=dict(
                        type='str',
                        choices=['calico']
                    ),
                    pod_cidr=dict(
                        type='str'
                    ),
                    service_cidr=dict(
                        type='str'
                    ),
                    dns_service_ip=dict(
                        type='str'
                    ),
                    docker_bridge_cidr=dict(
                        type='str'
                    )
                )
            ),
            aad_profile=dict(
                type='dict',
                options=dict(
                    client_app_id=dict(
                        type='str'
                    ),
                    server_app_id=dict(
                        type='str'
                    ),
                    server_app_secret=dict(
                        type='str'
                    ),
                    tenant_id=dict(
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

        super(AzureRMManagedCluster, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['agent_pool_profiles', 'vm_size'], True)
        dict_map(self.parameters, ['agent_pool_profiles', 'vm_size'], {'standard_a1': 'Standard_A1', 'standard_a10': 'Standard_A10', 'standard_a11': 'Standard_A11', 'standard_a1_v2': 'Standard_A1_v2', 'standard_a2': 'Standard_A2', 'standard_a2_v2': 'Standard_A2_v2', 'standard_a2m_v2': 'Standard_A2m_v2', 'standard_a3': 'Standard_A3', 'standard_a4': 'Standard_A4', 'standard_a4_v2': 'Standard_A4_v2', 'standard_a4m_v2': 'Standard_A4m_v2', 'standard_a5': 'Standard_A5', 'standard_a6': 'Standard_A6', 'standard_a7': 'Standard_A7', 'standard_a8': 'Standard_A8', 'standard_a8_v2': 'Standard_A8_v2', 'standard_a8m_v2': 'Standard_A8m_v2', 'standard_a9': 'Standard_A9', 'standard_b2ms': 'Standard_B2ms', 'standard_b2s': 'Standard_B2s', 'standard_b4ms': 'Standard_B4ms', 'standard_b8ms': 'Standard_B8ms', 'standard_d1': 'Standard_D1', 'standard_d11': 'Standard_D11', 'standard_d11_v2': 'Standard_D11_v2', 'standard_d11_v2_promo': 'Standard_D11_v2_Promo', 'standard_d12': 'Standard_D12', 'standard_d12_v2': 'Standard_D12_v2', 'standard_d12_v2_promo': 'Standard_D12_v2_Promo', 'standard_d13': 'Standard_D13', 'standard_d13_v2': 'Standard_D13_v2', 'standard_d13_v2_promo': 'Standard_D13_v2_Promo', 'standard_d14': 'Standard_D14', 'standard_d14_v2': 'Standard_D14_v2', 'standard_d14_v2_promo': 'Standard_D14_v2_Promo', 'standard_d15_v2': 'Standard_D15_v2', 'standard_d16_v3': 'Standard_D16_v3', 'standard_d16s_v3': 'Standard_D16s_v3', 'standard_d1_v2': 'Standard_D1_v2', 'standard_d2': 'Standard_D2', 'standard_d2_v2': 'Standard_D2_v2', 'standard_d2_v2_promo': 'Standard_D2_v2_Promo', 'standard_d2_v3': 'Standard_D2_v3', 'standard_d2s_v3': 'Standard_D2s_v3', 'standard_d3': 'Standard_D3', 'standard_d32_v3': 'Standard_D32_v3', 'standard_d32s_v3': 'Standard_D32s_v3', 'standard_d3_v2': 'Standard_D3_v2', 'standard_d3_v2_promo': 'Standard_D3_v2_Promo', 'standard_d4': 'Standard_D4', 'standard_d4_v2': 'Standard_D4_v2', 'standard_d4_v2_promo': 'Standard_D4_v2_Promo', 'standard_d4_v3': 'Standard_D4_v3', 'standard_d4s_v3': 'Standard_D4s_v3', 'standard_d5_v2': 'Standard_D5_v2', 'standard_d5_v2_promo': 'Standard_D5_v2_Promo', 'standard_d64_v3': 'Standard_D64_v3', 'standard_d64s_v3': 'Standard_D64s_v3', 'standard_d8_v3': 'Standard_D8_v3', 'standard_d8s_v3': 'Standard_D8s_v3', 'standard_ds1': 'Standard_DS1', 'standard_ds11': 'Standard_DS11', 'standard_ds11_v2': 'Standard_DS11_v2', 'standard_ds11_v2_promo': 'Standard_DS11_v2_Promo', 'standard_ds12': 'Standard_DS12', 'standard_ds12_v2': 'Standard_DS12_v2', 'standard_ds12_v2_promo': 'Standard_DS12_v2_Promo', 'standard_ds13': 'Standard_DS13', 'standard_ds13-2_v2': 'Standard_DS13-2_v2', 'standard_ds13-4_v2': 'Standard_DS13-4_v2', 'standard_ds13_v2': 'Standard_DS13_v2', 'standard_ds13_v2_promo': 'Standard_DS13_v2_Promo', 'standard_ds14': 'Standard_DS14', 'standard_ds14-4_v2': 'Standard_DS14-4_v2', 'standard_ds14-8_v2': 'Standard_DS14-8_v2', 'standard_ds14_v2': 'Standard_DS14_v2', 'standard_ds14_v2_promo': 'Standard_DS14_v2_Promo', 'standard_ds15_v2': 'Standard_DS15_v2', 'standard_ds1_v2': 'Standard_DS1_v2', 'standard_ds2': 'Standard_DS2', 'standard_ds2_v2': 'Standard_DS2_v2', 'standard_ds2_v2_promo': 'Standard_DS2_v2_Promo', 'standard_ds3': 'Standard_DS3', 'standard_ds3_v2': 'Standard_DS3_v2', 'standard_ds3_v2_promo': 'Standard_DS3_v2_Promo', 'standard_ds4': 'Standard_DS4', 'standard_ds4_v2': 'Standard_DS4_v2', 'standard_ds4_v2_promo': 'Standard_DS4_v2_Promo', 'standard_ds5_v2': 'Standard_DS5_v2', 'standard_ds5_v2_promo': 'Standard_DS5_v2_Promo', 'standard_e16_v3': 'Standard_E16_v3', 'standard_e16s_v3': 'Standard_E16s_v3', 'standard_e2_v3': 'Standard_E2_v3', 'standard_e2s_v3': 'Standard_E2s_v3', 'standard_e32-16s_v3': 'Standard_E32-16s_v3', 'standard_e32-8s_v3': 'Standard_E32-8s_v3', 'standard_e32_v3': 'Standard_E32_v3', 'standard_e32s_v3': 'Standard_E32s_v3', 'standard_e4_v3': 'Standard_E4_v3', 'standard_e4s_v3': 'Standard_E4s_v3', 'standard_e64-16s_v3': 'Standard_E64-16s_v3', 'standard_e64-32s_v3': 'Standard_E64-32s_v3', 'standard_e64_v3': 'Standard_E64_v3', 'standard_e64s_v3': 'Standard_E64s_v3', 'standard_e8_v3': 'Standard_E8_v3', 'standard_e8s_v3': 'Standard_E8s_v3', 'standard_f1': 'Standard_F1', 'standard_f16': 'Standard_F16', 'standard_f16s': 'Standard_F16s', 'standard_f16s_v2': 'Standard_F16s_v2', 'standard_f1s': 'Standard_F1s', 'standard_f2': 'Standard_F2', 'standard_f2s': 'Standard_F2s', 'standard_f2s_v2': 'Standard_F2s_v2', 'standard_f32s_v2': 'Standard_F32s_v2', 'standard_f4': 'Standard_F4', 'standard_f4s': 'Standard_F4s', 'standard_f4s_v2': 'Standard_F4s_v2', 'standard_f64s_v2': 'Standard_F64s_v2', 'standard_f72s_v2': 'Standard_F72s_v2', 'standard_f8': 'Standard_F8', 'standard_f8s': 'Standard_F8s', 'standard_f8s_v2': 'Standard_F8s_v2', 'standard_g1': 'Standard_G1', 'standard_g2': 'Standard_G2', 'standard_g3': 'Standard_G3', 'standard_g4': 'Standard_G4', 'standard_g5': 'Standard_G5', 'standard_gs1': 'Standard_GS1', 'standard_gs2': 'Standard_GS2', 'standard_gs3': 'Standard_GS3', 'standard_gs4': 'Standard_GS4', 'standard_gs4-4': 'Standard_GS4-4', 'standard_gs4-8': 'Standard_GS4-8', 'standard_gs5': 'Standard_GS5', 'standard_gs5-16': 'Standard_GS5-16', 'standard_gs5-8': 'Standard_GS5-8', 'standard_h16': 'Standard_H16', 'standard_h16m': 'Standard_H16m', 'standard_h16mr': 'Standard_H16mr', 'standard_h16r': 'Standard_H16r', 'standard_h8': 'Standard_H8', 'standard_h8m': 'Standard_H8m', 'standard_l16s': 'Standard_L16s', 'standard_l32s': 'Standard_L32s', 'standard_l4s': 'Standard_L4s', 'standard_l8s': 'Standard_L8s', 'standard_m128-32ms': 'Standard_M128-32ms', 'standard_m128-64ms': 'Standard_M128-64ms', 'standard_m128ms': 'Standard_M128ms', 'standard_m128s': 'Standard_M128s', 'standard_m64-16ms': 'Standard_M64-16ms', 'standard_m64-32ms': 'Standard_M64-32ms', 'standard_m64ms': 'Standard_M64ms', 'standard_m64s': 'Standard_M64s', 'standard_nc12': 'Standard_NC12', 'standard_nc12s_v2': 'Standard_NC12s_v2', 'standard_nc12s_v3': 'Standard_NC12s_v3', 'standard_nc24': 'Standard_NC24', 'standard_nc24r': 'Standard_NC24r', 'standard_nc24rs_v2': 'Standard_NC24rs_v2', 'standard_nc24rs_v3': 'Standard_NC24rs_v3', 'standard_nc24s_v2': 'Standard_NC24s_v2', 'standard_nc24s_v3': 'Standard_NC24s_v3', 'standard_nc6': 'Standard_NC6', 'standard_nc6s_v2': 'Standard_NC6s_v2', 'standard_nc6s_v3': 'Standard_NC6s_v3', 'standard_nd12s': 'Standard_ND12s', 'standard_nd24rs': 'Standard_ND24rs', 'standard_nd24s': 'Standard_ND24s', 'standard_nd6s': 'Standard_ND6s', 'standard_nv12': 'Standard_NV12', 'standard_nv24': 'Standard_NV24', 'standard_nv6': 'Standard_NV6'})
        dict_camelize(self.parameters, ['agent_pool_profiles', 'os_type'], True)
        dict_camelize(self.parameters, ['agent_pool_profiles', 'type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Managed Cluster instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
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


def main():
    """Main execution"""
    AzureRMManagedCluster()


if __name__ == '__main__':
    main()

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
module: azure_rm_openshiftmanagedcluster
version_added: "2.8"
short_description: Manage Open Shift Managed Cluster instance.
description:
    - Create, update and delete instance of Open Shift Managed Cluster.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    resource_name:
        description:
            - The name of the openshift managed cluster resource.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    plan:
        description:
            - Define the resource plan as required by ARM for billing purposes
        suboptions:
            name:
                description:
                    - The plan ID.
            product:
                description:
                    - Specifies the product of the image from the marketplace. This is the same value as Offer under the imageReference element.
            promotion_code:
                description:
                    - The promotion code.
            publisher:
                description:
                    - The plan ID.
    open_shift_version:
        description:
            - Version of OpenShift specified when creating the cluster.
        required: True
    public_hostname:
        description:
            - Optional user-specified I(fqdn) for OpenShift API server.
    fqdn:
        description:
            - User-specified FQDN for OpenShift API server loadbalancer internal hostname.
    network_profile:
        description:
            - Configuration for OpenShift networking.
        suboptions:
            vnet_cidr:
                description:
                    - CIDR for the OpenShift Vnet.
            peer_vnet_id:
                description:
                    - CIDR of the Vnet to peer.
    router_profiles:
        description:
            - Configuration for OpenShift router(s).
        type: list
        suboptions:
            name:
                description:
                    - Name of the router profile.
            public_subdomain:
                description:
                    - DNS subdomain for openshift router.
    master_pool_profile:
        description:
            - Configuration for OpenShift master VMs.
        suboptions:
            name:
                description:
                    - Unique name of the master pool profile in the context of the subscription and resource group.
            count:
                description:
                    - Number of masters (VMs) to host docker containers. The default value is 3.
                required: True
            vm_size:
                description:
                    - Size of agent VMs.
                required: True
                choices:
                    - 'standard_d2s_v3'
                    - 'standard_d4s_v3'
            subnet_cidr:
                description:
                    - Subnet CIDR for the peering.
            os_type:
                description:
                    - OsType to be used to specify os type. Choose from C(linux) and C(windows). Default to C(linux).
                choices:
                    - 'linux'
                    - 'windows'
    agent_pool_profiles:
        description:
            - Configuration of OpenShift cluster VMs.
        type: list
        suboptions:
            name:
                description:
                    - Unique name of the pool profile in the context of the subscription and resource group.
                required: True
            count:
                description:
                    - Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 5 (inclusive). The default value is 2.
                required: True
            vm_size:
                description:
                    - Size of agent VMs.
                required: True
                choices:
                    - 'standard_d2s_v3'
                    - 'standard_d4s_v3'
            subnet_cidr:
                description:
                    - Subnet CIDR for the peering.
            os_type:
                description:
                    - OsType to be used to specify os type. Choose from C(linux) and C(windows). Default to C(linux).
                choices:
                    - 'linux'
                    - 'windows'
            role:
                description:
                    - Define the role of the AgentPoolProfile.
                choices:
                    - 'compute'
                    - 'infra'
    auth_profile:
        description:
            - Configures OpenShift authentication.
        suboptions:
            identity_providers:
                description:
                    - Type of authentication profile to use.
                type: list
                suboptions:
                    name:
                        description:
                            - Name of the I(provider).
                    provider:
                        description:
                            - Configuration of the provider.
                        suboptions:
                            kind:
                                description:
                                    - Constant filled by server.
                                required: True
    state:
      description:
        - Assert the state of the Open Shift Managed Cluster.
        - Use 'present' to create or update an Open Shift Managed Cluster and 'absent' to delete it.
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
  - name: Create (or update) Open Shift Managed Cluster
    azure_rm_openshiftmanagedcluster:
      resource_group: rg1
      resource_name: clustername1
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/subid1/resourcegroups/rg1/providers/Microsoft.ContainerService/openShiftManagedClusters/clustername1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.openshiftmanagedclusters import ContainerServiceClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOpenShiftManagedClusters(AzureRMModuleBase):
    """Configuration class for an Azure RM Open Shift Managed Cluster resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            plan=dict(
                type='dict'
            ),
            open_shift_version=dict(
                type='str',
                required=True
            ),
            public_hostname=dict(
                type='str'
            ),
            fqdn=dict(
                type='str'
            ),
            network_profile=dict(
                type='dict'
            ),
            router_profiles=dict(
                type='list'
            ),
            master_pool_profile=dict(
                type='dict'
            ),
            agent_pool_profiles=dict(
                type='list'
            ),
            auth_profile=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.resource_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMOpenShiftManagedClusters, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "plan":
                    self.parameters["plan"] = kwargs[key]
                elif key == "open_shift_version":
                    self.parameters["open_shift_version"] = kwargs[key]
                elif key == "public_hostname":
                    self.parameters["public_hostname"] = kwargs[key]
                elif key == "fqdn":
                    self.parameters["fqdn"] = kwargs[key]
                elif key == "network_profile":
                    self.parameters["network_profile"] = kwargs[key]
                elif key == "router_profiles":
                    self.parameters["router_profiles"] = kwargs[key]
                elif key == "master_pool_profile":
                    ev = kwargs[key]
                    if 'vm_size' in ev:
                        if ev['vm_size'] == 'standard_d2s_v3':
                            ev['vm_size'] = 'Standard_D2s_v3'
                        elif ev['vm_size'] == 'standard_d4s_v3':
                            ev['vm_size'] = 'Standard_D4s_v3'
                    if 'os_type' in ev:
                        if ev['os_type'] == 'linux':
                            ev['os_type'] = 'Linux'
                        elif ev['os_type'] == 'windows':
                            ev['os_type'] = 'Windows'
                    self.parameters["master_pool_profile"] = ev
                elif key == "agent_pool_profiles":
                    ev = kwargs[key]
                    if 'vm_size' in ev:
                        if ev['vm_size'] == 'standard_d2s_v3':
                            ev['vm_size'] = 'Standard_D2s_v3'
                        elif ev['vm_size'] == 'standard_d4s_v3':
                            ev['vm_size'] = 'Standard_D4s_v3'
                    if 'os_type' in ev:
                        if ev['os_type'] == 'linux':
                            ev['os_type'] = 'Linux'
                        elif ev['os_type'] == 'windows':
                            ev['os_type'] = 'Windows'
                    self.parameters["agent_pool_profiles"] = ev
                elif key == "auth_profile":
                    self.parameters["auth_profile"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ContainerServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_openshiftmanagedcluster()

        if not old_response:
            self.log("Open Shift Managed Cluster instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Open Shift Managed Cluster instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Open Shift Managed Cluster instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Open Shift Managed Cluster instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_openshiftmanagedcluster()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Open Shift Managed Cluster instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_openshiftmanagedcluster()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_openshiftmanagedcluster():
                time.sleep(20)
        else:
            self.log("Open Shift Managed Cluster instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_openshiftmanagedcluster(self):
        '''
        Creates or updates Open Shift Managed Cluster with the specified configuration.

        :return: deserialized Open Shift Managed Cluster instance state dictionary
        '''
        self.log("Creating / Updating the Open Shift Managed Cluster instance {0}".format(self.resource_name))

        try:
            response = self.mgmt_client.open_shift_managed_clusters.create_or_update(resource_group_name=self.resource_group,
                                                                                     resource_name=self.resource_name,
                                                                                     parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Open Shift Managed Cluster instance.')
            self.fail("Error creating the Open Shift Managed Cluster instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_openshiftmanagedcluster(self):
        '''
        Deletes specified Open Shift Managed Cluster instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Open Shift Managed Cluster instance {0}".format(self.resource_name))
        try:
            response = self.mgmt_client.open_shift_managed_clusters.delete(resource_group_name=self.resource_group,
                                                                           resource_name=self.resource_name)
        except CloudError as e:
            self.log('Error attempting to delete the Open Shift Managed Cluster instance.')
            self.fail("Error deleting the Open Shift Managed Cluster instance: {0}".format(str(e)))

        return True

    def get_openshiftmanagedcluster(self):
        '''
        Gets the properties of the specified Open Shift Managed Cluster.

        :return: deserialized Open Shift Managed Cluster instance state dictionary
        '''
        self.log("Checking if the Open Shift Managed Cluster instance {0} is present".format(self.resource_name))
        found = False
        try:
            response = self.mgmt_client.open_shift_managed_clusters.get(resource_group_name=self.resource_group,
                                                                        resource_name=self.resource_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Open Shift Managed Cluster instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Open Shift Managed Cluster instance.')
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
    AzureRMOpenShiftManagedClusters()


if __name__ == '__main__':
    main()

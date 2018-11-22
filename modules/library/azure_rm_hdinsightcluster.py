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
module: azure_rm_hdinsightcluster
version_added: "2.8"
short_description: Manage Azure Cluster instance.
description:
    - Create, update and delete instance of Azure Cluster.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the cluster.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    cluster_version:
        description:
            - The version of the cluster.
    os_type:
        description:
            - The type of operating system.
        choices:
            - 'windows'
            - 'linux'
    tier:
        description:
            - The cluster tier.
        choices:
            - 'standard'
            - 'premium'
    cluster_definition:
        description:
            - The cluster definition.
        suboptions:
            blueprint:
                description:
                    - The link to the blueprint.
            kind:
                description:
                    - The type of cluster.
            component_version:
                description:
                    - The versions of different services in the cluster.
            configurations:
                description:
                    - The cluster configurations.
    security_profile:
        description:
            - The security profile.
        suboptions:
            directory_type:
                description:
                    - The directory type.
                choices:
                    - 'active_directory'
            domain:
                description:
                    - "The organization's active directory domain."
            organizational_unit_dn:
                description:
                    - The organizational unit within the Active Directory to place the cluster and service accounts.
            ldaps_urls:
                description:
                    - The LDAPS protocol URLs to communicate with the Active Directory.
                type: list
            domain_username:
                description:
                    - The I(domain) user account that will have admin privileges on the cluster.
            domain_user_password:
                description:
                    - The I(domain) admin password.
            cluster_users_group_dns:
                description:
                    - Optional. The Distinguished Names for cluster user groups
                type: list
            aadds_resource_id:
                description:
                    - "The resource ID of the user's Azure Active Directory I(domain) Service."
            msi_resource_id:
                description:
                    - "User assigned identity that has permissions to read and create cluster-related artifacts in the user's AADDS."
    compute_profile_roles:
        description:
            - The list of roles in the cluster.
        type: list
        suboptions:
            name:
                description:
                    - The name of the role.
            min_instance_count:
                description:
                    - The minimum instance count of the cluster.
            target_instance_count:
                description:
                    - The instance count of the cluster.
            vm_size:
                description:
                    - The size of the VM
            linux_profile:
                description:
                    - The Linux OS profile.
            virtual_network_profile:
                description:
                    - The virtual network profile.
                suboptions:
                    id:
                        description:
                            - The ID of the virtual network.
                    subnet:
                        description:
                            - The name of the subnet.
            data_disks_groups:
                description:
                    - The data disks groups for the role.
                type: list
                suboptions:
                    disks_per_node:
                        description:
                            - The number of disks per node.
            script_actions:
                description:
                    - The list of script actions on the role.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the script action.
                            - Required when C(state) is I(present).
                    uri:
                        description:
                            - The URI to the script.
                            - Required when C(state) is I(present).
                    parameters:
                        description:
                            - The parameters for the script provided.
                            - Required when C(state) is I(present).
    storage_accounts:
        description:
            - The list of storage accounts in the cluster.
        type: list
        suboptions:
            name:
                description:
                    - The name of the storage account.
            is_default:
                description:
                    - Whether or not the storage account is the default storage account.
            container:
                description:
                    - The container in the storage account, only to be specified for WASB storage accounts.
            file_system:
                description:
                    - The filesystem, only to be specified for Azure Data Lake Storage Gen 2.
            key:
                description:
                    - The storage account access key.
    identity:
        description:
            - The identity of the cluster, if configured.
        suboptions:
            type:
                description:
                    - "The type of identity used for the cluster. The type 'C(system_assigned), C(user_assigned)' includes both an implicitly created
                       identity and a set of user assigned identities."
                choices:
                    - 'system_assigned'
                    - 'user_assigned'
                    - 'system_assigned, _user_assigned'
                    - 'none'
            user_assigned_identities:
                description:
                    - "The list of user identities associated with the cluster. The user identity dictionary key references will be ARM resource ids in the
                       form:
                       '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{ident
                      ityName}'."
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
    azure_rm_hdinsightcluster:
      resource_group: rg1
      name: cluster1
      location: eastus
      cluster_version: 3.5
      os_type: Linux
      tier: Standard
      cluster_definition:
        kind: Hadoop
        configurations: {
  "gateway": {
    "restAuthCredential.isEnabled": "true",
    "restAuthCredential.username": "admin",
    "restAuthCredential.password": "**********"
  }
}
      compute_profile_roles:
        - name: headnode
          min_instance_count: 1
          target_instance_count: 2
          vm_size: Standard_D3_V2
          linux_profile: {
  "username": "sshuser",
  "password": "**********"
}
      storage_accounts:
        - name: mystorage
          is_default: True
          container: containername
          key: storagekey
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.HDInsight/clusters/cluster1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.hdinsight import HDInsightManagementClient
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
            cluster_version=dict(
                type='str'
            ),
            os_type=dict(
                type='str',
                choices=['windows',
                         'linux']
            ),
            tier=dict(
                type='str',
                choices=['standard',
                         'premium']
            ),
            cluster_definition=dict(
                type='dict'
            ),
            security_profile=dict(
                type='dict'
            ),
            compute_profile_roles=dict(
                type='list'
            ),
            storage_accounts=dict(
                type='list'
            ),
            identity=dict(
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

        dict_expand(self.parameters, ['cluster_version'])
        dict_expand(self.parameters, ['os_type'])
        dict_camelize(self.parameters, ['os_type'], True)
        dict_expand(self.parameters, ['tier'])
        dict_camelize(self.parameters, ['tier'], True)
        dict_expand(self.parameters, ['cluster_definition'])
        dict_camelize(self.parameters, ['security_profile', 'directory_type'], True)
        dict_expand(self.parameters, ['security_profile'])
        dict_expand(self.parameters, ['compute_profile_roles', 'vm_size'])
        dict_rename(self.parameters, ['compute_profile_roles', 'linux_profile'], 'os_profile')
        dict_expand(self.parameters, ['compute_profile_roles', 'linux_profile'])
        dict_rename(self.parameters, ['compute_profile_roles'], 'compute_profile')
        dict_expand(self.parameters, ['compute_profile_roles'])
        dict_expand(self.parameters, ['compute_profile'])
        dict_rename(self.parameters, ['storage_accounts'], 'storage_profile')
        dict_expand(self.parameters, ['storage_accounts'])
        dict_expand(self.parameters, ['storage_profile'])
        dict_camelize(self.parameters, ['identity', 'type'], True)
        dict_map(self.parameters, ['identity', 'type'], ''system_assigned, _user_assigned': 'SystemAssigned, UserAssigned'')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(HDInsightManagementClient,
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
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_cluster():
                time.sleep(20)
        else:
            self.log("Cluster instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
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
    AzureRMCluster()


if __name__ == '__main__':
    main()

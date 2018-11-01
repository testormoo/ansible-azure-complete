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
module: azure_rm_kustocluster
version_added: "2.8"
short_description: Manage Cluster instance.
description:
    - Create, update and delete instance of Cluster.

options:
    resource_group:
        description:
            - The name of the resource group containing the Kusto cluster.
        required: True
    cluster_name:
        description:
            - The name of the Kusto cluster.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The SKU of the cluster.
        required: True
        suboptions:
            name:
                description:
                    - SKU name.
                required: True
                choices:
                    - 'kc8'
                    - 'kc16'
                    - 'ks8'
                    - 'ks16'
                    - 'd13_v2'
                    - 'd14_v2'
                    - 'l8'
                    - 'l16'
            capacity:
                description:
                    - SKU capacity.
            tier:
                description:
                    - SKU tier.
                required: True
    trusted_external_tenants:
        description:
            - "The cluster's external tenants."
        type: list
        suboptions:
            value:
                description:
                    - GUID representing an external tenant.
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
    azure_rm_kustocluster:
      resource_group: kustorptest
      cluster_name: KustoClusterRPTest4
      location: eastus
      sku:
        name: L8
        capacity: 2
        tier: Standard
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/12345678-1234-1234-1234-123456789098/resourceGroups/kustorptest/providers/Microsoft.Kusto/Clusters/KustoClusterRPTest4
state:
    description:
        - "The state of the resource. Possible values include: 'Creating', 'Unavailable', 'Running', 'Deleting', 'Deleted', 'Stopping', 'Stopped',
           'Starting'"
    returned: always
    type: str
    sample: state
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.kusto import KustoManagementClient
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
            cluster_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                required=True
            ),
            trusted_external_tenants=dict(
                type='list'
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
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'kc8':
                            ev['name'] = 'KC8'
                        elif ev['name'] == 'kc16':
                            ev['name'] = 'KC16'
                        elif ev['name'] == 'ks8':
                            ev['name'] = 'KS8'
                        elif ev['name'] == 'ks16':
                            ev['name'] = 'KS16'
                        elif ev['name'] == 'd13_v2':
                            ev['name'] = 'D13_v2'
                        elif ev['name'] == 'd14_v2':
                            ev['name'] = 'D14_v2'
                        elif ev['name'] == 'l8':
                            ev['name'] = 'L8'
                        elif ev['name'] == 'l16':
                            ev['name'] = 'L16'
                    self.parameters["sku"] = ev
                elif key == "trusted_external_tenants":
                    self.parameters["trusted_external_tenants"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(KustoManagementClient,
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
                self.log("Need to check if Cluster instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Cluster instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_cluster()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
        self.log("Creating / Updating the Cluster instance {0}".format(self.cluster_name))

        try:
            response = self.mgmt_client.clusters.create_or_update(resource_group_name=self.resource_group,
                                                                  cluster_name=self.cluster_name,
                                                                  parameters=self.parameters)
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
        self.log("Deleting the Cluster instance {0}".format(self.cluster_name))
        try:
            response = self.mgmt_client.clusters.delete(resource_group_name=self.resource_group,
                                                        cluster_name=self.cluster_name)
        except CloudError as e:
            self.log('Error attempting to delete the Cluster instance.')
            self.fail("Error deleting the Cluster instance: {0}".format(str(e)))

        return True

    def get_cluster(self):
        '''
        Gets the properties of the specified Cluster.

        :return: deserialized Cluster instance state dictionary
        '''
        self.log("Checking if the Cluster instance {0} is present".format(self.cluster_name))
        found = False
        try:
            response = self.mgmt_client.clusters.get(resource_group_name=self.resource_group,
                                                     cluster_name=self.cluster_name)
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
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMClusters()


if __name__ == '__main__':
    main()

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
module: azure_rm_machinelearningcomputeoperationalizationcluster_facts
version_added: "2.8"
short_description: Get Azure Operationalization Cluster facts.
description:
    - Get facts of Azure Operationalization Cluster.

options:
    resource_group:
        description:
            - Name of the resource group in which the cluster is located.
    cluster_name:
        description:
            - The name of the cluster.
    skiptoken:
        description:
            - Continuation token for pagination.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Operationalization Cluster
    azure_rm_machinelearningcomputeoperationalizationcluster_facts:
      resource_group: resource_group_name
      cluster_name: cluster_name

  - name: List instances of Operationalization Cluster
    azure_rm_machinelearningcomputeoperationalizationcluster_facts:
      resource_group: resource_group_name
      skiptoken: skiptoken

  - name: List instances of Operationalization Cluster
    azure_rm_machinelearningcomputeoperationalizationcluster_facts:
      skiptoken: skiptoken
'''

RETURN = '''
operationalization_clusters:
    description: A list of dictionaries containing facts for Operationalization Cluster.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Specifies the resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.MachineLearningCompute/operationa
                    lizationClusters/myCluster"
        name:
            description:
                - Specifies the name of the resource.
            returned: always
            type: str
            sample: myCluster
        location:
            description:
                - Specifies the location of the resource.
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Contains resource tags defined as key/value pairs.
            returned: always
            type: complex
            sample: "{\n  'key1': 'alpha',\n  'key2': 'beta'\n}"
        description:
            description:
                - The description of the cluster.
            returned: always
            type: str
            sample: My Operationalization Cluster
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.machinelearningcompute import MachineLearningComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMOperationalizationClustersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            cluster_name=dict(
                type='str'
            ),
            skiptoken=dict(
                type='str'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.cluster_name = None
        self.skiptoken = None
        self.tags = None
        super(AzureRMOperationalizationClustersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MachineLearningComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.cluster_name is not None):
            self.results['operationalization_clusters'] = self.get()
        elif self.resource_group is not None:
            self.results['operationalization_clusters'] = self.list_by_resource_group()
        else:
            self.results['operationalization_clusters'] = self.list_by_subscription_id()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.operationalization_clusters.get(resource_group_name=self.resource_group,
                                                                        cluster_name=self.cluster_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for OperationalizationClusters.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.operationalization_clusters.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for OperationalizationClusters.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription_id(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.operationalization_clusters.list_by_subscription_id()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for OperationalizationClusters.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'description': d.get('description', None)
        }
        return d


def main():
    AzureRMOperationalizationClustersFacts()


if __name__ == '__main__':
    main()

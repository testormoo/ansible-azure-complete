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
module: azure_rm_hdinsightcluster_facts
version_added: "2.8"
short_description: Get Azure Cluster facts.
description:
    - Get facts of Cluster.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    cluster_name:
        description:
            - The name of the cluster.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Cluster
    azure_rm_hdinsightcluster_facts:
      resource_group: resource_group_name
      cluster_name: cluster_name

  - name: List instances of Cluster
    azure_rm_hdinsightcluster_facts:
      resource_group: resource_group_name
'''

RETURN = '''
clusters:
    description: A list of dictionaries containing facts for Clusters.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.HDInsight/clusters/cluster1
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: cluster1
        location:
            description:
                - The Azure Region where the resource lives
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: "{\n  'key1': 'val1'\n}"
        etag:
            description:
                - The ETag for the resource
            returned: always
            type: str
            sample: f0212a39-b827-45e0-9ffa-4f5232e58851
        properties:
            description:
                - The properties of the cluster.
            returned: always
            type: complex
            sample: properties
            contains:
                tier:
                    description:
                        - "The cluster tier. Possible values include: 'Standard', 'Premium'"
                    returned: always
                    type: str
                    sample: Standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.hdinsight import HDInsightManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMClustersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
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
        self.tags = None
        super(AzureRMClustersFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(HDInsightManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.cluster_name is not None):
            self.results['clusters'] = self.get()
        elif (self.resource_group is not None):
            self.results['clusters'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.clusters.get(resource_group_name=self.resource_group,
                                                     cluster_name=self.cluster_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Clusters.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.clusters.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Clusters.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        #d = {
        #    'resource_group': self.resource_group,
        #    'id': d['id'],
        #    'name': d['name'],
        #    'location': d['location'],
        #    'etag': d['etag']
        #}
        return d


def main():
    AzureRMClustersFacts()


if __name__ == '__main__':
    main()

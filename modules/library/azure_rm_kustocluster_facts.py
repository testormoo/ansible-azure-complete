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
module: azure_rm_kustocluster_facts
version_added: "2.8"
short_description: Get Azure Cluster facts.
description:
    - Get facts of Azure Cluster.

options:
    resource_group:
        description:
            - The name of the resource group containing the Kusto cluster.
        required: True
    cluster_name:
        description:
            - The name of the Kusto cluster.
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
    azure_rm_kustocluster_facts:
      resource_group: resource_group_name
      cluster_name: cluster_name

  - name: List instances of Cluster
    azure_rm_kustocluster_facts:
      resource_group: resource_group_name
'''

RETURN = '''
clusters:
    description: A list of dictionaries containing facts for Cluster.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: /subscriptions/12345678-1234-1234-1234-123456789098/resourceGroups/kustorptest/providers/Microsoft.Kusto/Clusters/KustoClusterRPTest4
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: KustoClusterRPTest4
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        location:
            description:
                - The geo-location where the resource lives
            returned: always
            type: str
            sample: westus
        etag:
            description:
                - An ETag of the resource created.
            returned: always
            type: str
            sample: "W/'datetime'2017-12-06T12%3A05%3A57.2528942Z''"
        sku:
            description:
                - The SKU of the cluster.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "SKU name. Possible values include: 'KC8', 'KC16', 'KS8', 'KS16', 'D13_v2', 'D14_v2', 'L8', 'L16'"
                    returned: always
                    type: str
                    sample: L8
                capacity:
                    description:
                        - SKU capacity.
                    returned: always
                    type: int
                    sample: 2
                tier:
                    description:
                        - SKU tier.
                    returned: always
                    type: str
                    sample: Standard
        state:
            description:
                - "The state of the resource. Possible values include: 'Creating', 'Unavailable', 'Running', 'Deleting', 'Deleted', 'Stopping', 'Stopped',
                   'Starting'"
            returned: always
            type: str
            sample: state
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.kusto import KustoManagementClient
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
        super(AzureRMClustersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(KustoManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.cluster_name is not None:
            self.results['clusters'] = self.get()
        else:
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
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'etag': d.get('etag', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'capacity': d.get('sku', {}).get('capacity', None),
                'tier': d.get('sku', {}).get('tier', None)
            },
            'state': d.get('state', None)
        }
        return d


def main():
    AzureRMClustersFacts()


if __name__ == '__main__':
    main()

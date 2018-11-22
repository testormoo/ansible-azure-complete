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
module: azure_rm_containerserviceopenshiftmanagedcluster_facts
version_added: "2.8"
short_description: Get Azure Open Shift Managed Cluster facts.
description:
    - Get facts of Azure Open Shift Managed Cluster.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the openshift managed cluster resource.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Open Shift Managed Cluster
    azure_rm_containerserviceopenshiftmanagedcluster_facts:
      resource_group: resource_group_name
      name: resource_name
'''

RETURN = '''
open_shift_managed_clusters:
    description: A list of dictionaries containing facts for Open Shift Managed Cluster.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/subid1/resourcegroups/rg1/providers/Microsoft.ContainerService/openShiftManagedClusters/clustername1
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: clustername1
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: location1
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'archv2': '',\n  'tier': 'production'\n}"
        fqdn:
            description:
                - User-specified FQDN for OpenShift API server loadbalancer internal hostname.
            returned: always
            type: str
            sample: clustername1.location1.cloudapp.azure.com
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.containerservice import ContainerServiceClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMOpenShiftManagedClusterFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
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
        self.name = None
        self.tags = None
        super(AzureRMOpenShiftManagedClusterFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ContainerServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['open_shift_managed_clusters'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.open_shift_managed_clusters.get(resource_group_name=self.resource_group,
                                                                        resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Open Shift Managed Cluster.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'fqdn': d.get('fqdn', None)
        }
        return d


def main():
    AzureRMOpenShiftManagedClusterFacts()


if __name__ == '__main__':
    main()

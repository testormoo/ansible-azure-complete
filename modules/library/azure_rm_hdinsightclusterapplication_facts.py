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
module: azure_rm_hdinsightclusterapplication_facts
version_added: "2.8"
short_description: Get Azure Application facts.
description:
    - Get facts of Application.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    cluster_name:
        description:
            - The name of the cluster.
        required: True
    application_name:
        description:
            - The constant value for the application name.
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
  - name: Get instance of Application
    azure_rm_hdinsightclusterapplication_facts:
      resource_group: resource_group_name
      cluster_name: cluster_name
      application_name: application_name
'''

RETURN = '''
applications:
    description: A list of dictionaries containing facts for Applications.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource.
            returned: always
            type: str
            sample: /subscriptions/subId/resourceGroups/rg1/providers/Microsoft.HDInsight/clusters/cluster1/applications/app
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: app
        etag:
            description:
                - The ETag for the application
            returned: always
            type: str
            sample: CF938302-6B4D-44A0-A6D2-C0D67E847AEC
        tags:
            description:
                - The tags for the application.
            returned: always
            type: complex
            sample: "{\n  'key1': 'val1'\n}"
        properties:
            description:
                - The properties of the application.
            returned: always
            type: complex
            sample: properties
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.cluster import HDInsightManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApplicationsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
                type='str',
                required=True
            ),
            application_name=dict(
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
        self.cluster_name = None
        self.application_name = None
        self.tags = None
        super(AzureRMApplicationsFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(HDInsightManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.cluster_name is not None and
                self.application_name is not None):
            self.results['applications'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.applications.get(resource_group_name=self.resource_group,
                                                         cluster_name=self.cluster_name,
                                                         application_name=self.application_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Applications.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d['id'],
            'name': d['name'],
            'etag': d['etag'],
            'tags': d['tags'],
            'properties': d{
            }
        }
        return d


def main():
    AzureRMApplicationsFacts()


if __name__ == '__main__':
    main()

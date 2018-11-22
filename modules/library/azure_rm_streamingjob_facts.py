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
module: azure_rm_streamingjob_facts
version_added: "2.8"
short_description: Get Azure Streaming Job facts.
description:
    - Get facts of Azure Streaming Job.

options:
    expand:
        description:
            - "The $expand OData query parameter. This is a comma-separated list of additional streaming job properties to include in the response, beyond
               the default set returned when this parameter is absent. The default set is all streaming job properties other than 'inputs',
               'transformation', 'outputs', and 'functions'."
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the streaming job.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Streaming Job
    azure_rm_streamingjob_facts:
      expand: expand
      resource_group: resource_group_name
      name: job_name

  - name: List instances of Streaming Job
    azure_rm_streamingjob_facts:
      expand: expand
      resource_group: resource_group_name
'''

RETURN = '''
streaming_jobs:
    description: A list of dictionaries containing facts for Streaming Job.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/56b5e0a9-b645-407d-99b0-c64f86013e3d/resourceGroups/sjrg6936/providers/Microsoft.StreamAnalytics/streamingjobs/sj59
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: sj59
        location:
            description:
                - Resource location. Required on PUT (CreateOrReplace) requests.
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'key1': 'value1',\n  'randomKey': 'randomValue',\n  'key3': 'value3'\n}"
        sku:
            description:
                - Describes the SKU of the streaming job. Required on PUT (CreateOrReplace) requests.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The name of the SKU. Required on PUT (CreateOrReplace) requests. Possible values include: 'Standard'"
                    returned: always
                    type: str
                    sample: Standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.streamingjobs import StreamAnalyticsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMStreamingJobFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            expand=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.expand = None
        self.resource_group = None
        self.name = None
        self.tags = None
        super(AzureRMStreamingJobFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StreamAnalyticsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['streaming_jobs'] = self.get()
        else:
            self.results['streaming_jobs'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.streaming_jobs.get(resource_group_name=self.resource_group,
                                                           job_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Streaming Job.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.streaming_jobs.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Streaming Job.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            }
        }
        return d


def main():
    AzureRMStreamingJobFacts()


if __name__ == '__main__':
    main()

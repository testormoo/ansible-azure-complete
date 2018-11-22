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
module: azure_rm_datafactorydataset_facts
version_added: "2.8"
short_description: Get Azure Dataset facts.
description:
    - Get facts of Azure Dataset.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    name:
        description:
            - The dataset name.
    if_none_match:
        description:
            - "ETag of the dataset entity. Should only be specified for get. If the ETag matches the existing entity tag, or if * was provided, then no
               content will be returned."

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Dataset
    azure_rm_datafactorydataset_facts:
      resource_group: resource_group_name
      factory_name: factory_name
      name: dataset_name
      if_none_match: if_none_match

  - name: List instances of Dataset
    azure_rm_datafactorydataset_facts:
      resource_group: resource_group_name
      factory_name: factory_name
'''

RETURN = '''
datasets:
    description: A list of dictionaries containing facts for Dataset.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/example
                    FactoryName/datasets/exampleDataset"
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: exampleDataset
        etag:
            description:
                - Etag identifies change in the resource.
            returned: always
            type: str
            sample: 0a0068d4-0000-0000-0000-5b245bd30000
        properties:
            description:
                - Dataset properties.
            returned: always
            type: complex
            sample: properties
            contains:
                description:
                    description:
                        - Dataset description.
                    returned: always
                    type: str
                    sample: Example description
                parameters:
                    description:
                        - Parameters for dataset.
                    returned: always
                    type: complex
                    sample: "{\n  'MyFolderPath': {\n    'type': 'String'\n  },\n  'MyFileName': {\n    'type': 'String'\n  }\n}"
                type:
                    description:
                        - Constant filled by server.
                    returned: always
                    type: str
                    sample: AzureBlob
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDatasetFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            factory_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            if_none_match=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.factory_name = None
        self.name = None
        self.if_none_match = None
        super(AzureRMDatasetFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['datasets'] = self.get()
        else:
            self.results['datasets'] = self.list_by_factory()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.datasets.get(resource_group_name=self.resource_group,
                                                     factory_name=self.factory_name,
                                                     dataset_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Dataset.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_factory(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.datasets.list_by_factory(resource_group_name=self.resource_group,
                                                                 factory_name=self.factory_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Dataset.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None),
            'properties': {
                'description': d.get('properties', {}).get('description', None),
                'parameters': d.get('properties', {}).get('parameters', None),
                'type': d.get('properties', {}).get('type', None)
            }
        }
        return d


def main():
    AzureRMDatasetFacts()


if __name__ == '__main__':
    main()

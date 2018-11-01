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
module: azure_rm_streamingjobstransformation_facts
version_added: "2.8"
short_description: Get Azure Transformation facts.
description:
    - Get facts of Azure Transformation.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    job_name:
        description:
            - The name of the streaming job.
        required: True
    transformation_name:
        description:
            - The name of the transformation.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Transformation
    azure_rm_streamingjobstransformation_facts:
      resource_group: resource_group_name
      job_name: job_name
      transformation_name: transformation_name
'''

RETURN = '''
transformations:
    description: A list of dictionaries containing facts for Transformation.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: "/subscriptions/56b5e0a9-b645-407d-99b0-c64f86013e3d/resourceGroups/sjrg4423/providers/Microsoft.StreamAnalytics/streamingjobs/sj8374/tra
                    nsformations/transformation952"
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: transformation952
        query:
            description:
                - "Specifies the query that will be run in the streaming job. You can learn more about the Stream Analytics Query Language (SAQL) here:
                   https://msdn.microsoft.com/library/azure/dn834998 . Required on PUT (CreateOrReplace) requests."
            returned: always
            type: str
            sample: Select Id, Name from inputtest
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.streamingjobs import StreamAnalyticsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTransformationsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            job_name=dict(
                type='str',
                required=True
            ),
            transformation_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.job_name = None
        self.transformation_name = None
        super(AzureRMTransformationsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StreamAnalyticsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['transformations'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.transformations.get(resource_group_name=self.resource_group,
                                                            job_name=self.job_name,
                                                            transformation_name=self.transformation_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Transformations.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'query': d.get('query', None)
        }
        return d


def main():
    AzureRMTransformationsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_databoxjob_facts
version_added: "2.8"
short_description: Get Azure Job facts.
description:
    - Get facts of Azure Job.

options:
    resource_group:
        description:
            - The Resource Group Name
        required: True
    name:
        description:
            - "The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any
               alphanumeric and underscore only"
    expand:
        description:
            - $expand is supported on details parameter for job, which provides details on the job stages.
    skip_token:
        description:
            - $skipToken is supported on Get list of jobs, which provides the next page in the list of jobs.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Job
    azure_rm_databoxjob_facts:
      resource_group: resource_group_name
      name: job_name
      expand: expand

  - name: List instances of Job
    azure_rm_databoxjob_facts:
      resource_group: resource_group_name
      skip_token: skip_token
'''

RETURN = '''
jobs:
    description: A list of dictionaries containing facts for Job.
    returned: always
    type: complex
    contains:
        location:
            description:
                - "The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia,
                   etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will
                   succeed."
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
            returned: always
            type: complex
            sample: {}
        sku:
            description:
                - The sku type.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The sku name. Possible values include: 'DataBox', 'DataBoxDisk', 'DataBoxHeavy'"
                    returned: always
                    type: str
                    sample: DataBox
        status:
            description:
                - "Name of the stage which is in progress. Possible values include: 'DeviceOrdered', 'DevicePrepared', 'Dispatched', 'Delivered',
                   'PickedUp', 'AtAzureDC', 'DataCopy', 'Completed', 'CompletedWithErrors', 'Cancelled', 'Failed_IssueReportedAtCustomer',
                   'Failed_IssueDetectedAtAzureDC', 'Aborted'"
            returned: always
            type: str
            sample: DeviceOrdered
        name:
            description:
                - Name of the object.
            returned: always
            type: str
            sample: SdkJob7196
        id:
            description:
                - Id of the object.
            returned: always
            type: str
            sample: /subscriptions/fa68082f-8ff7-4a25-95c7-ce9da541242f/resourceGroups/SdkRg8120/providers/Microsoft.DataBox/jobs/SdkJob7196
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.databox import DataBoxManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            expand=dict(
                type='str'
            ),
            skip_token=dict(
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
        self.name = None
        self.expand = None
        self.skip_token = None
        self.tags = None
        super(AzureRMJobFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataBoxManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['jobs'] = self.get()
        else:
            self.results['jobs'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.get(resource_group_name=self.resource_group,
                                                 job_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Job.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            },
            'status': d.get('status', None),
            'name': d.get('name', None),
            'id': d.get('id', None)
        }
        return d


def main():
    AzureRMJobFacts()


if __name__ == '__main__':
    main()

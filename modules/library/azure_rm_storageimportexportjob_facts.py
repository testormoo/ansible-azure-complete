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
module: azure_rm_storageimportexportjob_facts
version_added: "2.8"
short_description: Get Azure Job facts.
description:
    - Get facts of Azure Job.

options:
    top:
        description:
            - An integer value that specifies how many jobs at most should be returned. The value cannot exceed 100.
    filter:
        description:
            - Can be used to restrict the results to certain conditions.
    resource_group:
        description:
            - The resource group name uniquely identifies the resource group within the user subscription.
    self.config.accept_language:
        description:
            - Specifies the preferred language for the response.
    name:
        description:
            - The name of the import/export job.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Job
    azure_rm_storageimportexportjob_facts:
      top: top
      filter: filter
      resource_group: resource_group_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Job
    azure_rm_storageimportexportjob_facts:
      top: top
      filter: filter
      self.config.accept_language: self.config.accept_language

  - name: Get instance of Job
    azure_rm_storageimportexportjob_facts:
      name: job_name
      resource_group: resource_group_name
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
jobs:
    description: A list of dictionaries containing facts for Job.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Specifies the resource identifier of the job.
            returned: always
            type: str
            sample: /subscriptions/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/resourceGroups/Default-Storage-WestUS/providers/Microsoft.ImportExport/jobs/test
        name:
            description:
                - Specifies the name of the job.
            returned: always
            type: str
            sample: test-by1-import
        location:
            description:
                - Specifies the Azure location where the job is created.
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Specifies the tags that are assigned to the job.
            returned: always
            type: str
            sample: tags
        properties:
            description:
                - Specifies the job properties
            returned: always
            type: complex
            sample: properties
            contains:
                state:
                    description:
                        - Current state of the job.
                    returned: always
                    type: str
                    sample: Creating
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storageimportexport import StorageImportExport
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            top=dict(
                type='int'
            ),
            filter=dict(
                type='str'
            ),
            resource_group=dict(
                type='str'
            ),
            self.config.accept_language=dict(
                type='str'
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
        self.top = None
        self.filter = None
        self.resource_group = None
        self.self.config.accept_language = None
        self.name = None
        self.tags = None
        super(AzureRMJobsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorageImportExport,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None:
            self.results['jobs'] = self.list_by_resource_group()
        else:
            self.results['jobs'] = self.list_by_subscription()
        elif (self.name is not None and
                self.resource_group is not None):
            self.results['jobs'] = self.get()
        return self.results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Jobs.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Jobs.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.jobs.get(job_name=self.name,
                                                 resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Jobs.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'properties': {
                'state': d.get('properties', {}).get('state', None)
            }
        }
        return d


def main():
    AzureRMJobsFacts()


if __name__ == '__main__':
    main()

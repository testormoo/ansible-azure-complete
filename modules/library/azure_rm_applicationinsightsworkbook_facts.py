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
module: azure_rm_applicationinsightsworkbook_facts
version_added: "2.8"
short_description: Get Azure Workbook facts.
description:
    - Get facts of Azure Workbook.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    category:
        description:
            - Category of workbook to return.
    tags:
        description:
            - Tags presents on each workbook returned.
    can_fetch_content:
        description:
            - Flag indicating whether or not to return the full content for each applicable workbook. If false, only return summary content for workbooks.
    name:
        description:
            - The name of the Application Insights component resource.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Workbook
    azure_rm_applicationinsightsworkbook_facts:
      resource_group: resource_group_name
      category: category
      tags: tags
      can_fetch_content: can_fetch_content

  - name: Get instance of Workbook
    azure_rm_applicationinsightsworkbook_facts:
      resource_group: resource_group_name
      name: resource_name
'''

RETURN = '''
workbooks:
    description: A list of dictionaries containing facts for Workbook.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Azure resource Id
            returned: always
            type: str
            sample: c0deea5e-3344-40f2-96f8-6f8e1c3b5722
        name:
            description:
                - Azure resource name
            returned: always
            type: str
            sample: deadb33f-8bee-4d3b-a059-9be8dac93960
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "[\n  'TagSample01',\n  'TagSample02'\n]"
        kind:
            description:
                - "The kind of workbook. Choices are user and shared. Possible values include: 'user', 'shared'"
            returned: always
            type: str
            sample: shared
        version:
            description:
                - "This instance's version of the data model. This can change as new features are added that can be marked workbook."
            returned: always
            type: str
            sample: ME
        category:
            description:
                - Workbook category, as defined by the user at creation time.
            returned: always
            type: str
            sample: workbook
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkbookFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            category=dict(
                type='str'
            ),
            tags=dict(
                type='str'
            ),
            can_fetch_content=dict(
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
        self.resource_group = None
        self.category = None
        self.tags = None
        self.can_fetch_content = None
        self.name = None
        self.tags = None
        super(AzureRMWorkbookFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.category is not None:
            self.results['workbooks'] = self.list_by_resource_group()
        elif self.name is not None:
            self.results['workbooks'] = self.get()
        return self.results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workbooks.list_by_resource_group(resource_group_name=self.resource_group,
                                                                         category=self.category)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workbook.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workbooks.get(resource_group_name=self.resource_group,
                                                      resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workbook.')

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
            'kind': d.get('kind', None),
            'version': d.get('version', None),
            'category': d.get('category', None)
        }
        return d


def main():
    AzureRMWorkbookFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_apimanagementapiissuecomment_facts
version_added: "2.8"
short_description: Get Azure Api Issue Comment facts.
description:
    - Get facts of Azure Api Issue Comment.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - API identifier. Must be unique in the current API Management service instance.
        required: True
    issue_id:
        description:
            - Issue identifier. Must be unique in the current API Management service instance.
        required: True
    filter:
        description:
            - | Field       | Supported operators    | Supported functions               |
            - |-------------|------------------------|-----------------------------------|
            - | id          | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
            - | userId          | ge, le, eq, ne, gt, lt | substringof, startswith, endswith |
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    comment_id:
        description:
            - Comment identifier within an Issue. Must be unique in the current Issue.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Api Issue Comment
    azure_rm_apimanagementapiissuecomment_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      issue_id: issue_id
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Api Issue Comment
    azure_rm_apimanagementapiissuecomment_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      issue_id: issue_id
      comment_id: comment_id
'''

RETURN = '''
api_issue_comment:
    description: A list of dictionaries containing facts for Api Issue Comment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourcegroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/57d1f7558aa04f15146d9d8a/issues/57d2
                    ef278aa04f0ad01d6cdc/comments/599e29ab193c3c0bd0b3e2fb"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 599e29ab193c3c0bd0b3e2fb
        text:
            description:
                - Comment text.
            returned: always
            type: str
            sample: Issue comment.
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiIssueCommentFacts(AzureRMModuleBase):
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
            api_id=dict(
                type='str',
                required=True
            ),
            issue_id=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str'
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            ),
            comment_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.api_id = None
        self.issue_id = None
        self.filter = None
        self.top = None
        self.skip = None
        self.comment_id = None
        super(AzureRMApiIssueCommentFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['api_issue_comment'] = self.list_by_service()
        elif self.comment_id is not None:
            self.results['api_issue_comment'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_issue_comment.list_by_service(resource_group_name=self.resource_group,
                                                                          service_name=self.name,
                                                                          api_id=self.api_id,
                                                                          issue_id=self.issue_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ApiIssueComment.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_issue_comment.get(resource_group_name=self.resource_group,
                                                              service_name=self.name,
                                                              api_id=self.api_id,
                                                              issue_id=self.issue_id,
                                                              comment_id=self.comment_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ApiIssueComment.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'text': d.get('text', None)
        }
        return d


def main():
    AzureRMApiIssueCommentFacts()


if __name__ == '__main__':
    main()

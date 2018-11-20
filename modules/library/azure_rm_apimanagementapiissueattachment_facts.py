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
module: azure_rm_apimanagementapiissueattachment_facts
version_added: "2.8"
short_description: Get Azure Api Issue Attachment facts.
description:
    - Get facts of Azure Api Issue Attachment.

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
    attachment_id:
        description:
            - Attachment identifier within an Issue. Must be unique in the current Issue.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Api Issue Attachment
    azure_rm_apimanagementapiissueattachment_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      issue_id: issue_id
      filter: filter
      top: top
      skip: skip

  - name: Get instance of Api Issue Attachment
    azure_rm_apimanagementapiissueattachment_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      issue_id: issue_id
      attachment_id: attachment_id
'''

RETURN = '''
api_issue_attachment:
    description: A list of dictionaries containing facts for Api Issue Attachment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourcegroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/57d1f7558aa04f15146d9d8a/issues/57d2
                    ef278aa04f0ad01d6cdc/attachments/57d2ef278aa04f0888cba3f3"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 57d2ef278aa04f0888cba3f3
        title:
            description:
                - Filename by which the binary data will be saved.
            returned: always
            type: str
            sample: Issue attachment.
        content:
            description:
                - An HTTP link or Base64-encoded binary data.
            returned: always
            type: str
            sample: "https://.../image.jpg"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiIssueAttachmentFacts(AzureRMModuleBase):
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
            attachment_id=dict(
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
        self.attachment_id = None
        super(AzureRMApiIssueAttachmentFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['api_issue_attachment'] = self.list_by_service()
        elif self.attachment_id is not None:
            self.results['api_issue_attachment'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_issue_attachment.list_by_service(resource_group_name=self.resource_group,
                                                                             service_name=self.name,
                                                                             api_id=self.api_id,
                                                                             issue_id=self.issue_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ApiIssueAttachment.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_issue_attachment.get(resource_group_name=self.resource_group,
                                                                 service_name=self.name,
                                                                 api_id=self.api_id,
                                                                 issue_id=self.issue_id,
                                                                 attachment_id=self.attachment_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ApiIssueAttachment.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'title': d.get('title', None),
            'content': d.get('content', None)
        }
        return d


def main():
    AzureRMApiIssueAttachmentFacts()


if __name__ == '__main__':
    main()

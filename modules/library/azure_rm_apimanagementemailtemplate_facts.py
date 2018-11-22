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
module: azure_rm_apimanagementemailtemplate_facts
version_added: "2.8"
short_description: Get Azure Email Template facts.
description:
    - Get facts of Azure Email Template.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    top:
        description:
            - Number of records to return.
    skip:
        description:
            - Number of records to skip.
    name:
        description:
            - Email Template Name Identifier.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Email Template
    azure_rm_apimanagementemailtemplate_facts:
      resource_group: resource_group_name
      service_name: service_name
      top: top
      skip: skip

  - name: Get instance of Email Template
    azure_rm_apimanagementemailtemplate_facts:
      resource_group: resource_group_name
      service_name: service_name
      name: template_name
'''

RETURN = '''
email_template:
    description: A list of dictionaries containing facts for Email Template.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/templates/NewIssueNotificationMessage
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: NewIssueNotificationMessage
        subject:
            description:
                - Subject of the Template.
            returned: always
            type: str
            sample: Your request $IssueName was received
        body:
            description:
                - Email Template Body. This should be a valid XDocument
            returned: always
            type: str
            sample: "<!DOCTYPE html >\n\n<html>\n\n  <head />\n\n  <body>\n\n    <p style='font-size:12pt;font-family:'Segoe UI''>Dear $DevFirstName
                     $DevLastName,</p>\n\n    <p style='font-size:12pt;font-family:'Segoe UI''>Thank you for contacting us. Our API team will review your
                     issue and get back to you soon.</p>\n\n    <p style='font-size:12pt;font-family:'Segoe UI''>\n\n          Click this <a
                     href='http://$DevPortalUrl/issues/$IssueId'>link</a> to view or edit your request.\n\n        </p>\n\n    <p
                     style='font-size:12pt;font-family:'Segoe UI''>Best,</p>\n\n    <p style='font-size:12pt;font-family:'Segoe UI''>The $OrganizationName
                     API Team</p>\n\n  </body>\n\n</html>"
        title:
            description:
                - Title of the Template.
            returned: always
            type: str
            sample: New issue received
        description:
            description:
                - Description of the Email Template.
            returned: always
            type: str
            sample: This email is sent to developers after they create a new topic on the Issues page of the developer portal.
        parameters:
            description:
                - Email Template Parameter values.
            returned: always
            type: complex
            sample: parameters
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEmailTemplateFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            top=dict(
                type='int'
            ),
            skip=dict(
                type='int'
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.service_name = None
        self.top = None
        self.skip = None
        self.name = None
        super(AzureRMEmailTemplateFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['email_template'] = self.get()
        else:
            self.results['email_template'] = self.list_by_service()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.email_template.list_by_service(resource_group_name=self.resource_group,
                                                                       service_name=self.service_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Email Template.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.email_template.get(resource_group_name=self.resource_group,
                                                           service_name=self.service_name,
                                                           template_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Email Template.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'subject': d.get('subject', None),
            'body': d.get('body', None),
            'title': d.get('title', None),
            'description': d.get('description', None),
            'parameters': {
            }
        }
        return d


def main():
    AzureRMEmailTemplateFacts()


if __name__ == '__main__':
    main()

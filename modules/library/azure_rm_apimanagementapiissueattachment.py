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
module: azure_rm_apimanagementapiissueattachment
version_added: "2.8"
short_description: Manage Api Issue Attachment instance.
description:
    - Create, update and delete instance of Api Issue Attachment.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
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
    attachment_id:
        description:
            - Attachment identifier within an Issue. Must be unique in the current Issue.
        required: True
    title:
        description:
            - Filename by which the binary data will be saved.
        required: True
    content_format:
        description:
            - "Either 'link' if I(content) is provided via an HTTP link or the MIME type of the Base64-encoded binary data provided in the 'I(content)'
               property."
        required: True
    content:
        description:
            - An HTTP link or Base64-encoded binary data.
        required: True
    if_match:
        description:
            - "ETag of the Issue Entity. ETag should match the current entity state from the header response of the GET request or it should be * for
               unconditional update."
    state:
      description:
        - Assert the state of the Api Issue Attachment.
        - Use 'present' to create or update an Api Issue Attachment and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Api Issue Attachment
    azure_rm_apimanagementapiissueattachment:
      resource_group: rg1
      service_name: apimService1
      api_id: 57d1f7558aa04f15146d9d8a
      issue_id: 57d2ef278aa04f0ad01d6cdc
      attachment_id: 57d2ef278aa04f0888cba3f3
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/57d1f7558aa04f15146d9d8a/issues/57d2ef278aa0
            4f0ad01d6cdc/attachments/57d2ef278aa04f0888cba3f3"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApiIssueAttachment(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Issue Attachment resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
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
            attachment_id=dict(
                type='str',
                required=True
            ),
            title=dict(
                type='str',
                required=True
            ),
            content_format=dict(
                type='str',
                required=True
            ),
            content=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.service_name = None
        self.api_id = None
        self.issue_id = None
        self.attachment_id = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiIssueAttachment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "title":
                    self.parameters["title"] = kwargs[key]
                elif key == "content_format":
                    self.parameters["content_format"] = kwargs[key]
                elif key == "content":
                    self.parameters["content"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_apiissueattachment()

        if not old_response:
            self.log("Api Issue Attachment instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Issue Attachment instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Api Issue Attachment instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Issue Attachment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apiissueattachment()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Issue Attachment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apiissueattachment()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_apiissueattachment():
                time.sleep(20)
        else:
            self.log("Api Issue Attachment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_apiissueattachment(self):
        '''
        Creates or updates Api Issue Attachment with the specified configuration.

        :return: deserialized Api Issue Attachment instance state dictionary
        '''
        self.log("Creating / Updating the Api Issue Attachment instance {0}".format(self.attachment_id))

        try:
            response = self.mgmt_client.api_issue_attachment.create_or_update(resource_group_name=self.resource_group,
                                                                              service_name=self.service_name,
                                                                              api_id=self.api_id,
                                                                              issue_id=self.issue_id,
                                                                              attachment_id=self.attachment_id,
                                                                              parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Issue Attachment instance.')
            self.fail("Error creating the Api Issue Attachment instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apiissueattachment(self):
        '''
        Deletes specified Api Issue Attachment instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Issue Attachment instance {0}".format(self.attachment_id))
        try:
            response = self.mgmt_client.api_issue_attachment.delete(resource_group_name=self.resource_group,
                                                                    service_name=self.service_name,
                                                                    api_id=self.api_id,
                                                                    issue_id=self.issue_id,
                                                                    attachment_id=self.attachment_id,
                                                                    if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Api Issue Attachment instance.')
            self.fail("Error deleting the Api Issue Attachment instance: {0}".format(str(e)))

        return True

    def get_apiissueattachment(self):
        '''
        Gets the properties of the specified Api Issue Attachment.

        :return: deserialized Api Issue Attachment instance state dictionary
        '''
        self.log("Checking if the Api Issue Attachment instance {0} is present".format(self.attachment_id))
        found = False
        try:
            response = self.mgmt_client.api_issue_attachment.get(resource_group_name=self.resource_group,
                                                                 service_name=self.service_name,
                                                                 api_id=self.api_id,
                                                                 issue_id=self.issue_id,
                                                                 attachment_id=self.attachment_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Issue Attachment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Issue Attachment instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMApiIssueAttachment()


if __name__ == '__main__':
    main()

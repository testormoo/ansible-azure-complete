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
module: azure_rm_apimanagementemailtemplate
version_added: "2.8"
short_description: Manage Email Template instance.
description:
    - Create, update and delete instance of Email Template.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    template_name:
        description:
            - Email Template Name Identifier.
        required: True
        choices:
            - 'application_approved_notification_message'
            - 'account_closed_developer'
            - 'quota_limit_approaching_developer_notification_message'
            - 'new_developer_notification_message'
            - 'email_change_identity_default'
            - 'invite_user_notification_message'
            - 'new_comment_notification_message'
            - 'confirm_sign_up_identity_default'
            - 'new_issue_notification_message'
            - 'purchase_developer_notification_message'
            - 'password_reset_identity_default'
            - 'password_reset_by_admin_notification_message'
            - 'reject_developer_notification_message'
            - 'request_developer_notification_message'
    subject:
        description:
            - Subject of the Template.
    title:
        description:
            - Title of the Template.
    description:
        description:
            - Description of the Email Template.
    body:
        description:
            - Email Template Body. This should be a valid XDocument
    parameters:
        description:
            - Email Template Parameter values.
        type: list
        suboptions:
            name:
                description:
                    - Template parameter name.
            title:
                description:
                    - Template parameter title.
            description:
                description:
                    - Template parameter description.
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Email Template.
        - Use 'present' to create or update an Email Template and 'absent' to delete it.
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
  - name: Create (or update) Email Template
    azure_rm_apimanagementemailtemplate:
      resource_group: rg1
      service_name: apimService1
      template_name: newIssueNotificationMessage
      if_match: NOT FOUND
'''

RETURN = '''
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


class AzureRMEmailTemplate(AzureRMModuleBase):
    """Configuration class for an Azure RM Email Template resource"""

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
            template_name=dict(
                type='str',
                choices=['application_approved_notification_message',
                         'account_closed_developer',
                         'quota_limit_approaching_developer_notification_message',
                         'new_developer_notification_message',
                         'email_change_identity_default',
                         'invite_user_notification_message',
                         'new_comment_notification_message',
                         'confirm_sign_up_identity_default',
                         'new_issue_notification_message',
                         'purchase_developer_notification_message',
                         'password_reset_identity_default',
                         'password_reset_by_admin_notification_message',
                         'reject_developer_notification_message',
                         'request_developer_notification_message'],
                required=True
            ),
            subject=dict(
                type='str'
            ),
            title=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            body=dict(
                type='str'
            ),
            parameters=dict(
                type='list'
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
        self.template_name = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEmailTemplate, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "subject":
                    self.parameters["subject"] = kwargs[key]
                elif key == "title":
                    self.parameters["title"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "body":
                    self.parameters["body"] = kwargs[key]
                elif key == "parameters":
                    self.parameters["parameters"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_emailtemplate()

        if not old_response:
            self.log("Email Template instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Email Template instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Email Template instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Email Template instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_emailtemplate()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Email Template instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_emailtemplate()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_emailtemplate():
                time.sleep(20)
        else:
            self.log("Email Template instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_emailtemplate(self):
        '''
        Creates or updates Email Template with the specified configuration.

        :return: deserialized Email Template instance state dictionary
        '''
        self.log("Creating / Updating the Email Template instance {0}".format(self.template_name))

        try:
            response = self.mgmt_client.email_template.create_or_update(resource_group_name=self.resource_group,
                                                                        service_name=self.service_name,
                                                                        template_name=self.template_name,
                                                                        parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Email Template instance.')
            self.fail("Error creating the Email Template instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_emailtemplate(self):
        '''
        Deletes specified Email Template instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Email Template instance {0}".format(self.template_name))
        try:
            response = self.mgmt_client.email_template.delete(resource_group_name=self.resource_group,
                                                              service_name=self.service_name,
                                                              template_name=self.template_name,
                                                              if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Email Template instance.')
            self.fail("Error deleting the Email Template instance: {0}".format(str(e)))

        return True

    def get_emailtemplate(self):
        '''
        Gets the properties of the specified Email Template.

        :return: deserialized Email Template instance state dictionary
        '''
        self.log("Checking if the Email Template instance {0} is present".format(self.template_name))
        found = False
        try:
            response = self.mgmt_client.email_template.get(resource_group_name=self.resource_group,
                                                           service_name=self.service_name,
                                                           template_name=self.template_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Email Template instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Email Template instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMEmailTemplate()


if __name__ == '__main__':
    main()

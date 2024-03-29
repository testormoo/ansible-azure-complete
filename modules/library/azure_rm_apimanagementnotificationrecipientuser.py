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
module: azure_rm_apimanagementnotificationrecipientuser
version_added: "2.8"
short_description: Manage Azure Notification Recipient User instance.
description:
    - Create, update and delete instance of Azure Notification Recipient User.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    name:
        description:
            - Notification Name Identifier.
        required: True
        choices:
            - 'request_publisher_notification_message'
            - 'purchase_publisher_notification_message'
            - 'new_application_notification_message'
            - 'bcc'
            - 'new_issue_publisher_notification_message'
            - 'account_closed_publisher'
            - 'quota_limit_approaching_publisher_notification_message'
    uid:
        description:
            - User identifier. Must be unique in the current API Management service instance.
        required: True
    state:
      description:
        - Assert the state of the Notification Recipient User.
        - Use 'present' to create or update an Notification Recipient User and 'absent' to delete it.
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
  - name: Create (or update) Notification Recipient User
    azure_rm_apimanagementnotificationrecipientuser:
      resource_group: rg1
      service_name: apimService1
      name: RequestPublisherNotificationMessage
      uid: 576823d0a40f7e74ec07d642
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/notifications/RequestPublisherNotificationMessage
            /recipientUsers/576823d0a40f7e74ec07d642"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMNotificationRecipientUser(AzureRMModuleBase):
    """Configuration class for an Azure RM Notification Recipient User resource"""

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
            name=dict(
                type='str',
                choices=['request_publisher_notification_message',
                         'purchase_publisher_notification_message',
                         'new_application_notification_message',
                         'bcc',
                         'new_issue_publisher_notification_message',
                         'account_closed_publisher',
                         'quota_limit_approaching_publisher_notification_message'],
                required=True
            ),
            uid=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.service_name = None
        self.name = None
        self.uid = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMNotificationRecipientUser, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                 supports_check_mode=True,
                                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_notificationrecipientuser()

        if not old_response:
            self.log("Notification Recipient User instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Notification Recipient User instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Notification Recipient User instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_notificationrecipientuser()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Notification Recipient User instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_notificationrecipientuser()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Notification Recipient User instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_notificationrecipientuser(self):
        '''
        Creates or updates Notification Recipient User with the specified configuration.

        :return: deserialized Notification Recipient User instance state dictionary
        '''
        self.log("Creating / Updating the Notification Recipient User instance {0}".format(self.uid))

        try:
            response = self.mgmt_client.notification_recipient_user.create_or_update(resource_group_name=self.resource_group,
                                                                                     service_name=self.service_name,
                                                                                     notification_name=self.name,
                                                                                     uid=self.uid)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Notification Recipient User instance.')
            self.fail("Error creating the Notification Recipient User instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_notificationrecipientuser(self):
        '''
        Deletes specified Notification Recipient User instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Notification Recipient User instance {0}".format(self.uid))
        try:
            response = self.mgmt_client.notification_recipient_user.delete(resource_group_name=self.resource_group,
                                                                           service_name=self.service_name,
                                                                           notification_name=self.name,
                                                                           uid=self.uid)
        except CloudError as e:
            self.log('Error attempting to delete the Notification Recipient User instance.')
            self.fail("Error deleting the Notification Recipient User instance: {0}".format(str(e)))

        return True

    def get_notificationrecipientuser(self):
        '''
        Gets the properties of the specified Notification Recipient User.

        :return: deserialized Notification Recipient User instance state dictionary
        '''
        self.log("Checking if the Notification Recipient User instance {0} is present".format(self.uid))
        found = False
        try:
            response = self.mgmt_client.notification_recipient_user.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Notification Recipient User instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Notification Recipient User instance.')
        if found is True:
            return response.as_dict()

        return False


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            else:
                key = list(old[0])[0]
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def main():
    """Main execution"""
    AzureRMNotificationRecipientUser()


if __name__ == '__main__':
    main()

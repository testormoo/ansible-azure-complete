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
module: azure_rm_apimanagementnotification
version_added: "2.8"
short_description: Manage Notification instance.
description:
    - Create, update and delete instance of Notification.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    notification_name:
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
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Notification.
        - Use 'present' to create or update an Notification and 'absent' to delete it.
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
  - name: Create (or update) Notification
    azure_rm_apimanagementnotification:
      resource_group: rg1
      service_name: apimService1
      notification_name: RequestPublisherNotificationMessage
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/notifications/RequestPublisherNotificationMessage
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


class AzureRMNotification(AzureRMModuleBase):
    """Configuration class for an Azure RM Notification resource"""

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
            notification_name=dict(
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
        self.notification_name = None
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMNotification, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_notification()

        if not old_response:
            self.log("Notification instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Notification instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Notification instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Notification instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_notification()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Notification instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_notification()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_notification():
                time.sleep(20)
        else:
            self.log("Notification instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_notification(self):
        '''
        Creates or updates Notification with the specified configuration.

        :return: deserialized Notification instance state dictionary
        '''
        self.log("Creating / Updating the Notification instance {0}".format(self.notification_name))

        try:
            response = self.mgmt_client.notification.create_or_update(resource_group_name=self.resource_group,
                                                                      service_name=self.service_name,
                                                                      notification_name=self.notification_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Notification instance.')
            self.fail("Error creating the Notification instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_notification(self):
        '''
        Deletes specified Notification instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Notification instance {0}".format(self.notification_name))
        try:
            response = self.mgmt_client.notification.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Notification instance.')
            self.fail("Error deleting the Notification instance: {0}".format(str(e)))

        return True

    def get_notification(self):
        '''
        Gets the properties of the specified Notification.

        :return: deserialized Notification instance state dictionary
        '''
        self.log("Checking if the Notification instance {0} is present".format(self.notification_name))
        found = False
        try:
            response = self.mgmt_client.notification.get(resource_group_name=self.resource_group,
                                                         service_name=self.service_name,
                                                         notification_name=self.notification_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Notification instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Notification instance.')
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
    AzureRMNotification()


if __name__ == '__main__':
    main()

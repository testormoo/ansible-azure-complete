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
module: azure_rm_apimanagementnotificationrecipientemail_facts
version_added: "2.8"
short_description: Get Azure Notification Recipient Email facts.
description:
    - Get facts of Azure Notification Recipient Email.

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

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Notification Recipient Email
    azure_rm_apimanagementnotificationrecipientemail_facts:
      resource_group: resource_group_name
      service_name: service_name
      notification_name: notification_name
'''

RETURN = '''
notification_recipient_email:
    description: A list of dictionaries containing facts for Notification Recipient Email.
    returned: always
    type: complex
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


class AzureRMNotificationRecipientEmailFacts(AzureRMModuleBase):
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
            notification_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.service_name = None
        self.notification_name = None
        super(AzureRMNotificationRecipientEmailFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['notification_recipient_email'] = self.list_by_notification()
        return self.results

    def list_by_notification(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.notification_recipient_email.list_by_notification(resource_group_name=self.resource_group,
                                                                                          service_name=self.service_name,
                                                                                          notification_name=self.notification_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for NotificationRecipientEmail.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMNotificationRecipientEmailFacts()


if __name__ == '__main__':
    main()
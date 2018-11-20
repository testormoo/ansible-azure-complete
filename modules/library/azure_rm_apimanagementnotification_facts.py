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
module: azure_rm_apimanagementnotification_facts
version_added: "2.8"
short_description: Get Azure Notification facts.
description:
    - Get facts of Azure Notification.

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
            - Notification Name Identifier.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Notification
    azure_rm_apimanagementnotification_facts:
      resource_group: resource_group_name
      service_name: service_name
      top: top
      skip: skip

  - name: Get instance of Notification
    azure_rm_apimanagementnotification_facts:
      resource_group: resource_group_name
      service_name: service_name
      name: notification_name
'''

RETURN = '''
notification:
    description: A list of dictionaries containing facts for Notification.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/notifications/RequestPublisherNotificatio
                    nMessage"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: RequestPublisherNotificationMessage
        title:
            description:
                - Title of the Notification.
            returned: always
            type: str
            sample: Subscription requests (requiring approval)
        description:
            description:
                - Description of the Notification.
            returned: always
            type: str
            sample: The following email recipients and users will receive email notifications about subscription requests for API products requiring approval.
        recipients:
            description:
                - Recipient Parameter values.
            returned: always
            type: complex
            sample: recipients
            contains:
                emails:
                    description:
                        - List of Emails subscribed for the notification.
                    returned: always
                    type: str
                    sample: "[\n
                             '/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/recipientEmails/contoso@live.co
                            m',\n
                             '/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/recipientEmails/foobar!live',\n
                             '/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/recipientEmails/foobar@live.com
                            '\n]"
                users:
                    description:
                        - List of Users subscribed for the notification.
                    returned: always
                    type: str
                    sample: "[\n
                             '/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/users/576823d0a40f7e74ec07d642'
                            \n]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNotificationFacts(AzureRMModuleBase):
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
        super(AzureRMNotificationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['notification'] = self.list_by_service()
        elif self.name is not None:
            self.results['notification'] = self.get()
        return self.results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.notification.list_by_service(resource_group_name=self.resource_group,
                                                                     service_name=self.service_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Notification.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.notification.get(resource_group_name=self.resource_group,
                                                         service_name=self.service_name,
                                                         notification_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Notification.')

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
            'description': d.get('description', None),
            'recipients': {
                'emails': d.get('recipients', {}).get('emails', None),
                'users': d.get('recipients', {}).get('users', None)
            }
        }
        return d


def main():
    AzureRMNotificationFacts()


if __name__ == '__main__':
    main()

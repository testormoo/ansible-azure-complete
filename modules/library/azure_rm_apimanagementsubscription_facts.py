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
module: azure_rm_apimanagementsubscription_facts
version_added: "2.8"
short_description: Get Azure Subscription facts.
description:
    - Get facts of Azure Subscription.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    sid:
        description:
            - Subscription entity Identifier. The entity represents the association between a user and a product in API Management.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Subscription
    azure_rm_apimanagementsubscription_facts:
      resource_group: resource_group_name
      name: service_name
      sid: sid
'''

RETURN = '''
subscription:
    description: A list of dictionaries containing facts for Subscription.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/subscriptions/5931a769d8d14f0ad8ce13b8
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: 5931a769d8d14f0ad8ce13b8
        state:
            description:
                - "Subscription state. Possible states are * active - the subscription is active, * suspended - the subscription is blocked, and the
                   subscriber cannot call any APIs of the product, * submitted - the subscription request has been made by the developer, but has not yet
                   been approved or rejected, * rejected - the subscription request has been denied by an administrator, * cancelled - the subscription has
                   been cancelled by the developer or administrator, * expired - the subscription reached its expiration date and was deactivated. Possible
                   values include: 'suspended', 'active', 'expired', 'submitted', 'rejected', 'cancelled'"
            returned: always
            type: str
            sample: submitted
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSubscriptionFacts(AzureRMModuleBase):
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
            sid=dict(
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
        self.name = None
        self.sid = None
        super(AzureRMSubscriptionFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['subscription'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.subscription.get(resource_group_name=self.resource_group,
                                                         service_name=self.name,
                                                         sid=self.sid)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Subscription.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'state': d.get('state', None)
        }
        return d


def main():
    AzureRMSubscriptionFacts()


if __name__ == '__main__':
    main()

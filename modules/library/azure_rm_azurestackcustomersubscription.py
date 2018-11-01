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
module: azure_rm_azurestackcustomersubscription
version_added: "2.8"
short_description: Manage Customer Subscription instance.
description:
    - Create, update and delete instance of Customer Subscription.

options:
    resource_group:
        description:
            - Name of the resource group.
        required: True
    registration_name:
        description:
            - Name of the Azure Stack registration.
        required: True
    customer_subscription_name:
        description:
            - Name of the product.
        required: True
    etag:
        description:
            - The entity tag used for optimistic concurency when modifying the resource.
    tenant_id:
        description:
            - Tenant Id.
    state:
      description:
        - Assert the state of the Customer Subscription.
        - Use 'present' to create or update an Customer Subscription and 'absent' to delete it.
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
  - name: Create (or update) Customer Subscription
    azure_rm_azurestackcustomersubscription:
      resource_group: azurestack
      registration_name: testregistration
      customer_subscription_name: E09A4E93-29A7-4EBA-A6D4-76202383F07F
'''

RETURN = '''
id:
    description:
        - ID of the resource.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.azurestack import AzureStackManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMCustomerSubscriptions(AzureRMModuleBase):
    """Configuration class for an Azure RM Customer Subscription resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registration_name=dict(
                type='str',
                required=True
            ),
            customer_subscription_name=dict(
                type='str',
                required=True
            ),
            etag=dict(
                type='str'
            ),
            tenant_id=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.registration_name = None
        self.customer_subscription_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCustomerSubscriptions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "etag":
                    self.parameters["etag"] = kwargs[key]
                elif key == "tenant_id":
                    self.parameters["tenant_id"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureStackManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_customersubscription()

        if not old_response:
            self.log("Customer Subscription instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Customer Subscription instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Customer Subscription instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Customer Subscription instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_customersubscription()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Customer Subscription instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_customersubscription()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_customersubscription():
                time.sleep(20)
        else:
            self.log("Customer Subscription instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_customersubscription(self):
        '''
        Creates or updates Customer Subscription with the specified configuration.

        :return: deserialized Customer Subscription instance state dictionary
        '''
        self.log("Creating / Updating the Customer Subscription instance {0}".format(self.customer_subscription_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.customer_subscriptions.create(resource_group=self.resource_group,
                                                                          registration_name=self.registration_name,
                                                                          customer_subscription_name=self.customer_subscription_name,
                                                                          customer_creation_parameters=self.parameters)
            else:
                response = self.mgmt_client.customer_subscriptions.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Customer Subscription instance.')
            self.fail("Error creating the Customer Subscription instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_customersubscription(self):
        '''
        Deletes specified Customer Subscription instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Customer Subscription instance {0}".format(self.customer_subscription_name))
        try:
            response = self.mgmt_client.customer_subscriptions.delete(resource_group=self.resource_group,
                                                                      registration_name=self.registration_name,
                                                                      customer_subscription_name=self.customer_subscription_name)
        except CloudError as e:
            self.log('Error attempting to delete the Customer Subscription instance.')
            self.fail("Error deleting the Customer Subscription instance: {0}".format(str(e)))

        return True

    def get_customersubscription(self):
        '''
        Gets the properties of the specified Customer Subscription.

        :return: deserialized Customer Subscription instance state dictionary
        '''
        self.log("Checking if the Customer Subscription instance {0} is present".format(self.customer_subscription_name))
        found = False
        try:
            response = self.mgmt_client.customer_subscriptions.get(resource_group=self.resource_group,
                                                                   registration_name=self.registration_name,
                                                                   customer_subscription_name=self.customer_subscription_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Customer Subscription instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Customer Subscription instance.')
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
    AzureRMCustomerSubscriptions()


if __name__ == '__main__':
    main()
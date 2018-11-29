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
short_description: Manage Azure Customer Subscription instance.
description:
    - Create, update and delete instance of Azure Customer Subscription.

options:
    resource_group:
        description:
            - Name of the resource group.
        required: True
    registration_name:
        description:
            - Name of the Azure Stack registration.
        required: True
    name:
        description:
            - Name of the product.
        required: True
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
      name: E09A4E93-29A7-4EBA-A6D4-76202383F07F
      tenant_id: dbab3982-796f-4d03-9908-044c08aef8a2
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMCustomerSubscription(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCustomerSubscription, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.customer_creation_parameters[key] = kwargs[key]


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
                if (not default_compare(self.customer_creation_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Customer Subscription instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_customersubscription()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Customer Subscription instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_customersubscription()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Customer Subscription instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_customersubscription(self):
        '''
        Creates or updates Customer Subscription with the specified configuration.

        :return: deserialized Customer Subscription instance state dictionary
        '''
        self.log("Creating / Updating the Customer Subscription instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.customer_subscriptions.create(resource_group=self.resource_group,
                                                                          registration_name=self.registration_name,
                                                                          customer_subscription_name=self.name,
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
        self.log("Deleting the Customer Subscription instance {0}".format(self.name))
        try:
            response = self.mgmt_client.customer_subscriptions.delete(resource_group=self.resource_group,
                                                                      registration_name=self.registration_name,
                                                                      customer_subscription_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Customer Subscription instance.')
            self.fail("Error deleting the Customer Subscription instance: {0}".format(str(e)))

        return True

    def get_customersubscription(self):
        '''
        Gets the properties of the specified Customer Subscription.

        :return: deserialized Customer Subscription instance state dictionary
        '''
        self.log("Checking if the Customer Subscription instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.customer_subscriptions.get(resource_group=self.resource_group,
                                                                   registration_name=self.registration_name,
                                                                   customer_subscription_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Customer Subscription instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Customer Subscription instance.')
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
    AzureRMCustomerSubscription()


if __name__ == '__main__':
    main()

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
module: azure_rm_apimanagementsubscription
version_added: "2.8"
short_description: Manage Subscription instance.
description:
    - Create, update and delete instance of Subscription.

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
    user_id:
        description:
            - User (user id path) for whom subscription is being created in form /users/{uid}
            - Required when C(state) is I(present).
    product_id:
        description:
            - Product (product id path) for which subscription is being created in form /products/{productid}
            - Required when C(state) is I(present).
    display_name:
        description:
            - Subscription name.
            - Required when C(state) is I(present).
    primary_key:
        description:
            - Primary subscription key. If not specified during request key will be generated automatically.
    secondary_key:
        description:
            - Secondary subscription key. If not specified during request key will be generated automatically.
    state:
        description:
            - "Initial subscription state. If no value is specified, subscription is created with C(submitted) state. Possible states are * C(active) - the
               subscription is C(active), * C(suspended) - the subscription is blocked, and the subscriber cannot call any APIs of the product, *
               C(submitted) - the subscription request has been made by the developer, but has not yet been approved or C(rejected), * C(rejected) - the
               subscription request has been denied by an administrator, * C(cancelled) - the subscription has been C(cancelled) by the developer or
               administrator, * C(expired) - the subscription reached its expiration date and was deactivated."
        choices:
            - 'suspended'
            - 'active'
            - 'expired'
            - 'submitted'
            - 'rejected'
            - 'cancelled'
    notify:
        description:
            - Notify change in Subscription I(state).
            -  - If false, do not send any email notification for change of I(state) of subscription
            -  - If true, send email notification of change of I(state) of subscription
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Subscription.
        - Use 'present' to create or update an Subscription and 'absent' to delete it.
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
  - name: Create (or update) Subscription
    azure_rm_apimanagementsubscription:
      resource_group: rg1
      name: apimService1
      sid: testsub
      user_id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/users/57127d485157a511ace86ae7
      product_id: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/products/5600b59475ff190048060002
      display_name: testsub
      notify: NOT FOUND
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


class AzureRMSubscription(AzureRMModuleBase):
    """Configuration class for an Azure RM Subscription resource"""

    def __init__(self):
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
            ),
            user_id=dict(
                type='str'
            ),
            product_id=dict(
                type='str'
            ),
            display_name=dict(
                type='str'
            ),
            primary_key=dict(
                type='str'
            ),
            secondary_key=dict(
                type='str'
            ),
            state=dict(
                type='str',
                choices=['suspended',
                         'active',
                         'expired',
                         'submitted',
                         'rejected',
                         'cancelled']
            ),
            notify=dict(
                type='str'
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
        self.name = None
        self.sid = None
        self.parameters = dict()
        self.notify = None
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSubscription, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "user_id":
                    self.parameters["user_id"] = kwargs[key]
                elif key == "product_id":
                    self.parameters["product_id"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "primary_key":
                    self.parameters["primary_key"] = kwargs[key]
                elif key == "secondary_key":
                    self.parameters["secondary_key"] = kwargs[key]
                elif key == "state":
                    self.parameters["state"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_subscription()

        if not old_response:
            self.log("Subscription instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Subscription instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Subscription instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_subscription()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Subscription instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_subscription()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_subscription():
                time.sleep(20)
        else:
            self.log("Subscription instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_subscription(self):
        '''
        Creates or updates Subscription with the specified configuration.

        :return: deserialized Subscription instance state dictionary
        '''
        self.log("Creating / Updating the Subscription instance {0}".format(self.sid))

        try:
            response = self.mgmt_client.subscription.create_or_update(resource_group_name=self.resource_group,
                                                                      service_name=self.name,
                                                                      sid=self.sid,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Subscription instance.')
            self.fail("Error creating the Subscription instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_subscription(self):
        '''
        Deletes specified Subscription instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Subscription instance {0}".format(self.sid))
        try:
            response = self.mgmt_client.subscription.delete(resource_group_name=self.resource_group,
                                                            service_name=self.name,
                                                            sid=self.sid,
                                                            if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Subscription instance.')
            self.fail("Error deleting the Subscription instance: {0}".format(str(e)))

        return True

    def get_subscription(self):
        '''
        Gets the properties of the specified Subscription.

        :return: deserialized Subscription instance state dictionary
        '''
        self.log("Checking if the Subscription instance {0} is present".format(self.sid))
        found = False
        try:
            response = self.mgmt_client.subscription.get(resource_group_name=self.resource_group,
                                                         service_name=self.name,
                                                         sid=self.sid)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Subscription instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Subscription instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def main():
    """Main execution"""
    AzureRMSubscription()


if __name__ == '__main__':
    main()

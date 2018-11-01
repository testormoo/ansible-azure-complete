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
module: azure_rm_apimanagementproduct
version_added: "2.8"
short_description: Manage Product instance.
description:
    - Create, update and delete instance of Product.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    product_id:
        description:
            - Product identifier. Must be unique in the current API Management service instance.
        required: True
    description:
        description:
            - Product description. May include HTML formatting tags.
    terms:
        description:
            - "Product terms of use. Developers trying to subscribe to the product will be presented and required to accept these terms before they can
               complete the subscription process."
    subscription_required:
        description:
            - "Whether a product subscription is required for accessing APIs included in this product. If true, the product is referred to as 'protected'
               and a valid subscription key is required for a request to an API included in the product to succeed. If false, the product is referred to as
               'open' and requests to an API included in the product can be made without a subscription key. If property is omitted when creating a new
               product it's value is assumed to be true."
    approval_required:
        description:
            - "whether subscription approval is required. If false, new subscriptions will be approved automatically enabling developers to call the
               product's APIs immediately after subscribing. If true, administrators must manually approve the subscription before the developer can any of
               the product's APIs. Can be present only if I(subscription_required) property is present and has a value of false."
    subscriptions_limit:
        description:
            - "Whether the number of subscriptions a user can have to this product at the same time. Set to null or omit to allow unlimited per user
               subscriptions. Can be present only if I(subscription_required) property is present and has a value of false."
    state:
        description:
            - "whether product is C(published) or not. C(published) products are discoverable by users of developer portal. Non C(published) products are
               visible only to administrators. Default state of Product is C(not_published)."
        choices:
            - 'not_published'
            - 'published'
    display_name:
        description:
            - Product name.
        required: True
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Product.
        - Use 'present' to create or update an Product and 'absent' to delete it.
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
  - name: Create (or update) Product
    azure_rm_apimanagementproduct:
      resource_group: rg1
      service_name: apimService1
      product_id: testproduct
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


class AzureRMProduct(AzureRMModuleBase):
    """Configuration class for an Azure RM Product resource"""

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
            product_id=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            terms=dict(
                type='str'
            ),
            subscription_required=dict(
                type='str'
            ),
            approval_required=dict(
                type='str'
            ),
            subscriptions_limit=dict(
                type='int'
            ),
            state=dict(
                type='str',
                choices=['not_published',
                         'published']
            ),
            display_name=dict(
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
        self.product_id = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProduct, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "terms":
                    self.parameters["terms"] = kwargs[key]
                elif key == "subscription_required":
                    self.parameters["subscription_required"] = kwargs[key]
                elif key == "approval_required":
                    self.parameters["approval_required"] = kwargs[key]
                elif key == "subscriptions_limit":
                    self.parameters["subscriptions_limit"] = kwargs[key]
                elif key == "state":
                    ev = kwargs[key]
                    if ev == 'not_published':
                        ev = 'notPublished'
                    self.parameters["state"] = ev
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_product()

        if not old_response:
            self.log("Product instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Product instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Product instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Product instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_product()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Product instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_product()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_product():
                time.sleep(20)
        else:
            self.log("Product instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_product(self):
        '''
        Creates or updates Product with the specified configuration.

        :return: deserialized Product instance state dictionary
        '''
        self.log("Creating / Updating the Product instance {0}".format(self.product_id))

        try:
            response = self.mgmt_client.product.create_or_update(resource_group_name=self.resource_group,
                                                                 service_name=self.service_name,
                                                                 product_id=self.product_id,
                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Product instance.')
            self.fail("Error creating the Product instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_product(self):
        '''
        Deletes specified Product instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Product instance {0}".format(self.product_id))
        try:
            response = self.mgmt_client.product.delete(resource_group_name=self.resource_group,
                                                       service_name=self.service_name,
                                                       product_id=self.product_id,
                                                       if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Product instance.')
            self.fail("Error deleting the Product instance: {0}".format(str(e)))

        return True

    def get_product(self):
        '''
        Gets the properties of the specified Product.

        :return: deserialized Product instance state dictionary
        '''
        self.log("Checking if the Product instance {0} is present".format(self.product_id))
        found = False
        try:
            response = self.mgmt_client.product.get(resource_group_name=self.resource_group,
                                                    service_name=self.service_name,
                                                    product_id=self.product_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Product instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Product instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
        }
        return d


def main():
    """Main execution"""
    AzureRMProduct()


if __name__ == '__main__':
    main()

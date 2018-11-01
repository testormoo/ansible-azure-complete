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
module: azure_rm_apimanagementproductpolicy
version_added: "2.8"
short_description: Manage Product Policy instance.
description:
    - Create, update and delete instance of Product Policy.

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
    policy_id:
        description:
            - The identifier of the Policy.
        required: True
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    policy_content:
        description:
            - Json escaped C(xml) Encoded contents of the Policy.
        required: True
    content_format:
        description:
            - Format of the I(policy_content).
        choices:
            - 'xml'
            - 'xml-link'
            - 'rawxml'
            - 'rawxml-link'
    state:
      description:
        - Assert the state of the Product Policy.
        - Use 'present' to create or update an Product Policy and 'absent' to delete it.
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
  - name: Create (or update) Product Policy
    azure_rm_apimanagementproductpolicy:
      resource_group: rg1
      service_name: apimService1
      product_id: 5702e97e5157a50f48dce801
      policy_id: policy
      if_match: NOT FOUND
      policy_content: NOT FOUND
      content_format: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/products/5702e97e5157a50f48dce801/policies/policy
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


class AzureRMProductPolicy(AzureRMModuleBase):
    """Configuration class for an Azure RM Product Policy resource"""

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
            policy_id=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            policy_content=dict(
                type='str',
                required=True
            ),
            content_format=dict(
                type='str',
                choices=['xml',
                         'xml-link',
                         'rawxml',
                         'rawxml-link']
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
        self.policy_id = None
        self.if_match = None
        self.policy_content = None
        self.content_format = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProductPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_productpolicy()

        if not old_response:
            self.log("Product Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Product Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Product Policy instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Product Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_productpolicy()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Product Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_productpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_productpolicy():
                time.sleep(20)
        else:
            self.log("Product Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_productpolicy(self):
        '''
        Creates or updates Product Policy with the specified configuration.

        :return: deserialized Product Policy instance state dictionary
        '''
        self.log("Creating / Updating the Product Policy instance {0}".format(self.policy_id))

        try:
            response = self.mgmt_client.product_policy.create_or_update(resource_group_name=self.resource_group,
                                                                        service_name=self.service_name,
                                                                        product_id=self.product_id,
                                                                        policy_id=self.policy_id,
                                                                        policy_content=self.policy_content)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Product Policy instance.')
            self.fail("Error creating the Product Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_productpolicy(self):
        '''
        Deletes specified Product Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Product Policy instance {0}".format(self.policy_id))
        try:
            response = self.mgmt_client.product_policy.delete(resource_group_name=self.resource_group,
                                                              service_name=self.service_name,
                                                              product_id=self.product_id,
                                                              policy_id=self.policy_id,
                                                              if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Product Policy instance.')
            self.fail("Error deleting the Product Policy instance: {0}".format(str(e)))

        return True

    def get_productpolicy(self):
        '''
        Gets the properties of the specified Product Policy.

        :return: deserialized Product Policy instance state dictionary
        '''
        self.log("Checking if the Product Policy instance {0} is present".format(self.policy_id))
        found = False
        try:
            response = self.mgmt_client.product_policy.get(resource_group_name=self.resource_group,
                                                           service_name=self.service_name,
                                                           product_id=self.product_id,
                                                           policy_id=self.policy_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Product Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Product Policy instance.')
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
    AzureRMProductPolicy()


if __name__ == '__main__':
    main()

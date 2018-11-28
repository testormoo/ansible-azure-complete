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
module: azure_rm_apimanagementapioperationpolicy
version_added: "2.8"
short_description: Manage Azure Api Operation Policy instance.
description:
    - Create, update and delete instance of Azure Api Operation Policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."
        required: True
    operation_id:
        description:
            - Operation identifier within an API. Must be unique in the current API Management service instance.
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
        - Assert the state of the Api Operation Policy.
        - Use 'present' to create or update an Api Operation Policy and 'absent' to delete it.
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
  - name: Create (or update) Api Operation Policy
    azure_rm_apimanagementapioperationpolicy:
      resource_group: rg1
      name: apimService1
      api_id: 5600b57e7e8880006a040001
      operation_id: 5600b57e7e8880006a080001
      policy_id: policy
      if_match: *
      policy_content: NOT FOUND
      content_format: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/5600b57e7e8880006a040001/operations/5600b57e
            7e8880006a080001/policies/policy"
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


class AzureRMApiOperationPolicy(AzureRMModuleBase):
    """Configuration class for an Azure RM Api Operation Policy resource"""

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
            api_id=dict(
                type='str',
                required=True
            ),
            operation_id=dict(
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
        self.name = None
        self.api_id = None
        self.operation_id = None
        self.policy_id = None
        self.if_match = None
        self.policy_content = None
        self.content_format = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiOperationPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_apioperationpolicy()

        if not old_response:
            self.log("Api Operation Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Operation Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Operation Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_apioperationpolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Operation Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apioperationpolicy()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Api Operation Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_apioperationpolicy(self):
        '''
        Creates or updates Api Operation Policy with the specified configuration.

        :return: deserialized Api Operation Policy instance state dictionary
        '''
        self.log("Creating / Updating the Api Operation Policy instance {0}".format(self.policy_id))

        try:
            response = self.mgmt_client.api_operation_policy.create_or_update(resource_group_name=self.resource_group,
                                                                              service_name=self.name,
                                                                              api_id=self.api_id,
                                                                              operation_id=self.operation_id,
                                                                              policy_id=self.policy_id,
                                                                              policy_content=self.policy_content)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Api Operation Policy instance.')
            self.fail("Error creating the Api Operation Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apioperationpolicy(self):
        '''
        Deletes specified Api Operation Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Operation Policy instance {0}".format(self.policy_id))
        try:
            response = self.mgmt_client.api_operation_policy.delete(resource_group_name=self.resource_group,
                                                                    service_name=self.name,
                                                                    api_id=self.api_id,
                                                                    operation_id=self.operation_id,
                                                                    if_match=self.if_match,
                                                                    policy_id=self.policy_id)
        except CloudError as e:
            self.log('Error attempting to delete the Api Operation Policy instance.')
            self.fail("Error deleting the Api Operation Policy instance: {0}".format(str(e)))

        return True

    def get_apioperationpolicy(self):
        '''
        Gets the properties of the specified Api Operation Policy.

        :return: deserialized Api Operation Policy instance state dictionary
        '''
        self.log("Checking if the Api Operation Policy instance {0} is present".format(self.policy_id))
        found = False
        try:
            response = self.mgmt_client.api_operation_policy.get(resource_group_name=self.resource_group,
                                                                 service_name=self.name,
                                                                 api_id=self.api_id,
                                                                 operation_id=self.operation_id,
                                                                 policy_id=self.policy_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Operation Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Operation Policy instance.')
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
    AzureRMApiOperationPolicy()


if __name__ == '__main__':
    main()

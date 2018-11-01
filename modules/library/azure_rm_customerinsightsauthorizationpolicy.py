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
module: azure_rm_customerinsightsauthorizationpolicy
version_added: "2.8"
short_description: Manage Authorization Policy instance.
description:
    - Create, update and delete instance of Authorization Policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    authorization_policy_name:
        description:
            - The name of the policy.
        required: True
    permissions:
        description:
            - The permissions associated with the policy.
        required: True
        type: list
    primary_key:
        description:
            - Primary key assiciated with the policy.
    secondary_key:
        description:
            - Secondary key assiciated with the policy.
    state:
      description:
        - Assert the state of the Authorization Policy.
        - Use 'present' to create or update an Authorization Policy and 'absent' to delete it.
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
  - name: Create (or update) Authorization Policy
    azure_rm_customerinsightsauthorizationpolicy:
      resource_group: TestHubRG
      hub_name: azSdkTestHub
      authorization_policy_name: testPolicy4222
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups//TestHubRG/providers/Microsoft.CustomerInsights/hubs/azSdkTestHub/AuthorizationPolicies/testPolicy4222
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAuthorizationPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Authorization Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            authorization_policy_name=dict(
                type='str',
                required=True
            ),
            permissions=dict(
                type='list',
                required=True
            ),
            primary_key=dict(
                type='str'
            ),
            secondary_key=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.authorization_policy_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAuthorizationPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                           supports_check_mode=True,
                                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "permissions":
                    self.parameters["permissions"] = kwargs[key]
                elif key == "primary_key":
                    self.parameters["primary_key"] = kwargs[key]
                elif key == "secondary_key":
                    self.parameters["secondary_key"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_authorizationpolicy()

        if not old_response:
            self.log("Authorization Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Authorization Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Authorization Policy instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Authorization Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_authorizationpolicy()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Authorization Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_authorizationpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_authorizationpolicy():
                time.sleep(20)
        else:
            self.log("Authorization Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_authorizationpolicy(self):
        '''
        Creates or updates Authorization Policy with the specified configuration.

        :return: deserialized Authorization Policy instance state dictionary
        '''
        self.log("Creating / Updating the Authorization Policy instance {0}".format(self.authorization_policy_name))

        try:
            response = self.mgmt_client.authorization_policies.create_or_update(resource_group_name=self.resource_group,
                                                                                hub_name=self.hub_name,
                                                                                authorization_policy_name=self.authorization_policy_name,
                                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Authorization Policy instance.')
            self.fail("Error creating the Authorization Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_authorizationpolicy(self):
        '''
        Deletes specified Authorization Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Authorization Policy instance {0}".format(self.authorization_policy_name))
        try:
            response = self.mgmt_client.authorization_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Authorization Policy instance.')
            self.fail("Error deleting the Authorization Policy instance: {0}".format(str(e)))

        return True

    def get_authorizationpolicy(self):
        '''
        Gets the properties of the specified Authorization Policy.

        :return: deserialized Authorization Policy instance state dictionary
        '''
        self.log("Checking if the Authorization Policy instance {0} is present".format(self.authorization_policy_name))
        found = False
        try:
            response = self.mgmt_client.authorization_policies.get(resource_group_name=self.resource_group,
                                                                   hub_name=self.hub_name,
                                                                   authorization_policy_name=self.authorization_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Authorization Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Authorization Policy instance.')
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
    AzureRMAuthorizationPolicies()


if __name__ == '__main__':
    main()

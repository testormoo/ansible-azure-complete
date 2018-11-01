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
module: azure_rm_timeseriesinsightsaccesspolicy
version_added: "2.8"
short_description: Manage Access Policy instance.
description:
    - Create, update and delete instance of Access Policy.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    environment_name:
        description:
            - The name of the Time Series Insights environment associated with the specified resource group.
        required: True
    access_policy_name:
        description:
            - Name of the access policy.
        required: True
    principal_object_id:
        description:
            - The objectId of the principal in Azure Active Directory.
    description:
        description:
            - An description of the access policy.
    roles:
        description:
            - The list of roles the principal is assigned on the environment.
        type: list
    state:
      description:
        - Assert the state of the Access Policy.
        - Use 'present' to create or update an Access Policy and 'absent' to delete it.
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
  - name: Create (or update) Access Policy
    azure_rm_timeseriesinsightsaccesspolicy:
      resource_group: rg1
      environment_name: env1
      access_policy_name: ap1
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.TimeSeriesInsights/Environments/env1/accessPolicies/ap1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.timeseriesinsights import TimeSeriesInsightsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAccessPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Access Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            environment_name=dict(
                type='str',
                required=True
            ),
            access_policy_name=dict(
                type='str',
                required=True
            ),
            principal_object_id=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            roles=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.environment_name = None
        self.access_policy_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAccessPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "principal_object_id":
                    self.parameters["principal_object_id"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "roles":
                    self.parameters["roles"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(TimeSeriesInsightsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_accesspolicy()

        if not old_response:
            self.log("Access Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Access Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Access Policy instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Access Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_accesspolicy()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Access Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_accesspolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_accesspolicy():
                time.sleep(20)
        else:
            self.log("Access Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_accesspolicy(self):
        '''
        Creates or updates Access Policy with the specified configuration.

        :return: deserialized Access Policy instance state dictionary
        '''
        self.log("Creating / Updating the Access Policy instance {0}".format(self.access_policy_name))

        try:
            response = self.mgmt_client.access_policies.create_or_update(resource_group_name=self.resource_group,
                                                                         environment_name=self.environment_name,
                                                                         access_policy_name=self.access_policy_name,
                                                                         parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Access Policy instance.')
            self.fail("Error creating the Access Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_accesspolicy(self):
        '''
        Deletes specified Access Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Access Policy instance {0}".format(self.access_policy_name))
        try:
            response = self.mgmt_client.access_policies.delete(resource_group_name=self.resource_group,
                                                               environment_name=self.environment_name,
                                                               access_policy_name=self.access_policy_name)
        except CloudError as e:
            self.log('Error attempting to delete the Access Policy instance.')
            self.fail("Error deleting the Access Policy instance: {0}".format(str(e)))

        return True

    def get_accesspolicy(self):
        '''
        Gets the properties of the specified Access Policy.

        :return: deserialized Access Policy instance state dictionary
        '''
        self.log("Checking if the Access Policy instance {0} is present".format(self.access_policy_name))
        found = False
        try:
            response = self.mgmt_client.access_policies.get(resource_group_name=self.resource_group,
                                                            environment_name=self.environment_name,
                                                            access_policy_name=self.access_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Access Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Access Policy instance.')
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
    AzureRMAccessPolicies()


if __name__ == '__main__':
    main()

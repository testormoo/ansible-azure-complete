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
short_description: Manage Azure Access Policy instance.
description:
    - Create, update and delete instance of Azure Access Policy.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    environment_name:
        description:
            - The name of the Time Series Insights environment associated with the specified resource group.
        required: True
    name:
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
      name: ap1
      principal_object_id: aGuid
      description: some description
      roles:
        - [
  "Reader"
]
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMAccessPolicy(AzureRMModuleBase):
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
            name=dict(
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAccessPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Access Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_accesspolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Access Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_accesspolicy()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Access Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_accesspolicy(self):
        '''
        Creates or updates Access Policy with the specified configuration.

        :return: deserialized Access Policy instance state dictionary
        '''
        self.log("Creating / Updating the Access Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.access_policies.create_or_update(resource_group_name=self.resource_group,
                                                                         environment_name=self.environment_name,
                                                                         access_policy_name=self.name,
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
        self.log("Deleting the Access Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.access_policies.delete(resource_group_name=self.resource_group,
                                                               environment_name=self.environment_name,
                                                               access_policy_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Access Policy instance.')
            self.fail("Error deleting the Access Policy instance: {0}".format(str(e)))

        return True

    def get_accesspolicy(self):
        '''
        Gets the properties of the specified Access Policy.

        :return: deserialized Access Policy instance state dictionary
        '''
        self.log("Checking if the Access Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.access_policies.get(resource_group_name=self.resource_group,
                                                            environment_name=self.environment_name,
                                                            access_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Access Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Access Policy instance.')
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
    AzureRMAccessPolicy()


if __name__ == '__main__':
    main()

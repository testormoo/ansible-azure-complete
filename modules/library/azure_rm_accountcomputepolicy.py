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
module: azure_rm_accountcomputepolicy
version_added: "2.8"
short_description: Manage Compute Policy instance.
description:
    - Create, update and delete instance of Compute Policy.

options:
    resource_group:
        description:
            - The name of the Azure resource C(group).
        required: True
    account_name:
        description:
            - The name of the Data Lake Analytics account.
        required: True
    name:
        description:
            - The name of the compute policy to create or update.
        required: True
    object_id:
        description:
            - The AAD object identifier for the entity to create a policy for.
            - Required when C(state) is I(present).
    object_type:
        description:
            - The type of AAD object the object identifier refers to.
            - Required when C(state) is I(present).
        choices:
            - 'user'
            - 'group'
            - 'service_principal'
    max_degree_of_parallelism_per_job:
        description:
            - "The maximum degree of parallelism per job this C(user) can use to submit jobs. This property, the min priority per job property, or both must
               be passed."
    min_priority_per_job:
        description:
            - "The minimum priority per job this C(user) can use to submit jobs. This property, the max degree of parallelism per job property, or both must
               be passed."
    state:
      description:
        - Assert the state of the Compute Policy.
        - Use 'present' to create or update an Compute Policy and 'absent' to delete it.
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
  - name: Create (or update) Compute Policy
    azure_rm_accountcomputepolicy:
      resource_group: contosorg
      account_name: contosoadla
      name: test_policy
      object_id: 776b9091-8916-4638-87f7-9c989a38da98
      object_type: User
      max_degree_of_parallelism_per_job: 10
      min_priority_per_job: 30
'''

RETURN = '''
id:
    description:
        - The resource identifier.
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
    from azure.mgmt.account import DataLakeAnalyticsAccountManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMComputePolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Compute Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            object_id=dict(
                type='str'
            ),
            object_type=dict(
                type='str',
                choices=['user',
                         'group',
                         'service_principal']
            ),
            max_degree_of_parallelism_per_job=dict(
                type='int'
            ),
            min_priority_per_job=dict(
                type='int'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMComputePolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "object_id":
                    self.parameters["object_id"] = kwargs[key]
                elif key == "object_type":
                    self.parameters["object_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "max_degree_of_parallelism_per_job":
                    self.parameters["max_degree_of_parallelism_per_job"] = kwargs[key]
                elif key == "min_priority_per_job":
                    self.parameters["min_priority_per_job"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataLakeAnalyticsAccountManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_computepolicy()

        if not old_response:
            self.log("Compute Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Compute Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Compute Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_computepolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Compute Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_computepolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_computepolicy():
                time.sleep(20)
        else:
            self.log("Compute Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_computepolicy(self):
        '''
        Creates or updates Compute Policy with the specified configuration.

        :return: deserialized Compute Policy instance state dictionary
        '''
        self.log("Creating / Updating the Compute Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.compute_policies.create_or_update(resource_group_name=self.resource_group,
                                                                          account_name=self.account_name,
                                                                          compute_policy_name=self.name,
                                                                          parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Compute Policy instance.')
            self.fail("Error creating the Compute Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_computepolicy(self):
        '''
        Deletes specified Compute Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Compute Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.compute_policies.delete(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                compute_policy_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Compute Policy instance.')
            self.fail("Error deleting the Compute Policy instance: {0}".format(str(e)))

        return True

    def get_computepolicy(self):
        '''
        Gets the properties of the specified Compute Policy.

        :return: deserialized Compute Policy instance state dictionary
        '''
        self.log("Checking if the Compute Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.compute_policies.get(resource_group_name=self.resource_group,
                                                             account_name=self.account_name,
                                                             compute_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Compute Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Compute Policy instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMComputePolicies()


if __name__ == '__main__':
    main()
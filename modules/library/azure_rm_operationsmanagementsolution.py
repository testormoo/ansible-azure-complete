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
module: azure_rm_operationsmanagementsolution
version_added: "2.8"
short_description: Manage Solution instance.
description:
    - Create, update and delete instance of Solution.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
        required: True
    name:
        description:
            - User Solution Name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    plan:
        description:
            - Plan for solution object supported by the OperationsManagement resource provider.
        suboptions:
            name:
                description:
                    - "name of the solution to be created. For Microsoft published solution it should be in the format of solutionType(workspaceName).
                       SolutionType part is case sensitive. For third party solution, it can be anything."
            publisher:
                description:
                    - Publisher name. For gallery solution, it is Microsoft.
            promotion_code:
                description:
                    - promotionCode, Not really used now, can you left as empty
            product:
                description:
                    - "name of the solution to enabled/add. For Microsoft published gallery solution it should be in the format of
                       OMSGallery/<solutionType>. This is case sensitive"
    workspace_resource_id:
        description:
            - The azure resourceId for the workspace where the solution will be deployed/enabled.
            - Required when C(state) is I(present).
    contained_resources:
        description:
            - The azure resources that will be contained within the solutions. They will be locked and gets deleted automatically when the solution is deleted.
        type: list
    referenced_resources:
        description:
            - The resources that will be referenced from this solution. Deleting any of those solution out of band will break the solution.
        type: list
    state:
      description:
        - Assert the state of the Solution.
        - Use 'present' to create or update an Solution and 'absent' to delete it.
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
  - name: Create (or update) Solution
    azure_rm_operationsmanagementsolution:
      resource_group: rg1
      name: solution1
      location: eastus
      plan:
        name: name1
        publisher: publisher1
        promotion_code: promocode1
        product: product1
      workspace_resource_id: /subscriptions/sub2/resourceGroups/rg2/providers/Microsoft.OperationalInsights/workspaces/ws1
      contained_resources:
        - [
  "/subscriptions/sub2/resourceGroups/rg2/providers/provider1/resources/resource1",
  "/subscriptions/sub2/resourceGroups/rg2/providers/provider2/resources/resource2"
]
      referenced_resources:
        - [
  "/subscriptions/sub2/resourceGroups/rg2/providers/provider1/resources/resource2",
  "/subscriptions/sub2/resourceGroups/rg2/providers/provider2/resources/resource3"
]
'''

RETURN = '''
id:
    description:
        - Resource ID.
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
    from azure.mgmt.operationsmanagement import OperationsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSolutions(AzureRMModuleBase):
    """Configuration class for an Azure RM Solution resource"""

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
            location=dict(
                type='str'
            ),
            plan=dict(
                type='dict'
            ),
            workspace_resource_id=dict(
                type='str'
            ),
            contained_resources=dict(
                type='list'
            ),
            referenced_resources=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSolutions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "plan":
                    self.parameters["plan"] = kwargs[key]
                elif key == "workspace_resource_id":
                    self.parameters.setdefault("properties", {})["workspace_resource_id"] = kwargs[key]
                elif key == "contained_resources":
                    self.parameters.setdefault("properties", {})["contained_resources"] = kwargs[key]
                elif key == "referenced_resources":
                    self.parameters.setdefault("properties", {})["referenced_resources"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(OperationsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_solution()

        if not old_response:
            self.log("Solution instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Solution instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Solution instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_solution()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Solution instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_solution()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_solution():
                time.sleep(20)
        else:
            self.log("Solution instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_solution(self):
        '''
        Creates or updates Solution with the specified configuration.

        :return: deserialized Solution instance state dictionary
        '''
        self.log("Creating / Updating the Solution instance {0}".format(self.name))

        try:
            response = self.mgmt_client.solutions.create_or_update(resource_group_name=self.resource_group,
                                                                   solution_name=self.name,
                                                                   parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Solution instance.')
            self.fail("Error creating the Solution instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_solution(self):
        '''
        Deletes specified Solution instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Solution instance {0}".format(self.name))
        try:
            response = self.mgmt_client.solutions.delete(resource_group_name=self.resource_group,
                                                         solution_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Solution instance.')
            self.fail("Error deleting the Solution instance: {0}".format(str(e)))

        return True

    def get_solution(self):
        '''
        Gets the properties of the specified Solution.

        :return: deserialized Solution instance state dictionary
        '''
        self.log("Checking if the Solution instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.solutions.get(resource_group_name=self.resource_group,
                                                      solution_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Solution instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Solution instance.')
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


def main():
    """Main execution"""
    AzureRMSolutions()


if __name__ == '__main__':
    main()

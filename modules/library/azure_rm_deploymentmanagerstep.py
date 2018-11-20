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
module: azure_rm_deploymentmanagerstep
version_added: "2.8"
short_description: Manage Step instance.
description:
    - Create, update and delete instance of Step.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    name:
        description:
            - The name of the deployment step.
        required: True
    step_info:
        description:
            - The step object.
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                    - Required when C(state) is I(present).
            step_type:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Step.
        - Use 'present' to create or update an Step and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Step
    azure_rm_deploymentmanagerstep:
      resource_group: myResourceGroup
      name: deploymentStep1
      step_info:
        location: centralus
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
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
    from azure.mgmt.deploymentmanager import AzureDeploymentManager
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSteps(AzureRMModuleBase):
    """Configuration class for an Azure RM Step resource"""

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
            step_info=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.step_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSteps, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.step_info["location"] = kwargs[key]
                elif key == "step_type":
                    self.step_info.setdefault("properties", {})["step_type"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureDeploymentManager,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_step()

        if not old_response:
            self.log("Step instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Step instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Step instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_step()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Step instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_step()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_step():
                time.sleep(20)
        else:
            self.log("Step instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_step(self):
        '''
        Creates or updates Step with the specified configuration.

        :return: deserialized Step instance state dictionary
        '''
        self.log("Creating / Updating the Step instance {0}".format(self.name))

        try:
            response = self.mgmt_client.steps.create_or_update(resource_group_name=self.resource_group,
                                                               step_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Step instance.')
            self.fail("Error creating the Step instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_step(self):
        '''
        Deletes specified Step instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Step instance {0}".format(self.name))
        try:
            response = self.mgmt_client.steps.delete(resource_group_name=self.resource_group,
                                                     step_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Step instance.')
            self.fail("Error deleting the Step instance: {0}".format(str(e)))

        return True

    def get_step(self):
        '''
        Gets the properties of the specified Step.

        :return: deserialized Step instance state dictionary
        '''
        self.log("Checking if the Step instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.steps.get(resource_group_name=self.resource_group,
                                                  step_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Step instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Step instance.')
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
    AzureRMSteps()


if __name__ == '__main__':
    main()

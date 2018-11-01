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
module: azure_rm_deploymentmanagerrollout
version_added: "2.8"
short_description: Manage Rollout instance.
description:
    - Create, update and delete instance of Rollout.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    rollout_name:
        description:
            - The rollout name.
        required: True
    rollout_request:
        description:
            - Source rollout request object that defines the rollout.
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                required: True
            identity:
                description:
                    - Identity for the resource.
                required: True
                suboptions:
                    type:
                        description:
                            - The identity type.
                        required: True
                    identity_ids:
                        description:
                            - The list of identities.
                        required: True
                        type: list
            build_version:
                description:
                    - The version of the build being deployed.
                required: True
            artifact_source_id:
                description:
                    - The reference to the artifact source resource Id where the payload is located.
            target_service_topology_id:
                description:
                    - The resource Id of the service topology from which service units are being referenced in step groups to be deployed.
                required: True
            step_groups:
                description:
                    - The list of step groups that define the orchestration.
                required: True
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the step group.
                        required: True
                    depends_on_step_groups:
                        description:
                            - The list of step group names on which this step group depends on.
                        type: list
                    pre_deployment_steps:
                        description:
                            - The list of steps to be run before deploying the target.
                        type: list
                        suboptions:
                            step_id:
                                description:
                                    - The resource Id of the step to be run.
                                required: True
                    deployment_target_id:
                        description:
                            - "The resource Id of service unit to be deployed. The service unit should be from the service topology referenced in
                               targetServiceTopologyId"
                        required: True
                    post_deployment_steps:
                        description:
                            - The list of steps to be run after deploying the target.
                        type: list
                        suboptions:
                            step_id:
                                description:
                                    - The resource Id of the step to be run.
                                required: True
    state:
      description:
        - Assert the state of the Rollout.
        - Use 'present' to create or update an Rollout and 'absent' to delete it.
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
  - name: Create (or update) Rollout
    azure_rm_deploymentmanagerrollout:
      resource_group: myResourceGroup
      rollout_name: myRollout
      rollout_request:
        location: centralus
        identity:
          type: userAssigned
          identity_ids:
            - [
  "/subscriptions/caac1590-e859-444f-a9e0-62091c0f5929/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userassignedidentities/myuseridentity"
]
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


class AzureRMRollouts(AzureRMModuleBase):
    """Configuration class for an Azure RM Rollout resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            rollout_name=dict(
                type='str',
                required=True
            ),
            rollout_request=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.rollout_name = None
        self.rollout_request = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRollouts, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.rollout_request["location"] = kwargs[key]
                elif key == "identity":
                    self.rollout_request["identity"] = kwargs[key]
                elif key == "build_version":
                    self.rollout_request["build_version"] = kwargs[key]
                elif key == "artifact_source_id":
                    self.rollout_request["artifact_source_id"] = kwargs[key]
                elif key == "target_service_topology_id":
                    self.rollout_request["target_service_topology_id"] = kwargs[key]
                elif key == "step_groups":
                    self.rollout_request["step_groups"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureDeploymentManager,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_rollout()

        if not old_response:
            self.log("Rollout instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Rollout instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Rollout instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Rollout instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_rollout()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Rollout instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_rollout()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_rollout():
                time.sleep(20)
        else:
            self.log("Rollout instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_rollout(self):
        '''
        Creates or updates Rollout with the specified configuration.

        :return: deserialized Rollout instance state dictionary
        '''
        self.log("Creating / Updating the Rollout instance {0}".format(self.rollout_name))

        try:
            response = self.mgmt_client.rollouts.create_or_update(resource_group_name=self.resource_group,
                                                                  rollout_name=self.rollout_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Rollout instance.')
            self.fail("Error creating the Rollout instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_rollout(self):
        '''
        Deletes specified Rollout instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Rollout instance {0}".format(self.rollout_name))
        try:
            response = self.mgmt_client.rollouts.delete(resource_group_name=self.resource_group,
                                                        rollout_name=self.rollout_name)
        except CloudError as e:
            self.log('Error attempting to delete the Rollout instance.')
            self.fail("Error deleting the Rollout instance: {0}".format(str(e)))

        return True

    def get_rollout(self):
        '''
        Gets the properties of the specified Rollout.

        :return: deserialized Rollout instance state dictionary
        '''
        self.log("Checking if the Rollout instance {0} is present".format(self.rollout_name))
        found = False
        try:
            response = self.mgmt_client.rollouts.get(resource_group_name=self.resource_group,
                                                     rollout_name=self.rollout_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Rollout instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Rollout instance.')
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
    AzureRMRollouts()


if __name__ == '__main__':
    main()

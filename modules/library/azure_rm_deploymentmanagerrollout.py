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
short_description: Manage Azure Rollout instance.
description:
    - Create, update and delete instance of Azure Rollout.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    name:
        description:
            - The rollout name.
        required: True
    location:
        description:
            - The geo-location where the resource lives
            - Required when C(state) is I(present).
    identity:
        description:
            - Identity for the resource.
            - Required when C(state) is I(present).
        suboptions:
            type:
                description:
                    - The identity type.
                    - Required when C(state) is I(present).
            identity_ids:
                description:
                    - The list of identities.
                    - Required when C(state) is I(present).
                type: list
    build_version:
        description:
            - The version of the build being deployed.
            - Required when C(state) is I(present).
    artifact_source_id:
        description:
            - The reference to the artifact source resource Id where the payload is located.
    target_service_topology_id:
        description:
            - The resource Id of the service topology from which service units are being referenced in step groups to be deployed.
            - Required when C(state) is I(present).
    step_groups:
        description:
            - The list of step groups that define the orchestration.
            - Required when C(state) is I(present).
        type: list
        suboptions:
            name:
                description:
                    - The name of the step group.
                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
            deployment_target_id:
                description:
                    - The resource Id of service unit to be deployed. The service unit should be from the service topology referenced in targetServiceTopologyId
                    - Required when C(state) is I(present).
            post_deployment_steps:
                description:
                    - The list of steps to be run after deploying the target.
                type: list
                suboptions:
                    step_id:
                        description:
                            - The resource Id of the step to be run.
                            - Required when C(state) is I(present).
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
      name: myRollout
      location: centralus
      identity:
        type: userAssigned
        identity_ids:
          - [
  "/subscriptions/caac1590-e859-444f-a9e0-62091c0f5929/resourceGroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userassignedidentities/myuseridentity"
]
      build_version: 1.0.0.1
      artifact_source_id: /subscriptions/caac1590-e859-444f-a9e0-62091c0f5929/resourceGroups/myResourceGroup/Microsoft.DeploymentManager/artifactSources/myArtifactSource
      target_service_topology_id: /subscriptions/caac1590-e859-444f-a9e0-62091c0f5929/resourceGroups/myResourceGroup/Microsoft.DeploymentManager/serviceTopologies/myTopology
      step_groups:
        - name: FirstRegion
          pre_deployment_steps:
            - step_id: Microsoft.DeploymentManager/steps/preDeployStep1
          deployment_target_id: Microsoft.DeploymentManager/serviceTopologies/myTopology/services/myService/serviceUnits/myServiceUnit1'
          post_deployment_steps:
            - step_id: Microsoft.DeploymentManager/steps/postDeployStep1
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMRollout(AzureRMModuleBase):
    """Configuration class for an Azure RM Rollout resource"""

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
            identity=dict(
                type='dict',
                options=dict(
                    type=dict(
                        type='str'
                    ),
                    identity_ids=dict(
                        type='list'
                    )
                )
            ),
            build_version=dict(
                type='str'
            ),
            artifact_source_id=dict(
                type='str'
            ),
            target_service_topology_id=dict(
                type='str'
            ),
            step_groups=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    depends_on_step_groups=dict(
                        type='list'
                    ),
                    pre_deployment_steps=dict(
                        type='list',
                        options=dict(
                            step_id=dict(
                                type='str'
                            )
                        )
                    ),
                    deployment_target_id=dict(
                        type='str'
                    ),
                    post_deployment_steps=dict(
                        type='list',
                        options=dict(
                            step_id=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.rollout_request = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRollout, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.rollout_request[key] = kwargs[key]


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
                if (not default_compare(self.rollout_request, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Rollout instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_rollout()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Rollout instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_rollout()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Rollout instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_rollout(self):
        '''
        Creates or updates Rollout with the specified configuration.

        :return: deserialized Rollout instance state dictionary
        '''
        self.log("Creating / Updating the Rollout instance {0}".format(self.name))

        try:
            response = self.mgmt_client.rollouts.create_or_update(resource_group_name=self.resource_group,
                                                                  rollout_name=self.name)
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
        self.log("Deleting the Rollout instance {0}".format(self.name))
        try:
            response = self.mgmt_client.rollouts.delete(resource_group_name=self.resource_group,
                                                        rollout_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Rollout instance.')
            self.fail("Error deleting the Rollout instance: {0}".format(str(e)))

        return True

    def get_rollout(self):
        '''
        Gets the properties of the specified Rollout.

        :return: deserialized Rollout instance state dictionary
        '''
        self.log("Checking if the Rollout instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.rollouts.get(resource_group_name=self.resource_group,
                                                     rollout_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Rollout instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Rollout instance.')
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
    AzureRMRollout()


if __name__ == '__main__':
    main()

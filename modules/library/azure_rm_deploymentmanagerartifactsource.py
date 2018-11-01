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
module: azure_rm_deploymentmanagerartifactsource
version_added: "2.8"
short_description: Manage Artifact Source instance.
description:
    - Create, update and delete instance of Artifact Source.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    artifact_source_name:
        description:
            - The name of the artifact source.
        required: True
    artifact_source_info:
        description:
            - Source object that defines the resource.
        suboptions:
            location:
                description:
                    - The geo-location where the resource lives
                required: True
            source_type:
                description:
                    - The type of artifact source used.
                required: True
            artifact_root:
                description:
                    - "The path from the location that the 'I(authentication)' property [say, a SAS URI to the blob container] refers to, to the location of
                       the artifacts. This can be used to differentiate different versions of the artifacts. Or, different types of artifacts like binaries
                       or templates. The location referenced by the I(authentication) property concatenated with this optional artifactRoot path forms the
                       artifact source location where the artifacts are expected to be found."
            authentication:
                description:
                    - The authentication method to use to access the artifact source.
                required: True
                suboptions:
                    type:
                        description:
                            - Constant filled by server.
                        required: True
    state:
      description:
        - Assert the state of the Artifact Source.
        - Use 'present' to create or update an Artifact Source and 'absent' to delete it.
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
  - name: Create (or update) Artifact Source
    azure_rm_deploymentmanagerartifactsource:
      resource_group: myResourceGroup
      artifact_source_name: myArtifactSource
      artifact_source_info:
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


class AzureRMArtifactSources(AzureRMModuleBase):
    """Configuration class for an Azure RM Artifact Source resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            artifact_source_name=dict(
                type='str',
                required=True
            ),
            artifact_source_info=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.artifact_source_name = None
        self.artifact_source_info = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMArtifactSources, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.artifact_source_info["location"] = kwargs[key]
                elif key == "source_type":
                    self.artifact_source_info["source_type"] = kwargs[key]
                elif key == "artifact_root":
                    self.artifact_source_info["artifact_root"] = kwargs[key]
                elif key == "authentication":
                    self.artifact_source_info["authentication"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureDeploymentManager,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_artifactsource()

        if not old_response:
            self.log("Artifact Source instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Artifact Source instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Artifact Source instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Artifact Source instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_artifactsource()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Artifact Source instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_artifactsource()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_artifactsource():
                time.sleep(20)
        else:
            self.log("Artifact Source instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_artifactsource(self):
        '''
        Creates or updates Artifact Source with the specified configuration.

        :return: deserialized Artifact Source instance state dictionary
        '''
        self.log("Creating / Updating the Artifact Source instance {0}".format(self.artifact_source_name))

        try:
            response = self.mgmt_client.artifact_sources.create_or_update(resource_group_name=self.resource_group,
                                                                          artifact_source_name=self.artifact_source_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Artifact Source instance.')
            self.fail("Error creating the Artifact Source instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_artifactsource(self):
        '''
        Deletes specified Artifact Source instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Artifact Source instance {0}".format(self.artifact_source_name))
        try:
            response = self.mgmt_client.artifact_sources.delete(resource_group_name=self.resource_group,
                                                                artifact_source_name=self.artifact_source_name)
        except CloudError as e:
            self.log('Error attempting to delete the Artifact Source instance.')
            self.fail("Error deleting the Artifact Source instance: {0}".format(str(e)))

        return True

    def get_artifactsource(self):
        '''
        Gets the properties of the specified Artifact Source.

        :return: deserialized Artifact Source instance state dictionary
        '''
        self.log("Checking if the Artifact Source instance {0} is present".format(self.artifact_source_name))
        found = False
        try:
            response = self.mgmt_client.artifact_sources.get(resource_group_name=self.resource_group,
                                                             artifact_source_name=self.artifact_source_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Artifact Source instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Artifact Source instance.')
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
    AzureRMArtifactSources()


if __name__ == '__main__':
    main()
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
module: azure_rm_blueprintartifact
version_added: "2.8"
short_description: Manage Artifact instance.
description:
    - Create, update and delete instance of Artifact.

options:
    management_group_name:
        description:
            - ManagementGroup where blueprint stores.
        required: True
    blueprint_name:
        description:
            - name of the blueprint.
        required: True
    name:
        description:
            - name of the I(artifact).
        required: True
    artifact:
        description:
            - Blueprint artifact to save.
        required: True
        suboptions:
            kind:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Artifact.
        - Use 'present' to create or update an Artifact and 'absent' to delete it.
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
  - name: Create (or update) Artifact
    azure_rm_blueprintartifact:
      management_group_name: ContosoOnlineGroup
      blueprint_name: simpleBlueprint
      name: storageTemplate
      artifact:
        kind: template
'''

RETURN = '''
id:
    description:
        - String Id used to locate any resource on Azure.
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
    from azure.mgmt.blueprint import BlueprintManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMArtifacts(AzureRMModuleBase):
    """Configuration class for an Azure RM Artifact resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            management_group_name=dict(
                type='str',
                required=True
            ),
            blueprint_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            artifact=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.management_group_name = None
        self.blueprint_name = None
        self.name = None
        self.artifact = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMArtifacts, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "kind":
                    self.artifact["kind"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BlueprintManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_artifact()

        if not old_response:
            self.log("Artifact instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Artifact instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Artifact instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_artifact()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Artifact instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_artifact()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_artifact():
                time.sleep(20)
        else:
            self.log("Artifact instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_artifact(self):
        '''
        Creates or updates Artifact with the specified configuration.

        :return: deserialized Artifact instance state dictionary
        '''
        self.log("Creating / Updating the Artifact instance {0}".format(self.name))

        try:
            response = self.mgmt_client.artifacts.create_or_update(management_group_name=self.management_group_name,
                                                                   blueprint_name=self.blueprint_name,
                                                                   artifact_name=self.name,
                                                                   artifact=self.artifact)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Artifact instance.')
            self.fail("Error creating the Artifact instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_artifact(self):
        '''
        Deletes specified Artifact instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Artifact instance {0}".format(self.name))
        try:
            response = self.mgmt_client.artifacts.delete(management_group_name=self.management_group_name,
                                                         blueprint_name=self.blueprint_name,
                                                         artifact_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Artifact instance.')
            self.fail("Error deleting the Artifact instance: {0}".format(str(e)))

        return True

    def get_artifact(self):
        '''
        Gets the properties of the specified Artifact.

        :return: deserialized Artifact instance state dictionary
        '''
        self.log("Checking if the Artifact instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.artifacts.get(management_group_name=self.management_group_name,
                                                      blueprint_name=self.blueprint_name,
                                                      artifact_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Artifact instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Artifact instance.')
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
    AzureRMArtifacts()


if __name__ == '__main__':
    main()

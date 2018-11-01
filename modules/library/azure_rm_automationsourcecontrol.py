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
module: azure_rm_automationsourcecontrol
version_added: "2.8"
short_description: Manage Source Control instance.
description:
    - Create, update and delete instance of Source Control.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    source_control_name:
        description:
            - The source control name.
        required: True
    repo_url:
        description:
            - The repo url of the source control.
    branch:
        description:
            - The repo branch of the source control. Include branch as empty string for C(vso_tfvc).
    folder_path:
        description:
            - The folder path of the source control. Path must be relative.
    auto_sync:
        description:
            - The auto async of the source control. Default is false.
    publish_runbook:
        description:
            - The auto publish of the source control. Default is true.
    source_type:
        description:
            - The source type. Must be one of C(vso_git), C(vso_tfvc), C(git_hub), case sensitive.
        choices:
            - 'vso_git'
            - 'vso_tfvc'
            - 'git_hub'
    security_token:
        description:
            - The authorization token for the repo of the source control.
        suboptions:
            access_token:
                description:
                    - The access token.
            refresh_token:
                description:
                    - The refresh token.
            token_type:
                description:
                    - The token type. Must be either C(personal_access_token) or C(oauth).
                choices:
                    - 'personal_access_token'
                    - 'oauth'
    description:
        description:
            - The user description of the source control.
    state:
      description:
        - Assert the state of the Source Control.
        - Use 'present' to create or update an Source Control and 'absent' to delete it.
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
  - name: Create (or update) Source Control
    azure_rm_automationsourcecontrol:
      resource_group: rg
      automation_account_name: sampleAccount9
      source_control_name: sampleSourceControl
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/sampleAccount9/sourcecontrols/sampleSourceControl
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSourceControl(AzureRMModuleBase):
    """Configuration class for an Azure RM Source Control resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            source_control_name=dict(
                type='str',
                required=True
            ),
            repo_url=dict(
                type='str'
            ),
            branch=dict(
                type='str'
            ),
            folder_path=dict(
                type='str'
            ),
            auto_sync=dict(
                type='str'
            ),
            publish_runbook=dict(
                type='str'
            ),
            source_type=dict(
                type='str',
                choices=['vso_git',
                         'vso_tfvc',
                         'git_hub']
            ),
            security_token=dict(
                type='dict'
            ),
            description=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.source_control_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSourceControl, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "repo_url":
                    self.parameters["repo_url"] = kwargs[key]
                elif key == "branch":
                    self.parameters["branch"] = kwargs[key]
                elif key == "folder_path":
                    self.parameters["folder_path"] = kwargs[key]
                elif key == "auto_sync":
                    self.parameters["auto_sync"] = kwargs[key]
                elif key == "publish_runbook":
                    self.parameters["publish_runbook"] = kwargs[key]
                elif key == "source_type":
                    self.parameters["source_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "security_token":
                    ev = kwargs[key]
                    if 'token_type' in ev:
                        if ev['token_type'] == 'personal_access_token':
                            ev['token_type'] = 'PersonalAccessToken'
                        elif ev['token_type'] == 'oauth':
                            ev['token_type'] = 'Oauth'
                    self.parameters["security_token"] = ev
                elif key == "description":
                    self.parameters["description"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_sourcecontrol()

        if not old_response:
            self.log("Source Control instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Source Control instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Source Control instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Source Control instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_sourcecontrol()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Source Control instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sourcecontrol()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_sourcecontrol():
                time.sleep(20)
        else:
            self.log("Source Control instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_sourcecontrol(self):
        '''
        Creates or updates Source Control with the specified configuration.

        :return: deserialized Source Control instance state dictionary
        '''
        self.log("Creating / Updating the Source Control instance {0}".format(self.source_control_name))

        try:
            response = self.mgmt_client.source_control.create_or_update(resource_group_name=self.resource_group,
                                                                        automation_account_name=self.automation_account_name,
                                                                        source_control_name=self.source_control_name,
                                                                        parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Source Control instance.')
            self.fail("Error creating the Source Control instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_sourcecontrol(self):
        '''
        Deletes specified Source Control instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Source Control instance {0}".format(self.source_control_name))
        try:
            response = self.mgmt_client.source_control.delete(resource_group_name=self.resource_group,
                                                              automation_account_name=self.automation_account_name,
                                                              source_control_name=self.source_control_name)
        except CloudError as e:
            self.log('Error attempting to delete the Source Control instance.')
            self.fail("Error deleting the Source Control instance: {0}".format(str(e)))

        return True

    def get_sourcecontrol(self):
        '''
        Gets the properties of the specified Source Control.

        :return: deserialized Source Control instance state dictionary
        '''
        self.log("Checking if the Source Control instance {0} is present".format(self.source_control_name))
        found = False
        try:
            response = self.mgmt_client.source_control.get(resource_group_name=self.resource_group,
                                                           automation_account_name=self.automation_account_name,
                                                           source_control_name=self.source_control_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Source Control instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Source Control instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMSourceControl()


if __name__ == '__main__':
    main()

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
short_description: Manage Azure Source Control instance.
description:
    - Create, update and delete instance of Azure Source Control.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    name:
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
      name: sampleSourceControl
      repo_url: https://sampleUser.visualstudio.com/myProject/_git/myRepository
      branch: master
      folder_path: /folderOne/folderTwo
      auto_sync: True
      publish_runbook: True
      source_type: VsoGit
      security_token:
        access_token: 3a326f7a0dcd343ea58fee21f2fd5fb4c1234567
        token_type: PersonalAccessToken
      description: my description
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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
            name=dict(
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
                type='dict',
                options=dict(
                    access_token=dict(
                        type='str'
                    ),
                    refresh_token=dict(
                        type='str'
                    ),
                    token_type=dict(
                        type='str',
                        choices=['personal_access_token',
                                 'oauth']
                    )
                )
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
        self.name = None
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

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['source_type'], True)
        dict_camelize(self.parameters, ['security_token', 'token_type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Source Control instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_sourcecontrol()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Source Control instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_sourcecontrol()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Source Control instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_sourcecontrol(self):
        '''
        Creates or updates Source Control with the specified configuration.

        :return: deserialized Source Control instance state dictionary
        '''
        self.log("Creating / Updating the Source Control instance {0}".format(self.name))

        try:
            response = self.mgmt_client.source_control.create_or_update(resource_group_name=self.resource_group,
                                                                        automation_account_name=self.automation_account_name,
                                                                        source_control_name=self.name,
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
        self.log("Deleting the Source Control instance {0}".format(self.name))
        try:
            response = self.mgmt_client.source_control.delete(resource_group_name=self.resource_group,
                                                              automation_account_name=self.automation_account_name,
                                                              source_control_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Source Control instance.')
            self.fail("Error deleting the Source Control instance: {0}".format(str(e)))

        return True

    def get_sourcecontrol(self):
        '''
        Gets the properties of the specified Source Control.

        :return: deserialized Source Control instance state dictionary
        '''
        self.log("Checking if the Source Control instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.source_control.get(resource_group_name=self.resource_group,
                                                           automation_account_name=self.automation_account_name,
                                                           source_control_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Source Control instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Source Control instance.')
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
            else:
                key = list(old[0])[0]
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


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def main():
    """Main execution"""
    AzureRMSourceControl()


if __name__ == '__main__':
    main()

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
module: azure_rm_automationrunbook
version_added: "2.8"
short_description: Manage Runbook instance.
description:
    - Create, update and delete instance of Runbook.

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
            - The runbook name.
        required: True
    log_verbose:
        description:
            - Gets or sets verbose log option.
    log_progress:
        description:
            - Gets or sets progress log option.
    runbook_type:
        description:
            - Gets or sets the type of the runbook.
            - Required when C(state) is I(present).
        choices:
            - 'script'
            - 'graph'
            - 'power_shell_workflow'
            - 'power_shell'
            - 'graph_power_shell_workflow'
            - 'graph_power_shell'
    draft:
        description:
            - Gets or sets the draft runbook properties.
        suboptions:
            in_edit:
                description:
                    - Gets or sets whether runbook is in edit mode.
            draft_content_link:
                description:
                    - Gets or sets the draft runbook content link.
                suboptions:
                    uri:
                        description:
                            - Gets or sets the uri of the runbook content.
                    content_hash:
                        description:
                            - Gets or sets the hash.
                        suboptions:
                            algorithm:
                                description:
                                    - Gets or sets the content hash algorithm used to hash the content.
                                    - Required when C(state) is I(present).
                            value:
                                description:
                                    - Gets or sets expected hash value of the content.
                                    - Required when C(state) is I(present).
                    version:
                        description:
                            - Gets or sets the version of the content.
            creation_time:
                description:
                    - Gets or sets the creation time of the runbook draft.
            last_modified_time:
                description:
                    - Gets or sets the last modified time of the runbook draft.
            parameters:
                description:
                    - Gets or sets the runbook draft parameters.
            output_types:
                description:
                    - Gets or sets the runbook output types.
                type: list
    publish_content_link:
        description:
            - Gets or sets the published runbook content link.
        suboptions:
            uri:
                description:
                    - Gets or sets the uri of the runbook content.
            content_hash:
                description:
                    - Gets or sets the hash.
                suboptions:
                    algorithm:
                        description:
                            - Gets or sets the content hash algorithm used to hash the content.
                            - Required when C(state) is I(present).
                    value:
                        description:
                            - Gets or sets expected hash value of the content.
                            - Required when C(state) is I(present).
            version:
                description:
                    - Gets or sets the version of the content.
    description:
        description:
            - Gets or sets the description of the runbook.
    log_activity_trace:
        description:
            - Gets or sets the activity-level tracing options of the runbook.
    name:
        description:
            - Gets or sets the name of the resource.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
      description:
        - Assert the state of the Runbook.
        - Use 'present' to create or update an Runbook and 'absent' to delete it.
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
  - name: Create (or update) Runbook
    azure_rm_automationrunbook:
      resource_group: rg
      automation_account_name: ContoseAutomationAccount
      name: Get-AzureVMTutorial
      log_verbose: False
      log_progress: True
      runbook_type: PowerShellWorkflow
      publish_content_link:
        uri: https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-automation-runbook-getvms/Runbooks/Get-AzureVMTutorial.ps1
        content_hash:
          algorithm: SHA256
          value: 115775B8FF2BE672D8A946BD0B489918C724DDE15A440373CA54461D53010A80
      description: Description of the Runbook
      log_activity_trace: 1
      name: Get-AzureVMTutorial
      location: eastus
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: id
state:
    description:
        - "Gets or sets the state of the runbook. Possible values include: 'New', 'Edit', 'Published'"
    returned: always
    type: str
    sample: state
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


class AzureRMRunbook(AzureRMModuleBase):
    """Configuration class for an Azure RM Runbook resource"""

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
            log_verbose=dict(
                type='str'
            ),
            log_progress=dict(
                type='str'
            ),
            runbook_type=dict(
                type='str',
                choices=['script',
                         'graph',
                         'power_shell_workflow',
                         'power_shell',
                         'graph_power_shell_workflow',
                         'graph_power_shell']
            ),
            draft=dict(
                type='dict'
            ),
            publish_content_link=dict(
                type='dict'
            ),
            description=dict(
                type='str'
            ),
            log_activity_trace=dict(
                type='int'
            ),
            name=dict(
                type='str'
            ),
            location=dict(
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

        super(AzureRMRunbook, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "log_verbose":
                    self.parameters["log_verbose"] = kwargs[key]
                elif key == "log_progress":
                    self.parameters["log_progress"] = kwargs[key]
                elif key == "runbook_type":
                    self.parameters["runbook_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "draft":
                    self.parameters["draft"] = kwargs[key]
                elif key == "publish_content_link":
                    self.parameters["publish_content_link"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "log_activity_trace":
                    self.parameters["log_activity_trace"] = kwargs[key]
                elif key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_runbook()

        if not old_response:
            self.log("Runbook instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Runbook instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Runbook instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_runbook()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Runbook instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_runbook()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_runbook():
                time.sleep(20)
        else:
            self.log("Runbook instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_runbook(self):
        '''
        Creates or updates Runbook with the specified configuration.

        :return: deserialized Runbook instance state dictionary
        '''
        self.log("Creating / Updating the Runbook instance {0}".format(self.name))

        try:
            response = self.mgmt_client.runbook.create_or_update(resource_group_name=self.resource_group,
                                                                 automation_account_name=self.automation_account_name,
                                                                 runbook_name=self.name,
                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Runbook instance.')
            self.fail("Error creating the Runbook instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_runbook(self):
        '''
        Deletes specified Runbook instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Runbook instance {0}".format(self.name))
        try:
            response = self.mgmt_client.runbook.delete(resource_group_name=self.resource_group,
                                                       automation_account_name=self.automation_account_name,
                                                       runbook_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Runbook instance.')
            self.fail("Error deleting the Runbook instance: {0}".format(str(e)))

        return True

    def get_runbook(self):
        '''
        Gets the properties of the specified Runbook.

        :return: deserialized Runbook instance state dictionary
        '''
        self.log("Checking if the Runbook instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.runbook.get(resource_group_name=self.resource_group,
                                                    automation_account_name=self.automation_account_name,
                                                    runbook_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Runbook instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Runbook instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
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
    AzureRMRunbook()


if __name__ == '__main__':
    main()

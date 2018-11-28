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
short_description: Manage Azure Runbook instance.
description:
    - Create, update and delete instance of Azure Runbook.

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
                type='dict',
                options=dict(
                    in_edit=dict(
                        type='str'
                    ),
                    draft_content_link=dict(
                        type='dict',
                        options=dict(
                            uri=dict(
                                type='str'
                            ),
                            content_hash=dict(
                                type='dict',
                                options=dict(
                                    algorithm=dict(
                                        type='str'
                                    ),
                                    value=dict(
                                        type='str'
                                    )
                                )
                            ),
                            version=dict(
                                type='str'
                            )
                        )
                    ),
                    creation_time=dict(
                        type='datetime'
                    ),
                    last_modified_time=dict(
                        type='datetime'
                    ),
                    parameters=dict(
                        type='dict'
                    ),
                    output_types=dict(
                        type='list'
                    )
                )
            ),
            publish_content_link=dict(
                type='dict',
                options=dict(
                    uri=dict(
                        type='str'
                    ),
                    content_hash=dict(
                        type='dict',
                        options=dict(
                            algorithm=dict(
                                type='str'
                            ),
                            value=dict(
                                type='str'
                            )
                        )
                    ),
                    version=dict(
                        type='str'
                    )
                )
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
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['runbook_type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Runbook instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None)
                })
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
    AzureRMRunbook()


if __name__ == '__main__':
    main()

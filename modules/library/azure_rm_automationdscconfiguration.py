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
module: azure_rm_automationdscconfiguration
version_added: "2.8"
short_description: Manage Dsc Configuration instance.
description:
    - Create, update and delete instance of Dsc Configuration.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    configuration_name:
        description:
            - The create or update I(parameters) for configuration.
        required: True
    log_verbose:
        description:
            - Gets or sets verbose log option.
    log_progress:
        description:
            - Gets or sets progress log option.
    source:
        description:
            - Gets or sets the source.
        required: True
        suboptions:
            hash:
                description:
                    - Gets or sets the hash.
                suboptions:
                    algorithm:
                        description:
                            - Gets or sets the content hash algorithm used to hash the content.
                        required: True
                    value:
                        description:
                            - Gets or sets expected hash value of the content.
                        required: True
            type:
                description:
                    - Gets or sets the content source type.
                choices:
                    - 'embedded_content'
                    - 'uri'
            value:
                description:
                    - Gets or sets the value of the content. This is based on the content source I(type).
            version:
                description:
                    - Gets or sets the version of the content.
    parameters:
        description:
            - Gets or sets the configuration parameters.
    description:
        description:
            - Gets or sets the description of the configuration.
    name:
        description:
            - Gets or sets name of the resource.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
      description:
        - Assert the state of the Dsc Configuration.
        - Use 'present' to create or update an Dsc Configuration and 'absent' to delete it.
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
  - name: Create (or update) Dsc Configuration
    azure_rm_automationdscconfiguration:
      resource_group: rg
      automation_account_name: myAutomationAccount18
      configuration_name: SetupServer
      name: SetupServer
      location: eastus
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/configurations/SetupServer
state:
    description:
        - "Gets or sets the state of the configuration. Possible values include: 'New', 'Edit', 'Published'"
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


class AzureRMDscConfiguration(AzureRMModuleBase):
    """Configuration class for an Azure RM Dsc Configuration resource"""

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
            configuration_name=dict(
                type='str',
                required=True
            ),
            log_verbose=dict(
                type='str'
            ),
            log_progress=dict(
                type='str'
            ),
            source=dict(
                type='dict',
                required=True
            ),
            parameters=dict(
                type='dict'
            ),
            description=dict(
                type='str'
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
        self.configuration_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDscConfiguration, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "source":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'embedded_content':
                            ev['type'] = 'embeddedContent'
                    self.parameters["source"] = ev
                elif key == "parameters":
                    self.parameters["parameters"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "location":
                    self.parameters["location"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_dscconfiguration()

        if not old_response:
            self.log("Dsc Configuration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Dsc Configuration instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Dsc Configuration instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dsc Configuration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dscconfiguration()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dsc Configuration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dscconfiguration()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_dscconfiguration():
                time.sleep(20)
        else:
            self.log("Dsc Configuration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_dscconfiguration(self):
        '''
        Creates or updates Dsc Configuration with the specified configuration.

        :return: deserialized Dsc Configuration instance state dictionary
        '''
        self.log("Creating / Updating the Dsc Configuration instance {0}".format(self.configuration_name))

        try:
            response = self.mgmt_client.dsc_configuration.create_or_update(resource_group_name=self.resource_group,
                                                                           automation_account_name=self.automation_account_name,
                                                                           configuration_name=self.configuration_name,
                                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Dsc Configuration instance.')
            self.fail("Error creating the Dsc Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_dscconfiguration(self):
        '''
        Deletes specified Dsc Configuration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Dsc Configuration instance {0}".format(self.configuration_name))
        try:
            response = self.mgmt_client.dsc_configuration.delete(resource_group_name=self.resource_group,
                                                                 automation_account_name=self.automation_account_name,
                                                                 configuration_name=self.configuration_name)
        except CloudError as e:
            self.log('Error attempting to delete the Dsc Configuration instance.')
            self.fail("Error deleting the Dsc Configuration instance: {0}".format(str(e)))

        return True

    def get_dscconfiguration(self):
        '''
        Gets the properties of the specified Dsc Configuration.

        :return: deserialized Dsc Configuration instance state dictionary
        '''
        self.log("Checking if the Dsc Configuration instance {0} is present".format(self.configuration_name))
        found = False
        try:
            response = self.mgmt_client.dsc_configuration.get(resource_group_name=self.resource_group,
                                                              automation_account_name=self.automation_account_name,
                                                              configuration_name=self.configuration_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Dsc Configuration instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Dsc Configuration instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMDscConfiguration()


if __name__ == '__main__':
    main()

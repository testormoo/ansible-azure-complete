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
module: azure_rm_automationdscnodeconfiguration
version_added: "2.8"
short_description: Manage Azure Dsc Node Configuration instance.
description:
    - Create, update and delete instance of Azure Dsc Node Configuration.

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
            - The Dsc node I(configuration) name.
        required: True
    source:
        description:
            - Gets or sets the source.
            - Required when C(state) is I(present).
        suboptions:
            hash:
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
    configuration:
        description:
            - Gets or sets the configuration of the node.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - Gets or sets the name of the Dsc configuration.
    increment_node_configuration_build:
        description:
            - If a new build version of NodeConfiguration is required.
    name:
        description:
            - Name of the node I(configuration).
    state:
      description:
        - Assert the state of the Dsc Node Configuration.
        - Use 'present' to create or update an Dsc Node Configuration and 'absent' to delete it.
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
  - name: Create (or update) Dsc Node Configuration
    azure_rm_automationdscnodeconfiguration:
      resource_group: rg
      automation_account_name: myAutomationAccount20
      name: configName.nodeConfigName
      source:
        hash:
          algorithm: sha256
          value: 6DE256A57F01BFA29B88696D5E77A383D6E61484C7686E8DB955FA10ACE9FFE5
        type: embeddedContent
        value:
instance of MSFT_RoleResource as $MSFT_RoleResource1ref
{
ResourceID = "[WindowsFeature]IIS";
 Ensure = "Present";
 SourceInfo = "::3::32::WindowsFeature";
 Name = "Web-Server";
 ModuleName = "PsDesiredStateConfiguration";
ModuleVersion = "1.0";
 ConfigurationName = "configName";
};
instance of OMI_ConfigurationDocument
                    {
 Version="2.0.0";
                        MinimumCompatibleVersion = "1.0.0";
                        CompatibleVersionAdditionalProperties= {"Omi_BaseResource:ConfigurationName"};
                        Author="weijiel";
                        GenerationDate="03/30/2017 13:40:25";
                        GenerationHost="TEST-BACKEND";
                        Name="configName";
                    };
        version: 1.0
      configuration:
        name: configName
      increment_node_configuration_build: True
      name: configName.nodeConfigName
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
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
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDscNodeConfiguration(AzureRMModuleBase):
    """Configuration class for an Azure RM Dsc Node Configuration resource"""

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
            source=dict(
                type='dict'
                options=dict(
                    hash=dict(
                        type='dict'
                        options=dict(
                            algorithm=dict(
                                type='str'
                            ),
                            value=dict(
                                type='str'
                            )
                        )
                    ),
                    type=dict(
                        type='str',
                        choices=['embedded_content',
                                 'uri']
                    ),
                    value=dict(
                        type='str'
                    ),
                    version=dict(
                        type='str'
                    )
                )
            ),
            configuration=dict(
                type='dict'
                options=dict(
                    name=dict(
                        type='str'
                    )
                )
            ),
            increment_node_configuration_build=dict(
                type='str'
            ),
            name=dict(
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

        super(AzureRMDscNodeConfiguration, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['source', 'type'], True)
        dict_map(self.parameters, ['source', 'type'], {'embedded_content': 'embeddedContent'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_dscnodeconfiguration()

        if not old_response:
            self.log("Dsc Node Configuration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Dsc Node Configuration instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dsc Node Configuration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dscnodeconfiguration()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dsc Node Configuration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dscnodeconfiguration()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Dsc Node Configuration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_dscnodeconfiguration(self):
        '''
        Creates or updates Dsc Node Configuration with the specified configuration.

        :return: deserialized Dsc Node Configuration instance state dictionary
        '''
        self.log("Creating / Updating the Dsc Node Configuration instance {0}".format(self.name))

        try:
            response = self.mgmt_client.dsc_node_configuration.create_or_update(resource_group_name=self.resource_group,
                                                                                automation_account_name=self.automation_account_name,
                                                                                node_configuration_name=self.name,
                                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Dsc Node Configuration instance.')
            self.fail("Error creating the Dsc Node Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_dscnodeconfiguration(self):
        '''
        Deletes specified Dsc Node Configuration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Dsc Node Configuration instance {0}".format(self.name))
        try:
            response = self.mgmt_client.dsc_node_configuration.delete(resource_group_name=self.resource_group,
                                                                      automation_account_name=self.automation_account_name,
                                                                      node_configuration_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Dsc Node Configuration instance.')
            self.fail("Error deleting the Dsc Node Configuration instance: {0}".format(str(e)))

        return True

    def get_dscnodeconfiguration(self):
        '''
        Gets the properties of the specified Dsc Node Configuration.

        :return: deserialized Dsc Node Configuration instance state dictionary
        '''
        self.log("Checking if the Dsc Node Configuration instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.dsc_node_configuration.get(resource_group_name=self.resource_group,
                                                                   automation_account_name=self.automation_account_name,
                                                                   node_configuration_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Dsc Node Configuration instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Dsc Node Configuration instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMDscNodeConfiguration()


if __name__ == '__main__':
    main()

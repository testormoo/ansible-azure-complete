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
module: azure_rm_logicintegrationaccountassembly
version_added: "2.8"
short_description: Manage Integration Account Assembly instance.
description:
    - Create, update and delete instance of Integration Account Assembly.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    assembly_artifact_name:
        description:
            - The assembly artifact name.
        required: True
    assembly_artifact:
        description:
            - The assembly artifact.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            created_time:
                description:
                    - The artifact creation time.
            changed_time:
                description:
                    - The artifact changed time.
            metadata:
                description:
            content:
                description:
            content_type:
                description:
                    - The I(content) type.
            content_link:
                description:
                    - The I(content) link.
                suboptions:
                    uri:
                        description:
                            - The content link URI.
                    content_version:
                        description:
                            - The content version.
                    content_size:
                        description:
                            - The content size.
                    content_hash:
                        description:
                            - The content hash.
                        suboptions:
                            algorithm:
                                description:
                                    - The algorithm of the content hash.
                            value:
                                description:
                                    - The value of the content hash.
                    metadata:
                        description:
                            - The metadata.
            assembly_name:
                description:
                    - The assembly name.
                required: True
            assembly_version:
                description:
                    - The assembly version.
            assembly_culture:
                description:
                    - The assembly culture.
            assembly_public_key_token:
                description:
                    - The assembly public key token.
    state:
      description:
        - Assert the state of the Integration Account Assembly.
        - Use 'present' to create or update an Integration Account Assembly and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Assembly
    azure_rm_logicintegrationaccountassembly:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      assembly_artifact_name: testAssembly
      assembly_artifact:
        location: westus
        metadata: {}
        content: Base64 encoded Assembly Content
        assembly_name: System.IdentityModel.Tokens.Jwt
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/testIntegrati
            onAccount/assemblies/testAssembly"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIntegrationAccountAssemblies(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Assembly resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            integration_account_name=dict(
                type='str',
                required=True
            ),
            assembly_artifact_name=dict(
                type='str',
                required=True
            ),
            assembly_artifact=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.integration_account_name = None
        self.assembly_artifact_name = None
        self.assembly_artifact = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountAssemblies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                  supports_check_mode=True,
                                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.assembly_artifact["location"] = kwargs[key]
                elif key == "created_time":
                    self.assembly_artifact.setdefault("properties", {})["created_time"] = kwargs[key]
                elif key == "changed_time":
                    self.assembly_artifact.setdefault("properties", {})["changed_time"] = kwargs[key]
                elif key == "metadata":
                    self.assembly_artifact.setdefault("properties", {})["metadata"] = kwargs[key]
                elif key == "content":
                    self.assembly_artifact.setdefault("properties", {})["content"] = kwargs[key]
                elif key == "content_type":
                    self.assembly_artifact.setdefault("properties", {})["content_type"] = kwargs[key]
                elif key == "content_link":
                    self.assembly_artifact.setdefault("properties", {})["content_link"] = kwargs[key]
                elif key == "assembly_name":
                    self.assembly_artifact.setdefault("properties", {})["assembly_name"] = kwargs[key]
                elif key == "assembly_version":
                    self.assembly_artifact.setdefault("properties", {})["assembly_version"] = kwargs[key]
                elif key == "assembly_culture":
                    self.assembly_artifact.setdefault("properties", {})["assembly_culture"] = kwargs[key]
                elif key == "assembly_public_key_token":
                    self.assembly_artifact.setdefault("properties", {})["assembly_public_key_token"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountassembly()

        if not old_response:
            self.log("Integration Account Assembly instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Assembly instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Integration Account Assembly instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Assembly instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountassembly()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Assembly instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountassembly()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccountassembly():
                time.sleep(20)
        else:
            self.log("Integration Account Assembly instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccountassembly(self):
        '''
        Creates or updates Integration Account Assembly with the specified configuration.

        :return: deserialized Integration Account Assembly instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Assembly instance {0}".format(self.assembly_artifact_name))

        try:
            response = self.mgmt_client.integration_account_assemblies.create_or_update(resource_group_name=self.resource_group,
                                                                                        integration_account_name=self.integration_account_name,
                                                                                        assembly_artifact_name=self.assembly_artifact_name,
                                                                                        assembly_artifact=self.assembly_artifact)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Assembly instance.')
            self.fail("Error creating the Integration Account Assembly instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountassembly(self):
        '''
        Deletes specified Integration Account Assembly instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Assembly instance {0}".format(self.assembly_artifact_name))
        try:
            response = self.mgmt_client.integration_account_assemblies.delete(resource_group_name=self.resource_group,
                                                                              integration_account_name=self.integration_account_name,
                                                                              assembly_artifact_name=self.assembly_artifact_name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Assembly instance.')
            self.fail("Error deleting the Integration Account Assembly instance: {0}".format(str(e)))

        return True

    def get_integrationaccountassembly(self):
        '''
        Gets the properties of the specified Integration Account Assembly.

        :return: deserialized Integration Account Assembly instance state dictionary
        '''
        self.log("Checking if the Integration Account Assembly instance {0} is present".format(self.assembly_artifact_name))
        found = False
        try:
            response = self.mgmt_client.integration_account_assemblies.get(resource_group_name=self.resource_group,
                                                                           integration_account_name=self.integration_account_name,
                                                                           assembly_artifact_name=self.assembly_artifact_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Assembly instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Assembly instance.')
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
    AzureRMIntegrationAccountAssemblies()


if __name__ == '__main__':
    main()

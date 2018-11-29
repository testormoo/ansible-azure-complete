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
short_description: Manage Azure Integration Account Assembly instance.
description:
    - Create, update and delete instance of Azure Integration Account Assembly.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    name:
        description:
            - The assembly artifact name.
        required: True
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
            - Required when C(state) is I(present).
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
      name: testAssembly
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMIntegrationAccountAssembly(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            created_time=dict(
                type='datetime'
            ),
            changed_time=dict(
                type='datetime'
            ),
            metadata=dict(
                type='str'
            ),
            content=dict(
                type='str'
            ),
            content_type=dict(
                type='str'
            ),
            content_link=dict(
                type='dict',
                options=dict(
                    uri=dict(
                        type='str'
                    ),
                    content_version=dict(
                        type='str'
                    ),
                    content_size=dict(
                        type='int'
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
                    metadata=dict(
                        type='str'
                    )
                )
            ),
            assembly_name=dict(
                type='str'
            ),
            assembly_version=dict(
                type='str'
            ),
            assembly_culture=dict(
                type='str'
            ),
            assembly_public_key_token=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.integration_account_name = None
        self.name = None
        self.assembly_artifact = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountAssembly, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                  supports_check_mode=True,
                                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.assembly_artifact[key] = kwargs[key]

        dict_expand(self.assembly_artifact, ['created_time'])
        dict_expand(self.assembly_artifact, ['changed_time'])
        dict_expand(self.assembly_artifact, ['metadata'])
        dict_expand(self.assembly_artifact, ['content'])
        dict_expand(self.assembly_artifact, ['content_type'])
        dict_expand(self.assembly_artifact, ['content_link'])
        dict_expand(self.assembly_artifact, ['assembly_name'])
        dict_expand(self.assembly_artifact, ['assembly_version'])
        dict_expand(self.assembly_artifact, ['assembly_culture'])
        dict_expand(self.assembly_artifact, ['assembly_public_key_token'])

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
                if (not default_compare(self.assembly_artifact, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Assembly instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountassembly()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Assembly instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountassembly()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Integration Account Assembly instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_integrationaccountassembly(self):
        '''
        Creates or updates Integration Account Assembly with the specified configuration.

        :return: deserialized Integration Account Assembly instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Assembly instance {0}".format(self.name))

        try:
            response = self.mgmt_client.integration_account_assemblies.create_or_update(resource_group_name=self.resource_group,
                                                                                        integration_account_name=self.integration_account_name,
                                                                                        assembly_artifact_name=self.name,
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
        self.log("Deleting the Integration Account Assembly instance {0}".format(self.name))
        try:
            response = self.mgmt_client.integration_account_assemblies.delete(resource_group_name=self.resource_group,
                                                                              integration_account_name=self.integration_account_name,
                                                                              assembly_artifact_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Assembly instance.')
            self.fail("Error deleting the Integration Account Assembly instance: {0}".format(str(e)))

        return True

    def get_integrationaccountassembly(self):
        '''
        Gets the properties of the specified Integration Account Assembly.

        :return: deserialized Integration Account Assembly instance state dictionary
        '''
        self.log("Checking if the Integration Account Assembly instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.integration_account_assemblies.get(resource_group_name=self.resource_group,
                                                                           integration_account_name=self.integration_account_name,
                                                                           assembly_artifact_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Assembly instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Assembly instance.')
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


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def main():
    """Main execution"""
    AzureRMIntegrationAccountAssembly()


if __name__ == '__main__':
    main()

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
module: azure_rm_logicintegrationaccountcertificate
version_added: "2.8"
short_description: Manage Azure Integration Account Certificate instance.
description:
    - Create, update and delete instance of Azure Integration Account Certificate.

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
            - The integration account certificate name.
        required: True
    location:
        description:
            - The resource location.
    metadata:
        description:
            - The metadata.
    key:
        description:
            - The key details in the key vault.
        suboptions:
            key_vault:
                description:
                    - The key vault reference.
                    - Required when C(state) is I(present).
                suboptions:
                    id:
                        description:
                            - The resource id.
            key_name:
                description:
                    - The private key name in key vault.
                    - Required when C(state) is I(present).
            key_version:
                description:
                    - The private key version in key vault.
    public_certificate:
        description:
            - The public certificate.
    state:
      description:
        - Assert the state of the Integration Account Certificate.
        - Use 'present' to create or update an Integration Account Certificate and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Certificate
    azure_rm_logicintegrationaccountcertificate:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      name: testCertificate
      location: brazilsouth
      key:
        key_vault:
          id: /subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourcegroups/testResourceGroup/providers/microsoft.keyvault/vaults/<keyVaultName>
        key_name: <keyName>
        key_version: 87d9764197604449b9b8eb7bd8710868
      public_certificate: <publicCertificateValue>
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/testIntegrati
            onAccount/certificates/testCertificate"
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


class AzureRMIntegrationAccountCertificate(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Certificate resource"""

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
            metadata=dict(
                type='str'
            ),
            key=dict(
                type='dict'
                options=dict(
                    key_vault=dict(
                        type='dict'
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    key_name=dict(
                        type='str'
                    ),
                    key_version=dict(
                        type='str'
                    )
                )
            ),
            public_certificate=dict(
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
        self.certificate = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountCertificate, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.certificate[key] = kwargs[key]

        dict_resource_id(self.certificate, ['key', 'key_vault', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountcertificate()

        if not old_response:
            self.log("Integration Account Certificate instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Certificate instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.certificate, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Certificate instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountcertificate()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Certificate instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountcertificate()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Integration Account Certificate instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_integrationaccountcertificate(self):
        '''
        Creates or updates Integration Account Certificate with the specified configuration.

        :return: deserialized Integration Account Certificate instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Certificate instance {0}".format(self.name))

        try:
            response = self.mgmt_client.integration_account_certificates.create_or_update(resource_group_name=self.resource_group,
                                                                                          integration_account_name=self.integration_account_name,
                                                                                          certificate_name=self.name,
                                                                                          certificate=self.certificate)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Certificate instance.')
            self.fail("Error creating the Integration Account Certificate instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountcertificate(self):
        '''
        Deletes specified Integration Account Certificate instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Certificate instance {0}".format(self.name))
        try:
            response = self.mgmt_client.integration_account_certificates.delete(resource_group_name=self.resource_group,
                                                                                integration_account_name=self.integration_account_name,
                                                                                certificate_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Certificate instance.')
            self.fail("Error deleting the Integration Account Certificate instance: {0}".format(str(e)))

        return True

    def get_integrationaccountcertificate(self):
        '''
        Gets the properties of the specified Integration Account Certificate.

        :return: deserialized Integration Account Certificate instance state dictionary
        '''
        self.log("Checking if the Integration Account Certificate instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.integration_account_certificates.get(resource_group_name=self.resource_group,
                                                                             integration_account_name=self.integration_account_name,
                                                                             certificate_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Certificate instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Certificate instance.')
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
    AzureRMIntegrationAccountCertificate()


if __name__ == '__main__':
    main()

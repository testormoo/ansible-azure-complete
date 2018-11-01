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
module: azure_rm_storsimplestorageaccountcredential
version_added: "2.8"
short_description: Manage Storage Account Credential instance.
description:
    - Create, update and delete instance of Storage Account Credential.

options:
    credential_name:
        description:
            - The credential name.
        required: True
    storage_account:
        description:
            - The storage account credential to be added or updated.
        required: True
        suboptions:
            cloud_type:
                description:
                    - The cloud service provider.
                required: True
                choices:
                    - 'azure'
                    - 's3'
                    - 's3_rrs'
                    - 'open_stack'
                    - 'hp'
            end_point:
                description:
                    - The storage endpoint
                required: True
            login:
                description:
                    - The storage account login
                required: True
            location:
                description:
                    - "The storage account's geo location"
            enable_ssl:
                description:
                    - SSL needs to be C(enabled) or not.
                required: True
                choices:
                    - 'enabled'
                    - 'disabled'
            access_key:
                description:
                    - The details of the storage account password
                suboptions:
                    value:
                        description:
                            - "The value of the secret itself. If the secret is in plaintext then I(encryption_algorithm) will be C(none) and
                               EncryptionCertThumbprint will be null."
                        required: True
                    encryption_certificate_thumbprint:
                        description:
                            - "Thumbprint certificate that was used to encrypt 'I(value)'"
                    encryption_algorithm:
                        description:
                            - "Algorithm used to encrypt 'I(value)'."
                        required: True
                        choices:
                            - 'none'
                            - 'aes256'
                            - 'rsaes_pkcs1_v_1_5'
    resource_group:
        description:
            - The resource group name
        required: True
    manager_name:
        description:
            - The manager name
        required: True
    state:
      description:
        - Assert the state of the Storage Account Credential.
        - Use 'present' to create or update an Storage Account Credential and 'absent' to delete it.
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
  - name: Create (or update) Storage Account Credential
    azure_rm_storsimplestorageaccountcredential:
      credential_name: DummySacForSDKTest
      resource_group: ResourceGroupForSDKTest
      manager_name: hAzureSDKOperations
'''

RETURN = '''
id:
    description:
        - The identifier.
    returned: always
    type: str
    sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzureSDKOper
            ations/storageAccountCredentials/sacforsdktest"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMStorageAccountCredentials(AzureRMModuleBase):
    """Configuration class for an Azure RM Storage Account Credential resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            credential_name=dict(
                type='str',
                required=True
            ),
            storage_account=dict(
                type='dict',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            manager_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.credential_name = None
        self.storage_account = dict()
        self.resource_group = None
        self.manager_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStorageAccountCredentials, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                               supports_check_mode=True,
                                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "cloud_type":
                    ev = kwargs[key]
                    if ev == 's3_rrs':
                        ev = 'S3_RRS'
                    elif ev == 'hp':
                        ev = 'HP'
                    self.storage_account["cloud_type"] = _snake_to_camel(ev, True)
                elif key == "end_point":
                    self.storage_account["end_point"] = kwargs[key]
                elif key == "login":
                    self.storage_account["login"] = kwargs[key]
                elif key == "location":
                    self.storage_account["location"] = kwargs[key]
                elif key == "enable_ssl":
                    self.storage_account["enable_ssl"] = _snake_to_camel(kwargs[key], True)
                elif key == "access_key":
                    ev = kwargs[key]
                    if 'encryption_algorithm' in ev:
                        if ev['encryption_algorithm'] == 'none':
                            ev['encryption_algorithm'] = 'None'
                        elif ev['encryption_algorithm'] == 'aes256':
                            ev['encryption_algorithm'] = 'AES256'
                        elif ev['encryption_algorithm'] == 'rsaes_pkcs1_v_1_5':
                            ev['encryption_algorithm'] = 'RSAES_PKCS1_v_1_5'
                    self.storage_account["access_key"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_storageaccountcredential()

        if not old_response:
            self.log("Storage Account Credential instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Storage Account Credential instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Storage Account Credential instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Storage Account Credential instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_storageaccountcredential()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Storage Account Credential instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_storageaccountcredential()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_storageaccountcredential():
                time.sleep(20)
        else:
            self.log("Storage Account Credential instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_storageaccountcredential(self):
        '''
        Creates or updates Storage Account Credential with the specified configuration.

        :return: deserialized Storage Account Credential instance state dictionary
        '''
        self.log("Creating / Updating the Storage Account Credential instance {0}".format(self.manager_name))

        try:
            response = self.mgmt_client.storage_account_credentials.create_or_update(credential_name=self.credential_name,
                                                                                     storage_account=self.storage_account,
                                                                                     resource_group_name=self.resource_group,
                                                                                     manager_name=self.manager_name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Storage Account Credential instance.')
            self.fail("Error creating the Storage Account Credential instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_storageaccountcredential(self):
        '''
        Deletes specified Storage Account Credential instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Storage Account Credential instance {0}".format(self.manager_name))
        try:
            response = self.mgmt_client.storage_account_credentials.delete(credential_name=self.credential_name,
                                                                           resource_group_name=self.resource_group,
                                                                           manager_name=self.manager_name)
        except CloudError as e:
            self.log('Error attempting to delete the Storage Account Credential instance.')
            self.fail("Error deleting the Storage Account Credential instance: {0}".format(str(e)))

        return True

    def get_storageaccountcredential(self):
        '''
        Gets the properties of the specified Storage Account Credential.

        :return: deserialized Storage Account Credential instance state dictionary
        '''
        self.log("Checking if the Storage Account Credential instance {0} is present".format(self.manager_name))
        found = False
        try:
            response = self.mgmt_client.storage_account_credentials.get(credential_name=self.credential_name,
                                                                        resource_group_name=self.resource_group,
                                                                        manager_name=self.manager_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Storage Account Credential instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Storage Account Credential instance.')
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
    AzureRMStorageAccountCredentials()


if __name__ == '__main__':
    main()
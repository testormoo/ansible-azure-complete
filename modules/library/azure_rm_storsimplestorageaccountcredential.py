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
short_description: Manage Azure Storage Account Credential instance.
description:
    - Create, update and delete instance of Azure Storage Account Credential.

options:
    credential_name:
        description:
            - The credential name.
        required: True
    cloud_type:
        description:
            - The cloud service provider.
            - Required when C(state) is I(present).
        choices:
            - 'azure'
            - 's3'
            - 's3_rrs'
            - 'open_stack'
            - 'hp'
    end_point:
        description:
            - The storage endpoint
            - Required when C(state) is I(present).
    login:
        description:
            - The storage account login
            - Required when C(state) is I(present).
    location:
        description:
            - "The storage account's geo location"
    enable_ssl:
        description:
            - "SSL needs to be enabled or not. Possible values include: 'Enabled', 'Disabled'"
            - Required when C(state) is I(present).
        type: bool
    access_key:
        description:
            - The details of the storage account password
        suboptions:
            value:
                description:
                    - "The value of the secret itself. If the secret is in plaintext then I(encryption_algorithm) will be C(none) and
                       EncryptionCertThumbprint will be null."
                    - Required when C(state) is I(present).
            encryption_certificate_thumbprint:
                description:
                    - "Thumbprint certificate that was used to encrypt 'I(value)'"
            encryption_algorithm:
                description:
                    - "Algorithm used to encrypt 'I(value)'."
                    - Required when C(state) is I(present).
                choices:
                    - 'none'
                    - 'aes256'
                    - 'rsaes_pkcs1_v_1_5'
    resource_group:
        description:
            - The resource group name
        required: True
    name:
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
      cloud_type: Azure
      end_point: blob.core.windows.net
      login: SacForSDKTest
      location: West US
      enable_ssl: enable_ssl
      access_key:
        value: Ev1tm0QBmpGGm4a58GkqLqx8veJEEgQtg5K3Jizpmy7JdSv9dlcRwk59THw6KIdMDlEHcS8mPyneBtOEQsh4wkcFB7qrmQz+KsRAyIhEm6bwPEm3qN8+aDDzNcXn/6vu/sqV0AP7zit9/s7SxXGxjKrz4zKnOy16/DbzRRmUHNO+HO6JUM0cUfHXTX0mEecbsXqBq0A8IEG8z+bJgXX1EhoGkzE6yVsObm4S1AcKrLiwWjqmSLji5Q8gGO+y4KTTmC3p45h5GHHXjJyOccHhySWDAffxnTzUD/sOoh+aD2VkAYrL3DdnkVzhAdfcZfVI4soONx7tYMloZIVsfW1M2Q==
        encryption_certificate_thumbprint: D73DB57C4CDD6761E159F8D1E8A7D759424983FD
        encryption_algorithm: RSAES_PKCS1_v_1_5
      resource_group: ResourceGroupForSDKTest
      name: hAzureSDKOperations
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMStorageAccountCredential(AzureRMModuleBase):
    """Configuration class for an Azure RM Storage Account Credential resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            credential_name=dict(
                type='str',
                required=True
            ),
            cloud_type=dict(
                type='str',
                choices=['azure',
                         's3',
                         's3_rrs',
                         'open_stack',
                         'hp']
            ),
            end_point=dict(
                type='str'
            ),
            login=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            enable_ssl=dict(
                type='bool'
            ),
            access_key=dict(
                type='dict',
                options=dict(
                    value=dict(
                        type='str'
                    ),
                    encryption_certificate_thumbprint=dict(
                        type='str'
                    ),
                    encryption_algorithm=dict(
                        type='str',
                        choices=['none',
                                 'aes256',
                                 'rsaes_pkcs1_v_1_5']
                    )
                )
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStorageAccountCredential, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                supports_check_mode=True,
                                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.storage_account[key] = kwargs[key]

        dict_camelize(self.storage_account, ['cloud_type'], True)
        dict_map(self.storage_account, ['cloud_type'], {'s3_rrs': 'S3_RRS', 'hp': 'HP'})
        dict_map(self.storage_account, ['enable_ssl'], {True: 'Enabled', False: 'Disabled'})
        dict_upper(self.storage_account, ['access_key', 'encryption_algorithm'])
        dict_map(self.storage_account, ['access_key', 'encryption_algorithm'], {'none': 'None', 'rsaes_pkcs1_v_1_5': 'RSAES_PKCS1_v_1_5'})

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
                if (not default_compare(self.storage_account, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Storage Account Credential instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_storageaccountcredential()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Storage Account Credential instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_storageaccountcredential()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Storage Account Credential instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_storageaccountcredential(self):
        '''
        Creates or updates Storage Account Credential with the specified configuration.

        :return: deserialized Storage Account Credential instance state dictionary
        '''
        self.log("Creating / Updating the Storage Account Credential instance {0}".format(self.name))

        try:
            response = self.mgmt_client.storage_account_credentials.create_or_update(credential_name=self.credential_name,
                                                                                     storage_account=self.storage_account,
                                                                                     resource_group_name=self.resource_group,
                                                                                     manager_name=self.name)
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
        self.log("Deleting the Storage Account Credential instance {0}".format(self.name))
        try:
            response = self.mgmt_client.storage_account_credentials.delete(credential_name=self.credential_name,
                                                                           resource_group_name=self.resource_group,
                                                                           manager_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Storage Account Credential instance.')
            self.fail("Error deleting the Storage Account Credential instance: {0}".format(str(e)))

        return True

    def get_storageaccountcredential(self):
        '''
        Gets the properties of the specified Storage Account Credential.

        :return: deserialized Storage Account Credential instance state dictionary
        '''
        self.log("Checking if the Storage Account Credential instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.storage_account_credentials.get(credential_name=self.credential_name,
                                                                        resource_group_name=self.resource_group,
                                                                        manager_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Storage Account Credential instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Storage Account Credential instance.')
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
   if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def main():
    """Main execution"""
    AzureRMStorageAccountCredential()


if __name__ == '__main__':
    main()

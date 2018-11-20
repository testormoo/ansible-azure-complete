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
module: azure_rm_storsimplestorageaccountcredential_facts
version_added: "2.8"
short_description: Get Azure Storage Account Credential facts.
description:
    - Get facts of Azure Storage Account Credential.

options:
    credential_name:
        description:
            - The name of storage account credential to be fetched.
    resource_group:
        description:
            - The resource group name
        required: True
    name:
        description:
            - The manager name
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Storage Account Credential
    azure_rm_storsimplestorageaccountcredential_facts:
      credential_name: credential_name
      resource_group: resource_group_name
      name: manager_name

  - name: List instances of Storage Account Credential
    azure_rm_storsimplestorageaccountcredential_facts:
      resource_group: resource_group_name
      name: manager_name
'''

RETURN = '''
storage_account_credentials:
    description: A list of dictionaries containing facts for Storage Account Credential.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The identifier.
            returned: always
            type: str
            sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzur
                    eSDKOperations/storageAccountCredentials/sacforsdktest"
        name:
            description:
                - The name.
            returned: always
            type: str
            sample: sacforsdktest
        login:
            description:
                - The storage account login
            returned: always
            type: str
            sample: sacforsdktest
        location:
            description:
                - "The storage account's geo location"
            returned: always
            type: str
            sample: West US
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMStorageAccountCredentialsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            credential_name=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.credential_name = None
        self.resource_group = None
        self.name = None
        super(AzureRMStorageAccountCredentialsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.credential_name is not None:
            self.results['storage_account_credentials'] = self.get()
        else:
            self.results['storage_account_credentials'] = self.list_by_manager()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.storage_account_credentials.get(credential_name=self.credential_name,
                                                                        resource_group_name=self.resource_group,
                                                                        manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for StorageAccountCredentials.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_manager(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.storage_account_credentials.list_by_manager(resource_group_name=self.resource_group,
                                                                                    manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for StorageAccountCredentials.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'login': d.get('login', None),
            'location': d.get('location', None)
        }
        return d


def main():
    AzureRMStorageAccountCredentialsFacts()


if __name__ == '__main__':
    main()

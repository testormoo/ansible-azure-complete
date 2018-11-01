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
module: azure_rm_sqlmanagedinstanceencryptionprotector_facts
version_added: "2.8"
short_description: Get Azure Managed Instance Encryption Protector facts.
description:
    - Get facts of Azure Managed Instance Encryption Protector.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    managed_instance_name:
        description:
            - The name of the managed instance.
        required: True
    encryption_protector_name:
        description:
            - The name of the encryption protector to be retrieved.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Managed Instance Encryption Protector
    azure_rm_sqlmanagedinstanceencryptionprotector_facts:
      resource_group: resource_group_name
      managed_instance_name: managed_instance_name
      encryption_protector_name: encryption_protector_name

  - name: List instances of Managed Instance Encryption Protector
    azure_rm_sqlmanagedinstanceencryptionprotector_facts:
      resource_group: resource_group_name
      managed_instance_name: managed_instance_name
'''

RETURN = '''
managed_instance_encryption_protectors:
    description: A list of dictionaries containing facts for Managed Instance Encryption Protector.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-7398/providers/Microsoft.Sql/managedInstances/sqlcrudtest
                    -4645/encryptionProtector/current"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: current
        kind:
            description:
                - Kind of encryption protector. This is metadata used for the Azure portal experience.
            returned: always
            type: str
            sample: azurekeyvault
        uri:
            description:
                - The URI of the server key.
            returned: always
            type: str
            sample: "https://someVault.vault.azure.net/keys/someKey/01234567890123456789012345678901"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagedInstanceEncryptionProtectorsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            managed_instance_name=dict(
                type='str',
                required=True
            ),
            encryption_protector_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.managed_instance_name = None
        self.encryption_protector_name = None
        super(AzureRMManagedInstanceEncryptionProtectorsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.encryption_protector_name is not None:
            self.results['managed_instance_encryption_protectors'] = self.get()
        else:
            self.results['managed_instance_encryption_protectors'] = self.list_by_instance()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managed_instance_encryption_protectors.get(resource_group_name=self.resource_group,
                                                                                   managed_instance_name=self.managed_instance_name,
                                                                                   encryption_protector_name=self.encryption_protector_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ManagedInstanceEncryptionProtectors.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_instance(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managed_instance_encryption_protectors.list_by_instance(resource_group_name=self.resource_group,
                                                                                                managed_instance_name=self.managed_instance_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ManagedInstanceEncryptionProtectors.')

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
            'kind': d.get('kind', None),
            'uri': d.get('uri', None)
        }
        return d


def main():
    AzureRMManagedInstanceEncryptionProtectorsFacts()


if __name__ == '__main__':
    main()

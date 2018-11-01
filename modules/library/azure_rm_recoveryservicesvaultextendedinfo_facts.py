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
module: azure_rm_recoveryservicesvaultextendedinfo_facts
version_added: "2.8"
short_description: Get Azure Vault Extended Info facts.
description:
    - Get facts of Azure Vault Extended Info.

options:
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Vault Extended Info
    azure_rm_recoveryservicesvaultextendedinfo_facts:
      resource_group: resource_group_name
      vault_name: vault_name
'''

RETURN = '''
vault_extended_info:
    description: A list of dictionaries containing facts for Vault Extended Info.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id represents the complete path to the resource.
            returned: always
            type: str
            sample: "/subscriptions/77777777-b0c6-47a2-b37c-d8e65a629c18/resourceGroups/Default-RecoveryServices-ResourceGroup/providers/Microsoft.RecoverySe
                    rvices/vaults/swaggerExample/extendedInformation/vaultExtendedInfo"
        name:
            description:
                - Resource name associated with the resource.
            returned: always
            type: str
            sample: vaultExtendedInfo
        algorithm:
            description:
                - Algorithm for Vault ExtendedInfo
            returned: always
            type: str
            sample: None
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.recoveryservices import RecoveryServicesClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVaultExtendedInfoFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            vault_name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.vault_name = None
        super(AzureRMVaultExtendedInfoFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['vault_extended_info'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.vault_extended_info.get(resource_group_name=self.resource_group,
                                                                vault_name=self.vault_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for VaultExtendedInfo.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'algorithm': d.get('algorithm', None)
        }
        return d


def main():
    AzureRMVaultExtendedInfoFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_recoveryservicesvault_facts
version_added: "2.8"
short_description: Get Azure Vault facts.
description:
    - Get facts of Azure Vault.

options:
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
    name:
        description:
            - The name of the recovery services vault.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Vault
    azure_rm_recoveryservicesvault_facts:
      resource_group: resource_group_name
      name: vault_name

  - name: List instances of Vault
    azure_rm_recoveryservicesvault_facts:
      resource_group: resource_group_name

  - name: List instances of Vault
    azure_rm_recoveryservicesvault_facts:
'''

RETURN = '''
vaults:
    description: A list of dictionaries containing facts for Vault.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id represents the complete path to the resource.
            returned: always
            type: str
            sample: "/subscriptions/77777777-b0c6-47a2-b37c-d8e65a629c18/resourceGroups/Default-RecoveryServices-ResourceGroup/providers/Microsoft.RecoverySe
                    rvices/vaults/swaggerExample"
        name:
            description:
                - Resource name associated with the resource.
            returned: always
            type: str
            sample: swaggerExample
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: "{\n  'TestUpdatedKey': 'TestUpdatedValue'\n}"
        properties:
            description:
                -
            returned: always
            type: complex
            sample: properties
            contains:
        sku:
            description:
                -
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The Sku name. Possible values include: 'Standard', 'RS0'"
                    returned: always
                    type: str
                    sample: Standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.recoveryservices import RecoveryServicesClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVaultFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.tags = None
        super(AzureRMVaultFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['vaults'] = self.get()
        elif self.resource_group is not None:
            self.results['vaults'] = self.list_by_resource_group()
        else:
            self.results['vaults'] = self.list_by_subscription_id()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.vaults.get(resource_group_name=self.resource_group,
                                                   vault_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Vault.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.vaults.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Vault.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription_id(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.vaults.list_by_subscription_id()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Vault.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'properties': {
            },
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            }
        }
        return d


def main():
    AzureRMVaultFacts()


if __name__ == '__main__':
    main()

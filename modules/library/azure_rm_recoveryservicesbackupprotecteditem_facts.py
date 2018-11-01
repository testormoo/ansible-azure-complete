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
module: azure_rm_recoveryservicesbackupprotecteditem_facts
version_added: "2.8"
short_description: Get Azure Protected Item facts.
description:
    - Get facts of Azure Protected Item.

options:
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    fabric_name:
        description:
            - Fabric name associated with the backed up item.
        required: True
    container_name:
        description:
            - Container name associated with the backed up item.
        required: True
    protected_item_name:
        description:
            - Backed up item name whose details are to be fetched.
        required: True
    filter:
        description:
            - OData filter options.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Protected Item
    azure_rm_recoveryservicesbackupprotecteditem_facts:
      vault_name: vault_name
      resource_group: resource_group_name
      fabric_name: fabric_name
      container_name: container_name
      protected_item_name: protected_item_name
      filter: filter
'''

RETURN = '''
protected_items:
    description: A list of dictionaries containing facts for Protected Item.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id represents the complete path to the resource.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/PythonSDKBackupTestRg/providers/Microsoft.RecoveryServices/vaults/PyS
                    DKBackupTestRsVault/backupFabrics/Azure/protectionContainers/IaasVMContainer;iaasvmcontainer;iaasvm-rg;iaasvm-1/protectedItems/VM;iaasvm
                    container;iaasvm-rg;iaasvm-1"
        name:
            description:
                - Resource name associated with the resource.
            returned: always
            type: str
            sample: VM;iaasvmcontainer;iaasvm-rg;iaasvm-1
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        properties:
            description:
                - ProtectedItemResource properties
            returned: always
            type: complex
            sample: properties
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProtectedItemsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            vault_name=dict(
                type='str',
                required=True
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            fabric_name=dict(
                type='str',
                required=True
            ),
            container_name=dict(
                type='str',
                required=True
            ),
            protected_item_name=dict(
                type='str',
                required=True
            ),
            filter=dict(
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
        self.vault_name = None
        self.resource_group = None
        self.fabric_name = None
        self.container_name = None
        self.protected_item_name = None
        self.filter = None
        self.tags = None
        super(AzureRMProtectedItemsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['protected_items'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.protected_items.get(vault_name=self.vault_name,
                                                            resource_group_name=self.resource_group,
                                                            fabric_name=self.fabric_name,
                                                            container_name=self.container_name,
                                                            protected_item_name=self.protected_item_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ProtectedItems.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'properties': {
            }
        }
        return d


def main():
    AzureRMProtectedItemsFacts()


if __name__ == '__main__':
    main()

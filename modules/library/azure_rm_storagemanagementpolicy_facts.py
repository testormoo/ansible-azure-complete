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
module: azure_rm_storagemanagementpolicy_facts
version_added: "2.8"
short_description: Get Azure Management Policy facts.
description:
    - Get facts of Azure Management Policy.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    account_name:
        description:
            - "The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and
               use numbers and lower-case letters only."
        required: True
    management_policy_name:
        description:
            - "The name of the Storage Account Management Policy. It should always be 'default'"
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Management Policy
    azure_rm_storagemanagementpolicy_facts:
      resource_group: resource_group_name
      account_name: account_name
      management_policy_name: management_policy_name
'''

RETURN = '''
management_policies:
    description: A list of dictionaries containing facts for Management Policy.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: /subscriptions/{subscription-id}/resourceGroups/res7231/providers/Microsoft.Storage/storageAccounts/sto288/managementPolicies/default
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: DefaultManagementPolicy
        policy:
            description:
                - "The Storage Account ManagementPolicies Rules, in JSON format. See more details in:
                   https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts."
            returned: always
            type: str
            sample: "{\n  'version': '0.5',\n  'rules': [\n    {\n      'name': 'olcmtest',\n      'type': 'Lifecycle',\n      'definition': {\n
                     'filters': {\n          'blobTypes': [\n            'blockBlob'\n          ],\n          'prefixMatch': [\n
                     'olcmtestcontainer'\n          ]\n        },\n        'actions': {\n          'baseBlob': {\n            'tierToCool': {\n
                      'daysAfterModificationGreaterThan': '30'\n            },\n            'tierToArchive': {\n
                     'daysAfterModificationGreaterThan': '90'\n            },\n            'delete': {\n              'daysAfterModificationGreaterThan':
                     '1000'\n            }\n          },\n          'snapshot': {\n            'delete': {\n              'daysAfterCreationGreaterThan':
                     '30'\n            }\n          }\n        }\n      }\n    }\n  ]\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storage import StorageManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagementPoliciesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            management_policy_name=dict(
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
        self.account_name = None
        self.management_policy_name = None
        super(AzureRMManagementPoliciesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorageManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['management_policies'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.management_policies.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                management_policy_name=self.management_policy_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ManagementPolicies.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'policy': d.get('policy', None)
        }
        return d


def main():
    AzureRMManagementPoliciesFacts()


if __name__ == '__main__':
    main()

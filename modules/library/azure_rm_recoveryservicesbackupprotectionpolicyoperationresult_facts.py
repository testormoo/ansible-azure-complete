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
module: azure_rm_recoveryservicesbackupprotectionpolicyoperationresult_facts
version_added: "2.8"
short_description: Get Azure Protection Policy Operation Result facts.
description:
    - Get facts of Azure Protection Policy Operation Result.

options:
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    name:
        description:
            - "Backup policy name whose operation's result needs to be fetched."
        required: True
    operation_id:
        description:
            - Operation ID which represents the operation whose result needs to be fetched.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Protection Policy Operation Result
    azure_rm_recoveryservicesbackupprotectionpolicyoperationresult_facts:
      vault_name: vault_name
      resource_group: resource_group_name
      name: policy_name
      operation_id: operation_id
'''

RETURN = '''
protection_policy_operation_results:
    description: A list of dictionaries containing facts for Protection Policy Operation Result.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id represents the complete path to the resource.
            returned: always
            type: str
            sample: "/Subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/SwaggerTestRg/providers/Microsoft.RecoveryServices/vaults/NetSDKTestR
                    sVault/backupPolicies/testPolicy1"
        name:
            description:
                - Resource name associated with the resource.
            returned: always
            type: str
            sample: testPolicy1
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        properties:
            description:
                - ProtectionPolicyResource properties
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


class AzureRMProtectionPolicyOperationResultFacts(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            operation_id=dict(
                type='str',
                required=True
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
        self.name = None
        self.operation_id = None
        self.tags = None
        super(AzureRMProtectionPolicyOperationResultFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['protection_policy_operation_results'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.protection_policy_operation_results.get(vault_name=self.vault_name,
                                                                                resource_group_name=self.resource_group,
                                                                                policy_name=self.name,
                                                                                operation_id=self.operation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Protection Policy Operation Result.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
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
    AzureRMProtectionPolicyOperationResultFacts()


if __name__ == '__main__':
    main()

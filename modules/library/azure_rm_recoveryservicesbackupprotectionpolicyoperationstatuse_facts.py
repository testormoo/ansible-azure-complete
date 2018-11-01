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
module: azure_rm_recoveryservicesbackupprotectionpolicyoperationstatuse_facts
version_added: "2.8"
short_description: Get Azure Protection Policy Operation Statuse facts.
description:
    - Get facts of Azure Protection Policy Operation Statuse.

options:
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    policy_name:
        description:
            - "Backup policy name whose operation's status needs to be fetched."
        required: True
    operation_id:
        description:
            - Operation ID which represents an operation whose status needs to be fetched.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Protection Policy Operation Statuse
    azure_rm_recoveryservicesbackupprotectionpolicyoperationstatuse_facts:
      vault_name: vault_name
      resource_group: resource_group_name
      policy_name: policy_name
      operation_id: operation_id
'''

RETURN = '''
protection_policy_operation_statuses:
    description: A list of dictionaries containing facts for Protection Policy Operation Statuse.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ID of the operation.
            returned: always
            type: str
            sample: 00000000-0000-0000-0000-000000000000
        name:
            description:
                - Name of the operation.
            returned: always
            type: str
            sample: GetProtectionPolicyOperationStatus
        status:
            description:
                - "Operation status. Possible values include: 'Invalid', 'InProgress', 'Succeeded', 'Failed', 'Canceled'"
            returned: always
            type: str
            sample: Succeeded
        properties:
            description:
                - Additional information associated with this operation.
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


class AzureRMProtectionPolicyOperationStatusesFacts(AzureRMModuleBase):
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
            policy_name=dict(
                type='str',
                required=True
            ),
            operation_id=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.vault_name = None
        self.resource_group = None
        self.policy_name = None
        self.operation_id = None
        super(AzureRMProtectionPolicyOperationStatusesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['protection_policy_operation_statuses'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.protection_policy_operation_statuses.get(vault_name=self.vault_name,
                                                                                 resource_group_name=self.resource_group,
                                                                                 policy_name=self.policy_name,
                                                                                 operation_id=self.operation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ProtectionPolicyOperationStatuses.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'status': d.get('status', None),
            'properties': {
            }
        }
        return d


def main():
    AzureRMProtectionPolicyOperationStatusesFacts()


if __name__ == '__main__':
    main()
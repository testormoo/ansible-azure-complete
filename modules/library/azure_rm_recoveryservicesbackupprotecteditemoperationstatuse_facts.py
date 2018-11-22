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
module: azure_rm_recoveryservicesbackupprotecteditemoperationstatuse_facts
version_added: "2.8"
short_description: Get Azure Protected Item Operation Statuse facts.
description:
    - Get facts of Azure Protected Item Operation Statuse.

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
            - Fabric name associated with the backup item.
        required: True
    container_name:
        description:
            - Container name associated with the backup item.
        required: True
    name:
        description:
            - Backup item name whose details are to be fetched.
        required: True
    operation_id:
        description:
            - OperationID represents the operation whose status needs to be fetched.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Protected Item Operation Statuse
    azure_rm_recoveryservicesbackupprotecteditemoperationstatuse_facts:
      vault_name: vault_name
      resource_group: resource_group_name
      fabric_name: fabric_name
      container_name: container_name
      name: protected_item_name
      operation_id: operation_id
'''

RETURN = '''
protected_item_operation_statuses:
    description: A list of dictionaries containing facts for Protected Item Operation Statuse.
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
            sample: 00000000-0000-0000-0000-000000000000
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


class AzureRMProtectedItemOperationStatuseFacts(AzureRMModuleBase):
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
            name=dict(
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
        self.fabric_name = None
        self.container_name = None
        self.name = None
        self.operation_id = None
        super(AzureRMProtectedItemOperationStatuseFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['protected_item_operation_statuses'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.protected_item_operation_statuses.get(vault_name=self.vault_name,
                                                                              resource_group_name=self.resource_group,
                                                                              fabric_name=self.fabric_name,
                                                                              container_name=self.container_name,
                                                                              protected_item_name=self.name,
                                                                              operation_id=self.operation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Protected Item Operation Statuse.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
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
    AzureRMProtectedItemOperationStatuseFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_recoveryservicesbackupprotectioncontaineroperationresult_facts
version_added: "2.8"
short_description: Get Azure Protection Container Operation Result facts.
description:
    - Get facts of Azure Protection Container Operation Result.

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
            - Fabric name associated with the container.
        required: True
    container_name:
        description:
            - Container name whose information should be fetched.
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
  - name: Get instance of Protection Container Operation Result
    azure_rm_recoveryservicesbackupprotectioncontaineroperationresult_facts:
      vault_name: vault_name
      resource_group: resource_group_name
      fabric_name: fabric_name
      container_name: container_name
      operation_id: operation_id
'''

RETURN = '''
protection_container_operation_results:
    description: A list of dictionaries containing facts for Protection Container Operation Result.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id represents the complete path to the resource.
            returned: always
            type: str
            sample: id
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProtectionContainerOperationResultsFacts(AzureRMModuleBase):
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
        self.fabric_name = None
        self.container_name = None
        self.operation_id = None
        self.tags = None
        super(AzureRMProtectionContainerOperationResultsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['protection_container_operation_results'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.protection_container_operation_results.get(vault_name=self.vault_name,
                                                                                   resource_group_name=self.resource_group,
                                                                                   fabric_name=self.fabric_name,
                                                                                   container_name=self.container_name,
                                                                                   operation_id=self.operation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ProtectionContainerOperationResults.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMProtectionContainerOperationResultsFacts()


if __name__ == '__main__':
    main()

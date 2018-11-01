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
module: azure_rm_recoveryservicesbackupbackupstatu_facts
version_added: "2.8"
short_description: Get Azure Backup Statu facts.
description:
    - Get facts of Azure Backup Statu.

options:
    azure_region:
        description:
            - Azure region to hit Api
        required: True
    parameters:
        description:
            - Container Backup Status Request
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Backup Statu
    azure_rm_recoveryservicesbackupbackupstatu_facts:
      azure_region: azure_region
      parameters: parameters
'''

RETURN = '''
backup_status:
    description: A list of dictionaries containing facts for Backup Statu.
    returned: always
    type: complex
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


class AzureRMBackupStatusFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            azure_region=dict(
                type='str',
                required=True
            ),
            parameters=dict(
                type='dict',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.azure_region = None
        self.parameters = None
        super(AzureRMBackupStatusFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['backup_status'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.backup_status.get(azure_region=self.azure_region,
                                                          parameters=self.parameters)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for BackupStatus.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMBackupStatusFacts()


if __name__ == '__main__':
    main()

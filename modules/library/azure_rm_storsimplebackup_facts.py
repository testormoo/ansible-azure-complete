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
module: azure_rm_storsimplebackup_facts
version_added: "2.8"
short_description: Get Azure Backup facts.
description:
    - Get facts of Azure Backup.

options:
    device_name:
        description:
            - The device name.
    for_failover:
        description:
            - Set to true if you need backups which can be used for failover.
    resource_group:
        description:
            - The resource group name
        required: True
    name:
        description:
            - The manager name
        required: True
    filter:
        description:
            - OData Filter options

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Backup
    azure_rm_storsimplebackup_facts:
      device_name: device_name
      for_failover: for_failover
      resource_group: resource_group_name
      name: manager_name
      filter: filter

  - name: List instances of Backup
    azure_rm_storsimplebackup_facts:
      resource_group: resource_group_name
      name: manager_name
      filter: filter
'''

RETURN = '''
backups:
    description: A list of dictionaries containing facts for Backup.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            device_name=dict(
                type='str'
            ),
            for_failover=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.device_name = None
        self.for_failover = None
        self.resource_group = None
        self.name = None
        self.filter = None
        super(AzureRMBackupFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.device_name is not None:
            self.results['backups'] = self.list_by_device()
        else:
            self.results['backups'] = self.list_by_manager()
        return self.results

    def list_by_device(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.backups.list_by_device(device_name=self.device_name,
                                                               resource_group_name=self.resource_group,
                                                               manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Backup.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_manager(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.backups.list_by_manager(resource_group_name=self.resource_group,
                                                                manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Backup.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMBackupFacts()


if __name__ == '__main__':
    main()

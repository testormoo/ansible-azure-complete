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
module: azure_rm_sqltransparentdataencryptionactivity_facts
version_added: "2.8"
short_description: Get Azure Transparent Data Encryption Activity facts.
description:
    - Get facts of Azure Transparent Data Encryption Activity.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database for which the transparent data encryption applies.
        required: True
    transparent_data_encryption_name:
        description:
            - The name of the transparent data encryption configuration.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Transparent Data Encryption Activity
    azure_rm_sqltransparentdataencryptionactivity_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name
      transparent_data_encryption_name: transparent_data_encryption_name
'''

RETURN = '''
transparent_data_encryption_activities:
    description: A list of dictionaries containing facts for Transparent Data Encryption Activity.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTransparentDataEncryptionActivitiesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            database_name=dict(
                type='str',
                required=True
            ),
            transparent_data_encryption_name=dict(
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
        self.server_name = None
        self.database_name = None
        self.transparent_data_encryption_name = None
        super(AzureRMTransparentDataEncryptionActivitiesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['transparent_data_encryption_activities'] = self.list_by_configuration()
        return self.results

    def list_by_configuration(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.transparent_data_encryption_activities.list_by_configuration(resource_group_name=self.resource_group,
                                                                                                     server_name=self.server_name,
                                                                                                     database_name=self.database_name,
                                                                                                     transparent_data_encryption_name=self.transparent_data_encryption_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for TransparentDataEncryptionActivities.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMTransparentDataEncryptionActivitiesFacts()


if __name__ == '__main__':
    main()

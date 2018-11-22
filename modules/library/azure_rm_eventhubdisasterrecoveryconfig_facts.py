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
module: azure_rm_eventhubdisasterrecoveryconfig_facts
version_added: "2.8"
short_description: Get Azure Disaster Recovery Config facts.
description:
    - Get facts of Azure Disaster Recovery Config.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    name:
        description:
            - The Namespace name
        required: True
    alias:
        description:
            - The Disaster Recovery configuration name
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Disaster Recovery Config
    azure_rm_eventhubdisasterrecoveryconfig_facts:
      resource_group: resource_group_name
      name: namespace_name
      alias: alias
'''

RETURN = '''
disaster_recovery_configs:
    description: A list of dictionaries containing facts for Disaster Recovery Config.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: "/subscriptions/exampleSubscriptionId/resourceGroups/exampleResourceGroup/providers/Microsoft.EventHub/namespaces/sdk-Namespace-37/disast
                    erRecoveryConfig/sdk-DisasterRecovery-3814"
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: sdk-DisasterRecovery-3814
        role:
            description:
                - "role of namespace in GEO DR - possible values 'Primary' or 'PrimaryNotReplicating' or 'Secondary'. Possible values include: 'Primary',
                   'PrimaryNotReplicating', 'Secondary'"
            returned: always
            type: str
            sample: Secondary
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventhub import EventHubManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDisasterRecoveryConfigFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            alias=dict(
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
        self.name = None
        self.alias = None
        super(AzureRMDisasterRecoveryConfigFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['disaster_recovery_configs'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.disaster_recovery_configs.get(resource_group_name=self.resource_group,
                                                                      namespace_name=self.name,
                                                                      alias=self.alias)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Disaster Recovery Config.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'role': d.get('role', None)
        }
        return d


def main():
    AzureRMDisasterRecoveryConfigFacts()


if __name__ == '__main__':
    main()

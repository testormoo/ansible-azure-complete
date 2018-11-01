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
module: azure_rm_mariadbvirtualnetworkrule_facts
version_added: "2.8"
short_description: Get Azure Virtual Network Rule facts.
description:
    - Get facts of Azure Virtual Network Rule.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    virtual_network_rule_name:
        description:
            - The name of the virtual network rule.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Virtual Network Rule
    azure_rm_mariadbvirtualnetworkrule_facts:
      resource_group: resource_group_name
      server_name: server_name
      virtual_network_rule_name: virtual_network_rule_name

  - name: List instances of Virtual Network Rule
    azure_rm_mariadbvirtualnetworkrule_facts:
      resource_group: resource_group_name
      server_name: server_name
'''

RETURN = '''
virtual_network_rules:
    description: A list of dictionaries containing facts for Virtual Network Rule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID
            returned: always
            type: str
            sample: "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/TestGroup/providers/Microsoft.DBforMariaDB/servers/vnet-test-svr/virt
                    ualNetworkRules/vnet-firewall-rule"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: vnet-firewall-rule
        state:
            description:
                - "Virtual Network Rule State. Possible values include: 'Initializing', 'InProgress', 'Ready', 'Deleting', 'Unknown'"
            returned: always
            type: str
            sample: Ready
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.mariadb import MariaDBManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVirtualNetworkRulesFacts(AzureRMModuleBase):
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
            virtual_network_rule_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.server_name = None
        self.virtual_network_rule_name = None
        super(AzureRMVirtualNetworkRulesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MariaDBManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.virtual_network_rule_name is not None:
            self.results['virtual_network_rules'] = self.get()
        else:
            self.results['virtual_network_rules'] = self.list_by_server()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.virtual_network_rules.get(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  virtual_network_rule_name=self.virtual_network_rule_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for VirtualNetworkRules.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.virtual_network_rules.list_by_server(resource_group_name=self.resource_group,
                                                                             server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for VirtualNetworkRules.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'state': d.get('state', None)
        }
        return d


def main():
    AzureRMVirtualNetworkRulesFacts()


if __name__ == '__main__':
    main()
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
module: azure_rm_securityrule_facts
version_added: "2.8"
short_description: Get Azure Security Rule facts.
description:
    - Get facts of Azure Security Rule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    network_security_group_name:
        description:
            - The name of the network security group.
        required: True
    name:
        description:
            - The name of the security rule.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Security Rule
    azure_rm_securityrule_facts:
      resource_group: resource_group_name
      network_security_group_name: network_security_group_name
      name: security_rule_name
'''

RETURN = '''
security_rules:
    description: A list of dictionaries containing facts for Security Rule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/networkSecurityGroups/testnsg/securityRules/rule1
        protocol:
            description:
                - "Network protocol this rule applies to. Possible values are 'Tcp', 'Udp', and '*'. Possible values include: 'Tcp', 'Udp', '*'"
            returned: always
            type: str
            sample: *
        access:
            description:
                - "The network traffic is allowed or denied. Possible values are: 'Allow' and 'Deny'. Possible values include: 'Allow', 'Deny'"
            returned: always
            type: str
            sample: Allow
        priority:
            description:
                - "The priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The
                   lower the priority number, the higher the priority of the rule."
            returned: always
            type: int
            sample: 130
        direction:
            description:
                - "The direction of the rule. The direction specifies if rule will be evaluated on incoming or outcoming traffic. Possible values are:
                   'Inbound' and 'Outbound'. Possible values include: 'Inbound', 'Outbound'"
            returned: always
            type: str
            sample: Inbound
        name:
            description:
                - The name of the resource that is unique within a resource group. This name can be used to access the resource.
            returned: always
            type: str
            sample: rule1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSecurityRuleFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            network_security_group_name=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.network_security_group_name = None
        self.name = None
        super(AzureRMSecurityRuleFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['security_rules'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.security_rules.get(resource_group_name=self.resource_group,
                                                           network_security_group_name=self.network_security_group_name,
                                                           security_rule_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Security Rule.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'protocol': d.get('protocol', None),
            'access': d.get('access', None),
            'priority': d.get('priority', None),
            'direction': d.get('direction', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMSecurityRuleFacts()


if __name__ == '__main__':
    main()

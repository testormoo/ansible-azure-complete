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
module: azure_rm_monitoralertrule_facts
version_added: "2.8"
short_description: Get Azure Alert Rule facts.
description:
    - Get facts of Azure Alert Rule.

options:
    resource_group:
        description:
            - The name of the resource group.
    rule_name:
        description:
            - The name of the rule.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Alert Rule
    azure_rm_monitoralertrule_facts:
      resource_group: resource_group_name
      rule_name: rule_name

  - name: List instances of Alert Rule
    azure_rm_monitoralertrule_facts:
      resource_group: resource_group_name

  - name: List instances of Alert Rule
    azure_rm_monitoralertrule_facts:
'''

RETURN = '''
alert_rules:
    description: A list of dictionaries containing facts for Alert Rule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Azure resource Id
            returned: always
            type: str
            sample: /subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/Rac46PostSwapRG/providers/microsoft.insights/alertrules/chiricutin
        name:
            description:
                - Azure resource name
            returned: always
            type: str
            sample: chiricutin
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  '$type': 'Microsoft.WindowsAzure.Management.Common.Storage.CasePreservedDictionary,
                     Microsoft.WindowsAzure.Management.Common.Storage',\n
                     'hidden-link:/subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/Rac46PostSwapRG/providers/Microsoft.Web/sites/leoalertt
                    est': 'Resource'\n}"
        description:
            description:
                - the description of the alert rule that will be included in the alert email.
            returned: always
            type: str
            sample: Pura Vida
        condition:
            description:
                - the condition that results in the alert rule being activated.
            returned: always
            type: complex
            sample: condition
            contains:
        actions:
            description:
                - the array of actions that are performed when the alert rule becomes active, and when an alert condition is resolved.
            returned: always
            type: complex
            sample: actions
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAlertRulesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            rule_name=dict(
                type='str'
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
        self.resource_group = None
        self.rule_name = None
        self.tags = None
        super(AzureRMAlertRulesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.rule_name is not None):
            self.results['alert_rules'] = self.get()
        elif self.resource_group is not None:
            self.results['alert_rules'] = self.list_by_resource_group()
        else:
            self.results['alert_rules'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.alert_rules.get(resource_group_name=self.resource_group,
                                                        rule_name=self.rule_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AlertRules.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.alert_rules.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AlertRules.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.alert_rules.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AlertRules.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'description': d.get('description', None),
            'condition': {
            },
            'actions': {
            }
        }
        return d


def main():
    AzureRMAlertRulesFacts()


if __name__ == '__main__':
    main()

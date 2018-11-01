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
module: azure_rm_monitormetricalert_facts
version_added: "2.8"
short_description: Get Azure Metric Alert facts.
description:
    - Get facts of Azure Metric Alert.

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
  - name: Get instance of Metric Alert
    azure_rm_monitormetricalert_facts:
      resource_group: resource_group_name
      rule_name: rule_name

  - name: List instances of Metric Alert
    azure_rm_monitormetricalert_facts:
      resource_group: resource_group_name

  - name: List instances of Metric Alert
    azure_rm_monitormetricalert_facts:
'''

RETURN = '''
metric_alerts:
    description: A list of dictionaries containing facts for Metric Alert.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Azure resource Id
            returned: always
            type: str
            sample: /subscriptions/14ddf0c5-77c5-4b53-84f6-e1fa43ad68f7/resourceGroups/gigtest/providers/providers/microsoft.insights/metricalerts/chiricutin
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: global
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n
                     'hidden-link:/subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/Rac46PostSwapRG/providers/Microsoft.Web/sites/leoalertt
                    est': 'Resource'\n}"
        description:
            description:
                - the description of the metric alert that will be included in the alert email.
            returned: always
            type: str
            sample: This is the description of the rule1
        severity:
            description:
                - Alert severity {0, 1, 2, 3, 4}
            returned: always
            type: int
            sample: 3
        enabled:
            description:
                - the flag that indicates whether the metric alert is enabled.
            returned: always
            type: str
            sample: True
        scopes:
            description:
                - "the list of resource id's that this metric alert is scoped to."
            returned: always
            type: str
            sample: "[\n
                     '/subscriptions/14ddf0c5-77c5-4b53-84f6-e1fa43ad68f7/resourceGroups/gigtest/providers/Microsoft.Compute/virtualMachines/gigwadme'\n]"
        criteria:
            description:
                - defines the specific alert criteria information.
            returned: always
            type: complex
            sample: criteria
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


class AzureRMMetricAlertsFacts(AzureRMModuleBase):
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
        super(AzureRMMetricAlertsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.rule_name is not None):
            self.results['metric_alerts'] = self.get()
        elif self.resource_group is not None:
            self.results['metric_alerts'] = self.list_by_resource_group()
        else:
            self.results['metric_alerts'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.metric_alerts.get(resource_group_name=self.resource_group,
                                                          rule_name=self.rule_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for MetricAlerts.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.metric_alerts.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for MetricAlerts.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.metric_alerts.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for MetricAlerts.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'description': d.get('description', None),
            'severity': d.get('severity', None),
            'enabled': d.get('enabled', None),
            'scopes': d.get('scopes', None),
            'criteria': {
            },
            'actions': {
            }
        }
        return d


def main():
    AzureRMMetricAlertsFacts()


if __name__ == '__main__':
    main()

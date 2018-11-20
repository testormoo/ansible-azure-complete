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
module: azure_rm_monitormetricalertsstatus_facts
version_added: "2.8"
short_description: Get Azure Metric Alerts Status facts.
description:
    - Get facts of Azure Metric Alerts Status.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    rule_name:
        description:
            - The name of the rule.
        required: True
    name:
        description:
            - The name of the status.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Metric Alerts Status
    azure_rm_monitormetricalertsstatus_facts:
      resource_group: resource_group_name
      rule_name: rule_name
      name: status_name
'''

RETURN = '''
metric_alerts_status:
    description: A list of dictionaries containing facts for Metric Alerts Status.
    returned: always
    type: complex
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


class AzureRMMetricAlertsStatusFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            rule_name=dict(
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
        self.rule_name = None
        self.name = None
        super(AzureRMMetricAlertsStatusFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['metric_alerts_status'] = self.list_by_name()
        return self.results

    def list_by_name(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.metric_alerts_status.list_by_name(resource_group_name=self.resource_group,
                                                                          rule_name=self.rule_name,
                                                                          status_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for MetricAlertsStatus.')

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
    AzureRMMetricAlertsStatusFacts()


if __name__ == '__main__':
    main()

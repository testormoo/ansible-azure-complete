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
module: azure_rm_monitoralertruleincident_facts
version_added: "2.8"
short_description: Get Azure Alert Rule Incident facts.
description:
    - Get facts of Azure Alert Rule Incident.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    rule_name:
        description:
            - The name of the rule.
        required: True
    incident_name:
        description:
            - The name of the incident to retrieve.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Alert Rule Incident
    azure_rm_monitoralertruleincident_facts:
      resource_group: resource_group_name
      rule_name: rule_name
      incident_name: incident_name

  - name: List instances of Alert Rule Incident
    azure_rm_monitoralertruleincident_facts:
      resource_group: resource_group_name
      rule_name: rule_name
'''

RETURN = '''
alert_rule_incidents:
    description: A list of dictionaries containing facts for Alert Rule Incident.
    returned: always
    type: complex
    contains:
        name:
            description:
                - Incident name.
            returned: always
            type: str
            sample: Website_started
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAlertRuleIncidentsFacts(AzureRMModuleBase):
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
            incident_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.rule_name = None
        self.incident_name = None
        super(AzureRMAlertRuleIncidentsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.incident_name is not None:
            self.results['alert_rule_incidents'] = self.get()
        else:
            self.results['alert_rule_incidents'] = self.list_by_alert_rule()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.alert_rule_incidents.get(resource_group_name=self.resource_group,
                                                                 rule_name=self.rule_name,
                                                                 incident_name=self.incident_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AlertRuleIncidents.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_alert_rule(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.alert_rule_incidents.list_by_alert_rule(resource_group_name=self.resource_group,
                                                                                rule_name=self.rule_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AlertRuleIncidents.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMAlertRuleIncidentsFacts()


if __name__ == '__main__':
    main()

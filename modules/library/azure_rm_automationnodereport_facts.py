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
module: azure_rm_automationnodereport_facts
version_added: "2.8"
short_description: Get Azure Node Report facts.
description:
    - Get facts of Azure Node Report.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    name:
        description:
            - The name of the automation account.
        required: True
    node_id:
        description:
            - The parameters supplied to the list operation.
        required: True
    filter:
        description:
            - The filter to apply on the operation.
    report_id:
        description:
            - The report id.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Node Report
    azure_rm_automationnodereport_facts:
      resource_group: resource_group_name
      name: automation_account_name
      node_id: node_id
      filter: filter

  - name: Get instance of Node Report
    azure_rm_automationnodereport_facts:
      resource_group: resource_group_name
      name: automation_account_name
      node_id: node_id
      report_id: report_id
'''

RETURN = '''
node_reports:
    description: A list of dictionaries containing facts for Node Report.
    returned: always
    type: complex
    contains:
        status:
            description:
                - Gets or sets the status of the node report.
            returned: always
            type: str
            sample: Compliant
        id:
            description:
                - Gets or sets the id.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/nodes/nodeId/reports/903a
                    5ead-140c-11e7-a943-000d3a6140c9"
        errors:
            description:
                - Gets or sets the errors for the node report.
            returned: always
            type: complex
            sample: errors
            contains:
        resources:
            description:
                - Gets or sets the resource for the node report.
            returned: always
            type: complex
            sample: resources
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNodeReportsFacts(AzureRMModuleBase):
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
            node_id=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str'
            ),
            report_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.node_id = None
        self.filter = None
        self.report_id = None
        super(AzureRMNodeReportsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['node_reports'] = self.list_by_node()
        elif self.report_id is not None:
            self.results['node_reports'] = self.get()
        return self.results

    def list_by_node(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.node_reports.list_by_node(resource_group_name=self.resource_group,
                                                                  automation_account_name=self.name,
                                                                  node_id=self.node_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for NodeReports.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.node_reports.get(resource_group_name=self.resource_group,
                                                         automation_account_name=self.name,
                                                         node_id=self.node_id,
                                                         report_id=self.report_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for NodeReports.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'status': d.get('status', None),
            'id': d.get('id', None),
            'errors': {
            },
            'resources': {
            }
        }
        return d


def main():
    AzureRMNodeReportsFacts()


if __name__ == '__main__':
    main()

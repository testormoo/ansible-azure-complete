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
module: azure_rm_costmanagementreportconfig_facts
version_added: "2.8"
short_description: Get Azure Report Config facts.
description:
    - Get facts of Azure Report Config.

options:
    resource_group:
        description:
            - Azure Resource Group Name.
    name:
        description:
            - Report Config Name.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Report Config
    azure_rm_costmanagementreportconfig_facts:
      resource_group: resource_group_name

  - name: Get instance of Report Config
    azure_rm_costmanagementreportconfig_facts:
      name: report_config_name
'''

RETURN = '''
report_config:
    description: A list of dictionaries containing facts for Report Config.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id.
            returned: always
            type: str
            sample: subscriptions/{subscription-id}/providers/Microsoft.Consumption/reportconfigs/TestReportConfig
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: TestReportConfig
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        format:
            description:
                - "The format of the report being delivered. Possible values include: 'Csv'"
            returned: always
            type: str
            sample: Csv
        definition:
            description:
                - Has definition for the report config.
            returned: always
            type: complex
            sample: definition
            contains:
                type:
                    description:
                        - The type of the report.
                    returned: always
                    type: str
                    sample: Usage
                timeframe:
                    description:
                        - "The time frame for pulling data for the report. If custom, then a specific time period must be provided. Possible values include:
                           'WeekToDate', 'MonthToDate', 'YearToDate', 'Custom'"
                    returned: always
                    type: str
                    sample: Custom
                dataset:
                    description:
                        - Has definition for data in this report config.
                    returned: always
                    type: complex
                    sample: dataset
                    contains:
                        granularity:
                            description:
                                - "The granularity of rows in the report. Possible values include: 'Daily'"
                            returned: always
                            type: str
                            sample: Daily
                        configuration:
                            description:
                                - "Has configuration information for the data in the report. The configuration will be ignored if aggregation and grouping
                                   are provided."
                            returned: always
                            type: complex
                            sample: configuration
                            contains:
                                columns:
                                    description:
                                        - "Array of column names to be included in the report. Any valid report column name is allowed. If not provided,
                                           then report includes all columns."
                                    returned: always
                                    type: str
                                    sample: "[\n  'UsageDate',\n  'MeterId',\n  'InstanceId',\n  'ResourceLocation',\n  'UsageQuantity'\n]"
                        aggregation:
                            description:
                                - "Dictionary of aggregation expression to use in the report. The key of each item in the dictionary is the alias for the
                                   aggregated column. Report can have upto 2 aggregation clauses."
                            returned: always
                            type: complex
                            sample: "{\n  'usageSum': {\n    'name': 'UsageQuantity',\n    'function': 'Sum'\n  }\n}"
                        grouping:
                            description:
                                - Array of group by expression to use in the report. Report can have upto 2 group by clauses.
                            returned: always
                            type: complex
                            sample: grouping
                            contains:
                        filter:
                            description:
                                - Has filter expression to use in the report.
                            returned: always
                            type: complex
                            sample: filter
                            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.costmanagement import CostManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMReportConfigFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
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
        self.name = None
        self.tags = None
        super(AzureRMReportConfigFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(CostManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None:
            self.results['report_config'] = self.list_by_resource_group_name()
        elif self.name is not None:
            self.results['report_config'] = self.get()
        return self.results

    def list_by_resource_group_name(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.report_config.list_by_resource_group_name(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report Config.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.report_config.get(report_config_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Report Config.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'format': d.get('format', None),
            'definition': {
                'type': d.get('definition', {}).get('type', None),
                'timeframe': d.get('definition', {}).get('timeframe', None),
                'dataset': {
                    'granularity': d.get('definition', {}).get('dataset', {}).get('granularity', None),
                    'configuration': {
                        'columns': d.get('definition', {}).get('dataset', {}).get('configuration', {}).get('columns', None)
                    },
                    'aggregation': d.get('definition', {}).get('dataset', {}).get('aggregation', None),
                    'grouping': {
                    },
                    'filter': {
                    }
                }
            }
        }
        return d


def main():
    AzureRMReportConfigFacts()


if __name__ == '__main__':
    main()

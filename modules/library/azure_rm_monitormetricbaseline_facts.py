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
module: azure_rm_monitormetricbaseline_facts
version_added: "2.8"
short_description: Get Azure Metric Baseline facts.
description:
    - Get facts of Azure Metric Baseline.

options:
    resource_uri:
        description:
            - "The identifier of the resource. It has the following structure:
               subscriptions/{subscriptionName}/resourceGroups/{resourceGroupName}/providers/{providerName}/{resourceName}. For example:
               subscriptions/b368ca2f-e298-46b7-b0ab-012281956afa/resourceGroups/vms/providers/Microsoft.Compute/virtualMachines/vm1"
        required: True
    name:
        description:
            - The name of the metric to retrieve the baseline for.
        required: True
    timespan:
        description:
            - "The timespan of the query. It is a string with the following format 'startDateTime_ISO/endDateTime_ISO'."
    interval:
        description:
            - The interval (i.e. timegrain) of the query.
    aggregation:
        description:
            - The aggregation type of the metric to retrieve the baseline for.
    sensitivities:
        description:
            - The list of sensitivities (comma separated) to retrieve.
    result_type:
        description:
            - Allows retrieving only metadata of the baseline. On data request all information is retrieved.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Metric Baseline
    azure_rm_monitormetricbaseline_facts:
      resource_uri: resource_uri
      name: metric_name
      timespan: timespan
      interval: interval
      aggregation: aggregation
      sensitivities: sensitivities
      result_type: result_type
'''

RETURN = '''
metric_baseline:
    description: A list of dictionaries containing facts for Metric Baseline.
    returned: always
    type: complex
    contains:
        id:
            description:
                - the metric baseline Id.
            returned: always
            type: str
            sample: "/subscriptions/b368ca2f-e298-46b7-b0ab-012281956afa/resourceGroups/vms/providers/Microsoft.Compute/virtualMachines/vm1/providers/Microso
                    ft.Insights/baseline/PercentageCpu"
        name:
            description:
                - the name and the display name of the metric, i.e. it is localizable string.
            returned: always
            type: complex
            sample: name
            contains:
                value:
                    description:
                        - the invariant value.
                    returned: always
                    type: str
                    sample: PercentageCpu
        timespan:
            description:
                - "The timespan for which the data was retrieved. Its value consists of two datatimes concatenated, separated by '/'.  This may be adjusted
                   in the future and returned back from what was originally requested."
            returned: always
            type: str
            sample: "2017-04-14T02:20:00Z/2017-04-14T04:20:00Z"
        interval:
            description:
                - "The interval (window size) for which the metric data was returned in.  This may be adjusted in the future and returned back from what was
                   originally requested.  This is not present if a metadata request was made."
            returned: always
            type: str
            sample: PT1H
        aggregation:
            description:
                - The aggregation type of the metric.
            returned: always
            type: str
            sample: Average
        timestamps:
            description:
                - the array of timestamps of the baselines.
            returned: always
            type: datetime
            sample: "[\n  '2017-04-14T02:20:00Z',\n  '2017-04-14T03:20:00Z'\n]"
        baseline:
            description:
                - the baseline values for each sensitivity.
            returned: always
            type: complex
            sample: baseline
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


class AzureRMMetricBaselineFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_uri=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            timespan=dict(
                type='str'
            ),
            interval=dict(
                type='str'
            ),
            aggregation=dict(
                type='str'
            ),
            sensitivities=dict(
                type='str'
            ),
            result_type=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_uri = None
        self.name = None
        self.timespan = None
        self.interval = None
        self.aggregation = None
        self.sensitivities = None
        self.result_type = None
        super(AzureRMMetricBaselineFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['metric_baseline'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.metric_baseline.get(resource_uri=self.resource_uri,
                                                            metric_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Metric Baseline.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': {
                'value': d.get('name', {}).get('value', None)
            },
            'timespan': d.get('timespan', None),
            'interval': d.get('interval', None),
            'aggregation': d.get('aggregation', None),
            'timestamps': d.get('timestamps', None),
            'baseline': {
            }
        }
        return d


def main():
    AzureRMMetricBaselineFacts()


if __name__ == '__main__':
    main()

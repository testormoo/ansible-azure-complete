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
module: azure_rm_workloadmonitormonitor_facts
version_added: "2.8"
short_description: Get Azure Monitor facts.
description:
    - Get facts of Azure Monitor.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    resource_namespace:
        description:
            - The Namespace of the resource.
        required: True
    resource_type:
        description:
            - The type of the resource.
        required: True
    name:
        description:
            - Name of the resource.
        required: True
    filter:
        description:
            - Filter to be applied on the operation.
    skiptoken:
        description:
            - The page-continuation token to use with a paged version of this API.
    monitor_id:
        description:
            - Monitor Id.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Monitor
    azure_rm_workloadmonitormonitor_facts:
      resource_group: resource_group_name
      resource_namespace: resource_namespace
      resource_type: resource_type
      name: resource_name
      filter: filter
      skiptoken: skiptoken

  - name: Get instance of Monitor
    azure_rm_workloadmonitormonitor_facts:
      resource_group: resource_group_name
      resource_namespace: resource_namespace
      resource_type: resource_type
      name: resource_name
      monitor_id: monitor_id
'''

RETURN = '''
monitors:
    description: A list of dictionaries containing facts for Monitor.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/a7f23fdb-e626-4f95-89aa-3a360a90861e/resourcegroups/viv_rg/providers/Microsoft.WorkloadMonitor/workloadInsights/Canary-WL
                    I-2/monitors/ComponentTypeId='75582e9b-cae6-397b-6764-f7cf6cc620b0',MonitorId='1bbf53b8-2557-a521-f7c1-1023de57367a'"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: "ComponentTypeId='75582e9b-cae6-397b-6764-f7cf6cc620b0',MonitorId='1bbf53b8-2557-a521-f7c1-1023de57367a'"
        etag:
            description:
                - For optimistic concurrency control.
            returned: always
            type: str
            sample: etag
        description:
            description:
                - Description of the monitor
            returned: always
            type: str
            sample: Monitor the number of free MBytes remaining on a logical disk.
        criteria:
            description:
                - "Collection of MonitorCriteria. For PATCH calls, instead of partial list, complete list of expected criteria should be passed for proper
                   updation."
            returned: always
            type: complex
            sample: criteria
            contains:
        frequency:
            description:
                - Frequency at which monitor condition is evaluated
            returned: always
            type: int
            sample: 15
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.workloadmonitor import WorkloadMonitorAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMonitorFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_namespace=dict(
                type='str',
                required=True
            ),
            resource_type=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str'
            ),
            skiptoken=dict(
                type='str'
            ),
            monitor_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.resource_namespace = None
        self.resource_type = None
        self.name = None
        self.filter = None
        self.skiptoken = None
        self.monitor_id = None
        super(AzureRMMonitorFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(WorkloadMonitorAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.monitor_id is not None:
            self.results['monitors'] = self.get()
        else:
            self.results['monitors'] = self.list_by_resource()
        return self.results

    def list_by_resource(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.monitors.list_by_resource(resource_group_name=self.resource_group,
                                                                  resource_namespace=self.resource_namespace,
                                                                  resource_type=self.resource_type,
                                                                  resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Monitor.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.monitors.get(resource_group_name=self.resource_group,
                                                     resource_namespace=self.resource_namespace,
                                                     resource_type=self.resource_type,
                                                     resource_name=self.name,
                                                     monitor_id=self.monitor_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Monitor.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None),
            'description': d.get('description', None),
            'criteria': {
            },
            'frequency': d.get('frequency', None)
        }
        return d


def main():
    AzureRMMonitorFacts()


if __name__ == '__main__':
    main()

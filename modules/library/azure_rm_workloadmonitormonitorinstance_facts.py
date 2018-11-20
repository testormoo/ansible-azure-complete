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
module: azure_rm_workloadmonitormonitorinstance_facts
version_added: "2.8"
short_description: Get Azure Monitor Instance facts.
description:
    - Get facts of Azure Monitor Instance.

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
    select:
        description:
            - Properties to be returned in the response.
    filter:
        description:
            - Filter to be applied on the operation.
    apply:
        description:
            - Apply aggregation.
    orderby:
        description:
            - Sort the result on one or more properties.
    expand:
        description:
            - Include properties inline in the response.
    top:
        description:
            - Limit the result to the specified number of rows.
    skiptoken:
        description:
            - The page-continuation token to use with a paged version of this API.
    monitor_instance_id:
        description:
            - MonitorInstance Id.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Monitor Instance
    azure_rm_workloadmonitormonitorinstance_facts:
      resource_group: resource_group_name
      resource_namespace: resource_namespace
      resource_type: resource_type
      name: resource_name
      select: select
      filter: filter
      apply: apply
      orderby: orderby
      expand: expand
      top: top
      skiptoken: skiptoken

  - name: Get instance of Monitor Instance
    azure_rm_workloadmonitormonitorinstance_facts:
      resource_group: resource_group_name
      resource_namespace: resource_namespace
      resource_type: resource_type
      name: resource_name
      monitor_instance_id: monitor_instance_id
      select: select
      expand: expand
'''

RETURN = '''
monitor_instances:
    description: A list of dictionaries containing facts for Monitor Instance.
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
                    I-2/healthInstances/ComponentId='d91ce384-b682-883a-d02b-129bf37f218b',MonitorId=052f9b7d-7bf0-7f61-966b-f372e207ef4e'"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: "ComponentId='d91ce384-b682-883a-d02b-129bf37f218b',MonitorId=052f9b7d-7bf0-7f61-966b-f372e207ef4e'"
        etag:
            description:
                - For optimistic concurrency control.
            returned: always
            type: str
            sample: etag
        children:
            description:
                - Health instance children.
            returned: always
            type: complex
            sample: children
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.workloadmonitor import WorkloadMonitorAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMonitorInstancesFacts(AzureRMModuleBase):
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
            select=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
            apply=dict(
                type='str'
            ),
            orderby=dict(
                type='str'
            ),
            expand=dict(
                type='str'
            ),
            top=dict(
                type='str'
            ),
            skiptoken=dict(
                type='str'
            ),
            monitor_instance_id=dict(
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
        self.select = None
        self.filter = None
        self.apply = None
        self.orderby = None
        self.expand = None
        self.top = None
        self.skiptoken = None
        self.monitor_instance_id = None
        super(AzureRMMonitorInstancesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(WorkloadMonitorAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['monitor_instances'] = self.list_by_resource()
        elif self.monitor_instance_id is not None:
            self.results['monitor_instances'] = self.get()
        return self.results

    def list_by_resource(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.monitor_instances.list_by_resource(resource_group_name=self.resource_group,
                                                                           resource_namespace=self.resource_namespace,
                                                                           resource_type=self.resource_type,
                                                                           resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for MonitorInstances.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.monitor_instances.get(resource_group_name=self.resource_group,
                                                              resource_namespace=self.resource_namespace,
                                                              resource_type=self.resource_type,
                                                              resource_name=self.name,
                                                              monitor_instance_id=self.monitor_instance_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for MonitorInstances.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None),
            'children': {
            }
        }
        return d


def main():
    AzureRMMonitorInstancesFacts()


if __name__ == '__main__':
    main()

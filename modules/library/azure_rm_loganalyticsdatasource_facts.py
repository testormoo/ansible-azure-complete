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
module: azure_rm_loganalyticsdatasource_facts
version_added: "2.8"
short_description: Get Azure Data Source facts.
description:
    - Get facts of Azure Data Source.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
        required: True
    workspace_name:
        description:
            - The workspace that contains the data sources.
        required: True
    filter:
        description:
            - The filter to apply on the operation.
    skiptoken:
        description:
            - Starting point of the collection of data source instances.
    data_source_name:
        description:
            - Name of the datasource
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Data Source
    azure_rm_loganalyticsdatasource_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      filter: filter
      skiptoken: skiptoken

  - name: Get instance of Data Source
    azure_rm_loganalyticsdatasource_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      data_source_name: data_source_name
'''

RETURN = '''
data_sources:
    description: A list of dictionaries containing facts for Data Source.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000005/resourceGroups/OIAutoRest5123/providers/Microsoft.OperationalInsights/workspaces/AzT
                    est9724/datasources/AzTestDS774"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: AzTestDS774
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: tags
        properties:
            description:
                - "The data source properties in raw json format, each kind of data source have it's own schema."
            returned: always
            type: str
            sample: "{\n  'linkedResourceId': '/subscriptions/00000000-0000-0000-0000-00000000000/providers/microsoft.insights/eventtypes/management'\n}"
        kind:
            description:
                - "Possible values include: 'AzureActivityLog', 'ChangeTrackingPath', 'ChangeTrackingDefaultPath', 'ChangeTrackingDefaultRegistry',
                   'ChangeTrackingCustomRegistry', 'CustomLog', 'CustomLogCollection', 'GenericDataSource', 'IISLogs', 'LinuxPerformanceObject',
                   'LinuxPerformanceCollection', 'LinuxSyslog', 'LinuxSyslogCollection', 'WindowsEvent', 'WindowsPerformanceCounter'"
            returned: always
            type: str
            sample: AzureActivityLog
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.loganalytics import OperationalInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDataSourcesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workspace_name=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str'
            ),
            skiptoken=dict(
                type='str'
            ),
            data_source_name=dict(
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
        self.workspace_name = None
        self.filter = None
        self.skiptoken = None
        self.data_source_name = None
        self.tags = None
        super(AzureRMDataSourcesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(OperationalInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.filter is not None:
            self.results['data_sources'] = self.list_by_workspace()
        elif self.data_source_name is not None:
            self.results['data_sources'] = self.get()
        return self.results

    def list_by_workspace(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.data_sources.list_by_workspace(resource_group_name=self.resource_group,
                                                                       workspace_name=self.workspace_name,
                                                                       filter=self.filter)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DataSources.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.data_sources.get(resource_group_name=self.resource_group,
                                                         workspace_name=self.workspace_name,
                                                         data_source_name=self.data_source_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DataSources.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'properties': d.get('properties', None),
            'kind': d.get('kind', None)
        }
        return d


def main():
    AzureRMDataSourcesFacts()


if __name__ == '__main__':
    main()

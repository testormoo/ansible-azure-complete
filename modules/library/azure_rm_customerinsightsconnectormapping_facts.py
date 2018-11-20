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
module: azure_rm_customerinsightsconnectormapping_facts
version_added: "2.8"
short_description: Get Azure Connector Mapping facts.
description:
    - Get facts of Azure Connector Mapping.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    connector_name:
        description:
            - The name of the connector.
        required: True
    name:
        description:
            - The name of the connector mapping.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Connector Mapping
    azure_rm_customerinsightsconnectormapping_facts:
      resource_group: resource_group_name
      hub_name: hub_name
      connector_name: connector_name
      name: mapping_name

  - name: List instances of Connector Mapping
    azure_rm_customerinsightsconnectormapping_facts:
      resource_group: resource_group_name
      hub_name: hub_name
      connector_name: connector_name
'''

RETURN = '''
connector_mappings:
    description: A list of dictionaries containing facts for Connector Mapping.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/sdkTestHub/connec
                    tors/testConnector8858/mappings/testMapping12491"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: sdkTestHub/testConnector8858/testMapping12491
        description:
            description:
                - The description of the connector mapping.
            returned: always
            type: str
            sample: Test mapping
        state:
            description:
                - "State of connector mapping. Possible values include: 'Creating', 'Created', 'Failed', 'Ready', 'Running', 'Stopped', 'Expiring'"
            returned: always
            type: str
            sample: Created
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMConnectorMappingsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            connector_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.hub_name = None
        self.connector_name = None
        self.name = None
        super(AzureRMConnectorMappingsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['connector_mappings'] = self.get()
        else:
            self.results['connector_mappings'] = self.list_by_connector()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.connector_mappings.get(resource_group_name=self.resource_group,
                                                               hub_name=self.hub_name,
                                                               connector_name=self.connector_name,
                                                               mapping_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ConnectorMappings.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_connector(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.connector_mappings.list_by_connector(resource_group_name=self.resource_group,
                                                                             hub_name=self.hub_name,
                                                                             connector_name=self.connector_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ConnectorMappings.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None),
            'state': d.get('state', None)
        }
        return d


def main():
    AzureRMConnectorMappingsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_loganalyticslinkedservice_facts
version_added: "2.8"
short_description: Get Azure Linked Service facts.
description:
    - Get facts of Azure Linked Service.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
        required: True
    workspace_name:
        description:
            - Name of the Log Analytics Workspace that contains the linkedServices resource
        required: True
    name:
        description:
            - Name of the linked service.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Linked Service
    azure_rm_loganalyticslinkedservice_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      name: linked_service_name

  - name: List instances of Linked Service
    azure_rm_loganalyticslinkedservice_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
'''

RETURN = '''
linked_services:
    description: A list of dictionaries containing facts for Linked Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000005/resourcegroups/mms-eus/providers/microsoft.operationalinsights/workspaces/testlinkws
                    /linkedservices/automation"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: TestLinkWS/Automation
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: tags
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.loganalytics import OperationalInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMLinkedServicesFacts(AzureRMModuleBase):
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
        self.workspace_name = None
        self.name = None
        self.tags = None
        super(AzureRMLinkedServicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(OperationalInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['linked_services'] = self.get()
        else:
            self.results['linked_services'] = self.list_by_workspace()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.linked_services.get(resource_group_name=self.resource_group,
                                                            workspace_name=self.workspace_name,
                                                            linked_service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LinkedServices.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_workspace(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.linked_services.list_by_workspace(resource_group_name=self.resource_group,
                                                                          workspace_name=self.workspace_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for LinkedServices.')

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
            'name': d.get('name', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMLinkedServicesFacts()


if __name__ == '__main__':
    main()

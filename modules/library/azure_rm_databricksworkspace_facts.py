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
module: azure_rm_databricksworkspace_facts
version_added: "2.8"
short_description: Get Azure Workspace facts.
description:
    - Get facts of Azure Workspace.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
    workspace_name:
        description:
            - The name of the workspace.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Workspace
    azure_rm_databricksworkspace_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name

  - name: List instances of Workspace
    azure_rm_databricksworkspace_facts:
      resource_group: resource_group_name

  - name: List instances of Workspace
    azure_rm_databricksworkspace_facts:
'''

RETURN = '''
workspaces:
    description: A list of dictionaries containing facts for Workspace.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Databricks/workspaces/myWorkspace
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: myWorkspace
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        location:
            description:
                - The geo-location where the resource lives
            returned: always
            type: str
            sample: East US 2
        parameters:
            description:
                - Name and value pairs that define the workspace parameters.
            returned: always
            type: str
            sample: parameters
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.databricks import DatabricksClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkspacesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            workspace_name=dict(
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
        self.tags = None
        super(AzureRMWorkspacesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DatabricksClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.workspace_name is not None):
            self.results['workspaces'] = self.get()
        elif self.resource_group is not None:
            self.results['workspaces'] = self.list_by_resource_group()
        else:
            self.results['workspaces'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workspaces.get(resource_group_name=self.resource_group,
                                                       workspace_name=self.workspace_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workspaces.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workspaces.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workspaces.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workspaces.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workspaces.')

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
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'parameters': d.get('parameters', None)
        }
        return d


def main():
    AzureRMWorkspacesFacts()


if __name__ == '__main__':
    main()

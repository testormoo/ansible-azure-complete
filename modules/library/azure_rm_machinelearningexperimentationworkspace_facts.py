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
module: azure_rm_machinelearningexperimentationworkspace_facts
version_added: "2.8"
short_description: Get Azure Workspace facts.
description:
    - Get facts of Azure Workspace.

options:
    resource_group:
        description:
            - The name of the resource group to which the machine learning team account belongs.
        required: True
    account_name:
        description:
            - The name of the machine learning team account.
        required: True
    name:
        description:
            - The name of the machine learning team account workspace.
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
    azure_rm_machinelearningexperimentationworkspace_facts:
      resource_group: resource_group_name
      account_name: account_name
      name: workspace_name

  - name: List instances of Workspace
    azure_rm_machinelearningexperimentationworkspace_facts:
      account_name: account_name
      resource_group: resource_group_name
'''

RETURN = '''
workspaces:
    description: A list of dictionaries containing facts for Workspace.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/accountcrud-1234/providers/Microsoft.MachineLearningExperimentation/a
                    ccounts/accountcrud5678/workspaces/testworkspace"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: testworkspace
        location:
            description:
                - The location of the resource. This cannot be changed after the resource is created.
            returned: always
            type: str
            sample: East US 2 EUAP
        tags:
            description:
                - The tags of the resource.
            returned: always
            type: complex
            sample: "{\n  'tagKey1': 'TagValue1'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.machinelearningexperimentation import MLTeamAccountManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkspaceFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
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
        self.account_name = None
        self.name = None
        self.tags = None
        super(AzureRMWorkspaceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MLTeamAccountManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['workspaces'] = self.get()
        else:
            self.results['workspaces'] = self.list_by_accounts()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workspaces.get(resource_group_name=self.resource_group,
                                                       account_name=self.account_name,
                                                       workspace_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workspace.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_accounts(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workspaces.list_by_accounts(account_name=self.account_name,
                                                                    resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Workspace.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMWorkspaceFacts()


if __name__ == '__main__':
    main()

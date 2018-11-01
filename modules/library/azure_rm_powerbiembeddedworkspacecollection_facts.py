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
module: azure_rm_powerbiembeddedworkspacecollection_facts
version_added: "2.8"
short_description: Get Azure Workspace Collection facts.
description:
    - Get facts of Azure Workspace Collection.

options:
    resource_group:
        description:
            - Azure resource group

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Workspace Collection
    azure_rm_powerbiembeddedworkspacecollection_facts:
      resource_group: resource_group_name

  - name: List instances of Workspace Collection
    azure_rm_powerbiembeddedworkspacecollection_facts:
'''

RETURN = '''
workspace_collections:
    description: A list of dictionaries containing facts for Workspace Collection.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.powerbiembedded import PowerBIEmbeddedManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWorkspaceCollectionsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        super(AzureRMWorkspaceCollectionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(PowerBIEmbeddedManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None:
            self.results['workspace_collections'] = self.list_by_resource_group()
        else:
            self.results['workspace_collections'] = self.list_by_subscription()
        return self.results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workspace_collections.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WorkspaceCollections.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.workspace_collections.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for WorkspaceCollections.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMWorkspaceCollectionsFacts()


if __name__ == '__main__':
    main()

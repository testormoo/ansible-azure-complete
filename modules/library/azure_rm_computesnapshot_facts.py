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
module: azure_rm_computesnapshot_facts
version_added: "2.8"
short_description: Get Azure Snapshot facts.
description:
    - Get facts of Azure Snapshot.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - "The name of the snapshot that is being created. The name can't be changed after the snapshot is created. Supported characters for the name
               are a-z, A-Z, 0-9 and _. The max name length is 80 characters."
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Snapshot
    azure_rm_computesnapshot_facts:
      resource_group: resource_group_name
      name: snapshot_name

  - name: List instances of Snapshot
    azure_rm_computesnapshot_facts:
      resource_group: resource_group_name
'''

RETURN = '''
snapshots:
    description: A list of dictionaries containing facts for Snapshot.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.Compute/snapshots/mySnapshot
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: mySnapshot
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'department': 'Development',\n  'project': 'Snapshots'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSnapshotFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
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
        self.name = None
        self.tags = None
        super(AzureRMSnapshotFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['snapshots'] = self.get()
        else:
            self.results['snapshots'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.snapshots.get(resource_group_name=self.resource_group,
                                                      snapshot_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Snapshot.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.snapshots.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Snapshot.')

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
    AzureRMSnapshotFacts()


if __name__ == '__main__':
    main()

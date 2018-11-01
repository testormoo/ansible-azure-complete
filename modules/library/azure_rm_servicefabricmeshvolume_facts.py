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
module: azure_rm_servicefabricmeshvolume_facts
version_added: "2.8"
short_description: Get Azure Volume facts.
description:
    - Get facts of Azure Volume.

options:
    resource_group:
        description:
            - Azure resource group name
    volume_resource_name:
        description:
            - The identity of the volume.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Volume
    azure_rm_servicefabricmeshvolume_facts:
      resource_group: resource_group_name
      volume_resource_name: volume_resource_name

  - name: List instances of Volume
    azure_rm_servicefabricmeshvolume_facts:
      resource_group: resource_group_name

  - name: List instances of Volume
    azure_rm_servicefabricmeshvolume_facts:
'''

RETURN = '''
volume:
    description: A list of dictionaries containing facts for Volume.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified identifier for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/volumes/sampleVolume
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: sampleVolume
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - The geo-location where the resource lives
            returned: always
            type: str
            sample: EastUS
        description:
            description:
                - User readable description of the volume.
            returned: always
            type: str
            sample: Service Fabric Mesh sample volume.
        status:
            description:
                - "Status of the volume. Possible values include: 'Unknown', 'Ready', 'Upgrading', 'Creating', 'Deleting', 'Failed'"
            returned: always
            type: str
            sample: Ready
        provider:
            description:
                - Provider of the volume.
            returned: always
            type: str
            sample: SFAzureFile
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.servicefabricmesh import ServiceFabricMeshManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMVolumeFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            volume_resource_name=dict(
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
        self.volume_resource_name = None
        self.tags = None
        super(AzureRMVolumeFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.volume_resource_name is not None):
            self.results['volume'] = self.get()
        elif self.resource_group is not None:
            self.results['volume'] = self.list_by_resource_group()
        else:
            self.results['volume'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.volume.get(resource_group_name=self.resource_group,
                                                   volume_resource_name=self.volume_resource_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Volume.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.volume.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Volume.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.volume.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Volume.')

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
            'description': d.get('description', None),
            'status': d.get('status', None),
            'provider': d.get('provider', None)
        }
        return d


def main():
    AzureRMVolumeFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_computeimage_facts
version_added: "2.8"
short_description: Get Azure Image facts.
description:
    - Get facts of Azure Image.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    image_name:
        description:
            - The name of the image.
    expand:
        description:
            - The expand expression to apply on the operation.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Image
    azure_rm_computeimage_facts:
      resource_group: resource_group_name
      image_name: image_name
      expand: expand

  - name: List instances of Image
    azure_rm_computeimage_facts:
      resource_group: resource_group_name
'''

RETURN = '''
images:
    description: A list of dictionaries containing facts for Image.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/{subscriptionId}/resourceGroups/myResourceGroup/providers/Microsoft.Compute/images/myImage
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: myImage
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: West US
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
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMImagesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            image_name=dict(
                type='str'
            ),
            expand=dict(
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
        self.image_name = None
        self.expand = None
        self.tags = None
        super(AzureRMImagesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.image_name is not None:
            self.results['images'] = self.get()
        else:
            self.results['images'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.images.get(resource_group_name=self.resource_group,
                                                   image_name=self.image_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Images.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.images.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Images.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMImagesFacts()


if __name__ == '__main__':
    main()

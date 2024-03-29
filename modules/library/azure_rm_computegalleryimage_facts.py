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
module: azure_rm_computegalleryimage_facts
version_added: "2.8"
short_description: Get Azure Gallery Image facts.
description:
    - Get facts of Azure Gallery Image.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    gallery_name:
        description:
            - The name of the Shared Image Gallery from which the Image Definitions are to be retrieved.
        required: True
    name:
        description:
            - The name of the gallery Image Definition to be retrieved.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Gallery Image
    azure_rm_computegalleryimage_facts:
      resource_group: resource_group_name
      gallery_name: gallery_name
      name: gallery_image_name

  - name: List instances of Gallery Image
    azure_rm_computegalleryimage_facts:
      resource_group: resource_group_name
      gallery_name: gallery_name
'''

RETURN = '''
gallery_images:
    description: A list of dictionaries containing facts for Gallery Image.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: id
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: myGalleryImageName
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
        identifier:
            description:
                -
            returned: always
            type: complex
            sample: identifier
            contains:
                publisher:
                    description:
                        - The name of the gallery Image Definition publisher.
                    returned: always
                    type: str
                    sample: myPublisherName
                offer:
                    description:
                        - The name of the gallery Image Definition offer.
                    returned: always
                    type: str
                    sample: myOfferName
                sku:
                    description:
                        - The name of the gallery Image Definition SKU.
                    returned: always
                    type: str
                    sample: mySkuName
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMGalleryImageFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            gallery_name=dict(
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
        self.gallery_name = None
        self.name = None
        self.tags = None
        super(AzureRMGalleryImageFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['gallery_images'] = self.get()
        else:
            self.results['gallery_images'] = self.list_by_gallery()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.gallery_images.get(resource_group_name=self.resource_group,
                                                           gallery_name=self.gallery_name,
                                                           gallery_image_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Gallery Image.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_gallery(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.gallery_images.list_by_gallery(resource_group_name=self.resource_group,
                                                                       gallery_name=self.gallery_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Gallery Image.')

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
            'tags': d.get('tags', None),
            'identifier': {
                'publisher': d.get('identifier', {}).get('publisher', None),
                'offer': d.get('identifier', {}).get('offer', None),
                'sku': d.get('identifier', {}).get('sku', None)
            }
        }
        return d


def main():
    AzureRMGalleryImageFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_computevirtualmachineextensionimage_facts
version_added: "2.8"
short_description: Get Azure Virtual Machine Extension Image facts.
description:
    - Get facts of Azure Virtual Machine Extension Image.

options:
    location:
        description:
            - The name of a supported Azure region.
        required: True
    name:
        description:
        required: True
    type:
        description:
        required: True
    version:
        description:
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Virtual Machine Extension Image
    azure_rm_computevirtualmachineextensionimage_facts:
      location: location
      name: publisher_name
      type: type
      version: version
'''

RETURN = '''
virtual_machine_extension_images:
    description: A list of dictionaries containing facts for Virtual Machine Extension Image.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: id
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


class AzureRMVirtualMachineExtensionImagesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            location=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            type=dict(
                type='str',
                required=True
            ),
            version=dict(
                type='str',
                required=True
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
        self.location = None
        self.name = None
        self.type = None
        self.version = None
        self.tags = None
        super(AzureRMVirtualMachineExtensionImagesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['virtual_machine_extension_images'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.virtual_machine_extension_images.get(location=self.location,
                                                                             publisher_name=self.name,
                                                                             type=self.type,
                                                                             version=self.version)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for VirtualMachineExtensionImages.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMVirtualMachineExtensionImagesFacts()


if __name__ == '__main__':
    main()

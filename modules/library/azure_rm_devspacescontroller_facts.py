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
module: azure_rm_devspacescontroller_facts
version_added: "2.8"
short_description: Get Azure Controller facts.
description:
    - Get facts of Azure Controller.

options:
    resource_group:
        description:
            - Resource group to which the resource belongs.
        required: True
    name:
        description:
            - Name of the resource.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Controller
    azure_rm_devspacescontroller_facts:
      resource_group: resource_group_name
      name: name

  - name: List instances of Controller
    azure_rm_devspacescontroller_facts:
      resource_group: resource_group_name
'''

RETURN = '''
controllers:
    description: A list of dictionaries containing facts for Controller.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.DevSpaces/controllers/myControlle
                    rResource"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: myControllerResource
        tags:
            description:
                - Tags for the Azure resource.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - Region where the Azure resource is located.
            returned: always
            type: str
            sample: eastus
        sku:
            description:
                -
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - The name of the SKU for Azure Dev Spaces Controller.
                    returned: always
                    type: str
                    sample: S1
                tier:
                    description:
                        - "The tier of the SKU for Azure Dev Spaces Controller. Possible values include: 'Standard'"
                    returned: always
                    type: str
                    sample: Standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.devspaces import DevSpacesManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMControllerFacts(AzureRMModuleBase):
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
        super(AzureRMControllerFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DevSpacesManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['controllers'] = self.get()
        else:
            self.results['controllers'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.controllers.get(resource_group_name=self.resource_group,
                                                        name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Controller.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.controllers.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Controller.')

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
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'tier': d.get('sku', {}).get('tier', None)
            }
        }
        return d


def main():
    AzureRMControllerFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_storsimplemanager_facts
version_added: "2.8"
short_description: Get Azure Manager facts.
description:
    - Get facts of Azure Manager.

options:
    resource_group:
        description:
            - The resource group name
        required: True
    manager_name:
        description:
            - The manager name
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Manager
    azure_rm_storsimplemanager_facts:
      resource_group: resource_group_name
      manager_name: manager_name

  - name: List instances of Manager
    azure_rm_storsimplemanager_facts:
      resource_group: resource_group_name
'''

RETURN = '''
managers:
    description: A list of dictionaries containing facts for Manager.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The Resource Id
            returned: always
            type: str
            sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/Managers/hMana
                    gerForSDKTest"
        name:
            description:
                - The Resource Name
            returned: always
            type: str
            sample: hManagerForSDKTest
        location:
            description:
                - The Geo location of the Manager
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Tags attached to the Manager
            returned: always
            type: complex
            sample: "{\n  'TagName': 'Demo manager for SDK test'\n}"
        sku:
            description:
                - Specifies the Sku
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "Refers to the sku name which should be 'Standard'"
                    returned: always
                    type: str
                    sample: Standard
        etag:
            description:
                - ETag of the Manager
            returned: always
            type: str
            sample: "W/'datetime'2018-08-12T15%3A10%3A31.6040125Z''"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagersFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            manager_name=dict(
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
        self.manager_name = None
        self.tags = None
        super(AzureRMManagersFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.manager_name is not None:
            self.results['managers'] = self.get()
        else:
            self.results['managers'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managers.get(resource_group_name=self.resource_group,
                                                     manager_name=self.manager_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Managers.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managers.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Managers.')

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
            'tags': d.get('tags', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            },
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMManagersFacts()


if __name__ == '__main__':
    main()

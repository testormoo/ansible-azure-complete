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
module: azure_rm_mediaasset_facts
version_added: "2.8"
short_description: Get Azure Asset facts.
description:
    - Get facts of Azure Asset.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    name:
        description:
            - The Asset name.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Asset
    azure_rm_mediaasset_facts:
      resource_group: resource_group_name
      account_name: account_name
      name: asset_name
'''

RETURN = '''
assets:
    description: A list of dictionaries containing facts for Asset.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource ID for the resource.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso/providers/Microsoft.Media/mediaservices/contosomedia/assets/C
                    limbingMountAdams"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: ClimbingMountAdams
        created:
            description:
                - The creation date of the Asset.
            returned: always
            type: datetime
            sample: "2013-02-01T00:00:00Z"
        description:
            description:
                - The Asset description.
            returned: always
            type: str
            sample: A documentary showing the ascent of Mount Adams
        container:
            description:
                - The name of the asset blob container.
            returned: always
            type: str
            sample: asset-1b648c1a-2268-461d-a1da-742bde23db40
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAssetFacts(AzureRMModuleBase):
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
                type='str',
                required=True
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
        super(AzureRMAssetFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['assets'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assets.get(resource_group_name=self.resource_group,
                                                   account_name=self.account_name,
                                                   asset_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Asset.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'created': d.get('created', None),
            'description': d.get('description', None),
            'container': d.get('container', None)
        }
        return d


def main():
    AzureRMAssetFacts()


if __name__ == '__main__':
    main()

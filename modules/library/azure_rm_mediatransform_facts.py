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
module: azure_rm_mediatransform_facts
version_added: "2.8"
short_description: Get Azure Transform facts.
description:
    - Get facts of Azure Transform.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    transform_name:
        description:
            - The Transform name.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Transform
    azure_rm_mediatransform_facts:
      resource_group: resource_group_name
      account_name: account_name
      transform_name: transform_name
'''

RETURN = '''
transforms:
    description: A list of dictionaries containing facts for Transform.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource ID for the resource.
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contosoresources/providers/Microsoft.Media/mediaservices/contosomedia
                    /transforms/sampleTransform"
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: sampleTransform
        created:
            description:
                - "The UTC date and time when the Transform was created, in 'YYYY-MM-DDThh:mm:ssZ' format."
            returned: always
            type: datetime
            sample: "2018-08-08T20:29:57.8095562+00:00"
        description:
            description:
                - An optional verbose description of the Transform.
            returned: always
            type: str
            sample: A sample Transform using the Standard Encoder with a built in preset.
        outputs:
            description:
                - An array of one or more TransformOutputs that the Transform should generate.
            returned: always
            type: complex
            sample: outputs
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTransformsFacts(AzureRMModuleBase):
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
            transform_name=dict(
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
        self.transform_name = None
        super(AzureRMTransformsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['transforms'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.transforms.get(resource_group_name=self.resource_group,
                                                       account_name=self.account_name,
                                                       transform_name=self.transform_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Transforms.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'created': d.get('created', None),
            'description': d.get('description', None),
            'outputs': {
            }
        }
        return d


def main():
    AzureRMTransformsFacts()


if __name__ == '__main__':
    main()

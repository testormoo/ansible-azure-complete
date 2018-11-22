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
module: azure_rm_feature_facts
version_added: "2.8"
short_description: Get Azure Feature facts.
description:
    - Get facts of Azure Feature.

options:
    resource_provider_namespace:
        description:
            - The resource provider namespace for the feature.
        required: True
    name:
        description:
            - The name of the feature to get.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Feature
    azure_rm_feature_facts:
      resource_provider_namespace: resource_provider_namespace
      name: feature_name
'''

RETURN = '''
features:
    description: A list of dictionaries containing facts for Feature.
    returned: always
    type: complex
    contains:
        name:
            description:
                - The name of the feature.
            returned: always
            type: str
            sample: Feature1
        properties:
            description:
                - Properties of the previewed feature.
            returned: always
            type: complex
            sample: properties
            contains:
                state:
                    description:
                        - The registration state of the feature for the subscription.
                    returned: always
                    type: str
                    sample: registered
        id:
            description:
                - The resource ID of the feature.
            returned: always
            type: str
            sample: feature_id1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.features import FeatureClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMFeatureFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_provider_namespace=dict(
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
        self.resource_provider_namespace = None
        self.name = None
        super(AzureRMFeatureFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(FeatureClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['features'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.features.get(resource_provider_namespace=self.resource_provider_namespace,
                                                     feature_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Feature.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'name': d.get('name', None),
            'properties': {
                'state': d.get('properties', {}).get('state', None)
            },
            'id': d.get('id', None)
        }
        return d


def main():
    AzureRMFeatureFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_advisorsuppression_facts
version_added: "2.8"
short_description: Get Azure Suppression facts.
description:
    - Get facts of Azure Suppression.

options:
    resource_uri:
        description:
            - The fully qualified Azure Resource Manager identifier of the resource to which the recommendation applies.
        required: True
    recommendation_id:
        description:
            - The recommendation ID.
        required: True
    name:
        description:
            - The name of the suppression.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Suppression
    azure_rm_advisorsuppression_facts:
      resource_uri: resource_uri
      recommendation_id: recommendation_id
      name: name
'''

RETURN = '''
suppressions:
    description: A list of dictionaries containing facts for Suppression.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource ID.
            returned: always
            type: str
            sample: /resourceUri/providers/Microsoft.Advisor/recommendations/recommendationId/suppressions/suppressionName1
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: suppressionName1
        ttl:
            description:
                - The duration for which the suppression is valid.
            returned: always
            type: str
            sample: "7.00:00:00"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.advisor import AdvisorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSuppressionFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_uri=dict(
                type='str',
                required=True
            ),
            recommendation_id=dict(
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
        self.resource_uri = None
        self.recommendation_id = None
        self.name = None
        super(AzureRMSuppressionFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AdvisorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['suppressions'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.suppressions.get(resource_uri=self.resource_uri,
                                                         recommendation_id=self.recommendation_id,
                                                         name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Suppression.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'ttl': d.get('ttl', None)
        }
        return d


def main():
    AzureRMSuppressionFacts()


if __name__ == '__main__':
    main()

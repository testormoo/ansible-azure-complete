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
module: azure_rm_advisorrecommendation_facts
version_added: "2.8"
short_description: Get Azure Recommendation facts.
description:
    - Get facts of Azure Recommendation.

options:
    resource_uri:
        description:
            - The fully qualified Azure Resource Manager identifier of the resource to which the recommendation applies.
        required: True
    recommendation_id:
        description:
            - The recommendation ID.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Recommendation
    azure_rm_advisorrecommendation_facts:
      resource_uri: resource_uri
      recommendation_id: recommendation_id
'''

RETURN = '''
recommendations:
    description: A list of dictionaries containing facts for Recommendation.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource ID.
            returned: always
            type: str
            sample: /resourceUri/providers/Microsoft.Advisor/recommendations/recommendationId
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: recommendationId
        category:
            description:
                - "The category of the recommendation. Possible values include: 'HighAvailability', 'Security', 'Performance', 'Cost'"
            returned: always
            type: str
            sample: HighAvailability
        impact:
            description:
                - "The business impact of the recommendation. Possible values include: 'High', 'Medium', 'Low'"
            returned: always
            type: str
            sample: Medium
        risk:
            description:
                - "The potential risk of not implementing the recommendation. Possible values include: 'Error', 'Warning', 'None'"
            returned: always
            type: str
            sample: Warning
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.advisor import AdvisorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRecommendationsFacts(AzureRMModuleBase):
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
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_uri = None
        self.recommendation_id = None
        super(AzureRMRecommendationsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AdvisorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['recommendations'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.recommendations.get(resource_uri=self.resource_uri,
                                                            recommendation_id=self.recommendation_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Recommendations.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'category': d.get('category', None),
            'impact': d.get('impact', None),
            'risk': d.get('risk', None)
        }
        return d


def main():
    AzureRMRecommendationsFacts()


if __name__ == '__main__':
    main()

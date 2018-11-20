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
module: azure_rm_timeseriesinsightsaccesspolicy_facts
version_added: "2.8"
short_description: Get Azure Access Policy facts.
description:
    - Get facts of Azure Access Policy.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    environment_name:
        description:
            - The name of the Time Series Insights environment associated with the specified resource group.
        required: True
    name:
        description:
            - The name of the Time Series Insights access policy associated with the specified environment.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Access Policy
    azure_rm_timeseriesinsightsaccesspolicy_facts:
      resource_group: resource_group_name
      environment_name: environment_name
      name: access_policy_name

  - name: List instances of Access Policy
    azure_rm_timeseriesinsightsaccesspolicy_facts:
      resource_group: resource_group_name
      environment_name: environment_name
'''

RETURN = '''
access_policies:
    description: A list of dictionaries containing facts for Access Policy.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.TimeSeriesInsights/Environments/env1/accessPolicies/ap1
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: ap1
        description:
            description:
                - An description of the access policy.
            returned: always
            type: str
            sample: some description
        roles:
            description:
                - The list of roles the principal is assigned on the environment.
            returned: always
            type: str
            sample: "[\n  'Reader'\n]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.timeseriesinsights import TimeSeriesInsightsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAccessPoliciesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            environment_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.environment_name = None
        self.name = None
        super(AzureRMAccessPoliciesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(TimeSeriesInsightsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['access_policies'] = self.get()
        else:
            self.results['access_policies'] = self.list_by_environment()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.access_policies.get(resource_group_name=self.resource_group,
                                                            environment_name=self.environment_name,
                                                            access_policy_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AccessPolicies.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_environment(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.access_policies.list_by_environment(resource_group_name=self.resource_group,
                                                                            environment_name=self.environment_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AccessPolicies.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None),
            'roles': d.get('roles', None)
        }
        return d


def main():
    AzureRMAccessPoliciesFacts()


if __name__ == '__main__':
    main()

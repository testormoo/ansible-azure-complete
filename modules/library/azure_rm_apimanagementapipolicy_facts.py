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
module: azure_rm_apimanagementapipolicy_facts
version_added: "2.8"
short_description: Get Azure Api Policy facts.
description:
    - Get facts of Azure Api Policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    api_id:
        description:
            - "API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n
               is the revision number."
        required: True
    policy_id:
        description:
            - The identifier of the Policy.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Api Policy
    azure_rm_apimanagementapipolicy_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
      policy_id: policy_id

  - name: List instances of Api Policy
    azure_rm_apimanagementapipolicy_facts:
      resource_group: resource_group_name
      name: service_name
      api_id: api_id
'''

RETURN = '''
api_policy:
    description: A list of dictionaries containing facts for Api Policy.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.ApiManagement/service/apimService1/apis/5600b59475ff190048040001/policies/policy
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: policy
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMApiPolicyFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            api_id=dict(
                type='str',
                required=True
            ),
            policy_id=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.api_id = None
        self.policy_id = None
        super(AzureRMApiPolicyFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.policy_id is not None:
            self.results['api_policy'] = self.get()
        else:
            self.results['api_policy'] = self.list_by_api()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_policy.get(resource_group_name=self.resource_group,
                                                       service_name=self.name,
                                                       api_id=self.api_id,
                                                       policy_id=self.policy_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api Policy.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_api(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_policy.list_by_api(resource_group_name=self.resource_group,
                                                               service_name=self.name,
                                                               api_id=self.api_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Api Policy.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMApiPolicyFacts()


if __name__ == '__main__':
    main()

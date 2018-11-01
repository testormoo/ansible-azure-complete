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
module: azure_rm_applicationinsightsapikey_facts
version_added: "2.8"
short_description: Get Azure A P I Key facts.
description:
    - Get facts of Azure A P I Key.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    resource_name:
        description:
            - The name of the Application Insights component resource.
        required: True
    key_id:
        description:
            - The API Key ID. This is unique within a Application Insights component.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of A P I Key
    azure_rm_applicationinsightsapikey_facts:
      resource_group: resource_group_name
      resource_name: resource_name
      key_id: key_id
'''

RETURN = '''
api_keys:
    description: A list of dictionaries containing facts for A P I Key.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The unique ID of the API key inside an Applciation Insights component. It is auto generated when the API key is created.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourcegroups/my-resource-group/providers/Microsoft.Insights/components/my-component/apikeys/bb820f1b-3110-4a8b-ba
                    2c-8c1129d7eb6a"
        name:
            description:
                - The name of the API key.
            returned: always
            type: str
            sample: test2
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAPIKeysFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            key_id=dict(
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
        self.resource_name = None
        self.key_id = None
        super(AzureRMAPIKeysFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['api_keys'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.api_keys.get(resource_group_name=self.resource_group,
                                                     resource_name=self.resource_name,
                                                     key_id=self.key_id)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for APIKeys.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMAPIKeysFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_applicationinsightswebtest_facts
version_added: "2.8"
short_description: Get Azure Web Test facts.
description:
    - Get facts of Azure Web Test.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    web_test_name:
        description:
            - The name of the Application Insights webtest resource.
    name:
        description:
            - The name of the Application Insights component resource.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Web Test
    azure_rm_applicationinsightswebtest_facts:
      resource_group: resource_group_name
      web_test_name: web_test_name

  - name: List instances of Web Test
    azure_rm_applicationinsightswebtest_facts:
      name: component_name
      resource_group: resource_group_name

  - name: List instances of Web Test
    azure_rm_applicationinsightswebtest_facts:
      resource_group: resource_group_name
'''

RETURN = '''
web_tests:
    description: A list of dictionaries containing facts for Web Test.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Azure resource Id
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/my-test-resources/providers/Microsoft.Insights/webtests/my-webtest-01-mywebservice
        name:
            description:
                - Azure resource name
            returned: always
            type: str
            sample: my-webtest-01-mywebservice
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: southcentralus
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'hidden-link:/subscriptions/subid/resourceGroups/my-test-resources/providers/Microsoft.Insights/components/mytester':
                     'Resource',\n  'hidden-link:/subscriptions/subid/resourceGroups/my-test-resources/providers/Microsoft.Web/sites/mytester':
                     'Resource'\n}"
        kind:
            description:
                - "The kind of web test that this web test watches. Choices are ping and multistep. Possible values include: 'ping', 'multistep'"
            returned: always
            type: str
            sample: ping
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWebTestFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            web_test_name=dict(
                type='str'
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
        self.web_test_name = None
        self.name = None
        self.tags = None
        super(AzureRMWebTestFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.web_test_name is not None:
            self.results['web_tests'] = self.get()
        elif self.name is not None:
            self.results['web_tests'] = self.list_by_component()
        else:
            self.results['web_tests'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.web_tests.get(resource_group_name=self.resource_group,
                                                      web_test_name=self.web_test_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Web Test.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_component(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.web_tests.list_by_component(component_name=self.name,
                                                                    resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Web Test.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.web_tests.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Web Test.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'kind': d.get('kind', None)
        }
        return d


def main():
    AzureRMWebTestFacts()


if __name__ == '__main__':
    main()

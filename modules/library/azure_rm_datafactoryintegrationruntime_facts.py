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
module: azure_rm_datafactoryintegrationruntime_facts
version_added: "2.8"
short_description: Get Azure Integration Runtime facts.
description:
    - Get facts of Azure Integration Runtime.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    name:
        description:
            - The integration runtime name.
    if_none_match:
        description:
            - "ETag of the integration runtime entity. Should only be specified for get. If the ETag matches the existing entity tag, or if * was provided,
               then no content will be returned."

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Integration Runtime
    azure_rm_datafactoryintegrationruntime_facts:
      resource_group: resource_group_name
      factory_name: factory_name
      name: integration_runtime_name
      if_none_match: if_none_match

  - name: List instances of Integration Runtime
    azure_rm_datafactoryintegrationruntime_facts:
      resource_group: resource_group_name
      factory_name: factory_name
'''

RETURN = '''
integration_runtimes:
    description: A list of dictionaries containing facts for Integration Runtime.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/example
                    FactoryName/integrationruntimes/exampleIntegrationRuntime"
        name:
            description:
                - The resource name.
            returned: always
            type: str
            sample: exampleIntegrationRuntime
        etag:
            description:
                - Etag identifies change in the resource.
            returned: always
            type: str
            sample: 0400f1a1-0000-0000-0000-5b2188640000
        properties:
            description:
                - Integration runtime properties.
            returned: always
            type: complex
            sample: properties
            contains:
                description:
                    description:
                        - Integration runtime description.
                    returned: always
                    type: str
                    sample: A selfhosted integration runtime
                type:
                    description:
                        - Constant filled by server.
                    returned: always
                    type: str
                    sample: SelfHosted
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIntegrationRuntimeFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            factory_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            if_none_match=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.factory_name = None
        self.name = None
        self.if_none_match = None
        super(AzureRMIntegrationRuntimeFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['integration_runtimes'] = self.get()
        else:
            self.results['integration_runtimes'] = self.list_by_factory()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_runtimes.get(resource_group_name=self.resource_group,
                                                                 factory_name=self.factory_name,
                                                                 integration_runtime_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Integration Runtime.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_factory(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_runtimes.list_by_factory(resource_group_name=self.resource_group,
                                                                             factory_name=self.factory_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Integration Runtime.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'etag': d.get('etag', None),
            'properties': {
                'description': d.get('properties', {}).get('description', None),
                'type': d.get('properties', {}).get('type', None)
            }
        }
        return d


def main():
    AzureRMIntegrationRuntimeFacts()


if __name__ == '__main__':
    main()

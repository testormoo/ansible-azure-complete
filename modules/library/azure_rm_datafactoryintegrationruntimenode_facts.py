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
module: azure_rm_datafactoryintegrationruntimenode_facts
version_added: "2.8"
short_description: Get Azure Integration Runtime Node facts.
description:
    - Get facts of Azure Integration Runtime Node.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    integration_runtime_name:
        description:
            - The integration runtime name.
        required: True
    node_name:
        description:
            - The integration runtime node name.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Integration Runtime Node
    azure_rm_datafactoryintegrationruntimenode_facts:
      resource_group: resource_group_name
      factory_name: factory_name
      integration_runtime_name: integration_runtime_name
      node_name: node_name
'''

RETURN = '''
integration_runtime_nodes:
    description: A list of dictionaries containing facts for Integration Runtime Node.
    returned: always
    type: complex
    contains:
        status:
            description:
                - "Status of the integration runtime node. Possible values include: 'NeedRegistration', 'Online', 'Limited', 'Offline', 'Upgrading',
                   'Initializing', 'InitializeFailed'"
            returned: always
            type: str
            sample: Online
        capabilities:
            description:
                - The integration runtime capabilities dictionary
            returned: always
            type: complex
            sample: "{\n  'serviceBusConnected': 'True',\n  'httpsPortEnabled': 'True',\n  'credentialInSync': 'True',\n  'connectedToResourceManager':
                     'True',\n  'nodeEnabled': 'True'\n}"
        version:
            description:
                - Version of the integration runtime node.
            returned: always
            type: str
            sample: 3.8.6743.6
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIntegrationRuntimeNodesFacts(AzureRMModuleBase):
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
            integration_runtime_name=dict(
                type='str',
                required=True
            ),
            node_name=dict(
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
        self.factory_name = None
        self.integration_runtime_name = None
        self.node_name = None
        super(AzureRMIntegrationRuntimeNodesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['integration_runtime_nodes'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_runtime_nodes.get(resource_group_name=self.resource_group,
                                                                      factory_name=self.factory_name,
                                                                      integration_runtime_name=self.integration_runtime_name,
                                                                      node_name=self.node_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IntegrationRuntimeNodes.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'status': d.get('status', None),
            'capabilities': d.get('capabilities', None),
            'version': d.get('version', None)
        }
        return d


def main():
    AzureRMIntegrationRuntimeNodesFacts()


if __name__ == '__main__':
    main()

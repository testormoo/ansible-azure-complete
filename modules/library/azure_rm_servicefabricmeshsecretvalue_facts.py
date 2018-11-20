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
module: azure_rm_servicefabricmeshsecretvalue_facts
version_added: "2.8"
short_description: Get Azure Secret Value facts.
description:
    - Get facts of Azure Secret Value.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    secret_resource_name:
        description:
            - The name of the secret resource.
        required: True
    name:
        description:
            - The name of the secret resource value which is typically the version identifier for the value.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Secret Value
    azure_rm_servicefabricmeshsecretvalue_facts:
      resource_group: resource_group_name
      secret_resource_name: secret_resource_name
      name: secret_value_resource_name
'''

RETURN = '''
secret_value:
    description: A list of dictionaries containing facts for Secret Value.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified identifier for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/secrets/dbConnectionSt
                    ring/values/v1"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: v1
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        location:
            description:
                - The geo-location where the resource lives
            returned: always
            type: str
            sample: EastUS
        value:
            description:
                - The actual value of the secret.
            returned: always
            type: str
            sample: value
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.servicefabricmesh import ServiceFabricMeshManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSecretValueFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            secret_resource_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
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
        self.secret_resource_name = None
        self.name = None
        self.tags = None
        super(AzureRMSecretValueFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['secret_value'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.secret_value.get(resource_group_name=self.resource_group,
                                                         secret_resource_name=self.secret_resource_name,
                                                         secret_value_resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for SecretValue.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'value': d.get('value', None)
        }
        return d


def main():
    AzureRMSecretValueFacts()


if __name__ == '__main__':
    main()

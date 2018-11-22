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
module: azure_rm_csmproject_facts
version_added: "2.8"
short_description: Get Azure Project facts.
description:
    - Get facts of Azure Project.

options:
    resource_group:
        description:
            - Name of the resource group within the Azure subscription.
        required: True
    root_resource_name:
        description:
            - Name of the Team Services account.
        required: True
    name:
        description:
            - Name of the Team Services project.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Project
    azure_rm_csmproject_facts:
      resource_group: resource_group_name
      root_resource_name: root_resource_name
      name: resource_name

  - name: List instances of Project
    azure_rm_csmproject_facts:
      resource_group: resource_group_name
      root_resource_name: root_resource_name
'''

RETURN = '''
projects:
    description: A list of dictionaries containing facts for Project.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Unique identifier of the resource.
            returned: always
            type: str
            sample: "/subscriptions/0de7f055-dbea-498d-8e9e-da287eedca90/resourceGroups/VS-Example-Group/providers/microsoft.visualstudio/account/ExampleAcco
                    unt/project/ExampleProject"
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: North Central US
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: ExampleProject
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        properties:
            description:
                - Key/value pair of resource properties.
            returned: always
            type: complex
            sample: "{\n  'AzureResourceName': 'ExampleProject',\n  'TfsUniqueIdentifier':
                     'vstfs:///Classification/TeamProject/7a4e6ba5-35bf-4667-86a4-9b598a88fa25'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.csm import VisualStudioResourceProviderClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProjectFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            root_resource_name=dict(
                type='str',
                required=True
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
        self.root_resource_name = None
        self.name = None
        self.tags = None
        super(AzureRMProjectFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(VisualStudioResourceProviderClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['projects'] = self.get()
        else:
            self.results['projects'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.projects.get(resource_group_name=self.resource_group,
                                                     root_resource_name=self.root_resource_name,
                                                     resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Project.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.projects.list_by_resource_group(resource_group_name=self.resource_group,
                                                                        root_resource_name=self.root_resource_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Project.')

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
            'location': d.get('location', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'properties': d.get('properties', None)
        }
        return d


def main():
    AzureRMProjectFacts()


if __name__ == '__main__':
    main()

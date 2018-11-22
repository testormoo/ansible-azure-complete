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
module: azure_rm_migrateproject_facts
version_added: "2.8"
short_description: Get Azure Project facts.
description:
    - Get facts of Azure Project.

options:
    resource_group:
        description:
            - Name of the Azure Resource Group that project is part of.
    name:
        description:
            - Name of the Azure Migrate project.
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.
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
    azure_rm_migrateproject_facts:
      resource_group: resource_group_name
      name: project_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Project
    azure_rm_migrateproject_facts:
      resource_group: resource_group_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Project
    azure_rm_migrateproject_facts:
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
projects:
    description: A list of dictionaries containing facts for Project.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Path reference to this project
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}"
            returned: always
            type: str
            sample: /subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01
        name:
            description:
                - Name of the project.
            returned: always
            type: str
            sample: project01
        location:
            description:
                - Azure location in which project is created.
            returned: always
            type: str
            sample: West Us
        tags:
            description:
                - Tags provided by Azure Tagging service.
            returned: always
            type: str
            sample: {}
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMProjectFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            self.config.accept_language=dict(
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
        self.name = None
        self.self.config.accept_language = None
        self.tags = None
        super(AzureRMProjectFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['projects'] = self.get()
        elif self.resource_group is not None:
            self.results['projects'] = self.list_by_resource_group()
        else:
            self.results['projects'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.projects.get(resource_group_name=self.resource_group,
                                                     project_name=self.name)
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
            response = self.mgmt_client.projects.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Project.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.projects.list_by_subscription()
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
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMProjectFacts()


if __name__ == '__main__':
    main()

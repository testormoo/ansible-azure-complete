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
module: azure_rm_migrategroup_facts
version_added: "2.8"
short_description: Get Azure Group facts.
description:
    - Get facts of Azure Group.

options:
    resource_group:
        description:
            - Name of the Azure Resource Group that project is part of.
        required: True
    project_name:
        description:
            - Name of the Azure Migrate project.
        required: True
    name:
        description:
            - Unique name of a group within a project.
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Group
    azure_rm_migrategroup_facts:
      resource_group: resource_group_name
      project_name: project_name
      name: group_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Group
    azure_rm_migrategroup_facts:
      resource_group: resource_group_name
      project_name: project_name
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
groups:
    description: A list of dictionaries containing facts for Group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Path reference to this group.
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}"
            returned: always
            type: str
            sample: "/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/groups
                    /group01"
        name:
            description:
                - Name of the group.
            returned: always
            type: str
            sample: group01
        machines:
            description:
                - List of machine names that are part of this group.
            returned: always
            type: str
            sample: "[\n
                     '/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/mach
                    ines/amansing_vm1',\n
                     '/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/mach
                    ines/amansing_vm2'\n]"
        assessments:
            description:
                - List of References to Assessments created on this group.
            returned: always
            type: str
            sample: "[\n
                     '/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/grou
                    ps/group01/assessments/assessment01',\n
                     '/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/grou
                    ps/group01/assessments/assessment02'\n]"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMGroupFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            project_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            self.config.accept_language=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.project_name = None
        self.name = None
        self.self.config.accept_language = None
        super(AzureRMGroupFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['groups'] = self.get()
        else:
            self.results['groups'] = self.list_by_project()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.groups.get(resource_group_name=self.resource_group,
                                                   project_name=self.project_name,
                                                   group_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Group.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_project(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.groups.list_by_project(resource_group_name=self.resource_group,
                                                               project_name=self.project_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Group.')

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
            'machines': d.get('machines', None),
            'assessments': d.get('assessments', None)
        }
        return d


def main():
    AzureRMGroupFacts()


if __name__ == '__main__':
    main()

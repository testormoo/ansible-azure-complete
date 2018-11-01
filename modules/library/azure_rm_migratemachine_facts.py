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
module: azure_rm_migratemachine_facts
version_added: "2.8"
short_description: Get Azure Machine facts.
description:
    - Get facts of Azure Machine.

options:
    resource_group:
        description:
            - Name of the Azure Resource Group that project is part of.
        required: True
    project_name:
        description:
            - Name of the Azure Migrate project.
        required: True
    machine_name:
        description:
            - Unique name of a machine in private datacenter.
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Machine
    azure_rm_migratemachine_facts:
      resource_group: resource_group_name
      project_name: project_name
      machine_name: machine_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Machine
    azure_rm_migratemachine_facts:
      resource_group: resource_group_name
      project_name: project_name
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
machines:
    description: A list of dictionaries containing facts for Machine.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Path reference to this machine.
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/machines/{machineNa
                  me}"
            returned: always
            type: str
            sample: "/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/projects01/machi
                    nes/amansing_vm1"
        name:
            description:
                - "Name of the machine. It is a GUID which is unique identifier of machine in private data center. For user-readable name, we have a
                   displayName property on this machine."
            returned: always
            type: str
            sample: amansing_vm1
        description:
            description:
                - Description of the machine
            returned: always
            type: str
            sample: Azure Migration Planner - Collector
        groups:
            description:
                - List of references to the groups that the machine is member of.
            returned: always
            type: str
            sample: "[\n
                     '/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/projects01/gro
                    ups/groups01',\n
                     '/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/projects01/gro
                    ups/groups02'\n]"
        disks:
            description:
                - Dictionary of disks attached to the machine. Key is ID of disk. Value is a disk object
            returned: always
            type: complex
            sample: "{\n  'scsi0:0': {\n    'gigabytesAllocated': '20',\n    'gigabytesConsumed': '0'\n  }\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMachinesFacts(AzureRMModuleBase):
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
            machine_name=dict(
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
        self.machine_name = None
        self.self.config.accept_language = None
        super(AzureRMMachinesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.machine_name is not None:
            self.results['machines'] = self.get()
        else:
            self.results['machines'] = self.list_by_project()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.machines.get(resource_group_name=self.resource_group,
                                                     project_name=self.project_name,
                                                     machine_name=self.machine_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Machines.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_project(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.machines.list_by_project(resource_group_name=self.resource_group,
                                                                 project_name=self.project_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Machines.')

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
            'groups': d.get('groups', None),
            'disks': d.get('disks', None)
        }
        return d


def main():
    AzureRMMachinesFacts()


if __name__ == '__main__':
    main()

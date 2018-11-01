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
module: azure_rm_migrateassessedmachine_facts
version_added: "2.8"
short_description: Get Azure Assessed Machine facts.
description:
    - Get facts of Azure Assessed Machine.

options:
    resource_group:
        description:
            - Name of the Azure Resource Group that project is part of.
        required: True
    project_name:
        description:
            - Name of the Azure Migrate project.
        required: True
    group_name:
        description:
            - Unique name of a group within a project.
        required: True
    assessment_name:
        description:
            - Unique name of an assessment within a project.
        required: True
    assessed_machine_name:
        description:
            - Unique name of an assessed machine evaluated as part of an assessment.
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Assessed Machine
    azure_rm_migrateassessedmachine_facts:
      resource_group: resource_group_name
      project_name: project_name
      group_name: group_name
      assessment_name: assessment_name
      assessed_machine_name: assessed_machine_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Assessed Machine
    azure_rm_migrateassessedmachine_facts:
      resource_group: resource_group_name
      project_name: project_name
      group_name: group_name
      assessment_name: assessment_name
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
assessed_machines:
    description: A list of dictionaries containing facts for Assessed Machine.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Path reference to this assessed machine.
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/
                  assessments/{assessmentName}/assessedMachines/{assessedMachineName}"
            returned: always
            type: str
            sample: "/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/groups
                    /group01/assessments/assessment01/assessedMachines/amansing_vm1"
        name:
            description:
                - Name of the machine.
            returned: always
            type: str
            sample: amansing_vm1
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
        description:
            description:
                - Description of the machine
            returned: always
            type: str
            sample: Azure Migration Planner - Collector
        disks:
            description:
                - Dictionary of disks attached to the machine. Key is ID of disk. Value is a disk object.
            returned: always
            type: complex
            sample: "{\n  'scsi0:0': {\n    'name': 'scsi0:0',\n    'gigabytesProvisioned': '20',\n    'gigabytesConsumed': '0',\n
                     'megabytesPerSecondOfRead': '0',\n    'megabytesPerSecondOfReadDataPointsExpected': '300',\n
                     'megabytesPerSecondOfReadDataPointsReceived': '280',\n    'megabytesPerSecondOfWrite': '0',\n
                     'megabytesPerSecondOfWriteDataPointsExpected': '300',\n    'megabytesPerSecondOfWriteDataPointsReceived': '280',\n
                     'numberOfReadOperationsPerSecond': '0',\n    'numberOfReadOperationsPerSecondDataPointsExpected': '300',\n
                     'numberOfReadOperationsPerSecondDataPointsReceived': '280',\n    'numberOfWriteOperationsPerSecond': '0',\n
                     'numberOfWriteOperationsPerSecondDataPointsExpected': '300',\n    'numberOfWriteOperationsPerSecondDataPointsReceived': '280',\n
                     'monthlyStorageCost': '0',\n    'recommendedDiskSize': 'Standard_S4',\n    'recommendedDiskType': 'Standard',\n
                     'gigabytesForRecommendedDiskSize': '32',\n    'suitability': 'Suitable',\n    'suitabilityExplanation': 'NotApplicable'\n  }\n}"
        suitability:
            description:
                - "Whether machine is suitable for migration to Azure. Possible values include: 'Unknown', 'NotSuitable', 'Suitable',
                   'ConditionallySuitable', 'ReadinessUnknown'"
            returned: always
            type: str
            sample: ConditionallySuitable
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAssessedMachinesFacts(AzureRMModuleBase):
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
            group_name=dict(
                type='str',
                required=True
            ),
            assessment_name=dict(
                type='str',
                required=True
            ),
            assessed_machine_name=dict(
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
        self.group_name = None
        self.assessment_name = None
        self.assessed_machine_name = None
        self.self.config.accept_language = None
        super(AzureRMAssessedMachinesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.assessed_machine_name is not None:
            self.results['assessed_machines'] = self.get()
        else:
            self.results['assessed_machines'] = self.list_by_assessment()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assessed_machines.get(resource_group_name=self.resource_group,
                                                              project_name=self.project_name,
                                                              group_name=self.group_name,
                                                              assessment_name=self.assessment_name,
                                                              assessed_machine_name=self.assessed_machine_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AssessedMachines.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_assessment(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assessed_machines.list_by_assessment(resource_group_name=self.resource_group,
                                                                             project_name=self.project_name,
                                                                             group_name=self.group_name,
                                                                             assessment_name=self.assessment_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for AssessedMachines.')

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
            'groups': d.get('groups', None),
            'description': d.get('description', None),
            'disks': d.get('disks', None),
            'suitability': d.get('suitability', None)
        }
        return d


def main():
    AzureRMAssessedMachinesFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_migrateassessment_facts
version_added: "2.8"
short_description: Get Azure Assessment facts.
description:
    - Get facts of Azure Assessment.

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
    name:
        description:
            - Unique name of an assessment within a project.
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Assessment
    azure_rm_migrateassessment_facts:
      resource_group: resource_group_name
      project_name: project_name
      group_name: group_name
      name: assessment_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Assessment
    azure_rm_migrateassessment_facts:
      resource_group: resource_group_name
      project_name: project_name
      group_name: group_name
      self.config.accept_language: self.config.accept_language

  - name: List instances of Assessment
    azure_rm_migrateassessment_facts:
      resource_group: resource_group_name
      project_name: project_name
      self.config.accept_language: self.config.accept_language
'''

RETURN = '''
assessments:
    description: A list of dictionaries containing facts for Assessment.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Path reference to this assessment.
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/
                  assessment/{assessmentName}"
            returned: always
            type: str
            sample: "/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/groups
                    /group01/assessments/assessment01"
        name:
            description:
                - Unique name of an assessment.
            returned: always
            type: str
            sample: assessment01
        percentile:
            description:
                - "Percentile of performance data used to recommend Azure size. Possible values include: 'Percentile50', 'Percentile90', 'Percentile95',
                   'Percentile99'"
            returned: always
            type: str
            sample: Percentile50
        stage:
            description:
                - "User configurable setting that describes the status of the assessment. Possible values include: 'InProgress', 'UnderReview', 'Approved'"
            returned: always
            type: str
            sample: InProgress
        currency:
            description:
                - "Currency to report prices in. Possible values include: 'Unknown', 'USD', 'DKK', 'CAD', 'IDR', 'JPY', 'KRW', 'NZD', 'NOK', 'RUB', 'SAR',
                   'ZAR', 'SEK', 'TRY', 'GBP', 'MXN', 'MYR', 'INR', 'HKD', 'BRL', 'TWD', 'EUR', 'CHF', 'ARS', 'AUD', 'CNY'"
            returned: always
            type: str
            sample: USD
        status:
            description:
                - "Wheter the assessment has been created and is valid. Possible values include: 'Created', 'Updated', 'Running', 'Completed', 'Invalid'"
            returned: always
            type: str
            sample: Invalid
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAssessmentFacts(AzureRMModuleBase):
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
                type='str'
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
        self.group_name = None
        self.name = None
        self.self.config.accept_language = None
        super(AzureRMAssessmentFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.group_name is not None and
                self.name is not None):
            self.results['assessments'] = self.get()
        elif self.group_name is not None:
            self.results['assessments'] = self.list_by_group()
        else:
            self.results['assessments'] = self.list_by_project()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assessments.get(resource_group_name=self.resource_group,
                                                        project_name=self.project_name,
                                                        group_name=self.group_name,
                                                        assessment_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Assessment.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assessments.list_by_group(resource_group_name=self.resource_group,
                                                                  project_name=self.project_name,
                                                                  group_name=self.group_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Assessment.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_project(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.assessments.list_by_project(resource_group_name=self.resource_group,
                                                                    project_name=self.project_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Assessment.')

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
            'percentile': d.get('percentile', None),
            'stage': d.get('stage', None),
            'currency': d.get('currency', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMAssessmentFacts()


if __name__ == '__main__':
    main()

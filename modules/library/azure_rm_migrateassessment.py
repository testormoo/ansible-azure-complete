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
module: azure_rm_migrateassessment
version_added: "2.8"
short_description: Manage Assessment instance.
description:
    - Create, update and delete instance of Assessment.

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
            - Unique name of an I(assessment) within a project.
        required: True
    self.config.accept_language:
        description:
            - Standard request header. Used by service to respond to client in appropriate language.
    assessment:
        description:
            - New or Updated Assessment object.
        suboptions:
            e_tag:
                description:
                    - For optimistic concurrency control.
            azure_location:
                description:
                    - Target Azure location for which the machines should be assessed. These enums are the same as used by Compute API.
                required: True
                choices:
                    - 'unknown'
                    - 'east_asia'
                    - 'southeast_asia'
                    - 'australia_east'
                    - 'australia_southeast'
                    - 'brazil_south'
                    - 'canada_central'
                    - 'canada_east'
                    - 'west_europe'
                    - 'north_europe'
                    - 'central_india'
                    - 'south_india'
                    - 'west_india'
                    - 'japan_east'
                    - 'japan_west'
                    - 'korea_central'
                    - 'korea_south'
                    - 'uk_west'
                    - 'uk_south'
                    - 'north_central_us'
                    - 'east_us'
                    - 'west_us2'
                    - 'south_central_us'
                    - 'central_us'
                    - 'east_us2'
                    - 'west_us'
                    - 'west_central_us'
                    - 'germany_central'
                    - 'germany_northeast'
                    - 'china_north'
                    - 'china_east'
            azure_offer_code:
                description:
                    - Offer code according to which cost estimation is done.
                required: True
                choices:
                    - 'unknown'
                    - 'msazr0003_p'
                    - 'msazr0044_p'
                    - 'msazr0059_p'
                    - 'msazr0060_p'
                    - 'msazr0062_p'
                    - 'msazr0063_p'
                    - 'msazr0064_p'
                    - 'msazr0029_p'
                    - 'msazr0022_p'
                    - 'msazr0023_p'
                    - 'msazr0148_p'
                    - 'msazr0025_p'
                    - 'msazr0036_p'
                    - 'msazr0120_p'
                    - 'msazr0121_p'
                    - 'msazr0122_p'
                    - 'msazr0123_p'
                    - 'msazr0124_p'
                    - 'msazr0125_p'
                    - 'msazr0126_p'
                    - 'msazr0127_p'
                    - 'msazr0128_p'
                    - 'msazr0129_p'
                    - 'msazr0130_p'
                    - 'msazr0111_p'
                    - 'msazr0144_p'
                    - 'msazr0149_p'
                    - 'msmcazr0044_p'
                    - 'msmcazr0059_p'
                    - 'msmcazr0060_p'
                    - 'msmcazr0063_p'
                    - 'msmcazr0120_p'
                    - 'msmcazr0121_p'
                    - 'msmcazr0125_p'
                    - 'msmcazr0128_p'
                    - 'msazrde0003_p'
                    - 'msazrde0044_p'
            azure_pricing_tier:
                description:
                    - Pricing tier for Size evaluation.
                required: True
                choices:
                    - 'standard'
                    - 'basic'
            azure_storage_redundancy:
                description:
                    - Storage Redundancy type offered by Azure.
                required: True
                choices:
                    - 'unknown'
                    - 'locally_redundant'
                    - 'zone_redundant'
                    - 'geo_redundant'
                    - 'read_access_geo_redundant'
            scaling_factor:
                description:
                    - "Scaling factor used over utilization data to add a performance buffer for new machines to be created in Azure. Min Value = 1.0, Max
                       value = 1.9, Default = 1.3."
                required: True
            percentile:
                description:
                    - Percentile of performance data used to recommend Azure size.
                required: True
                choices:
                    - 'percentile50'
                    - 'percentile90'
                    - 'percentile95'
                    - 'percentile99'
            time_range:
                description:
                    - Time range of performance data used to recommend a size.
                required: True
                choices:
                    - 'day'
                    - 'week'
                    - 'month'
            stage:
                description:
                    - User configurable setting that describes the status of the assessment.
                required: True
                choices:
                    - 'in_progress'
                    - 'under_review'
                    - 'approved'
            currency:
                description:
                    - Currency to report prices in.
                required: True
                choices:
                    - 'unknown'
                    - 'usd'
                    - 'dkk'
                    - 'cad'
                    - 'idr'
                    - 'jpy'
                    - 'krw'
                    - 'nzd'
                    - 'nok'
                    - 'rub'
                    - 'sar'
                    - 'zar'
                    - 'sek'
                    - 'try'
                    - 'gbp'
                    - 'mxn'
                    - 'myr'
                    - 'inr'
                    - 'hkd'
                    - 'brl'
                    - 'twd'
                    - 'eur'
                    - 'chf'
                    - 'ars'
                    - 'aud'
                    - 'cny'
            azure_hybrid_use_benefit:
                description:
                    - AHUB discount on windows virtual machines.
                required: True
                choices:
                    - 'unknown'
                    - 'yes'
                    - 'no'
            discount_percentage:
                description:
                    - Custom discount percentage to be applied on final costs. Can be in the range [0, 100].
                required: True
            sizing_criterion:
                description:
                    - Assessment sizing criterion.
                required: True
                choices:
                    - 'performance_based'
                    - 'as_on_premises'
    state:
      description:
        - Assert the state of the Assessment.
        - Use 'present' to create or update an Assessment and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Assessment
    azure_rm_migrateassessment:
      resource_group: myResourceGroup
      project_name: project01
      group_name: group01
      assessment_name: assessment01
      self.config.accept_language: NOT FOUND
      assessment:
        e_tag: "1100637e-0000-0000-0000-59f6ed1f0000"
'''

RETURN = '''
id:
    description:
        - "Path reference to this assessment.
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/assessme
          nt/{assessmentName}"
    returned: always
    type: str
    sample: "/subscriptions/75dd7e42-4fd1-4512-af04-83ad9864335b/resourceGroups/myResourceGroup/providers/Microsoft.Migrate/projects/project01/groups/group01
            /assessments/assessment01"
status:
    description:
        - "Wheter the assessment has been created and is valid. Possible values include: 'Created', 'Updated', 'Running', 'Completed', 'Invalid'"
    returned: always
    type: str
    sample: Invalid
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.migrate import AzureMigrate
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAssessments(AzureRMModuleBase):
    """Configuration class for an Azure RM Assessment resource"""

    def __init__(self):
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
            self.config.accept_language=dict(
                type='str'
            ),
            assessment=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.project_name = None
        self.group_name = None
        self.assessment_name = None
        self.self.config.accept_language = None
        self.assessment = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAssessments, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "e_tag":
                    self.assessment["e_tag"] = kwargs[key]
                elif key == "azure_location":
                    self.assessment["azure_location"] = _snake_to_camel(kwargs[key], True)
                elif key == "azure_offer_code":
                    ev = kwargs[key]
                    if ev == 'msazr0003_p':
                        ev = 'MSAZR0003P'
                    elif ev == 'msazr0044_p':
                        ev = 'MSAZR0044P'
                    elif ev == 'msazr0059_p':
                        ev = 'MSAZR0059P'
                    elif ev == 'msazr0060_p':
                        ev = 'MSAZR0060P'
                    elif ev == 'msazr0062_p':
                        ev = 'MSAZR0062P'
                    elif ev == 'msazr0063_p':
                        ev = 'MSAZR0063P'
                    elif ev == 'msazr0064_p':
                        ev = 'MSAZR0064P'
                    elif ev == 'msazr0029_p':
                        ev = 'MSAZR0029P'
                    elif ev == 'msazr0022_p':
                        ev = 'MSAZR0022P'
                    elif ev == 'msazr0023_p':
                        ev = 'MSAZR0023P'
                    elif ev == 'msazr0148_p':
                        ev = 'MSAZR0148P'
                    elif ev == 'msazr0025_p':
                        ev = 'MSAZR0025P'
                    elif ev == 'msazr0036_p':
                        ev = 'MSAZR0036P'
                    elif ev == 'msazr0120_p':
                        ev = 'MSAZR0120P'
                    elif ev == 'msazr0121_p':
                        ev = 'MSAZR0121P'
                    elif ev == 'msazr0122_p':
                        ev = 'MSAZR0122P'
                    elif ev == 'msazr0123_p':
                        ev = 'MSAZR0123P'
                    elif ev == 'msazr0124_p':
                        ev = 'MSAZR0124P'
                    elif ev == 'msazr0125_p':
                        ev = 'MSAZR0125P'
                    elif ev == 'msazr0126_p':
                        ev = 'MSAZR0126P'
                    elif ev == 'msazr0127_p':
                        ev = 'MSAZR0127P'
                    elif ev == 'msazr0128_p':
                        ev = 'MSAZR0128P'
                    elif ev == 'msazr0129_p':
                        ev = 'MSAZR0129P'
                    elif ev == 'msazr0130_p':
                        ev = 'MSAZR0130P'
                    elif ev == 'msazr0111_p':
                        ev = 'MSAZR0111P'
                    elif ev == 'msazr0144_p':
                        ev = 'MSAZR0144P'
                    elif ev == 'msazr0149_p':
                        ev = 'MSAZR0149P'
                    elif ev == 'msmcazr0044_p':
                        ev = 'MSMCAZR0044P'
                    elif ev == 'msmcazr0059_p':
                        ev = 'MSMCAZR0059P'
                    elif ev == 'msmcazr0060_p':
                        ev = 'MSMCAZR0060P'
                    elif ev == 'msmcazr0063_p':
                        ev = 'MSMCAZR0063P'
                    elif ev == 'msmcazr0120_p':
                        ev = 'MSMCAZR0120P'
                    elif ev == 'msmcazr0121_p':
                        ev = 'MSMCAZR0121P'
                    elif ev == 'msmcazr0125_p':
                        ev = 'MSMCAZR0125P'
                    elif ev == 'msmcazr0128_p':
                        ev = 'MSMCAZR0128P'
                    elif ev == 'msazrde0003_p':
                        ev = 'MSAZRDE0003P'
                    elif ev == 'msazrde0044_p':
                        ev = 'MSAZRDE0044P'
                    self.assessment["azure_offer_code"] = _snake_to_camel(ev, True)
                elif key == "azure_pricing_tier":
                    self.assessment["azure_pricing_tier"] = _snake_to_camel(kwargs[key], True)
                elif key == "azure_storage_redundancy":
                    self.assessment["azure_storage_redundancy"] = _snake_to_camel(kwargs[key], True)
                elif key == "scaling_factor":
                    self.assessment["scaling_factor"] = kwargs[key]
                elif key == "percentile":
                    self.assessment["percentile"] = _snake_to_camel(kwargs[key], True)
                elif key == "time_range":
                    self.assessment["time_range"] = _snake_to_camel(kwargs[key], True)
                elif key == "stage":
                    self.assessment["stage"] = _snake_to_camel(kwargs[key], True)
                elif key == "currency":
                    ev = kwargs[key]
                    if ev == 'usd':
                        ev = 'USD'
                    elif ev == 'dkk':
                        ev = 'DKK'
                    elif ev == 'cad':
                        ev = 'CAD'
                    elif ev == 'idr':
                        ev = 'IDR'
                    elif ev == 'jpy':
                        ev = 'JPY'
                    elif ev == 'krw':
                        ev = 'KRW'
                    elif ev == 'nzd':
                        ev = 'NZD'
                    elif ev == 'nok':
                        ev = 'NOK'
                    elif ev == 'rub':
                        ev = 'RUB'
                    elif ev == 'sar':
                        ev = 'SAR'
                    elif ev == 'zar':
                        ev = 'ZAR'
                    elif ev == 'sek':
                        ev = 'SEK'
                    elif ev == 'try':
                        ev = 'TRY'
                    elif ev == 'gbp':
                        ev = 'GBP'
                    elif ev == 'mxn':
                        ev = 'MXN'
                    elif ev == 'myr':
                        ev = 'MYR'
                    elif ev == 'inr':
                        ev = 'INR'
                    elif ev == 'hkd':
                        ev = 'HKD'
                    elif ev == 'brl':
                        ev = 'BRL'
                    elif ev == 'twd':
                        ev = 'TWD'
                    elif ev == 'eur':
                        ev = 'EUR'
                    elif ev == 'chf':
                        ev = 'CHF'
                    elif ev == 'ars':
                        ev = 'ARS'
                    elif ev == 'aud':
                        ev = 'AUD'
                    elif ev == 'cny':
                        ev = 'CNY'
                    self.assessment["currency"] = _snake_to_camel(ev, True)
                elif key == "azure_hybrid_use_benefit":
                    self.assessment["azure_hybrid_use_benefit"] = _snake_to_camel(kwargs[key], True)
                elif key == "discount_percentage":
                    self.assessment["discount_percentage"] = kwargs[key]
                elif key == "sizing_criterion":
                    self.assessment["sizing_criterion"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMigrate,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_assessment()

        if not old_response:
            self.log("Assessment instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Assessment instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Assessment instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Assessment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_assessment()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Assessment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_assessment()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_assessment():
                time.sleep(20)
        else:
            self.log("Assessment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_assessment(self):
        '''
        Creates or updates Assessment with the specified configuration.

        :return: deserialized Assessment instance state dictionary
        '''
        self.log("Creating / Updating the Assessment instance {0}".format(self.self.config.accept_language))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.assessments.create(resource_group_name=self.resource_group,
                                                               project_name=self.project_name,
                                                               group_name=self.group_name,
                                                               assessment_name=self.assessment_name)
            else:
                response = self.mgmt_client.assessments.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Assessment instance.')
            self.fail("Error creating the Assessment instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_assessment(self):
        '''
        Deletes specified Assessment instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Assessment instance {0}".format(self.self.config.accept_language))
        try:
            response = self.mgmt_client.assessments.delete(resource_group_name=self.resource_group,
                                                           project_name=self.project_name,
                                                           group_name=self.group_name,
                                                           assessment_name=self.assessment_name)
        except CloudError as e:
            self.log('Error attempting to delete the Assessment instance.')
            self.fail("Error deleting the Assessment instance: {0}".format(str(e)))

        return True

    def get_assessment(self):
        '''
        Gets the properties of the specified Assessment.

        :return: deserialized Assessment instance state dictionary
        '''
        self.log("Checking if the Assessment instance {0} is present".format(self.self.config.accept_language))
        found = False
        try:
            response = self.mgmt_client.assessments.get(resource_group_name=self.resource_group,
                                                        project_name=self.project_name,
                                                        group_name=self.group_name,
                                                        assessment_name=self.assessment_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Assessment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Assessment instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMAssessments()


if __name__ == '__main__':
    main()

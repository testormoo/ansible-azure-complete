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
short_description: Manage Azure Assessment instance.
description:
    - Create, update and delete instance of Azure Assessment.

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
    name:
        description:
            - Unique name of an assessment within a project.
        required: True
    self.config.accept_language:
        description:
            - C(standard) request header. Used by service to respond to client in appropriate language.
    e_tag:
        description:
            - For optimistic concurrency control.
    azure_location:
        description:
            - Target Azure location for which the machines should be assessed. These enums are the same as used by Compute API.
            - Required when C(state) is I(present).
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
            - Required when C(state) is I(present).
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
            - Required when C(state) is I(present).
        choices:
            - 'standard'
            - 'basic'
    azure_storage_redundancy:
        description:
            - Storage Redundancy type offered by Azure.
            - Required when C(state) is I(present).
        choices:
            - 'unknown'
            - 'locally_redundant'
            - 'zone_redundant'
            - 'geo_redundant'
            - 'read_access_geo_redundant'
    scaling_factor:
        description:
            - "Scaling factor used over utilization data to add a performance buffer for new machines to be created in Azure. Min Value = 1.0, Max value =
               1.9, Default = 1.3."
            - Required when C(state) is I(present).
    percentile:
        description:
            - Percentile of performance data used to recommend Azure size.
            - Required when C(state) is I(present).
        choices:
            - 'percentile50'
            - 'percentile90'
            - 'percentile95'
            - 'percentile99'
    time_range:
        description:
            - Time range of performance data used to recommend a size.
            - Required when C(state) is I(present).
        choices:
            - 'day'
            - 'week'
            - 'month'
    stage:
        description:
            - User configurable setting that describes the status of the assessment.
            - Required when C(state) is I(present).
        choices:
            - 'in_progress'
            - 'under_review'
            - 'approved'
    currency:
        description:
            - Currency to report prices in.
            - Required when C(state) is I(present).
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
            - Required when C(state) is I(present).
        choices:
            - 'unknown'
            - 'yes'
            - 'no'
    discount_percentage:
        description:
            - Custom discount percentage to be applied on final costs. Can be in the range [0, 100].
            - Required when C(state) is I(present).
    sizing_criterion:
        description:
            - Assessment sizing criterion.
            - Required when C(state) is I(present).
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
      name: assessment01
      self.config.accept_language: NOT FOUND
      e_tag: "1100637e-0000-0000-0000-59f6ed1f0000"
      azure_location: WestUs
      azure_offer_code: MSAZR0003P
      azure_pricing_tier: Standard
      azure_storage_redundancy: LocallyRedundant
      scaling_factor: 1.2
      percentile: Percentile50
      time_range: Day
      stage: InProgress
      currency: USD
      azure_hybrid_use_benefit: Yes
      discount_percentage: 100
      sizing_criterion: PerformanceBased
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMAssessment(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            self.config.accept_language=dict(
                type='str'
            ),
            e_tag=dict(
                type='str'
            ),
            azure_location=dict(
                type='str',
                choices=['unknown',
                         'east_asia',
                         'southeast_asia',
                         'australia_east',
                         'australia_southeast',
                         'brazil_south',
                         'canada_central',
                         'canada_east',
                         'west_europe',
                         'north_europe',
                         'central_india',
                         'south_india',
                         'west_india',
                         'japan_east',
                         'japan_west',
                         'korea_central',
                         'korea_south',
                         'uk_west',
                         'uk_south',
                         'north_central_us',
                         'east_us',
                         'west_us2',
                         'south_central_us',
                         'central_us',
                         'east_us2',
                         'west_us',
                         'west_central_us',
                         'germany_central',
                         'germany_northeast',
                         'china_north',
                         'china_east']
            ),
            azure_offer_code=dict(
                type='str',
                choices=['unknown',
                         'msazr0003_p',
                         'msazr0044_p',
                         'msazr0059_p',
                         'msazr0060_p',
                         'msazr0062_p',
                         'msazr0063_p',
                         'msazr0064_p',
                         'msazr0029_p',
                         'msazr0022_p',
                         'msazr0023_p',
                         'msazr0148_p',
                         'msazr0025_p',
                         'msazr0036_p',
                         'msazr0120_p',
                         'msazr0121_p',
                         'msazr0122_p',
                         'msazr0123_p',
                         'msazr0124_p',
                         'msazr0125_p',
                         'msazr0126_p',
                         'msazr0127_p',
                         'msazr0128_p',
                         'msazr0129_p',
                         'msazr0130_p',
                         'msazr0111_p',
                         'msazr0144_p',
                         'msazr0149_p',
                         'msmcazr0044_p',
                         'msmcazr0059_p',
                         'msmcazr0060_p',
                         'msmcazr0063_p',
                         'msmcazr0120_p',
                         'msmcazr0121_p',
                         'msmcazr0125_p',
                         'msmcazr0128_p',
                         'msazrde0003_p',
                         'msazrde0044_p']
            ),
            azure_pricing_tier=dict(
                type='str',
                choices=['standard',
                         'basic']
            ),
            azure_storage_redundancy=dict(
                type='str',
                choices=['unknown',
                         'locally_redundant',
                         'zone_redundant',
                         'geo_redundant',
                         'read_access_geo_redundant']
            ),
            scaling_factor=dict(
                type='float'
            ),
            percentile=dict(
                type='str',
                choices=['percentile50',
                         'percentile90',
                         'percentile95',
                         'percentile99']
            ),
            time_range=dict(
                type='str',
                choices=['day',
                         'week',
                         'month']
            ),
            stage=dict(
                type='str',
                choices=['in_progress',
                         'under_review',
                         'approved']
            ),
            currency=dict(
                type='str',
                choices=['unknown',
                         'usd',
                         'dkk',
                         'cad',
                         'idr',
                         'jpy',
                         'krw',
                         'nzd',
                         'nok',
                         'rub',
                         'sar',
                         'zar',
                         'sek',
                         'try',
                         'gbp',
                         'mxn',
                         'myr',
                         'inr',
                         'hkd',
                         'brl',
                         'twd',
                         'eur',
                         'chf',
                         'ars',
                         'aud',
                         'cny']
            ),
            azure_hybrid_use_benefit=dict(
                type='str',
                choices=['unknown',
                         'yes',
                         'no']
            ),
            discount_percentage=dict(
                type='float'
            ),
            sizing_criterion=dict(
                type='str',
                choices=['performance_based',
                         'as_on_premises']
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
        self.name = None
        self.self.config.accept_language = None
        self.assessment = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAssessment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.assessment[key] = kwargs[key]

        dict_camelize(self.assessment, ['azure_location'], True)
        dict_camelize(self.assessment, ['azure_offer_code'], True)
        dict_map(self.assessment, ['azure_offer_code'], {'msazr0003_p': 'MSAZR0003P', 'msazr0044_p': 'MSAZR0044P', 'msazr0059_p': 'MSAZR0059P', 'msazr0060_p': 'MSAZR0060P', 'msazr0062_p': 'MSAZR0062P', 'msazr0063_p': 'MSAZR0063P', 'msazr0064_p': 'MSAZR0064P', 'msazr0029_p': 'MSAZR0029P', 'msazr0022_p': 'MSAZR0022P', 'msazr0023_p': 'MSAZR0023P', 'msazr0148_p': 'MSAZR0148P', 'msazr0025_p': 'MSAZR0025P', 'msazr0036_p': 'MSAZR0036P', 'msazr0120_p': 'MSAZR0120P', 'msazr0121_p': 'MSAZR0121P', 'msazr0122_p': 'MSAZR0122P', 'msazr0123_p': 'MSAZR0123P', 'msazr0124_p': 'MSAZR0124P', 'msazr0125_p': 'MSAZR0125P', 'msazr0126_p': 'MSAZR0126P', 'msazr0127_p': 'MSAZR0127P', 'msazr0128_p': 'MSAZR0128P', 'msazr0129_p': 'MSAZR0129P', 'msazr0130_p': 'MSAZR0130P', 'msazr0111_p': 'MSAZR0111P', 'msazr0144_p': 'MSAZR0144P', 'msazr0149_p': 'MSAZR0149P', 'msmcazr0044_p': 'MSMCAZR0044P', 'msmcazr0059_p': 'MSMCAZR0059P', 'msmcazr0060_p': 'MSMCAZR0060P', 'msmcazr0063_p': 'MSMCAZR0063P', 'msmcazr0120_p': 'MSMCAZR0120P', 'msmcazr0121_p': 'MSMCAZR0121P', 'msmcazr0125_p': 'MSMCAZR0125P', 'msmcazr0128_p': 'MSMCAZR0128P', 'msazrde0003_p': 'MSAZRDE0003P', 'msazrde0044_p': 'MSAZRDE0044P'})
        dict_camelize(self.assessment, ['azure_pricing_tier'], True)
        dict_camelize(self.assessment, ['azure_storage_redundancy'], True)
        dict_camelize(self.assessment, ['percentile'], True)
        dict_camelize(self.assessment, ['time_range'], True)
        dict_camelize(self.assessment, ['stage'], True)
        dict_upper(self.assessment, ['currency'])
        dict_map(self.assessment, ['currency'], {'unknown': 'Unknown'})
        dict_camelize(self.assessment, ['azure_hybrid_use_benefit'], True)
        dict_camelize(self.assessment, ['sizing_criterion'], True)

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
                if (not default_compare(self.assessment, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Assessment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_assessment()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Assessment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_assessment()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Assessment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': response.get('status', None)
                })
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
                                                               assessment_name=self.name)
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
                                                           assessment_name=self.name)
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
                                                        assessment_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Assessment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Assessment instance.')
        if found is True:
            return response.as_dict()

        return False


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            else:
                key = list(old[0])[0]
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
   if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def main():
    """Main execution"""
    AzureRMAssessment()


if __name__ == '__main__':
    main()

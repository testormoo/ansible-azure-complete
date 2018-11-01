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
module: azure_rm_customerinsightsprediction
version_added: "2.8"
short_description: Manage Prediction instance.
description:
    - Create, update and delete instance of Prediction.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    prediction_name:
        description:
            - The name of the Prediction.
        required: True
    description:
        description:
            - Description of the prediction.
    display_name:
        description:
            - Display name of the prediction.
    involved_interaction_types:
        description:
            - Interaction types involved in the prediction.
        type: list
    involved_kpi_types:
        description:
            - KPI types involved in the prediction.
        type: list
    involved_relationships:
        description:
            - Relationships involved in the prediction.
        type: list
    negative_outcome_expression:
        description:
            - Negative outcome expression.
        required: True
    positive_outcome_expression:
        description:
            - Positive outcome expression.
        required: True
    primary_profile_type:
        description:
            - Primary profile type.
        required: True
    prediction_name:
        description:
            - Name of the prediction.
    scope_expression:
        description:
            - Scope expression.
        required: True
    auto_analyze:
        description:
            - Whether do auto analyze.
        required: True
    mappings:
        description:
            - Definition of the link mapping of prediction.
        required: True
        suboptions:
            score:
                description:
                    - The score of the link mapping.
            grade:
                description:
                    - The grade of the link mapping.
            reason:
                description:
                    - The reason of the link mapping.
    score_label:
        description:
            - Score label.
        required: True
    grades:
        description:
            - The prediction grades.
        type: list
        suboptions:
            grade_name:
                description:
                    - Name of the grade.
            min_score_threshold:
                description:
                    - Minimum score threshold.
            max_score_threshold:
                description:
                    - Maximum score threshold.
    state:
      description:
        - Assert the state of the Prediction.
        - Use 'present' to create or update an Prediction and 'absent' to delete it.
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
  - name: Create (or update) Prediction
    azure_rm_customerinsightsprediction:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      prediction_name: sdktest
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/azSdkTestHub/predictions/
            sdktest"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPredictions(AzureRMModuleBase):
    """Configuration class for an Azure RM Prediction resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            prediction_name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='dict'
            ),
            display_name=dict(
                type='dict'
            ),
            involved_interaction_types=dict(
                type='list'
            ),
            involved_kpi_types=dict(
                type='list'
            ),
            involved_relationships=dict(
                type='list'
            ),
            negative_outcome_expression=dict(
                type='str',
                required=True
            ),
            positive_outcome_expression=dict(
                type='str',
                required=True
            ),
            primary_profile_type=dict(
                type='str',
                required=True
            ),
            prediction_name=dict(
                type='str'
            ),
            scope_expression=dict(
                type='str',
                required=True
            ),
            auto_analyze=dict(
                type='str',
                required=True
            ),
            mappings=dict(
                type='dict',
                required=True
            ),
            score_label=dict(
                type='str',
                required=True
            ),
            grades=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.prediction_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPredictions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "involved_interaction_types":
                    self.parameters["involved_interaction_types"] = kwargs[key]
                elif key == "involved_kpi_types":
                    self.parameters["involved_kpi_types"] = kwargs[key]
                elif key == "involved_relationships":
                    self.parameters["involved_relationships"] = kwargs[key]
                elif key == "negative_outcome_expression":
                    self.parameters["negative_outcome_expression"] = kwargs[key]
                elif key == "positive_outcome_expression":
                    self.parameters["positive_outcome_expression"] = kwargs[key]
                elif key == "primary_profile_type":
                    self.parameters["primary_profile_type"] = kwargs[key]
                elif key == "prediction_name":
                    self.parameters["prediction_name"] = kwargs[key]
                elif key == "scope_expression":
                    self.parameters["scope_expression"] = kwargs[key]
                elif key == "auto_analyze":
                    self.parameters["auto_analyze"] = kwargs[key]
                elif key == "mappings":
                    self.parameters["mappings"] = kwargs[key]
                elif key == "score_label":
                    self.parameters["score_label"] = kwargs[key]
                elif key == "grades":
                    self.parameters["grades"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_prediction()

        if not old_response:
            self.log("Prediction instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Prediction instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Prediction instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Prediction instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_prediction()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Prediction instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_prediction()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_prediction():
                time.sleep(20)
        else:
            self.log("Prediction instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_prediction(self):
        '''
        Creates or updates Prediction with the specified configuration.

        :return: deserialized Prediction instance state dictionary
        '''
        self.log("Creating / Updating the Prediction instance {0}".format(self.prediction_name))

        try:
            response = self.mgmt_client.predictions.create_or_update(resource_group_name=self.resource_group,
                                                                     hub_name=self.hub_name,
                                                                     prediction_name=self.prediction_name,
                                                                     parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Prediction instance.')
            self.fail("Error creating the Prediction instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_prediction(self):
        '''
        Deletes specified Prediction instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Prediction instance {0}".format(self.prediction_name))
        try:
            response = self.mgmt_client.predictions.delete(resource_group_name=self.resource_group,
                                                           hub_name=self.hub_name,
                                                           prediction_name=self.prediction_name)
        except CloudError as e:
            self.log('Error attempting to delete the Prediction instance.')
            self.fail("Error deleting the Prediction instance: {0}".format(str(e)))

        return True

    def get_prediction(self):
        '''
        Gets the properties of the specified Prediction.

        :return: deserialized Prediction instance state dictionary
        '''
        self.log("Checking if the Prediction instance {0} is present".format(self.prediction_name))
        found = False
        try:
            response = self.mgmt_client.predictions.get(resource_group_name=self.resource_group,
                                                        hub_name=self.hub_name,
                                                        prediction_name=self.prediction_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Prediction instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Prediction instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMPredictions()


if __name__ == '__main__':
    main()
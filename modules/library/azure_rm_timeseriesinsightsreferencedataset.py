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
module: azure_rm_timeseriesinsightsreferencedataset
version_added: "2.8"
short_description: Manage Reference Data Set instance.
description:
    - Create, update and delete instance of Reference Data Set.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    environment_name:
        description:
            - The name of the Time Series Insights environment associated with the specified resource group.
        required: True
    reference_data_set_name:
        description:
            - Name of the reference data set.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    key_properties:
        description:
            - The list of key properties for the reference data set.
        required: True
        type: list
        suboptions:
            name:
                description:
                    - The name of the key property.
            type:
                description:
                    - The type of the key property.
                choices:
                    - 'string'
                    - 'double'
                    - 'bool'
                    - 'date_time'
    data_string_comparison_behavior:
        description:
            - "The reference data set key comparison behavior can be set using this property. By default, the value is 'C(ordinal)' - which means case
               sensitive key comparison will be performed while joining reference data with events or while adding new reference data. When
               'C(ordinal_ignore_case)' is set, case insensitive comparison will be used."
        choices:
            - 'ordinal'
            - 'ordinal_ignore_case'
    state:
      description:
        - Assert the state of the Reference Data Set.
        - Use 'present' to create or update an Reference Data Set and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Reference Data Set
    azure_rm_timeseriesinsightsreferencedataset:
      resource_group: rg1
      environment_name: env1
      reference_data_set_name: rds1
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.TimeSeriesInsights/Environments/env1/referenceDataSets/rds1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.timeseriesinsights import TimeSeriesInsightsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMReferenceDataSets(AzureRMModuleBase):
    """Configuration class for an Azure RM Reference Data Set resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            environment_name=dict(
                type='str',
                required=True
            ),
            reference_data_set_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            key_properties=dict(
                type='list',
                required=True
            ),
            data_string_comparison_behavior=dict(
                type='str',
                choices=['ordinal',
                         'ordinal_ignore_case']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.environment_name = None
        self.reference_data_set_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMReferenceDataSets, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "key_properties":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'string':
                            ev['type'] = 'String'
                        elif ev['type'] == 'double':
                            ev['type'] = 'Double'
                        elif ev['type'] == 'bool':
                            ev['type'] = 'Bool'
                        elif ev['type'] == 'date_time':
                            ev['type'] = 'DateTime'
                    self.parameters["key_properties"] = ev
                elif key == "data_string_comparison_behavior":
                    self.parameters["data_string_comparison_behavior"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(TimeSeriesInsightsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_referencedataset()

        if not old_response:
            self.log("Reference Data Set instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Reference Data Set instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Reference Data Set instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Reference Data Set instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_referencedataset()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Reference Data Set instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_referencedataset()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_referencedataset():
                time.sleep(20)
        else:
            self.log("Reference Data Set instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_referencedataset(self):
        '''
        Creates or updates Reference Data Set with the specified configuration.

        :return: deserialized Reference Data Set instance state dictionary
        '''
        self.log("Creating / Updating the Reference Data Set instance {0}".format(self.reference_data_set_name))

        try:
            response = self.mgmt_client.reference_data_sets.create_or_update(resource_group_name=self.resource_group,
                                                                             environment_name=self.environment_name,
                                                                             reference_data_set_name=self.reference_data_set_name,
                                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Reference Data Set instance.')
            self.fail("Error creating the Reference Data Set instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_referencedataset(self):
        '''
        Deletes specified Reference Data Set instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Reference Data Set instance {0}".format(self.reference_data_set_name))
        try:
            response = self.mgmt_client.reference_data_sets.delete(resource_group_name=self.resource_group,
                                                                   environment_name=self.environment_name,
                                                                   reference_data_set_name=self.reference_data_set_name)
        except CloudError as e:
            self.log('Error attempting to delete the Reference Data Set instance.')
            self.fail("Error deleting the Reference Data Set instance: {0}".format(str(e)))

        return True

    def get_referencedataset(self):
        '''
        Gets the properties of the specified Reference Data Set.

        :return: deserialized Reference Data Set instance state dictionary
        '''
        self.log("Checking if the Reference Data Set instance {0} is present".format(self.reference_data_set_name))
        found = False
        try:
            response = self.mgmt_client.reference_data_sets.get(resource_group_name=self.resource_group,
                                                                environment_name=self.environment_name,
                                                                reference_data_set_name=self.reference_data_set_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Reference Data Set instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Reference Data Set instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMReferenceDataSets()


if __name__ == '__main__':
    main()

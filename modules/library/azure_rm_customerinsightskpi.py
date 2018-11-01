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
module: azure_rm_customerinsightskpi
version_added: "2.8"
short_description: Manage Kpi instance.
description:
    - Create, update and delete instance of Kpi.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    kpi_name:
        description:
            - The name of the KPI.
        required: True
    entity_type:
        description:
            - The mapping entity type.
        required: True
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    entity_type_name:
        description:
            - The mapping entity name.
        required: True
    display_name:
        description:
            - Localized display name for the KPI.
    description:
        description:
            - Localized description for the KPI.
    calculation_window:
        description:
            - The calculation window.
        required: True
        choices:
            - 'lifetime'
            - 'hour'
            - 'day'
            - 'week'
            - 'month'
    calculation_window_field_name:
        description:
            - Name of calculation window field.
    function:
        description:
            - The computation function for the KPI.
        required: True
        choices:
            - 'sum'
            - 'avg'
            - 'min'
            - 'max'
            - 'last'
            - 'count'
            - 'none'
            - 'count_distinct'
    expression:
        description:
            - The computation expression for the KPI.
        required: True
    unit:
        description:
            - The unit of measurement for the KPI.
    filter:
        description:
            - The filter I(expression) for the KPI.
    group_by:
        description:
            - the group by properties for the KPI.
        type: list
    thres_holds:
        description:
            - The KPI thresholds.
        suboptions:
            lower_limit:
                description:
                    - The lower threshold limit.
                required: True
            upper_limit:
                description:
                    - The upper threshold limit.
                required: True
            increasing_kpi:
                description:
                    - Whether or not the KPI is an increasing KPI.
                required: True
    aliases:
        description:
            - The aliases.
        type: list
        suboptions:
            alias_name:
                description:
                    - KPI alias name.
                required: True
            expression:
                description:
                    - The expression.
                required: True
    extracts:
        description:
            - The KPI extracts.
        type: list
        suboptions:
            extract_name:
                description:
                    - KPI extract name.
                required: True
            expression:
                description:
                    - The expression.
                required: True
    state:
      description:
        - Assert the state of the Kpi.
        - Use 'present' to create or update an Kpi and 'absent' to delete it.
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
  - name: Create (or update) Kpi
    azure_rm_customerinsightskpi:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      kpi_name: kpiTest45453647
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/sdkTestHub/kpi/kpiTest454
            53647"
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


class AzureRMKpi(AzureRMModuleBase):
    """Configuration class for an Azure RM Kpi resource"""

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
            kpi_name=dict(
                type='str',
                required=True
            ),
            entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship'],
                required=True
            ),
            entity_type_name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='dict'
            ),
            description=dict(
                type='dict'
            ),
            calculation_window=dict(
                type='str',
                choices=['lifetime',
                         'hour',
                         'day',
                         'week',
                         'month'],
                required=True
            ),
            calculation_window_field_name=dict(
                type='str'
            ),
            function=dict(
                type='str',
                choices=['sum',
                         'avg',
                         'min',
                         'max',
                         'last',
                         'count',
                         'none',
                         'count_distinct'],
                required=True
            ),
            expression=dict(
                type='str',
                required=True
            ),
            unit=dict(
                type='str'
            ),
            filter=dict(
                type='str'
            ),
            group_by=dict(
                type='list'
            ),
            thres_holds=dict(
                type='dict'
            ),
            aliases=dict(
                type='list'
            ),
            extracts=dict(
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
        self.kpi_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMKpi, self).__init__(derived_arg_spec=self.module_arg_spec,
                                         supports_check_mode=True,
                                         supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "entity_type":
                    self.parameters["entity_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "entity_type_name":
                    self.parameters["entity_type_name"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "calculation_window":
                    self.parameters["calculation_window"] = _snake_to_camel(kwargs[key], True)
                elif key == "calculation_window_field_name":
                    self.parameters["calculation_window_field_name"] = kwargs[key]
                elif key == "function":
                    self.parameters["function"] = _snake_to_camel(kwargs[key], True)
                elif key == "expression":
                    self.parameters["expression"] = kwargs[key]
                elif key == "unit":
                    self.parameters["unit"] = kwargs[key]
                elif key == "filter":
                    self.parameters["filter"] = kwargs[key]
                elif key == "group_by":
                    self.parameters["group_by"] = kwargs[key]
                elif key == "thres_holds":
                    self.parameters["thres_holds"] = kwargs[key]
                elif key == "aliases":
                    self.parameters["aliases"] = kwargs[key]
                elif key == "extracts":
                    self.parameters["extracts"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_kpi()

        if not old_response:
            self.log("Kpi instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Kpi instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Kpi instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Kpi instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_kpi()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Kpi instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_kpi()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_kpi():
                time.sleep(20)
        else:
            self.log("Kpi instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_kpi(self):
        '''
        Creates or updates Kpi with the specified configuration.

        :return: deserialized Kpi instance state dictionary
        '''
        self.log("Creating / Updating the Kpi instance {0}".format(self.kpi_name))

        try:
            response = self.mgmt_client.kpi.create_or_update(resource_group_name=self.resource_group,
                                                             hub_name=self.hub_name,
                                                             kpi_name=self.kpi_name,
                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Kpi instance.')
            self.fail("Error creating the Kpi instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_kpi(self):
        '''
        Deletes specified Kpi instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Kpi instance {0}".format(self.kpi_name))
        try:
            response = self.mgmt_client.kpi.delete(resource_group_name=self.resource_group,
                                                   hub_name=self.hub_name,
                                                   kpi_name=self.kpi_name)
        except CloudError as e:
            self.log('Error attempting to delete the Kpi instance.')
            self.fail("Error deleting the Kpi instance: {0}".format(str(e)))

        return True

    def get_kpi(self):
        '''
        Gets the properties of the specified Kpi.

        :return: deserialized Kpi instance state dictionary
        '''
        self.log("Checking if the Kpi instance {0} is present".format(self.kpi_name))
        found = False
        try:
            response = self.mgmt_client.kpi.get(resource_group_name=self.resource_group,
                                                hub_name=self.hub_name,
                                                kpi_name=self.kpi_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Kpi instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Kpi instance.')
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
    AzureRMKpi()


if __name__ == '__main__':
    main()

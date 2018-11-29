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
short_description: Manage Azure Kpi instance.
description:
    - Create, update and delete instance of Azure Kpi.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    name:
        description:
            - The name of the KPI.
        required: True
    entity_type:
        description:
            - The mapping entity type.
            - Required when C(state) is I(present).
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    entity_type_name:
        description:
            - The mapping entity name.
            - Required when C(state) is I(present).
    display_name:
        description:
            - Localized display name for the KPI.
    description:
        description:
            - Localized description for the KPI.
    calculation_window:
        description:
            - The calculation window.
            - Required when C(state) is I(present).
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
            - Required when C(state) is I(present).
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
            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
            upper_limit:
                description:
                    - The upper threshold limit.
                    - Required when C(state) is I(present).
            increasing_kpi:
                description:
                    - Whether or not the KPI is an increasing KPI.
                    - Required when C(state) is I(present).
    aliases:
        description:
            - The aliases.
        type: list
        suboptions:
            alias_name:
                description:
                    - KPI alias name.
                    - Required when C(state) is I(present).
            expression:
                description:
                    - The expression.
                    - Required when C(state) is I(present).
    extracts:
        description:
            - The KPI extracts.
        type: list
        suboptions:
            extract_name:
                description:
                    - KPI extract name.
                    - Required when C(state) is I(present).
            expression:
                description:
                    - The expression.
                    - Required when C(state) is I(present).
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
      name: kpiTest45453647
      entity_type: Profile
      entity_type_name: testProfile2327128
      display_name: {
  "en-us": "Kpi DisplayName"
}
      description: {
  "en-us": "Kpi Description"
}
      calculation_window: Day
      function: Sum
      expression: SavingAccountBalance
      unit: unit
      group_by:
        - [
  "SavingAccountBalance"
]
      thres_holds:
        lower_limit: 5
        upper_limit: 50
        increasing_kpi: True
      aliases:
        - alias_name: alias
          expression: Id+4
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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
            name=dict(
                type='str',
                required=True
            ),
            entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship']
            ),
            entity_type_name=dict(
                type='str'
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
                         'month']
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
                         'count_distinct']
            ),
            expression=dict(
                type='str'
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
                type='dict',
                options=dict(
                    lower_limit=dict(
                        type='str'
                    ),
                    upper_limit=dict(
                        type='str'
                    ),
                    increasing_kpi=dict(
                        type='str'
                    )
                )
            ),
            aliases=dict(
                type='list',
                options=dict(
                    alias_name=dict(
                        type='str'
                    ),
                    expression=dict(
                        type='str'
                    )
                )
            ),
            extracts=dict(
                type='list',
                options=dict(
                    extract_name=dict(
                        type='str'
                    ),
                    expression=dict(
                        type='str'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.name = None
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

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['entity_type'], True)
        dict_camelize(self.parameters, ['calculation_window'], True)
        dict_camelize(self.parameters, ['function'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Kpi instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_kpi()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Kpi instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_kpi()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Kpi instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_kpi(self):
        '''
        Creates or updates Kpi with the specified configuration.

        :return: deserialized Kpi instance state dictionary
        '''
        self.log("Creating / Updating the Kpi instance {0}".format(self.name))

        try:
            response = self.mgmt_client.kpi.create_or_update(resource_group_name=self.resource_group,
                                                             hub_name=self.hub_name,
                                                             kpi_name=self.name,
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
        self.log("Deleting the Kpi instance {0}".format(self.name))
        try:
            response = self.mgmt_client.kpi.delete(resource_group_name=self.resource_group,
                                                   hub_name=self.hub_name,
                                                   kpi_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Kpi instance.')
            self.fail("Error deleting the Kpi instance: {0}".format(str(e)))

        return True

    def get_kpi(self):
        '''
        Gets the properties of the specified Kpi.

        :return: deserialized Kpi instance state dictionary
        '''
        self.log("Checking if the Kpi instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.kpi.get(resource_group_name=self.resource_group,
                                                hub_name=self.hub_name,
                                                kpi_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Kpi instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Kpi instance.')
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


def main():
    """Main execution"""
    AzureRMKpi()


if __name__ == '__main__':
    main()

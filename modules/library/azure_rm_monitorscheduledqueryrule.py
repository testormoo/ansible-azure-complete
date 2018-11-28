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
module: azure_rm_monitorscheduledqueryrule
version_added: "2.8"
short_description: Manage Azure Scheduled Query Rule instance.
description:
    - Create, update and delete instance of Azure Scheduled Query Rule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the rule.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    description:
        description:
            - The description of the Log Search rule.
    enabled:
        description:
            - The flag which indicates whether the Log Search rule is enabled. Value should be C(true) or C(false).
        choices:
            - 'true'
            - 'false'
    source:
        description:
            - Data Source against which rule will Query Data
            - Required when C(state) is I(present).
        suboptions:
            query:
                description:
                    - Log search query. Required for action type - AlertingAction
            authorized_resources:
                description:
                    - List of  Resource referred into I(query)
                type: list
            data_source_id:
                description:
                    - The resource uri over which log search I(query) is to be run.
                    - Required when C(state) is I(present).
            query_type:
                description:
                    - "Set value to 'C(result_count)'."
                choices:
                    - 'result_count'
    schedule:
        description:
            - Schedule (Frequnecy, Time Window) for rule. Required for I(action) type - AlertingAction
        suboptions:
            frequency_in_minutes:
                description:
                    - frequency (in minutes) at which rule condition should be evaluated.
                    - Required when C(state) is I(present).
            time_window_in_minutes:
                description:
                    - Time window for which data needs to be fetched for query (should be greater than or equal to I(frequency_in_minutes)).
                    - Required when C(state) is I(present).
    action:
        description:
            - Action needs to be taken on rule execution.
            - Required when C(state) is I(present).
        suboptions:
            odatatype:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Scheduled Query Rule.
        - Use 'present' to create or update an Scheduled Query Rule and 'absent' to delete it.
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
  - name: Create (or update) Scheduled Query Rule
    azure_rm_monitorscheduledqueryrule:
      resource_group: Rac46PostSwapRG
      name: logalertfoo
      location: eastus
      description: log alert description
      enabled: true
      source:
        query: Heartbeat | count
        data_source_id: /subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/Rac46PostSwapRG/providers/Microsoft.OperationalInsights/workspaces/sampleWorkspace
        query_type: ResultCount
      schedule:
        frequency_in_minutes: 15
        time_window_in_minutes: 15
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: /subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/Rac46PostSwapRG/providers/microsoft.insights/scheduledQueryRules/logalertfoo
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMScheduledQueryRule(AzureRMModuleBase):
    """Configuration class for an Azure RM Scheduled Query Rule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            enabled=dict(
                type='str',
                choices=['true',
                         'false']
            ),
            source=dict(
                type='dict'
                options=dict(
                    query=dict(
                        type='str'
                    ),
                    authorized_resources=dict(
                        type='list'
                    ),
                    data_source_id=dict(
                        type='str'
                    ),
                    query_type=dict(
                        type='str',
                        choices=['result_count']
                    )
                )
            ),
            schedule=dict(
                type='dict'
                options=dict(
                    frequency_in_minutes=dict(
                        type='int'
                    ),
                    time_window_in_minutes=dict(
                        type='int'
                    )
                )
            ),
            action=dict(
                type='dict'
                options=dict(
                    odatatype=dict(
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMScheduledQueryRule, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['source', 'query_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_scheduledqueryrule()

        if not old_response:
            self.log("Scheduled Query Rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Scheduled Query Rule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Scheduled Query Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_scheduledqueryrule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Scheduled Query Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_scheduledqueryrule()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Scheduled Query Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_scheduledqueryrule(self):
        '''
        Creates or updates Scheduled Query Rule with the specified configuration.

        :return: deserialized Scheduled Query Rule instance state dictionary
        '''
        self.log("Creating / Updating the Scheduled Query Rule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.scheduled_query_rules.create_or_update(resource_group_name=self.resource_group,
                                                                               rule_name=self.name,
                                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Scheduled Query Rule instance.')
            self.fail("Error creating the Scheduled Query Rule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_scheduledqueryrule(self):
        '''
        Deletes specified Scheduled Query Rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Scheduled Query Rule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.scheduled_query_rules.delete(resource_group_name=self.resource_group,
                                                                     rule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Scheduled Query Rule instance.')
            self.fail("Error deleting the Scheduled Query Rule instance: {0}".format(str(e)))

        return True

    def get_scheduledqueryrule(self):
        '''
        Gets the properties of the specified Scheduled Query Rule.

        :return: deserialized Scheduled Query Rule instance state dictionary
        '''
        self.log("Checking if the Scheduled Query Rule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.scheduled_query_rules.get(resource_group_name=self.resource_group,
                                                                  rule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Scheduled Query Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Scheduled Query Rule instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMScheduledQueryRule()


if __name__ == '__main__':
    main()

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
short_description: Manage Scheduled Query Rule instance.
description:
    - Create, update and delete instance of Scheduled Query Rule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    rule_name:
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
        required: True
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
                required: True
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
                required: True
            time_window_in_minutes:
                description:
                    - Time window for which data needs to be fetched for query (should be greater than or equal to I(frequency_in_minutes)).
                required: True
    action:
        description:
            - Action needs to be taken on rule execution.
        required: True
        suboptions:
            odatatype:
                description:
                    - Constant filled by server.
                required: True
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
      rule_name: logalertfoo
      location: eastus
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


class AzureRMScheduledQueryRules(AzureRMModuleBase):
    """Configuration class for an Azure RM Scheduled Query Rule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            rule_name=dict(
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
                type='dict',
                required=True
            ),
            schedule=dict(
                type='dict'
            ),
            action=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.rule_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMScheduledQueryRules, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "enabled":
                    self.parameters["enabled"] = kwargs[key]
                elif key == "source":
                    ev = kwargs[key]
                    if 'query_type' in ev:
                        if ev['query_type'] == 'result_count':
                            ev['query_type'] = 'ResultCount'
                    self.parameters["source"] = ev
                elif key == "schedule":
                    self.parameters["schedule"] = kwargs[key]
                elif key == "action":
                    self.parameters["action"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Scheduled Query Rule instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Scheduled Query Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_scheduledqueryrule()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Scheduled Query Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_scheduledqueryrule()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_scheduledqueryrule():
                time.sleep(20)
        else:
            self.log("Scheduled Query Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_scheduledqueryrule(self):
        '''
        Creates or updates Scheduled Query Rule with the specified configuration.

        :return: deserialized Scheduled Query Rule instance state dictionary
        '''
        self.log("Creating / Updating the Scheduled Query Rule instance {0}".format(self.rule_name))

        try:
            response = self.mgmt_client.scheduled_query_rules.create_or_update(resource_group_name=self.resource_group,
                                                                               rule_name=self.rule_name,
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
        self.log("Deleting the Scheduled Query Rule instance {0}".format(self.rule_name))
        try:
            response = self.mgmt_client.scheduled_query_rules.delete(resource_group_name=self.resource_group,
                                                                     rule_name=self.rule_name)
        except CloudError as e:
            self.log('Error attempting to delete the Scheduled Query Rule instance.')
            self.fail("Error deleting the Scheduled Query Rule instance: {0}".format(str(e)))

        return True

    def get_scheduledqueryrule(self):
        '''
        Gets the properties of the specified Scheduled Query Rule.

        :return: deserialized Scheduled Query Rule instance state dictionary
        '''
        self.log("Checking if the Scheduled Query Rule instance {0} is present".format(self.rule_name))
        found = False
        try:
            response = self.mgmt_client.scheduled_query_rules.get(resource_group_name=self.resource_group,
                                                                  rule_name=self.rule_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Scheduled Query Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Scheduled Query Rule instance.')
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
    AzureRMScheduledQueryRules()


if __name__ == '__main__':
    main()

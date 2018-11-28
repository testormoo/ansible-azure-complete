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
module: azure_rm_automationsoftwareupdateconfiguration
version_added: "2.8"
short_description: Manage Azure Software Update Configuration instance.
description:
    - Create, update and delete instance of Azure Software Update Configuration.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    name:
        description:
            - The name of the software update configuration to be created.
        required: True
    client_request_id:
        description:
            - Identifies this specific client request.
    update_configuration:
        description:
            - update specific properties for the Software update configuration
            - Required when C(state) is I(present).
        suboptions:
            operating_system:
                description:
                    - operating system of target machines.
                    - Required when C(state) is I(present).
                choices:
                    - 'windows'
                    - 'linux'
            windows:
                description:
                    - C(windows) specific update configuration.
                suboptions:
                    included_update_classifications:
                        description:
                            - Update classification included in the software update configuration. A comma separated string with required values.
                        choices:
                            - 'unclassified'
                            - 'critical'
                            - 'security'
                            - 'update_rollup'
                            - 'feature_pack'
                            - 'service_pack'
                            - 'definition'
                            - 'tools'
                            - 'updates'
                    excluded_kb_numbers:
                        description:
                            - KB numbers excluded from the software update configuration.
                        type: list
                    included_kb_numbers:
                        description:
                            - KB numbers included from the software update configuration.
                        type: list
                    reboot_setting:
                        description:
                            - Reboot setting for the software update configuration.
            linux:
                description:
                    - C(linux) specific update configuration.
                suboptions:
                    included_package_classifications:
                        description:
                            - Update classifications included in the software update configuration.
                        choices:
                            - 'unclassified'
                            - 'critical'
                            - 'security'
                            - 'other'
                    excluded_package_name_masks:
                        description:
                            - packages excluded from the software update configuration.
                        type: list
                    included_package_name_masks:
                        description:
                            - packages included from the software update configuration.
                        type: list
                    reboot_setting:
                        description:
                            - Reboot setting for the software update configuration.
            duration:
                description:
                    - "Maximum time allowed for the software update configuration run. Duration needs to be specified using the format PT[n]H[n]M[n]S as per
                       ISO8601"
            azure_virtual_machines:
                description:
                    - List of azure resource Ids for azure virtual machines targeted by the software update configuration.
                type: list
            non_azure_computer_names:
                description:
                    - List of names of non-azure machines targeted by the software update configuration.
                type: list
            targets:
                description:
                    - Group targets for the software update configuration.
                suboptions:
                    azure_queries:
                        description:
                            - List of Azure queries in the software update configuration.
                        type: list
                        suboptions:
                            scope:
                                description:
                                    - List of Subscription or Resource Group ARM Ids.
                                type: list
                            locations:
                                description:
                                    - List of locations to I(scope) the query to.
                                type: list
                            tag_settings:
                                description:
                                    - Tag settings for the VM.
                                suboptions:
                                    filter_operator:
                                        description:
                                            - Filter VMs by C(any) or C(all) specified tags.
                                        choices:
                                            - 'all'
                                            - 'any'
    schedule_info:
        description:
            - Schedule information for the Software update configuration
            - Required when C(state) is I(present).
        suboptions:
            start_time:
                description:
                    - Gets or sets the start time of the schedule.
            expiry_time:
                description:
                    - Gets or sets the end time of the schedule.
            expiry_time_offset_minutes:
                description:
                    - "Gets or sets the expiry time's offset in minutes."
            is_enabled:
                description:
                    - Gets or sets a value indicating whether this schedule is enabled.
            next_run:
                description:
                    - Gets or sets the next run time of the schedule.
            next_run_offset_minutes:
                description:
                    - "Gets or sets the next run time's offset in minutes."
            interval:
                description:
                    - Gets or sets the interval of the schedule.
            frequency:
                description:
                    - Gets or sets the frequency of the schedule.
                choices:
                    - 'one_time'
                    - 'day'
                    - 'hour'
                    - 'week'
                    - 'month'
            time_zone:
                description:
                    - Gets or sets the time zone of the schedule.
            advanced_schedule:
                description:
                    - Gets or sets the advanced schedule.
                suboptions:
                    week_days:
                        description:
                            - Days of the week that the job should execute on.
                        type: list
                    month_days:
                        description:
                            - Days of the month that the job should execute on. Must be between 1 and 31.
                        type: list
                    monthly_occurrences:
                        description:
                            - Occurrences of days within a month.
                        type: list
                        suboptions:
                            occurrence:
                                description:
                                    - Occurrence of the week within the month. Must be between 1 and 5
                            day:
                                description:
                                    - "Day of the I(occurrence). Must be one of C(monday), C(tuesday), C(wednesday), C(thursday), C(friday), C(saturday),
                                       C(sunday)."
                                choices:
                                    - 'monday'
                                    - 'tuesday'
                                    - 'wednesday'
                                    - 'thursday'
                                    - 'friday'
                                    - 'saturday'
                                    - 'sunday'
            creation_time:
                description:
                    - Gets or sets the creation time.
            last_modified_time:
                description:
                    - Gets or sets the last modified time.
            description:
                description:
                    - Gets or sets the description.
    error:
        description:
            - Details of provisioning error
        suboptions:
            code:
                description:
                    - Error code
            message:
                description:
                    - Error message indicating why the operation failed.
    tasks:
        description:
            - Tasks information for the Software update configuration.
        suboptions:
            pre_task:
                description:
                    - Pre task properties.
                suboptions:
                    parameters:
                        description:
                            - Gets or sets the parameters of the task.
                    source:
                        description:
                            - Gets or sets the name of the runbook.
            post_task:
                description:
                    - Post task properties.
                suboptions:
                    parameters:
                        description:
                            - Gets or sets the parameters of the task.
                    source:
                        description:
                            - Gets or sets the name of the runbook.
    state:
      description:
        - Assert the state of the Software Update Configuration.
        - Use 'present' to create or update an Software Update Configuration and 'absent' to delete it.
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
  - name: Create (or update) Software Update Configuration
    azure_rm_automationsoftwareupdateconfiguration:
      resource_group: mygroup
      automation_account_name: myaccount
      name: testpatch
      client_request_id: NOT FOUND
      update_configuration:
        operating_system: Windows
        windows:
          included_update_classifications: Critical
          excluded_kb_numbers:
            - [
  "168934",
  "168973"
]
          reboot_setting: IfRequired
        duration: PT2H0M
        azure_virtual_machines:
          - [
  "/subscriptions/5ae68d89-69a4-454f-b5ce-e443cc4e0067/resourceGroups/myresources/providers/Microsoft.Compute/virtualMachines/vm-01",
  "/subscriptions/5ae68d89-69a4-454f-b5ce-e443cc4e0067/resourceGroups/myresources/providers/Microsoft.Compute/virtualMachines/vm-02",
  "/subscriptions/5ae68d89-69a4-454f-b5ce-e443cc4e0067/resourceGroups/myresources/providers/Microsoft.Compute/virtualMachines/vm-03"
]
        non_azure_computer_names:
          - [
  "box1.contoso.com",
  "box2.contoso.com"
]
        targets:
          azure_queries:
            - scope:
                - [
  "/subscriptions/5ae68d89-69a4-454f-b5ce-e443cc4e0067/resourceGroups/myresources",
  "/subscriptions/5ae68d89-69a4-454f-b5ce-e443cc4e0067"
]
              locations:
                - [
  "Japan East",
  "UK South"
]
              tag_settings:
                filter_operator: All
      schedule_info:
        start_time: 2017-10-19T12:22:57+00:00
        expiry_time: 2018-11-09T11:22:57+00:00
        interval: 1
        frequency: Hour
        time_zone: America/Los_Angeles
        advanced_schedule:
          week_days:
            - [
  "Monday",
  "Thursday"
]
      tasks:
        pre_task:
          parameters: {
  "COMPUTERNAME": "Computer1"
}
          source: HelloWorld
        post_task:
          source: GetCache
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: "/subscriptions/51766542-3ed7-4a72-a187-0c8ab644ddab/resourceGroups/mygroup/providers/Microsoft.Automation/automationAccounts/myaccount/softwareU
            pdateConfigurations/testpatch"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSoftwareUpdateConfiguration(AzureRMModuleBase):
    """Configuration class for an Azure RM Software Update Configuration resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            client_request_id=dict(
                type='str'
            ),
            update_configuration=dict(
                type='dict',
                options=dict(
                    operating_system=dict(
                        type='str',
                        choices=['windows',
                                 'linux']
                    ),
                    windows=dict(
                        type='dict',
                        options=dict(
                            included_update_classifications=dict(
                                type='str',
                                choices=['unclassified',
                                         'critical',
                                         'security',
                                         'update_rollup',
                                         'feature_pack',
                                         'service_pack',
                                         'definition',
                                         'tools',
                                         'updates']
                            ),
                            excluded_kb_numbers=dict(
                                type='list'
                            ),
                            included_kb_numbers=dict(
                                type='list'
                            ),
                            reboot_setting=dict(
                                type='str'
                            )
                        )
                    ),
                    linux=dict(
                        type='dict',
                        options=dict(
                            included_package_classifications=dict(
                                type='str',
                                choices=['unclassified',
                                         'critical',
                                         'security',
                                         'other']
                            ),
                            excluded_package_name_masks=dict(
                                type='list'
                            ),
                            included_package_name_masks=dict(
                                type='list'
                            ),
                            reboot_setting=dict(
                                type='str'
                            )
                        )
                    ),
                    duration=dict(
                        type='str'
                    ),
                    azure_virtual_machines=dict(
                        type='list'
                    ),
                    non_azure_computer_names=dict(
                        type='list'
                    ),
                    targets=dict(
                        type='dict',
                        options=dict(
                            azure_queries=dict(
                                type='list',
                                options=dict(
                                    scope=dict(
                                        type='list'
                                    ),
                                    locations=dict(
                                        type='list'
                                    ),
                                    tag_settings=dict(
                                        type='dict',
                                        options=dict(
                                            filter_operator=dict(
                                                type='str',
                                                choices=['all',
                                                         'any']
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            schedule_info=dict(
                type='dict',
                options=dict(
                    start_time=dict(
                        type='datetime'
                    ),
                    expiry_time=dict(
                        type='datetime'
                    ),
                    expiry_time_offset_minutes=dict(
                        type='float'
                    ),
                    is_enabled=dict(
                        type='str'
                    ),
                    next_run=dict(
                        type='datetime'
                    ),
                    next_run_offset_minutes=dict(
                        type='float'
                    ),
                    interval=dict(
                        type='int'
                    ),
                    frequency=dict(
                        type='str',
                        choices=['one_time',
                                 'day',
                                 'hour',
                                 'week',
                                 'month']
                    ),
                    time_zone=dict(
                        type='str'
                    ),
                    advanced_schedule=dict(
                        type='dict',
                        options=dict(
                            week_days=dict(
                                type='list'
                            ),
                            month_days=dict(
                                type='list'
                            ),
                            monthly_occurrences=dict(
                                type='list',
                                options=dict(
                                    occurrence=dict(
                                        type='int'
                                    ),
                                    day=dict(
                                        type='str',
                                        choices=['monday',
                                                 'tuesday',
                                                 'wednesday',
                                                 'thursday',
                                                 'friday',
                                                 'saturday',
                                                 'sunday']
                                    )
                                )
                            )
                        )
                    ),
                    creation_time=dict(
                        type='datetime'
                    ),
                    last_modified_time=dict(
                        type='datetime'
                    ),
                    description=dict(
                        type='str'
                    )
                )
            ),
            error=dict(
                type='dict',
                options=dict(
                    code=dict(
                        type='str'
                    ),
                    message=dict(
                        type='str'
                    )
                )
            ),
            tasks=dict(
                type='dict',
                options=dict(
                    pre_task=dict(
                        type='dict',
                        options=dict(
                            parameters=dict(
                                type='dict'
                            ),
                            source=dict(
                                type='str'
                            )
                        )
                    ),
                    post_task=dict(
                        type='dict',
                        options=dict(
                            parameters=dict(
                                type='dict'
                            ),
                            source=dict(
                                type='str'
                            )
                        )
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
        self.automation_account_name = None
        self.name = None
        self.client_request_id = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSoftwareUpdateConfiguration, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                   supports_check_mode=True,
                                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['update_configuration', 'operating_system'], True)
        dict_camelize(self.parameters, ['update_configuration', 'windows', 'included_update_classifications'], True)
        dict_camelize(self.parameters, ['update_configuration', 'linux', 'included_package_classifications'], True)
        dict_camelize(self.parameters, ['update_configuration', 'targets', 'azure_queries', 'tag_settings', 'filter_operator'], True)
        dict_camelize(self.parameters, ['schedule_info', 'frequency'], True)
        dict_camelize(self.parameters, ['schedule_info', 'advanced_schedule', 'monthly_occurrences', 'day'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_softwareupdateconfiguration()

        if not old_response:
            self.log("Software Update Configuration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Software Update Configuration instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Software Update Configuration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_softwareupdateconfiguration()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Software Update Configuration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_softwareupdateconfiguration()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Software Update Configuration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_softwareupdateconfiguration(self):
        '''
        Creates or updates Software Update Configuration with the specified configuration.

        :return: deserialized Software Update Configuration instance state dictionary
        '''
        self.log("Creating / Updating the Software Update Configuration instance {0}".format(self.client_request_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.software_update_configurations.create(resource_group_name=self.resource_group,
                                                                                  automation_account_name=self.automation_account_name,
                                                                                  software_update_configuration_name=self.name,
                                                                                  parameters=self.parameters)
            else:
                response = self.mgmt_client.software_update_configurations.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Software Update Configuration instance.')
            self.fail("Error creating the Software Update Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_softwareupdateconfiguration(self):
        '''
        Deletes specified Software Update Configuration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Software Update Configuration instance {0}".format(self.client_request_id))
        try:
            response = self.mgmt_client.software_update_configurations.delete(resource_group_name=self.resource_group,
                                                                              automation_account_name=self.automation_account_name,
                                                                              software_update_configuration_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Software Update Configuration instance.')
            self.fail("Error deleting the Software Update Configuration instance: {0}".format(str(e)))

        return True

    def get_softwareupdateconfiguration(self):
        '''
        Gets the properties of the specified Software Update Configuration.

        :return: deserialized Software Update Configuration instance state dictionary
        '''
        self.log("Checking if the Software Update Configuration instance {0} is present".format(self.client_request_id))
        found = False
        try:
            response = self.mgmt_client.software_update_configurations.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Software Update Configuration instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Software Update Configuration instance.')
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
    AzureRMSoftwareUpdateConfiguration()


if __name__ == '__main__':
    main()

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
module: azure_rm_logicintegrationaccountbatchconfiguration
version_added: "2.8"
short_description: Manage Integration Account Batch Configuration instance.
description:
    - Create, update and delete instance of Integration Account Batch Configuration.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    name:
        description:
            - The batch configuration name.
        required: True
    batch_configuration:
        description:
            - The batch configuration.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            created_time:
                description:
                    - The artifact creation time.
            changed_time:
                description:
                    - The artifact changed time.
            metadata:
                description:
            batch_group_name:
                description:
                    - The name of the batch group.
                    - Required when C(state) is I(present).
            release_criteria:
                description:
                    - The batch release criteria.
                    - Required when C(state) is I(present).
                suboptions:
                    message_count:
                        description:
                            - The message count.
                    batch_size:
                        description:
                            - The batch size in bytes.
                    recurrence:
                        description:
                            - The recurrence.
                        suboptions:
                            frequency:
                                description:
                                    - The frequency.
                                choices:
                                    - 'not_specified'
                                    - 'second'
                                    - 'minute'
                                    - 'hour'
                                    - 'day'
                                    - 'week'
                                    - 'month'
                                    - 'year'
                            interval:
                                description:
                                    - The interval.
                            start_time:
                                description:
                                    - The start time.
                            end_time:
                                description:
                                    - The end time.
                            time_zone:
                                description:
                                    - The time zone.
                            schedule:
                                description:
                                    - The recurrence schedule.
                                suboptions:
                                    minutes:
                                        description:
                                            - The minutes.
                                        type: list
                                    hours:
                                        description:
                                            - The hours.
                                        type: list
                                    week_days:
                                        description:
                                            - The days of the week.
                                        type: list
                                    month_days:
                                        description:
                                            - The month days.
                                        type: list
                                    monthly_occurrences:
                                        description:
                                            - The monthly occurrences.
                                        type: list
    state:
      description:
        - Assert the state of the Integration Account Batch Configuration.
        - Use 'present' to create or update an Integration Account Batch Configuration and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Batch Configuration
    azure_rm_logicintegrationaccountbatchconfiguration:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      name: testBatchConfiguration
      batch_configuration:
        location: westus
        batch_group_name: DEFAULT
        release_criteria:
          message_count: 10
          batch_size: 234567
          recurrence:
            frequency: Minute
            interval: 1
            start_time: 2017-03-24T11:43:00
            time_zone: India Standard Time
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/testIntegrati
            onAccount/batchConfigurations/testBatchConfiguration"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIntegrationAccountBatchConfigurations(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Batch Configuration resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            integration_account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            batch_configuration=dict(
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
        self.integration_account_name = None
        self.name = None
        self.batch_configuration = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountBatchConfigurations, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                           supports_check_mode=True,
                                                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.batch_configuration["location"] = kwargs[key]
                elif key == "created_time":
                    self.batch_configuration.setdefault("properties", {})["created_time"] = kwargs[key]
                elif key == "changed_time":
                    self.batch_configuration.setdefault("properties", {})["changed_time"] = kwargs[key]
                elif key == "metadata":
                    self.batch_configuration.setdefault("properties", {})["metadata"] = kwargs[key]
                elif key == "batch_group_name":
                    self.batch_configuration.setdefault("properties", {})["batch_group_name"] = kwargs[key]
                elif key == "release_criteria":
                    self.batch_configuration.setdefault("properties", {})["release_criteria"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountbatchconfiguration()

        if not old_response:
            self.log("Integration Account Batch Configuration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Batch Configuration instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Batch Configuration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountbatchconfiguration()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Batch Configuration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountbatchconfiguration()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccountbatchconfiguration():
                time.sleep(20)
        else:
            self.log("Integration Account Batch Configuration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccountbatchconfiguration(self):
        '''
        Creates or updates Integration Account Batch Configuration with the specified configuration.

        :return: deserialized Integration Account Batch Configuration instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Batch Configuration instance {0}".format(self.name))

        try:
            response = self.mgmt_client.integration_account_batch_configurations.create_or_update(resource_group_name=self.resource_group,
                                                                                                  integration_account_name=self.integration_account_name,
                                                                                                  batch_configuration_name=self.name,
                                                                                                  batch_configuration=self.batch_configuration)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Batch Configuration instance.')
            self.fail("Error creating the Integration Account Batch Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountbatchconfiguration(self):
        '''
        Deletes specified Integration Account Batch Configuration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Batch Configuration instance {0}".format(self.name))
        try:
            response = self.mgmt_client.integration_account_batch_configurations.delete(resource_group_name=self.resource_group,
                                                                                        integration_account_name=self.integration_account_name,
                                                                                        batch_configuration_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Batch Configuration instance.')
            self.fail("Error deleting the Integration Account Batch Configuration instance: {0}".format(str(e)))

        return True

    def get_integrationaccountbatchconfiguration(self):
        '''
        Gets the properties of the specified Integration Account Batch Configuration.

        :return: deserialized Integration Account Batch Configuration instance state dictionary
        '''
        self.log("Checking if the Integration Account Batch Configuration instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.integration_account_batch_configurations.get(resource_group_name=self.resource_group,
                                                                                     integration_account_name=self.integration_account_name,
                                                                                     batch_configuration_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Batch Configuration instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Batch Configuration instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def main():
    """Main execution"""
    AzureRMIntegrationAccountBatchConfigurations()


if __name__ == '__main__':
    main()

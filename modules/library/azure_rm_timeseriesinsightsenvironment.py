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
module: azure_rm_timeseriesinsightsenvironment
version_added: "2.8"
short_description: Manage Environment instance.
description:
    - Create, update and delete instance of Environment.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    environment_name:
        description:
            - Name of the environment
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The sku determines the capacity of the environment, the SLA (in queries-per-minute and total capacity), and the billing rate.
        required: True
        suboptions:
            name:
                description:
                    - The name of this SKU.
                required: True
                choices:
                    - 's1'
                    - 's2'
            capacity:
                description:
                    - The capacity of the sku. This value can be changed to support scale out of environments after they have been created.
                required: True
    data_retention_time:
        description:
            - "ISO8601 timespan specifying the minimum number of days the environment's events will be available for query."
        required: True
    storage_limit_exceeded_behavior:
        description:
            - "The behavior the Time Series Insights service should take when the environment's capacity has been exceeded. If 'C(pause_ingress)' is
               specified, new events will not be read from the event source. If 'C(purge_old_data)' is specified, new events will continue to be read and
               old events will be deleted from the environment. The default behavior is C(purge_old_data)."
        choices:
            - 'purge_old_data'
            - 'pause_ingress'
    partition_key_properties:
        description:
            - The list of partition keys according to which the data in the environment will be ordered.
        type: list
        suboptions:
            name:
                description:
                    - The name of the property.
            type:
                description:
                    - The type of the property.
                choices:
                    - 'string'
    state:
      description:
        - Assert the state of the Environment.
        - Use 'present' to create or update an Environment and 'absent' to delete it.
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
  - name: Create (or update) Environment
    azure_rm_timeseriesinsightsenvironment:
      resource_group: rg1
      environment_name: env1
      location: eastus
      sku:
        name: S1
        capacity: 1
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.TimeSeriesInsights/Environments/env1
status:
    description:
        - An object that represents the status of the environment, and its internal state in the Time Series Insights service.
    returned: always
    type: complex
    sample: status
    contains:
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


class AzureRMEnvironments(AzureRMModuleBase):
    """Configuration class for an Azure RM Environment resource"""

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
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                required=True
            ),
            data_retention_time=dict(
                type='str',
                required=True
            ),
            storage_limit_exceeded_behavior=dict(
                type='str',
                choices=['purge_old_data',
                         'pause_ingress']
            ),
            partition_key_properties=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.environment_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEnvironments, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 's1':
                            ev['name'] = 'S1'
                        elif ev['name'] == 's2':
                            ev['name'] = 'S2'
                    self.parameters["sku"] = ev
                elif key == "data_retention_time":
                    self.parameters["data_retention_time"] = kwargs[key]
                elif key == "storage_limit_exceeded_behavior":
                    self.parameters["storage_limit_exceeded_behavior"] = _snake_to_camel(kwargs[key], True)
                elif key == "partition_key_properties":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'string':
                            ev['type'] = 'String'
                    self.parameters["partition_key_properties"] = ev

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(TimeSeriesInsightsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_environment()

        if not old_response:
            self.log("Environment instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Environment instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Environment instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Environment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_environment()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Environment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_environment()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_environment():
                time.sleep(20)
        else:
            self.log("Environment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_environment(self):
        '''
        Creates or updates Environment with the specified configuration.

        :return: deserialized Environment instance state dictionary
        '''
        self.log("Creating / Updating the Environment instance {0}".format(self.environment_name))

        try:
            response = self.mgmt_client.environments.create_or_update(resource_group_name=self.resource_group,
                                                                      environment_name=self.environment_name,
                                                                      parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Environment instance.')
            self.fail("Error creating the Environment instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_environment(self):
        '''
        Deletes specified Environment instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Environment instance {0}".format(self.environment_name))
        try:
            response = self.mgmt_client.environments.delete(resource_group_name=self.resource_group,
                                                            environment_name=self.environment_name)
        except CloudError as e:
            self.log('Error attempting to delete the Environment instance.')
            self.fail("Error deleting the Environment instance: {0}".format(str(e)))

        return True

    def get_environment(self):
        '''
        Gets the properties of the specified Environment.

        :return: deserialized Environment instance state dictionary
        '''
        self.log("Checking if the Environment instance {0} is present".format(self.environment_name))
        found = False
        try:
            response = self.mgmt_client.environments.get(resource_group_name=self.resource_group,
                                                         environment_name=self.environment_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Environment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Environment instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': {
            }
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMEnvironments()


if __name__ == '__main__':
    main()

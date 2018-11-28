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
short_description: Manage Azure Environment instance.
description:
    - Create, update and delete instance of Azure Environment.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    name:
        description:
            - Name of the environment
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The sku determines the capacity of the environment, the SLA (in queries-per-minute and total capacity), and the billing rate.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - The name of this SKU.
                    - Required when C(state) is I(present).
                choices:
                    - 's1'
                    - 's2'
            capacity:
                description:
                    - The capacity of the sku. This value can be changed to support scale out of environments after they have been created.
                    - Required when C(state) is I(present).
    data_retention_time:
        description:
            - "ISO8601 timespan specifying the minimum number of days the environment's events will be available for query."
            - Required when C(state) is I(present).
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
      name: env1
      location: eastus
      sku:
        name: S1
        capacity: 1
      data_retention_time: P31D
      partition_key_properties:
        - name: DeviceId1
          type: String
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMEnvironment(AzureRMModuleBase):
    """Configuration class for an Azure RM Environment resource"""

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
            sku=dict(
                type='dict'
                options=dict(
                    name=dict(
                        type='str',
                        choices=['s1',
                                 's2']
                    ),
                    capacity=dict(
                        type='int'
                    )
                )
            ),
            data_retention_time=dict(
                type='str'
            ),
            storage_limit_exceeded_behavior=dict(
                type='str',
                choices=['purge_old_data',
                         'pause_ingress']
            ),
            partition_key_properties=dict(
                type='list'
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    type=dict(
                        type='str',
                        choices=['string']
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

        super(AzureRMEnvironment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_camelize(self.parameters, ['storage_limit_exceeded_behavior'], True)
        dict_camelize(self.parameters, ['partition_key_properties', 'type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Environment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_environment()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Environment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_environment()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Environment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': {
                }
                })
        return self.results

    def create_update_environment(self):
        '''
        Creates or updates Environment with the specified configuration.

        :return: deserialized Environment instance state dictionary
        '''
        self.log("Creating / Updating the Environment instance {0}".format(self.name))

        try:
            response = self.mgmt_client.environments.create_or_update(resource_group_name=self.resource_group,
                                                                      environment_name=self.name,
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
        self.log("Deleting the Environment instance {0}".format(self.name))
        try:
            response = self.mgmt_client.environments.delete(resource_group_name=self.resource_group,
                                                            environment_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Environment instance.')
            self.fail("Error deleting the Environment instance: {0}".format(str(e)))

        return True

    def get_environment(self):
        '''
        Gets the properties of the specified Environment.

        :return: deserialized Environment instance state dictionary
        '''
        self.log("Checking if the Environment instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.environments.get(resource_group_name=self.resource_group,
                                                         environment_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Environment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Environment instance.')
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
    AzureRMEnvironment()


if __name__ == '__main__':
    main()

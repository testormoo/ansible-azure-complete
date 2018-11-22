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
module: azure_rm_monitormetricalert
version_added: "2.8"
short_description: Manage Azure Metric Alert instance.
description:
    - Create, update and delete instance of Azure Metric Alert.

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
            - the description of the metric alert that will be included in the alert email.
            - Required when C(state) is I(present).
    severity:
        description:
            - Alert severity {0, 1, 2, 3, 4}
            - Required when C(state) is I(present).
    enabled:
        description:
            - the flag that indicates whether the metric alert is enabled.
            - Required when C(state) is I(present).
    scopes:
        description:
            - "the list of resource id's that this metric alert is scoped to."
        type: list
    evaluation_frequency:
        description:
            - how often the metric alert is evaluated represented in ISO 8601 duration format.
            - Required when C(state) is I(present).
    window_size:
        description:
            - the period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold.
            - Required when C(state) is I(present).
    target_resource_type:
        description:
            - the resource type of the target resource(s) on which the alert is created/updated. Mandatory for MultipleResourceMultipleMetricCriteria.
    target_resource_region:
        description:
            - the region of the target resource(s) on which the alert is created/updated. Mandatory for MultipleResourceMultipleMetricCriteria.
    criteria:
        description:
            - defines the specific alert criteria information.
            - Required when C(state) is I(present).
        suboptions:
            additional_properties:
                description:
                    - Unmatched properties from the message are deserialized this collection
            odatatype:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    auto_mitigate:
        description:
            - the flag that indicates whether the alert should be auto resolved or not.
    actions:
        description:
            - the array of actions that are performed when the alert rule becomes active, and when an alert condition is resolved.
        type: list
        suboptions:
            action_group_id:
                description:
                    - the id of the action group to use.
            webhook_properties:
                description:
                    - The properties of a webhook object.
    state:
      description:
        - Assert the state of the Metric Alert.
        - Use 'present' to create or update an Metric Alert and 'absent' to delete it.
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
  - name: Create (or update) Metric Alert
    azure_rm_monitormetricalert:
      resource_group: gigtest
      name: chiricutin
      location: eastus
      description: This is the description of the rule1
      severity: 3
      enabled: True
      scopes:
        - [
  "/subscriptions/14ddf0c5-77c5-4b53-84f6-e1fa43ad68f7/resourceGroups/gigtest/providers/Microsoft.Compute/virtualMachines/gigwadme"
]
      evaluation_frequency: Pt1m
      window_size: Pt15m
      auto_mitigate: False
      actions:
        - action_group_id: /subscriptions/14ddf0c5-77c5-4b53-84f6-e1fa43ad68f7/resourcegroups/gigtest/providers/microsoft.insights/notificationgroups/group2
          webhook_properties: {
  "key11": "value11",
  "key12": "value12"
}
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: /subscriptions/14ddf0c5-77c5-4b53-84f6-e1fa43ad68f7/resourceGroups/gigtest/providers/providers/microsoft.insights/metricalerts/chiricutin
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


class AzureRMMetricAlert(AzureRMModuleBase):
    """Configuration class for an Azure RM Metric Alert resource"""

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
            severity=dict(
                type='int'
            ),
            enabled=dict(
                type='str'
            ),
            scopes=dict(
                type='list'
            ),
            evaluation_frequency=dict(
                type='str'
            ),
            window_size=dict(
                type='str'
            ),
            target_resource_type=dict(
                type='str'
            ),
            target_resource_region=dict(
                type='str'
            ),
            criteria=dict(
                type='dict'
            ),
            auto_mitigate=dict(
                type='str'
            ),
            actions=dict(
                type='list'
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

        super(AzureRMMetricAlert, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_metricalert()

        if not old_response:
            self.log("Metric Alert instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Metric Alert instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Metric Alert instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_metricalert()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Metric Alert instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_metricalert()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_metricalert():
                time.sleep(20)
        else:
            self.log("Metric Alert instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_metricalert(self):
        '''
        Creates or updates Metric Alert with the specified configuration.

        :return: deserialized Metric Alert instance state dictionary
        '''
        self.log("Creating / Updating the Metric Alert instance {0}".format(self.name))

        try:
            response = self.mgmt_client.metric_alerts.create_or_update(resource_group_name=self.resource_group,
                                                                       rule_name=self.name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Metric Alert instance.')
            self.fail("Error creating the Metric Alert instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_metricalert(self):
        '''
        Deletes specified Metric Alert instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Metric Alert instance {0}".format(self.name))
        try:
            response = self.mgmt_client.metric_alerts.delete(resource_group_name=self.resource_group,
                                                             rule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Metric Alert instance.')
            self.fail("Error deleting the Metric Alert instance: {0}".format(str(e)))

        return True

    def get_metricalert(self):
        '''
        Gets the properties of the specified Metric Alert.

        :return: deserialized Metric Alert instance state dictionary
        '''
        self.log("Checking if the Metric Alert instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.metric_alerts.get(resource_group_name=self.resource_group,
                                                          rule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Metric Alert instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Metric Alert instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMMetricAlert()


if __name__ == '__main__':
    main()

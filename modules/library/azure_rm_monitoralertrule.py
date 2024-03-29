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
module: azure_rm_monitoralertrule
version_added: "2.8"
short_description: Manage Azure Alert Rule instance.
description:
    - Create, update and delete instance of Azure Alert Rule.

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
    alert_rule_resource_name:
        description:
            - the name of the alert rule.
            - Required when C(state) is I(present).
    description:
        description:
            - the description of the alert rule that will be included in the alert email.
    is_enabled:
        description:
            - the flag that indicates whether the alert rule is enabled.
            - Required when C(state) is I(present).
    condition:
        description:
            - the condition that results in the alert rule being activated.
            - Required when C(state) is I(present).
        suboptions:
            data_source:
                description:
                    - the resource from which the rule collects its data. For this type dataSource will always be of type RuleMetricDataSource.
                suboptions:
                    resource_uri:
                        description:
                            - "the resource identifier of the resource the rule monitors. **NOTE**: this property cannot be updated for an existing rule."
                    odatatype:
                        description:
                            - Constant filled by server.
                            - Required when C(state) is I(present).
            odatatype:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    actions:
        description:
            - the array of actions that are performed when the alert rule becomes active, and when an alert I(condition) is resolved.
        type: list
        suboptions:
            odatatype:
                description:
                    - Constant filled by server.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Alert Rule.
        - Use 'present' to create or update an Alert Rule and 'absent' to delete it.
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
  - name: Create (or update) Alert Rule
    azure_rm_monitoralertrule:
      resource_group: Rac46PostSwapRG
      name: chiricutin
      location: eastus
      alert_rule_resource_name: chiricutin
      description: Pura Vida
      is_enabled: True
      condition:
        data_source:
          resource_uri: /subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/Rac46PostSwapRG/providers/Microsoft.Web/sites/leoalerttest
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: /subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/Rac46PostSwapRG/providers/microsoft.insights/alertrules/chiricutin
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


class AzureRMAlertRule(AzureRMModuleBase):
    """Configuration class for an Azure RM Alert Rule resource"""

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
            alert_rule_resource_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            is_enabled=dict(
                type='str'
            ),
            condition=dict(
                type='dict',
                options=dict(
                    data_source=dict(
                        type='dict',
                        options=dict(
                            resource_uri=dict(
                                type='str'
                            ),
                            odatatype=dict(
                                type='str'
                            )
                        )
                    ),
                    odatatype=dict(
                        type='str'
                    )
                )
            ),
            actions=dict(
                type='list',
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

        super(AzureRMAlertRule, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        old_response = self.get_alertrule()

        if not old_response:
            self.log("Alert Rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Alert Rule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Alert Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_alertrule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Alert Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_alertrule()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Alert Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_alertrule(self):
        '''
        Creates or updates Alert Rule with the specified configuration.

        :return: deserialized Alert Rule instance state dictionary
        '''
        self.log("Creating / Updating the Alert Rule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.alert_rules.create_or_update(resource_group_name=self.resource_group,
                                                                     rule_name=self.name,
                                                                     parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Alert Rule instance.')
            self.fail("Error creating the Alert Rule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_alertrule(self):
        '''
        Deletes specified Alert Rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Alert Rule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.alert_rules.delete(resource_group_name=self.resource_group,
                                                           rule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Alert Rule instance.')
            self.fail("Error deleting the Alert Rule instance: {0}".format(str(e)))

        return True

    def get_alertrule(self):
        '''
        Gets the properties of the specified Alert Rule.

        :return: deserialized Alert Rule instance state dictionary
        '''
        self.log("Checking if the Alert Rule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.alert_rules.get(resource_group_name=self.resource_group,
                                                        rule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Alert Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Alert Rule instance.')
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


def main():
    """Main execution"""
    AzureRMAlertRule()


if __name__ == '__main__':
    main()

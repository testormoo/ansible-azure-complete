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
module: azure_rm_frontdoorpolicy
version_added: "2.8"
short_description: Manage Azure Policy instance.
description:
    - Create, update and delete instance of Azure Policy.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the resource group.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    policy_settings:
        description:
            - Describes  policySettings for policy
        suboptions:
            enabled_state:
                description:
                    - "describes if the policy is in enabled state or disabled state. Possible values include: 'Disabled', 'Enabled'"
                type: bool
            mode:
                description:
                    - Describes if it is in C(detection) mode  or C(prevention) mode at policy level.
                choices:
                    - 'prevention'
                    - 'detection'
    custom_rules:
        description:
            - Describes custom rules inside the policy
        suboptions:
            rules:
                description:
                    - List of rules
                type: list
                suboptions:
                    name:
                        description:
                            - Gets name of the resource that is unique within a policy. This name can be used to access the resource.
                    priority:
                        description:
                            - Describes priority of the rule. Rules with a lower value will be evaluated before rules with a higher value
                            - Required when C(state) is I(present).
                    rule_type:
                        description:
                            - Describes type of rule.
                            - Required when C(state) is I(present).
                        choices:
                            - 'match_rule'
                            - 'rate_limit_rule'
                    rate_limit_duration_in_minutes:
                        description:
                            - Defines rate limit duration. Default - 1 minute
                    rate_limit_threshold:
                        description:
                            - Defines rate limit thresold
                    match_conditions:
                        description:
                            - List of match conditions
                            - Required when C(state) is I(present).
                        type: list
                        suboptions:
                            match_variable:
                                description:
                                    - Match Variable.
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'remote_addr'
                                    - 'request_method'
                                    - 'query_string'
                                    - 'post_args'
                                    - 'request_uri'
                                    - 'request_header'
                                    - 'request_body'
                            selector:
                                description:
                                    - Name of selector in C(request_header) or C(request_body) to be matched
                            operator:
                                description:
                                    - Describes operator to be matched.
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'any'
                                    - 'ip_match'
                                    - 'geo_match'
                                    - 'equal'
                                    - 'contains'
                                    - 'less_than'
                                    - 'greater_than'
                                    - 'less_than_or_equal'
                                    - 'greater_than_or_equal'
                                    - 'begins_with'
                                    - 'ends_with'
                            negate_condition:
                                description:
                                    - Describes if this is negate condition or not
                            match_value:
                                description:
                                    - Match value
                                    - Required when C(state) is I(present).
                                type: list
                    action:
                        description:
                            - Type of Actions.
                            - Required when C(state) is I(present).
                        choices:
                            - 'allow'
                            - 'block'
                            - 'log'
                    transforms:
                        description:
                            - List of transforms
                        type: list
    managed_rules:
        description:
            - Describes managed rules inside the policy
        suboptions:
            rule_sets:
                description:
                    - List of rules
                type: list
                suboptions:
                    priority:
                        description:
                            - Describes priority of the rule
                    version:
                        description:
                            - defines version of the ruleset
                    rule_set_type:
                        description:
                            - Constant filled by server.
                            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Policy.
        - Use 'present' to create or update an Policy and 'absent' to delete it.
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
  - name: Create (or update) Policy
    azure_rm_frontdoorpolicy:
      resource_group: rg1
      name: Policy1
      location: eastus
      policy_settings:
        enabled_state: enabled_state
      custom_rules:
        rules:
          - name: Rule1
            priority: 1
            rule_type: RateLimitRule
            rate_limit_threshold: 1000
            match_conditions:
              - match_variable: RemoteAddr
                operator: IPMatch
                match_value:
                  - [
  "192.168.1.0/24",
  "10.0.0.0/24"
]
            action: Block
      managed_rules:
        rule_sets:
          - priority: 1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/FrontDoorWebApplicationFirewallPolicies/Policy1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.frontdoor import FrontDoorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPolicy(AzureRMModuleBase):
    """Configuration class for an Azure RM Policy resource"""

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
            policy_settings=dict(
                type='dict',
                options=dict(
                    enabled_state=dict(
                        type='bool'
                    ),
                    mode=dict(
                        type='str',
                        choices=['prevention',
                                 'detection']
                    )
                )
            ),
            custom_rules=dict(
                type='dict',
                options=dict(
                    rules=dict(
                        type='list',
                        options=dict(
                            name=dict(
                                type='str'
                            ),
                            priority=dict(
                                type='int'
                            ),
                            rule_type=dict(
                                type='str',
                                choices=['match_rule',
                                         'rate_limit_rule']
                            ),
                            rate_limit_duration_in_minutes=dict(
                                type='int'
                            ),
                            rate_limit_threshold=dict(
                                type='int'
                            ),
                            match_conditions=dict(
                                type='list',
                                options=dict(
                                    match_variable=dict(
                                        type='str',
                                        choices=['remote_addr',
                                                 'request_method',
                                                 'query_string',
                                                 'post_args',
                                                 'request_uri',
                                                 'request_header',
                                                 'request_body']
                                    ),
                                    selector=dict(
                                        type='str'
                                    ),
                                    operator=dict(
                                        type='str',
                                        choices=['any',
                                                 'ip_match',
                                                 'geo_match',
                                                 'equal',
                                                 'contains',
                                                 'less_than',
                                                 'greater_than',
                                                 'less_than_or_equal',
                                                 'greater_than_or_equal',
                                                 'begins_with',
                                                 'ends_with']
                                    ),
                                    negate_condition=dict(
                                        type='str'
                                    ),
                                    match_value=dict(
                                        type='list'
                                    )
                                )
                            ),
                            action=dict(
                                type='str',
                                choices=['allow',
                                         'block',
                                         'log']
                            ),
                            transforms=dict(
                                type='list'
                            )
                        )
                    )
                )
            ),
            managed_rules=dict(
                type='dict',
                options=dict(
                    rule_sets=dict(
                        type='list',
                        options=dict(
                            priority=dict(
                                type='int'
                            ),
                            version=dict(
                                type='int'
                            ),
                            rule_set_type=dict(
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_map(self.parameters, ['policy_settings', 'enabled_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.parameters, ['policy_settings', 'mode'], True)
        dict_camelize(self.parameters, ['custom_rules', 'rules', 'rule_type'], True)
        dict_camelize(self.parameters, ['custom_rules', 'rules', 'match_conditions', 'match_variable'], True)
        dict_camelize(self.parameters, ['custom_rules', 'rules', 'match_conditions', 'operator'], True)
        dict_map(self.parameters, ['custom_rules', 'rules', 'match_conditions', 'operator'], {'ip_match': 'IPMatch'})
        dict_camelize(self.parameters, ['custom_rules', 'rules', 'action'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_policy()

        if not old_response:
            self.log("Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_policy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_policy()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_policy(self):
        '''
        Creates or updates Policy with the specified configuration.

        :return: deserialized Policy instance state dictionary
        '''
        self.log("Creating / Updating the Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.policies.create_or_update(resource_group_name=self.resource_group,
                                                                  policy_name=self.name,
                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Policy instance.')
            self.fail("Error creating the Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_policy(self):
        '''
        Deletes specified Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.policies.delete(resource_group_name=self.resource_group,
                                                        policy_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Policy instance.')
            self.fail("Error deleting the Policy instance: {0}".format(str(e)))

        return True

    def get_policy(self):
        '''
        Gets the properties of the specified Policy.

        :return: deserialized Policy instance state dictionary
        '''
        self.log("Checking if the Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.policies.get(resource_group_name=self.resource_group,
                                                     policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Policy instance.')
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


def main():
    """Main execution"""
    AzureRMPolicy()


if __name__ == '__main__':
    main()

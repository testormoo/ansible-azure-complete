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
module: azure_rm_servicebusrule
version_added: "2.8"
short_description: Manage Rule instance.
description:
    - Create, update and delete instance of Rule.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    namespace_name:
        description:
            - The namespace name
        required: True
    topic_name:
        description:
            - The topic name.
        required: True
    subscription_name:
        description:
            - The subscription name.
        required: True
    name:
        description:
            - The rule name.
        required: True
    action:
        description:
            - Represents the filter actions which are allowed for the transformation of a message that have been matched by a filter expression.
        suboptions:
            sql_expression:
                description:
                    - "SQL expression. e.g. MyProperty='ABC'"
            compatibility_level:
                description:
                    - This property is reserved for future use. An integer value showing the compatibility level, currently hard-coded to 20.
            requires_preprocessing:
                description:
                    - Value that indicates whether the rule action requires preprocessing.
    filter_type:
        description:
            - Filter type that is evaluated against a BrokeredMessage.
        choices:
            - 'sql_filter'
            - 'correlation_filter'
    sql_filter:
        description:
            - Properties of C(sql_filter)
        suboptions:
            sql_expression:
                description:
                    - "The SQL expression. e.g. MyProperty='ABC'"
            requires_preprocessing:
                description:
                    - Value that indicates whether the rule action requires preprocessing.
    correlation_filter:
        description:
            - Properties of C(correlation_filter)
        suboptions:
            correlation_id:
                description:
                    - Identifier of the correlation.
            message_id:
                description:
                    - Identifier of the message.
            to:
                description:
                    - Address to send to.
            reply_to:
                description:
                    - Address of the queue I(to) reply I(to).
            label:
                description:
                    - Application specific label.
            session_id:
                description:
                    - Session identifier.
            reply_to_session_id:
                description:
                    - Session identifier I(to) reply I(to).
            content_type:
                description:
                    - Content type of the message.
            requires_preprocessing:
                description:
                    - Value that indicates whether the rule action requires preprocessing.
    state:
      description:
        - Assert the state of the Rule.
        - Use 'present' to create or update an Rule and 'absent' to delete it.
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
  - name: Create (or update) Rule
    azure_rm_servicebusrule:
      resource_group: resourceGroupName
      namespace_name: sdk-Namespace-1319
      topic_name: sdk-Topics-2081
      subscription_name: sdk-Subscriptions-8691
      name: sdk-Rules-6571
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/subscriptionId/resourceGroups/resourceGroupName/providers/Microsoft.ServiceBus/namespaces/sdk-Namespace-1319/topics/sdk-Topics-20
            81/subscriptions/sdk-Subscriptions-8691/rules/sdk-Rules-6571"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.servicebus import ServiceBusManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRules(AzureRMModuleBase):
    """Configuration class for an Azure RM Rule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            namespace_name=dict(
                type='str',
                required=True
            ),
            topic_name=dict(
                type='str',
                required=True
            ),
            subscription_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            action=dict(
                type='dict'
            ),
            filter_type=dict(
                type='str',
                choices=['sql_filter',
                         'correlation_filter']
            ),
            sql_filter=dict(
                type='dict'
            ),
            correlation_filter=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.namespace_name = None
        self.topic_name = None
        self.subscription_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "action":
                    self.parameters["action"] = kwargs[key]
                elif key == "filter_type":
                    self.parameters["filter_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "sql_filter":
                    self.parameters["sql_filter"] = kwargs[key]
                elif key == "correlation_filter":
                    self.parameters["correlation_filter"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceBusManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_rule()

        if not old_response:
            self.log("Rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Rule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_rule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_rule()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_rule():
                time.sleep(20)
        else:
            self.log("Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_rule(self):
        '''
        Creates or updates Rule with the specified configuration.

        :return: deserialized Rule instance state dictionary
        '''
        self.log("Creating / Updating the Rule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.rules.create_or_update(resource_group_name=self.resource_group,
                                                               namespace_name=self.namespace_name,
                                                               topic_name=self.topic_name,
                                                               subscription_name=self.subscription_name,
                                                               rule_name=self.name,
                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Rule instance.')
            self.fail("Error creating the Rule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_rule(self):
        '''
        Deletes specified Rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Rule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.rules.delete(resource_group_name=self.resource_group,
                                                     namespace_name=self.namespace_name,
                                                     topic_name=self.topic_name,
                                                     subscription_name=self.subscription_name,
                                                     rule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Rule instance.')
            self.fail("Error deleting the Rule instance: {0}".format(str(e)))

        return True

    def get_rule(self):
        '''
        Gets the properties of the specified Rule.

        :return: deserialized Rule instance state dictionary
        '''
        self.log("Checking if the Rule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.rules.get(resource_group_name=self.resource_group,
                                                  namespace_name=self.namespace_name,
                                                  topic_name=self.topic_name,
                                                  subscription_name=self.subscription_name,
                                                  rule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Rule instance.')
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMRules()


if __name__ == '__main__':
    main()

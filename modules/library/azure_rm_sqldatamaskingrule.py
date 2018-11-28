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
module: azure_rm_sqldatamaskingrule
version_added: "2.8"
short_description: Manage Azure Data Masking Rule instance.
description:
    - Create, update and delete instance of Azure Data Masking Rule.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database.
        required: True
    data_masking_policy_name:
        description:
            - The name of the database for which the data masking rule applies.
        required: True
    name:
        description:
            - The name of the data masking rule.
        required: True
    alias_name:
        description:
            - The alias name. This is a legacy parameter and is no longer used.
    rule_state:
        description:
            - "The rule state. Used to delete a rule. To delete an existing rule, specify the I(schema_name), I(table_name), I(column_name),
               I(masking_function), and specify ruleState as disabled. However, if the rule doesn't already exist, the rule will be created with ruleState
               set to enabled, regardless of the provided value of ruleState. Possible values include: 'Disabled', 'Enabled'"
        type: bool
    schema_name:
        description:
            - The schema name on which the data masking rule is applied.
            - Required when C(state) is I(present).
    table_name:
        description:
            - The table name on which the data masking rule is applied.
            - Required when C(state) is I(present).
    column_name:
        description:
            - The column name on which the data masking rule is applied.
            - Required when C(state) is I(present).
    masking_function:
        description:
            - The masking function that is used for the data masking rule.
            - Required when C(state) is I(present).
        choices:
            - 'default'
            - 'ccn'
            - 'email'
            - 'number'
            - 'ssn'
            - 'text'
    number_from:
        description:
            - The numberFrom property of the masking rule. Required if I(masking_function) is set to C(number), otherwise this parameter will be ignored.
    number_to:
        description:
            - The numberTo property of the data masking rule. Required if I(masking_function) is set to C(number), otherwise this parameter will be ignored.
    prefix_size:
        description:
            - "If I(masking_function) is set to C(text), the C(number) of characters to show unmasked in the beginning of the string. Otherwise, this
               parameter will be ignored."
    suffix_size:
        description:
            - "If I(masking_function) is set to C(text), the C(number) of characters to show unmasked at the end of the string. Otherwise, this parameter
               will be ignored."
    replacement_string:
        description:
            - "If I(masking_function) is set to C(text), the character to use for masking the unexposed part of the string. Otherwise, this parameter will
               be ignored."
    state:
      description:
        - Assert the state of the Data Masking Rule.
        - Use 'present' to create or update an Data Masking Rule and 'absent' to delete it.
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
  - name: Create (or update) Data Masking Rule
    azure_rm_sqldatamaskingrule:
      resource_group: sqlcrudtest-6852
      server_name: sqlcrudtest-2080
      database_name: sqlcrudtest-331
      data_masking_policy_name: Default
      name: rule1
      rule_state: rule_state
      schema_name: dbo
      table_name: Table_1
      column_name: test1
      masking_function: Text
      prefix_size: 1
      suffix_size: 0
      replacement_string: asdf
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-6852/providers/Microsoft.Sql/servers/sqlcrudtest-6852/databases/s
            qlcrudtest-331/dataMaskingPolicies/Default/rules/"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDataMaskingRule(AzureRMModuleBase):
    """Configuration class for an Azure RM Data Masking Rule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            database_name=dict(
                type='str',
                required=True
            ),
            data_masking_policy_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            alias_name=dict(
                type='str'
            ),
            rule_state=dict(
                type='bool'
            ),
            schema_name=dict(
                type='str'
            ),
            table_name=dict(
                type='str'
            ),
            column_name=dict(
                type='str'
            ),
            masking_function=dict(
                type='str',
                choices=['default',
                         'ccn',
                         'email',
                         'number',
                         'ssn',
                         'text']
            ),
            number_from=dict(
                type='str'
            ),
            number_to=dict(
                type='str'
            ),
            prefix_size=dict(
                type='str'
            ),
            suffix_size=dict(
                type='str'
            ),
            replacement_string=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.database_name = None
        self.data_masking_policy_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDataMaskingRule, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_map(self.parameters, ['rule_state'], {True: 'Enabled', False: 'Disabled'})
        dict_camelize(self.parameters, ['masking_function'], True)
        dict_map(self.parameters, ['masking_function'], {'ccn': 'CCN', 'ssn': 'SSN'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_datamaskingrule()

        if not old_response:
            self.log("Data Masking Rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Data Masking Rule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Data Masking Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_datamaskingrule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Data Masking Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_datamaskingrule()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Data Masking Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_datamaskingrule(self):
        '''
        Creates or updates Data Masking Rule with the specified configuration.

        :return: deserialized Data Masking Rule instance state dictionary
        '''
        self.log("Creating / Updating the Data Masking Rule instance {0}".format(self.))

        try:
            response = self.mgmt_client.data_masking_rules.create_or_update(resource_group_name=self.resource_group,
                                                                            server_name=self.server_name,
                                                                            database_name=self.database_name,
                                                                            data_masking_policy_name=self.data_masking_policy_name,
                                                                            data_masking_rule_name=self.name,
                                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Data Masking Rule instance.')
            self.fail("Error creating the Data Masking Rule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_datamaskingrule(self):
        '''
        Deletes specified Data Masking Rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Data Masking Rule instance {0}".format(self.))
        try:
            response = self.mgmt_client.data_masking_rules.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Data Masking Rule instance.')
            self.fail("Error deleting the Data Masking Rule instance: {0}".format(str(e)))

        return True

    def get_datamaskingrule(self):
        '''
        Gets the properties of the specified Data Masking Rule.

        :return: deserialized Data Masking Rule instance state dictionary
        '''
        self.log("Checking if the Data Masking Rule instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.data_masking_rules.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Data Masking Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Data Masking Rule instance.')
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
    AzureRMDataMaskingRule()


if __name__ == '__main__':
    main()

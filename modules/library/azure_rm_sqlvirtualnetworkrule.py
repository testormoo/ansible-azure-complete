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
module: azure_rm_sqlvirtualnetworkrule
version_added: "2.8"
short_description: Manage Azure Virtual Network Rule instance.
description:
    - Create, update and delete instance of Azure Virtual Network Rule.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the virtual network rule.
        required: True
    virtual_network_subnet_id:
        description:
            - The ARM resource id of the virtual network subnet.
        required: True
    ignore_missing_vnet_service_endpoint:
        description:
            - Create firewall rule before the virtual network has vnet service endpoint enabled.
    state:
      description:
        - Assert the state of the Virtual Network Rule.
        - Use 'present' to create or update an Virtual Network Rule and 'absent' to delete it.
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
  - name: Create (or update) Virtual Network Rule
    azure_rm_sqlvirtualnetworkrule:
      resource_group: Default
      server_name: vnet-test-svr
      name: vnet-firewall-rule
      virtual_network_subnet_id: NOT FOUND
      ignore_missing_vnet_service_endpoint: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default/providers/Microsoft.Sql/servers/vnet-test-svr/virtualNetworkRules/vne
            t-firewall-rule"
state:
    description:
        - "Virtual Network Rule State. Possible values include: 'Initializing', 'InProgress', 'Ready', 'Deleting', 'Unknown'"
    returned: always
    type: str
    sample: state
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


class AzureRMVirtualNetworkRule(AzureRMModuleBase):
    """Configuration class for an Azure RM Virtual Network Rule resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            virtual_network_subnet_id=dict(
                type='str',
                required=True
            ),
            ignore_missing_vnet_service_endpoint=dict(
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
        self.name = None
        self.virtual_network_subnet_id = None
        self.ignore_missing_vnet_service_endpoint = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVirtualNetworkRule, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_virtualnetworkrule()

        if not old_response:
            self.log("Virtual Network Rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Virtual Network Rule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Virtual Network Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_virtualnetworkrule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Virtual Network Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_virtualnetworkrule()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Virtual Network Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None)
                })
        return self.results

    def create_update_virtualnetworkrule(self):
        '''
        Creates or updates Virtual Network Rule with the specified configuration.

        :return: deserialized Virtual Network Rule instance state dictionary
        '''
        self.log("Creating / Updating the Virtual Network Rule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.virtual_network_rules.create_or_update(resource_group_name=self.resource_group,
                                                                               server_name=self.server_name,
                                                                               virtual_network_rule_name=self.name,
                                                                               virtual_network_subnet_id=self.virtual_network_subnet_id)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Virtual Network Rule instance.')
            self.fail("Error creating the Virtual Network Rule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetworkrule(self):
        '''
        Deletes specified Virtual Network Rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Virtual Network Rule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.virtual_network_rules.delete(resource_group_name=self.resource_group,
                                                                     server_name=self.server_name,
                                                                     virtual_network_rule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Virtual Network Rule instance.')
            self.fail("Error deleting the Virtual Network Rule instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkrule(self):
        '''
        Gets the properties of the specified Virtual Network Rule.

        :return: deserialized Virtual Network Rule instance state dictionary
        '''
        self.log("Checking if the Virtual Network Rule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_rules.get(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name,
                                                                  virtual_network_rule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Virtual Network Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Virtual Network Rule instance.')
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
    AzureRMVirtualNetworkRule()


if __name__ == '__main__':
    main()

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
module: azure_rm_inboundnatrule
version_added: "2.8"
short_description: Manage Azure Inbound Nat Rule instance.
description:
    - Create, update and delete instance of Azure Inbound Nat Rule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    load_balancer_name:
        description:
            - The name of the load balancer.
        required: True
    name:
        description:
            - The name of the inbound nat rule.
        required: True
    id:
        description:
            - Resource ID.
    frontend_ip_configuration:
        description:
            - A reference to frontend IP addresses.
        suboptions:
            id:
                description:
                    - Resource ID.
    protocol:
        description:
            - "Possible values include: 'C(udp)', 'C(tcp)', 'C(all)'"
        choices:
            - 'udp'
            - 'tcp'
            - 'all'
    frontend_port:
        description:
            - The port for the external endpoint. Port numbers for each rule must be unique within the Load Balancer. Acceptable values range from 1 to 65534.
    backend_port:
        description:
            - The port used for the internal endpoint. Acceptable values range from 1 to 65535.
    idle_timeout_in_minutes:
        description:
            - "The timeout for the C(tcp) idle connection. The value can be set between 4 and 30 minutes. The default value is 4 minutes. This element is
               only used when the I(protocol) is set to C(tcp)."
    enable_floating_ip:
        description:
            - "Configures a virtual machine's endpoint for the floating IP capability required to configure a SQL AlwaysOn Availability Group. This setting
               is required when using the SQL AlwaysOn Availability Groups in SQL server. This setting can't be changed after you create the endpoint."
    name:
        description:
            - Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
    state:
      description:
        - Assert the state of the Inbound Nat Rule.
        - Use 'present' to create or update an Inbound Nat Rule and 'absent' to delete it.
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
  - name: Create (or update) Inbound Nat Rule
    azure_rm_inboundnatrule:
      resource_group: testrg
      load_balancer_name: lb1
      name: natRule1.1
      frontend_ip_configuration:
        id: /subscriptions/subid/resourceGroups/testrg/providers/Microsoft.Network/loadBalancers/lb1/frontendIPConfigurations/ip1
      protocol: Tcp
      frontend_port: 3390
      backend_port: 3389
      idle_timeout_in_minutes: 4
      enable_floating_ip: False
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/testrg/providers/Microsoft.Network/loadBalancers/lb1/inboundNatRules/natRule1.1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMInboundNatRule(AzureRMModuleBase):
    """Configuration class for an Azure RM Inbound Nat Rule resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            load_balancer_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            id=dict(
                type='str'
            ),
            frontend_ip_configuration=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
            ),
            protocol=dict(
                type='str',
                choices=['udp',
                         'tcp',
                         'all']
            ),
            frontend_port=dict(
                type='int'
            ),
            backend_port=dict(
                type='int'
            ),
            idle_timeout_in_minutes=dict(
                type='int'
            ),
            enable_floating_ip=dict(
                type='str'
            ),
            name=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.load_balancer_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMInboundNatRule, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.inbound_nat_rule_parameters[key] = kwargs[key]

        dict_resource_id(self.inbound_nat_rule_parameters, ['id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_resource_id(self.inbound_nat_rule_parameters, ['frontend_ip_configuration', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.inbound_nat_rule_parameters, ['protocol'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_inboundnatrule()

        if not old_response:
            self.log("Inbound Nat Rule instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Inbound Nat Rule instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.inbound_nat_rule_parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Inbound Nat Rule instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_inboundnatrule()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Inbound Nat Rule instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_inboundnatrule()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Inbound Nat Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_inboundnatrule(self):
        '''
        Creates or updates Inbound Nat Rule with the specified configuration.

        :return: deserialized Inbound Nat Rule instance state dictionary
        '''
        self.log("Creating / Updating the Inbound Nat Rule instance {0}".format(self.name))

        try:
            response = self.mgmt_client.inbound_nat_rules.create_or_update(resource_group_name=self.resource_group,
                                                                           load_balancer_name=self.load_balancer_name,
                                                                           inbound_nat_rule_name=self.name,
                                                                           inbound_nat_rule_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Inbound Nat Rule instance.')
            self.fail("Error creating the Inbound Nat Rule instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_inboundnatrule(self):
        '''
        Deletes specified Inbound Nat Rule instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Inbound Nat Rule instance {0}".format(self.name))
        try:
            response = self.mgmt_client.inbound_nat_rules.delete(resource_group_name=self.resource_group,
                                                                 load_balancer_name=self.load_balancer_name,
                                                                 inbound_nat_rule_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Inbound Nat Rule instance.')
            self.fail("Error deleting the Inbound Nat Rule instance: {0}".format(str(e)))

        return True

    def get_inboundnatrule(self):
        '''
        Gets the properties of the specified Inbound Nat Rule.

        :return: deserialized Inbound Nat Rule instance state dictionary
        '''
        self.log("Checking if the Inbound Nat Rule instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.inbound_nat_rules.get(resource_group_name=self.resource_group,
                                                              load_balancer_name=self.load_balancer_name,
                                                              inbound_nat_rule_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Inbound Nat Rule instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Inbound Nat Rule instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMInboundNatRule()


if __name__ == '__main__':
    main()

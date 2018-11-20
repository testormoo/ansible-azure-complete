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
short_description: Manage Inbound Nat Rule instance.
description:
    - Create, update and delete instance of Inbound Nat Rule.

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


class AzureRMInboundNatRules(AzureRMModuleBase):
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
                type='dict'
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

        super(AzureRMInboundNatRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "id":
                    self.parameters["id"] = kwargs[key]
                elif key == "frontend_ip_configuration":
                    self.parameters["frontend_ip_configuration"] = kwargs[key]
                elif key == "protocol":
                    self.parameters["protocol"] = _snake_to_camel(kwargs[key], True)
                elif key == "frontend_port":
                    self.parameters["frontend_port"] = kwargs[key]
                elif key == "backend_port":
                    self.parameters["backend_port"] = kwargs[key]
                elif key == "idle_timeout_in_minutes":
                    self.parameters["idle_timeout_in_minutes"] = kwargs[key]
                elif key == "enable_floating_ip":
                    self.parameters["enable_floating_ip"] = kwargs[key]
                elif key == "name":
                    self.parameters["name"] = kwargs[key]

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
                if (not default_compare(self.parameters, old_response, '')):
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
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_inboundnatrule():
                time.sleep(20)
        else:
            self.log("Inbound Nat Rule instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
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
    AzureRMInboundNatRules()


if __name__ == '__main__':
    main()

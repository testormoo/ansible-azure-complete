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
module: azure_rm_publicipaddresse
version_added: "2.8"
short_description: Manage Azure Public I P Addresse instance.
description:
    - Create, update and delete instance of Azure Public I P Addresse.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the public IP address.
        required: True
    id:
        description:
            - Resource ID.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The public IP address SKU.
        suboptions:
            name:
                description:
                    - Name of a public IP address SKU.
                choices:
                    - 'basic'
                    - 'standard'
    public_ip_allocation_method:
        description:
            - "The public IP allocation method. Possible values are: 'C(static)' and 'C(dynamic)'."
        choices:
            - 'static'
            - 'dynamic'
    public_ip_address_version:
        description:
            - "The public IP address version. Possible values are: 'C(ipv4)' and 'C(ipv6)'."
        choices:
            - 'ipv4'
            - 'ipv6'
    dns_settings:
        description:
            - The FQDN of the DNS record associated with the public IP address.
        suboptions:
            domain_name_label:
                description:
                    - "Gets or sets the Domain name label.The concatenation of the domain name label and the regionalized DNS zone make up the fully
                       qualified domain name associated with the public IP address. If a domain name label is specified, an A DNS record is created for the
                       public IP in the Microsoft Azure DNS system."
            fqdn:
                description:
                    - "Gets the FQDN, Fully qualified domain name of the A DNS record associated with the public IP. This is the concatenation of the
                       I(domain_name_label) and the regionalized DNS zone."
            reverse_fqdn:
                description:
                    - "Gets or Sets the Reverse I(fqdn). A user-visible, fully qualified domain name that resolves to this public IP address. If the
                       reverseFqdn is specified, then a PTR DNS record is created pointing from the IP address in the in-addr.arpa domain to the reverse
                       I(fqdn). "
    ip_address:
        description:
            - The IP address associated with the public IP address resource.
    idle_timeout_in_minutes:
        description:
            - The idle timeout of the public IP address.
    resource_guid:
        description:
            - The resource GUID property of the public IP resource.
    zones:
        description:
            - A list of availability zones denoting the IP allocated for the resource needs to come from.
        type: list
    state:
      description:
        - Assert the state of the Public I P Addresse.
        - Use 'present' to create or update an Public I P Addresse and 'absent' to delete it.
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
  - name: Create (or update) Public I P Addresse
    azure_rm_publicipaddresse:
      resource_group: rg1
      name: test-ip
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/publicIPAddresses/test-ip
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


class AzureRMPublicIPAddresse(AzureRMModuleBase):
    """Configuration class for an Azure RM Public I P Addresse resource"""

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
            id=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            public_ip_allocation_method=dict(
                type='str',
                choices=['static',
                         'dynamic']
            ),
            public_ip_address_version=dict(
                type='str',
                choices=['ipv4',
                         'ipv6']
            ),
            dns_settings=dict(
                type='dict'
            ),
            ip_address=dict(
                type='str'
            ),
            idle_timeout_in_minutes=dict(
                type='int'
            ),
            resource_guid=dict(
                type='str'
            ),
            zones=dict(
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

        super(AzureRMPublicIPAddresse, self).__init__(derived_arg_spec=self.module_arg_spec,
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
        dict_camelize(self.parameters, ['public_ip_allocation_method'], True)
        dict_camelize(self.parameters, ['public_ip_address_version'], True)
        dict_map(self.parameters, ['public_ip_address_version'], ''ipv4': 'IPv4', 'ipv6': 'IPv6'')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_publicipaddresse()

        if not old_response:
            self.log("Public I P Addresse instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Public I P Addresse instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Public I P Addresse instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_publicipaddresse()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Public I P Addresse instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_publicipaddresse()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_publicipaddresse():
                time.sleep(20)
        else:
            self.log("Public I P Addresse instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_publicipaddresse(self):
        '''
        Creates or updates Public I P Addresse with the specified configuration.

        :return: deserialized Public I P Addresse instance state dictionary
        '''
        self.log("Creating / Updating the Public I P Addresse instance {0}".format(self.name))

        try:
            response = self.mgmt_client.public_ip_addresses.create_or_update(resource_group_name=self.resource_group,
                                                                             public_ip_address_name=self.name,
                                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Public I P Addresse instance.')
            self.fail("Error creating the Public I P Addresse instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_publicipaddresse(self):
        '''
        Deletes specified Public I P Addresse instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Public I P Addresse instance {0}".format(self.name))
        try:
            response = self.mgmt_client.public_ip_addresses.delete(resource_group_name=self.resource_group,
                                                                   public_ip_address_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Public I P Addresse instance.')
            self.fail("Error deleting the Public I P Addresse instance: {0}".format(str(e)))

        return True

    def get_publicipaddresse(self):
        '''
        Gets the properties of the specified Public I P Addresse.

        :return: deserialized Public I P Addresse instance state dictionary
        '''
        self.log("Checking if the Public I P Addresse instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.public_ip_addresses.get(resource_group_name=self.resource_group,
                                                                public_ip_address_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Public I P Addresse instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Public I P Addresse instance.')
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
    AzureRMPublicIPAddresse()


if __name__ == '__main__':
    main()

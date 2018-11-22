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
module: azure_rm_domainservice
version_added: "2.8"
short_description: Manage Azure Domain Service instance.
description:
    - Create, update and delete instance of Azure Domain Service.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    name:
        description:
            - The name of the domain service in the specified subscription and resource group.
        required: True
    domain_name:
        description:
            - The name of the Azure domain that the user would like to deploy Domain Services to.
    subnet_id:
        description:
            - "The name of the virtual network that Domain Services will be deployed on. The id of the subnet that Domain Services will be deployed on.
               /virtualNetwork/vnetName/subnets/subnetName."
    ldaps_settings:
        description:
            - Secure LDAP Settings
        suboptions:
            ldaps:
                description:
                    - "A flag to determine whether or not Secure LDAP is enabled or disabled. Possible values include: 'Enabled', 'Disabled'"
                type: bool
            pfx_certificate:
                description:
                    - "The certificate required to configure Secure LDAP. The parameter passed here should be a base64encoded representation of the
                       certificate pfx file."
            pfx_certificate_password:
                description:
                    - The password to decrypt the provided Secure LDAP certificate pfx file.
            external_access:
                description:
                    - "A flag to determine whether or not Secure LDAP access over the internet is enabled or disabled. Possible values include: 'Enabled',
                       'Disabled'"
                type: bool
    notification_settings:
        description:
            - Notification Settings
        suboptions:
            notify_global_admins:
                description:
                    - "Should global admins be notified. Possible values include: 'Enabled', 'Disabled'"
                type: bool
            notify_dc_admins:
                description:
                    - "Should domain controller admins be notified. Possible values include: 'Enabled', 'Disabled'"
                type: bool
            additional_recipients:
                description:
                    - The list of additional recipients
                type: list
    domain_security_settings:
        description:
            - DomainSecurity Settings
        suboptions:
            ntlm_v1:
                description:
                    - "A flag to determine whether or not NtlmV1 is enabled or disabled. Possible values include: 'Enabled', 'Disabled'"
                type: bool
            tls_v1:
                description:
                    - "A flag to determine whether or not TlsV1 is enabled or disabled. Possible values include: 'Enabled', 'Disabled'"
                type: bool
            sync_ntlm_passwords:
                description:
                    - "A flag to determine whether or not SyncNtlmPasswords is enabled or disabled. Possible values include: 'Enabled', 'Disabled'"
                type: bool
    filtered_sync:
        description:
            - "Enabled or Disabled flag to turn on Group-based filtered sync. Possible values include: 'Enabled', 'Disabled'"
        type: bool
    state:
      description:
        - Assert the state of the Domain Service.
        - Use 'present' to create or update an Domain Service and 'absent' to delete it.
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
  - name: Create (or update) Domain Service
    azure_rm_domainservice:
      resource_group: sva-tt-WUS
      name: zdomain.zforest.com
      domain_name: zdomain.zforest.com
      subnet_id: /subscriptions/1639790a-76a2-4ac4-98d9-8562f5dfcb4d/resourceGroups/Default-Networking/providers/Microsoft.Network/virtualNetworks/DCIaasTmpWusNet/subnets/Subnet-1
      ldaps_settings:
        ldaps: ldaps
        pfx_certificate: MIIDPDCCAiSgAwIBAgIQQUI9P6tq2p9OFIJa7DLNvTANBgkqhkiG9w0BAQsFADAgMR4w...
        pfx_certificate_password: Password01
        external_access: external_access
      notification_settings:
        notify_global_admins: notify_global_admins
        notify_dc_admins: notify_dc_admins
        additional_recipients:
          - [
  "jicha@microsoft.com",
  "caalmont@microsoft.com"
]
      domain_security_settings:
        ntlm_v1: ntlm_v1
        tls_v1: tls_v1
        sync_ntlm_passwords: sync_ntlm_passwords
      filtered_sync: filtered_sync
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/1639790a-76a2-4ac4-98d9-8562f5dfcb4d/resourceGroups/sva-tt-WUS/providers/Microsoft.AAD/domainServices/zdomain.zforest.com
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.domainservices import DomainServicesResourceProvider
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDomainService(AzureRMModuleBase):
    """Configuration class for an Azure RM Domain Service resource"""

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
            domain_name=dict(
                type='str'
            ),
            subnet_id=dict(
                type='str'
            ),
            ldaps_settings=dict(
                type='dict'
            ),
            notification_settings=dict(
                type='dict'
            ),
            domain_security_settings=dict(
                type='dict'
            ),
            filtered_sync=dict(
                type='bool'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDomainService, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.properties[key] = kwargs[key]

        dict_map(self.properties, ['ldaps_settings', 'ldaps'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.properties, ['ldaps_settings', 'external_access'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.properties, ['notification_settings', 'notify_global_admins'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.properties, ['notification_settings', 'notify_dc_admins'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.properties, ['domain_security_settings', 'ntlm_v1'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.properties, ['domain_security_settings', 'tls_v1'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.properties, ['domain_security_settings', 'sync_ntlm_passwords'], {True: 'Enabled', False: 'Disabled'})
        dict_map(self.properties, ['filtered_sync'], {True: 'Enabled', False: 'Disabled'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DomainServicesResourceProvider,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_domainservice()

        if not old_response:
            self.log("Domain Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Domain Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Domain Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_domainservice()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Domain Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_domainservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_domainservice():
                time.sleep(20)
        else:
            self.log("Domain Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_domainservice(self):
        '''
        Creates or updates Domain Service with the specified configuration.

        :return: deserialized Domain Service instance state dictionary
        '''
        self.log("Creating / Updating the Domain Service instance {0}".format(self.name))

        try:
            response = self.mgmt_client.domain_services.create_or_update(resource_group_name=self.resource_group,
                                                                         domain_service_name=self.name,
                                                                         properties=self.properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Domain Service instance.')
            self.fail("Error creating the Domain Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_domainservice(self):
        '''
        Deletes specified Domain Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Domain Service instance {0}".format(self.name))
        try:
            response = self.mgmt_client.domain_services.delete(resource_group_name=self.resource_group,
                                                               domain_service_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Domain Service instance.')
            self.fail("Error deleting the Domain Service instance: {0}".format(str(e)))

        return True

    def get_domainservice(self):
        '''
        Gets the properties of the specified Domain Service.

        :return: deserialized Domain Service instance state dictionary
        '''
        self.log("Checking if the Domain Service instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.domain_services.get(resource_group_name=self.resource_group,
                                                            domain_service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Domain Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Domain Service instance.')
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
    AzureRMDomainService()


if __name__ == '__main__':
    main()

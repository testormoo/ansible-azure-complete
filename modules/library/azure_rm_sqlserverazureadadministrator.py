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
module: azure_rm_sqlserverazureadadministrator
version_added: "2.8"
short_description: Manage Azure Server Azure A D Administrator instance.
description:
    - Create, update and delete instance of Azure Server Azure A D Administrator.

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
            - Name of the server administrator resource.
        required: True
    administrator_type:
        description:
            - The type of administrator.
            - Required when C(state) is I(present).
    login:
        description:
            - The server administrator login value.
            - Required when C(state) is I(present).
    sid:
        description:
            - The server administrator Sid (Secure ID).
            - Required when C(state) is I(present).
    tenant_id:
        description:
            - The server Active Directory Administrator tenant id.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Server Azure A D Administrator.
        - Use 'present' to create or update an Server Azure A D Administrator and 'absent' to delete it.
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
  - name: Create (or update) Server Azure A D Administrator
    azure_rm_sqlserverazureadadministrator:
      resource_group: sqlcrudtest-4799
      server_name: sqlcrudtest-6440
      name: activeDirectory
      administrator_type: ActiveDirectory
      login: bob@contoso.com
      sid: c6b82b90-a647-49cb-8a62-0d2d3cb7ac7c
      tenant_id: c6b82b90-a647-49cb-8a62-0d2d3cb7ac7c
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/sqlcrudtest-4799/providers/Microsoft.Sql/servers/sqlcrudtest-6440/administrat
            ors/activeDirectory"
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


class AzureRMServerAzureADAdministrator(AzureRMModuleBase):
    """Configuration class for an Azure RM Server Azure A D Administrator resource"""

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
            administrator_type=dict(
                type='str'
            ),
            login=dict(
                type='str'
            ),
            sid=dict(
                type='str'
            ),
            tenant_id=dict(
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
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServerAzureADAdministrator, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                    supports_check_mode=True,
                                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.properties[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_serverazureadadministrator()

        if not old_response:
            self.log("Server Azure A D Administrator instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Server Azure A D Administrator instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Server Azure A D Administrator instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_serverazureadadministrator()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Server Azure A D Administrator instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_serverazureadadministrator()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Server Azure A D Administrator instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_serverazureadadministrator(self):
        '''
        Creates or updates Server Azure A D Administrator with the specified configuration.

        :return: deserialized Server Azure A D Administrator instance state dictionary
        '''
        self.log("Creating / Updating the Server Azure A D Administrator instance {0}".format(self.name))

        try:
            response = self.mgmt_client.server_azure_ad_administrators.create_or_update(resource_group_name=self.resource_group,
                                                                                        server_name=self.server_name,
                                                                                        administrator_name=self.name,
                                                                                        properties=self.properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Server Azure A D Administrator instance.')
            self.fail("Error creating the Server Azure A D Administrator instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serverazureadadministrator(self):
        '''
        Deletes specified Server Azure A D Administrator instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Server Azure A D Administrator instance {0}".format(self.name))
        try:
            response = self.mgmt_client.server_azure_ad_administrators.delete(resource_group_name=self.resource_group,
                                                                              server_name=self.server_name,
                                                                              administrator_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Server Azure A D Administrator instance.')
            self.fail("Error deleting the Server Azure A D Administrator instance: {0}".format(str(e)))

        return True

    def get_serverazureadadministrator(self):
        '''
        Gets the properties of the specified Server Azure A D Administrator.

        :return: deserialized Server Azure A D Administrator instance state dictionary
        '''
        self.log("Checking if the Server Azure A D Administrator instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.server_azure_ad_administrators.get(resource_group_name=self.resource_group,
                                                                           server_name=self.server_name,
                                                                           administrator_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Server Azure A D Administrator instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Server Azure A D Administrator instance.')
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


def main():
    """Main execution"""
    AzureRMServerAzureADAdministrator()


if __name__ == '__main__':
    main()

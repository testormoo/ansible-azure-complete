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
module: azure_rm_apimanagementopenidconnectprovider
version_added: "2.8"
short_description: Manage Azure Open Id Connect Provider instance.
description:
    - Create, update and delete instance of Azure Open Id Connect Provider.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the API Management service.
        required: True
    opid:
        description:
            - Identifier of the OpenID Connect Provider.
        required: True
    display_name:
        description:
            - User-friendly OpenID Connect Provider name.
            - Required when C(state) is I(present).
    description:
        description:
            - User-friendly description of OpenID Connect Provider.
    metadata_endpoint:
        description:
            - Metadata endpoint URI.
            - Required when C(state) is I(present).
    client_id:
        description:
            - Client ID of developer console which is the client application.
            - Required when C(state) is I(present).
    client_secret:
        description:
            - Client Secret of developer console which is the client application.
    if_match:
        description:
            - ETag of the Entity. Not required when creating an entity, but required when updating an entity.
    state:
      description:
        - Assert the state of the Open Id Connect Provider.
        - Use 'present' to create or update an Open Id Connect Provider and 'absent' to delete it.
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
  - name: Create (or update) Open Id Connect Provider
    azure_rm_apimanagementopenidconnectprovider:
      resource_group: rg1
      name: apimService1
      opid: templateOpenIdConnect3
      display_name: templateoidprovider3
      metadata_endpoint: https://oidprovider-template3.net
      client_id: oidprovidertemplate3
      if_match: NOT FOUND
'''

RETURN = '''
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOpenIdConnectProvider(AzureRMModuleBase):
    """Configuration class for an Azure RM Open Id Connect Provider resource"""

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
            opid=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            metadata_endpoint=dict(
                type='str'
            ),
            client_id=dict(
                type='str'
            ),
            client_secret=dict(
                type='str'
            ),
            if_match=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.opid = None
        self.parameters = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMOpenIdConnectProvider, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_openidconnectprovider()

        if not old_response:
            self.log("Open Id Connect Provider instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Open Id Connect Provider instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Open Id Connect Provider instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_openidconnectprovider()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Open Id Connect Provider instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_openidconnectprovider()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Open Id Connect Provider instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                })
        return self.results

    def create_update_openidconnectprovider(self):
        '''
        Creates or updates Open Id Connect Provider with the specified configuration.

        :return: deserialized Open Id Connect Provider instance state dictionary
        '''
        self.log("Creating / Updating the Open Id Connect Provider instance {0}".format(self.opid))

        try:
            response = self.mgmt_client.open_id_connect_provider.create_or_update(resource_group_name=self.resource_group,
                                                                                  service_name=self.name,
                                                                                  opid=self.opid,
                                                                                  parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Open Id Connect Provider instance.')
            self.fail("Error creating the Open Id Connect Provider instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_openidconnectprovider(self):
        '''
        Deletes specified Open Id Connect Provider instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Open Id Connect Provider instance {0}".format(self.opid))
        try:
            response = self.mgmt_client.open_id_connect_provider.delete(resource_group_name=self.resource_group,
                                                                        service_name=self.name,
                                                                        opid=self.opid,
                                                                        if_match=self.if_match)
        except CloudError as e:
            self.log('Error attempting to delete the Open Id Connect Provider instance.')
            self.fail("Error deleting the Open Id Connect Provider instance: {0}".format(str(e)))

        return True

    def get_openidconnectprovider(self):
        '''
        Gets the properties of the specified Open Id Connect Provider.

        :return: deserialized Open Id Connect Provider instance state dictionary
        '''
        self.log("Checking if the Open Id Connect Provider instance {0} is present".format(self.opid))
        found = False
        try:
            response = self.mgmt_client.open_id_connect_provider.get(resource_group_name=self.resource_group,
                                                                     service_name=self.name,
                                                                     opid=self.opid)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Open Id Connect Provider instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Open Id Connect Provider instance.')
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
    AzureRMOpenIdConnectProvider()


if __name__ == '__main__':
    main()

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
module: azure_rm_relaywcfrelay
version_added: "2.8"
short_description: Manage Azure W C F Relay instance.
description:
    - Create, update and delete instance of Azure W C F Relay.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    namespace_name:
        description:
            - The namespace name
        required: True
    name:
        description:
            - The relay name.
        required: True
    relay_type:
        description:
            - WCF relay type.
        choices:
            - 'net_tcp'
            - 'http'
    requires_client_authorization:
        description:
            - Returns true if client authorization is needed for this relay; otherwise, false.
    requires_transport_security:
        description:
            - Returns true if transport security is needed for this relay; otherwise, false.
    user_metadata:
        description:
            - "The usermetadata is a placeholder to store user-defined string data for the WCF Relay endpoint. For example, it can be used to store
               descriptive data, such as list of teams and their contact information. Also, user-defined configuration settings can be stored."
    state:
      description:
        - Assert the state of the W C F Relay.
        - Use 'present' to create or update an W C F Relay and 'absent' to delete it.
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
  - name: Create (or update) W C F Relay
    azure_rm_relaywcfrelay:
      resource_group: RG-eg
      namespace_name: sdk-RelayNamespace-9953
      name: sdk-Relay-Wcf-1194
      relay_type: NetTcp
      requires_client_authorization: True
      requires_transport_security: True
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/e2f361f0-3b27-4503-a9cc-21cfba380093/resourceGroups/RG-eg/providers/Microsoft.Relay/namespaces/sdk-RelayNamespace-9953/WcfRelays/
            sdk-Relay-Wcf-1194"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.relay import RelayManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWCFRelay(AzureRMModuleBase):
    """Configuration class for an Azure RM W C F Relay resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            relay_type=dict(
                type='str',
                choices=['net_tcp',
                         'http']
            ),
            requires_client_authorization=dict(
                type='str'
            ),
            requires_transport_security=dict(
                type='str'
            ),
            user_metadata=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.namespace_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWCFRelay, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['relay_type'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RelayManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_wcfrelay()

        if not old_response:
            self.log("W C F Relay instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("W C F Relay instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the W C F Relay instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_wcfrelay()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("W C F Relay instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_wcfrelay()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("W C F Relay instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_wcfrelay(self):
        '''
        Creates or updates W C F Relay with the specified configuration.

        :return: deserialized W C F Relay instance state dictionary
        '''
        self.log("Creating / Updating the W C F Relay instance {0}".format(self.name))

        try:
            response = self.mgmt_client.wcf_relays.create_or_update(resource_group_name=self.resource_group,
                                                                    namespace_name=self.namespace_name,
                                                                    relay_name=self.name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the W C F Relay instance.')
            self.fail("Error creating the W C F Relay instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_wcfrelay(self):
        '''
        Deletes specified W C F Relay instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the W C F Relay instance {0}".format(self.name))
        try:
            response = self.mgmt_client.wcf_relays.delete(resource_group_name=self.resource_group,
                                                          namespace_name=self.namespace_name,
                                                          relay_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the W C F Relay instance.')
            self.fail("Error deleting the W C F Relay instance: {0}".format(str(e)))

        return True

    def get_wcfrelay(self):
        '''
        Gets the properties of the specified W C F Relay.

        :return: deserialized W C F Relay instance state dictionary
        '''
        self.log("Checking if the W C F Relay instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.wcf_relays.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.namespace_name,
                                                       relay_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("W C F Relay instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the W C F Relay instance.')
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


def main():
    """Main execution"""
    AzureRMWCFRelay()


if __name__ == '__main__':
    main()

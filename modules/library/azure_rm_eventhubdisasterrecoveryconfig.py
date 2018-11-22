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
module: azure_rm_eventhubdisasterrecoveryconfig
version_added: "2.8"
short_description: Manage Azure Disaster Recovery Config instance.
description:
    - Create, update and delete instance of Azure Disaster Recovery Config.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    namespace_name:
        description:
            - The Namespace name
        required: True
    alias:
        description:
            - The Disaster Recovery configuration name
        required: True
    partner_namespace:
        description:
            - ARM Id of the Primary/Secondary eventhub namespace name, which is part of GEO DR pairning
    name:
        description:
            - Alternate name specified when I(alias) and namespace names are same.
    state:
      description:
        - Assert the state of the Disaster Recovery Config.
        - Use 'present' to create or update an Disaster Recovery Config and 'absent' to delete it.
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
  - name: Create (or update) Disaster Recovery Config
    azure_rm_eventhubdisasterrecoveryconfig:
      resource_group: exampleResourceGroup
      namespace_name: sdk-Namespace-8859
      alias: sdk-DisasterRecovery-3814
      partner_namespace: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: "/subscriptions/exampleResourceGroup/resourceGroups/exampleResourceGroup/providers/Microsoft.EventHub/namespaces/sdk-Namespace-8859/disasterRecov
            eryConfig/sdk-DisasterRecovery-3814"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.eventhub import EventHubManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDisasterRecoveryConfig(AzureRMModuleBase):
    """Configuration class for an Azure RM Disaster Recovery Config resource"""

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
            alias=dict(
                type='str',
                required=True
            ),
            partner_namespace=dict(
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
        self.namespace_name = None
        self.alias = None
        self.partner_namespace = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDisasterRecoveryConfig, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_disasterrecoveryconfig()

        if not old_response:
            self.log("Disaster Recovery Config instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Disaster Recovery Config instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Disaster Recovery Config instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_disasterrecoveryconfig()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Disaster Recovery Config instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_disasterrecoveryconfig()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_disasterrecoveryconfig():
                time.sleep(20)
        else:
            self.log("Disaster Recovery Config instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_disasterrecoveryconfig(self):
        '''
        Creates or updates Disaster Recovery Config with the specified configuration.

        :return: deserialized Disaster Recovery Config instance state dictionary
        '''
        self.log("Creating / Updating the Disaster Recovery Config instance {0}".format(self.alias))

        try:
            response = self.mgmt_client.disaster_recovery_configs.create_or_update(resource_group_name=self.resource_group,
                                                                                   namespace_name=self.namespace_name,
                                                                                   alias=self.alias)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Disaster Recovery Config instance.')
            self.fail("Error creating the Disaster Recovery Config instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_disasterrecoveryconfig(self):
        '''
        Deletes specified Disaster Recovery Config instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Disaster Recovery Config instance {0}".format(self.alias))
        try:
            response = self.mgmt_client.disaster_recovery_configs.delete(resource_group_name=self.resource_group,
                                                                         namespace_name=self.namespace_name,
                                                                         alias=self.alias)
        except CloudError as e:
            self.log('Error attempting to delete the Disaster Recovery Config instance.')
            self.fail("Error deleting the Disaster Recovery Config instance: {0}".format(str(e)))

        return True

    def get_disasterrecoveryconfig(self):
        '''
        Gets the properties of the specified Disaster Recovery Config.

        :return: deserialized Disaster Recovery Config instance state dictionary
        '''
        self.log("Checking if the Disaster Recovery Config instance {0} is present".format(self.alias))
        found = False
        try:
            response = self.mgmt_client.disaster_recovery_configs.get(resource_group_name=self.resource_group,
                                                                      namespace_name=self.namespace_name,
                                                                      alias=self.alias)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Disaster Recovery Config instance : {0} found".format(response.name))
        except:
            self.log('Did not find the Disaster Recovery Config instance.')
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
    AzureRMDisasterRecoveryConfig()


if __name__ == '__main__':
    main()

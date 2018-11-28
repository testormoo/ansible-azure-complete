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
module: azure_rm_containerregistryreplication
version_added: "2.8"
short_description: Manage Azure Replication instance.
description:
    - Create, update and delete instance of Azure Replication.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        required: True
    registry_name:
        description:
            - The name of the container registry.
        required: True
    name:
        description:
            - The name of the replication.
        required: True
    location:
        description:
            - The location of the resource. This cannot be changed after the resource is created.
        required: True
    state:
      description:
        - Assert the state of the Replication.
        - Use 'present' to create or update an Replication and 'absent' to delete it.
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
  - name: Create (or update) Replication
    azure_rm_containerregistryreplication:
      resource_group: myResourceGroup
      registry_name: myRegistry
      name: myReplication
      location: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.ContainerRegistry/registries/myRegistry/r
            eplications/myReplication"
status:
    description:
        - The status of the replication at the time the operation was called.
    returned: always
    type: complex
    sample: status
    contains:
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.containerregistry import ContainerRegistryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMReplication(AzureRMModuleBase):
    """Configuration class for an Azure RM Replication resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registry_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.registry_name = None
        self.name = None
        self.location = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMReplication, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ContainerRegistryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_replication()

        if not old_response:
            self.log("Replication instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Replication instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Replication instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_replication()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Replication instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_replication()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Replication instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': {
                }
                })
        return self.results

    def create_update_replication(self):
        '''
        Creates or updates Replication with the specified configuration.

        :return: deserialized Replication instance state dictionary
        '''
        self.log("Creating / Updating the Replication instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.replications.create(resource_group_name=self.resource_group,
                                                                registry_name=self.registry_name,
                                                                replication_name=self.name,
                                                                location=self.location)
            else:
                response = self.mgmt_client.replications.update(resource_group_name=self.resource_group,
                                                                registry_name=self.registry_name,
                                                                replication_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Replication instance.')
            self.fail("Error creating the Replication instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_replication(self):
        '''
        Deletes specified Replication instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Replication instance {0}".format(self.name))
        try:
            response = self.mgmt_client.replications.delete(resource_group_name=self.resource_group,
                                                            registry_name=self.registry_name,
                                                            replication_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Replication instance.')
            self.fail("Error deleting the Replication instance: {0}".format(str(e)))

        return True

    def get_replication(self):
        '''
        Gets the properties of the specified Replication.

        :return: deserialized Replication instance state dictionary
        '''
        self.log("Checking if the Replication instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.replications.get(resource_group_name=self.resource_group,
                                                         registry_name=self.registry_name,
                                                         replication_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Replication instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Replication instance.')
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
    AzureRMReplication()


if __name__ == '__main__':
    main()

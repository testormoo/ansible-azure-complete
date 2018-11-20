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
module: azure_rm_containerregistry
version_added: "2.8"
short_description: Manage Registry instance.
description:
    - Create, update and delete instance of Registry.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        required: True
    name:
        description:
            - The name of the container registry.
        required: True
    location:
        description:
            - The location of the resource. This cannot be changed after the resource is created.
            - Required when C(state) is I(present).
    sku:
        description:
            - The SKU of the container registry.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - The SKU name of the container registry. Required for registry creation.
                    - Required when C(state) is I(present).
                choices:
                    - 'classic'
                    - 'basic'
                    - 'standard'
                    - 'premium'
    admin_user_enabled:
        description:
            - The value that indicates whether the admin user is enabled.
    storage_account:
        description:
            - The properties of the storage account for the container registry. Only applicable to Classic I(sku).
        suboptions:
            id:
                description:
                    - The resource ID of the storage account.
                    - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Registry.
        - Use 'present' to create or update an Registry and 'absent' to delete it.
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
  - name: Create (or update) Registry
    azure_rm_containerregistry:
      resource_group: myResourceGroup
      name: myRegistry
      location: westus
      sku:
        name: Standard
      admin_user_enabled: True
'''

RETURN = '''
id:
    description:
        - The resource ID.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.ContainerRegistry/registries/myRegistry
status:
    description:
        - The status of the container registry at the time the operation was called.
    returned: always
    type: complex
    sample: status
    contains:
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

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


class AzureRMRegistries(AzureRMModuleBase):
    """Configuration class for an Azure RM Registry resource"""

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
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            admin_user_enabled=dict(
                type='str'
            ),
            storage_account=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.registry = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRegistries, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.registry["location"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'classic':
                            ev['name'] = 'Classic'
                        elif ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                        elif ev['name'] == 'premium':
                            ev['name'] = 'Premium'
                    self.registry["sku"] = ev
                elif key == "admin_user_enabled":
                    self.registry["admin_user_enabled"] = kwargs[key]
                elif key == "storage_account":
                    self.registry["storage_account"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ContainerRegistryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_registry()

        if not old_response:
            self.log("Registry instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Registry instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Registry instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_registry()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Registry instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_registry()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_registry():
                time.sleep(20)
        else:
            self.log("Registry instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_registry(self):
        '''
        Creates or updates Registry with the specified configuration.

        :return: deserialized Registry instance state dictionary
        '''
        self.log("Creating / Updating the Registry instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.registries.create(resource_group_name=self.resource_group,
                                                              registry_name=self.name,
                                                              registry=self.registry)
            else:
                response = self.mgmt_client.registries.update(resource_group_name=self.resource_group,
                                                              registry_name=self.name,
                                                              registry_update_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Registry instance.')
            self.fail("Error creating the Registry instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_registry(self):
        '''
        Deletes specified Registry instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Registry instance {0}".format(self.name))
        try:
            response = self.mgmt_client.registries.delete(resource_group_name=self.resource_group,
                                                          registry_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Registry instance.')
            self.fail("Error deleting the Registry instance: {0}".format(str(e)))

        return True

    def get_registry(self):
        '''
        Gets the properties of the specified Registry.

        :return: deserialized Registry instance state dictionary
        '''
        self.log("Checking if the Registry instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.registries.get(resource_group_name=self.resource_group,
                                                       registry_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Registry instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Registry instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': {
            }
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


def main():
    """Main execution"""
    AzureRMRegistries()


if __name__ == '__main__':
    main()

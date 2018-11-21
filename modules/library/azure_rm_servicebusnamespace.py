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
module: azure_rm_servicebusnamespace
version_added: "2.8"
short_description: Manage Namespace instance.
description:
    - Create, update and delete instance of Namespace.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    name:
        description:
            - The namespace name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - Porperties of Sku
        suboptions:
            name:
                description:
                    - Name of this SKU.
                    - Required when C(state) is I(present).
                choices:
                    - 'basic'
                    - 'standard'
                    - 'premium'
            tier:
                description:
                    - The billing tier of this particular SKU.
                choices:
                    - 'basic'
                    - 'standard'
                    - 'premium'
            capacity:
                description:
                    - The specified messaging units for the I(tier). For C(C(premium)) I(tier), capacity are 1,2 and 4.
    state:
      description:
        - Assert the state of the Namespace.
        - Use 'present' to create or update an Namespace and 'absent' to delete it.
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
  - name: Create (or update) Namespace
    azure_rm_servicebusnamespace:
      resource_group: ArunMonocle
      name: sdk-Namespace2924
      location: eastus
      sku:
        name: Standard
        tier: Standard
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/5f750a97-50d9-4e36-8081-c9ee4c0210d4/resourceGroups/ArunMonocle/providers/Microsoft.ServiceBus/namespaces/sdk-Namespace-3285
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.servicebus import ServiceBusManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMNamespaces(AzureRMModuleBase):
    """Configuration class for an Azure RM Namespace resource"""

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

        super(AzureRMNamespaces, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                        elif ev['name'] == 'premium':
                            ev['name'] = 'Premium'
                    if 'tier' in ev:
                        if ev['tier'] == 'basic':
                            ev['tier'] = 'Basic'
                        elif ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                        elif ev['tier'] == 'premium':
                            ev['tier'] = 'Premium'
                    self.parameters["sku"] = ev

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ServiceBusManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_namespace()

        if not old_response:
            self.log("Namespace instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Namespace instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Namespace instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_namespace()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Namespace instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_namespace()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_namespace():
                time.sleep(20)
        else:
            self.log("Namespace instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_namespace(self):
        '''
        Creates or updates Namespace with the specified configuration.

        :return: deserialized Namespace instance state dictionary
        '''
        self.log("Creating / Updating the Namespace instance {0}".format(self.name))

        try:
            response = self.mgmt_client.namespaces.create_or_update(resource_group_name=self.resource_group,
                                                                    namespace_name=self.name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Namespace instance.')
            self.fail("Error creating the Namespace instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_namespace(self):
        '''
        Deletes specified Namespace instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Namespace instance {0}".format(self.name))
        try:
            response = self.mgmt_client.namespaces.delete(resource_group_name=self.resource_group,
                                                          namespace_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Namespace instance.')
            self.fail("Error deleting the Namespace instance: {0}".format(str(e)))

        return True

    def get_namespace(self):
        '''
        Gets the properties of the specified Namespace.

        :return: deserialized Namespace instance state dictionary
        '''
        self.log("Checking if the Namespace instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.namespaces.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Namespace instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Namespace instance.')
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


def main():
    """Main execution"""
    AzureRMNamespaces()


if __name__ == '__main__':
    main()
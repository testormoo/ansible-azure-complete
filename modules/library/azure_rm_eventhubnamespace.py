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
module: azure_rm_eventhubnamespace
version_added: "2.8"
short_description: Manage Namespace instance.
description:
    - Create, update and delete instance of Namespace.

options:
    resource_group:
        description:
            - Name of the resource group within the azure subscription.
        required: True
    namespace_name:
        description:
            - The Namespace name
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - Properties of sku resource
        suboptions:
            name:
                description:
                    - Name of this SKU.
                required: True
                choices:
                    - 'basic'
                    - 'standard'
            tier:
                description:
                    - The billing tier of this particular SKU.
                choices:
                    - 'basic'
                    - 'standard'
            capacity:
                description:
                    - The Event Hubs throughput units, vaule should be 0 to 20 throughput units.
    is_auto_inflate_enabled:
        description:
            - Value that indicates whether AutoInflate is enabled for eventhub namespace.
    maximum_throughput_units:
        description:
            - "Upper limit of throughput units when AutoInflate is enabled, vaule should be within 0 to 20 throughput units. ( '0' if AutoInflateEnabled =
               true)"
    kafka_enabled:
        description:
            - Value that indicates whether Kafka is enabled for eventhub namespace.
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
    azure_rm_eventhubnamespace:
      resource_group: ArunMonocle
      namespace_name: sdk-Namespace-5849
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
    sample: /subscriptions/5f750a97-50d9-4e36-8081-c9ee4c0210d4/resourceGroups/ArunMonocle/providers/Microsoft.EventHub/namespaces/sdk-Namespace-3668
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


class AzureRMNamespaces(AzureRMModuleBase):
    """Configuration class for an Azure RM Namespace resource"""

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
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            is_auto_inflate_enabled=dict(
                type='str'
            ),
            maximum_throughput_units=dict(
                type='int'
            ),
            kafka_enabled=dict(
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
                    if 'tier' in ev:
                        if ev['tier'] == 'basic':
                            ev['tier'] = 'Basic'
                        elif ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                    self.parameters["sku"] = ev
                elif key == "is_auto_inflate_enabled":
                    self.parameters["is_auto_inflate_enabled"] = kwargs[key]
                elif key == "maximum_throughput_units":
                    self.parameters["maximum_throughput_units"] = kwargs[key]
                elif key == "kafka_enabled":
                    self.parameters["kafka_enabled"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(EventHubManagementClient,
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
                self.log("Need to check if Namespace instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Namespace instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_namespace()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
        self.log("Creating / Updating the Namespace instance {0}".format(self.namespace_name))

        try:
            response = self.mgmt_client.namespaces.create_or_update(resource_group_name=self.resource_group,
                                                                    namespace_name=self.namespace_name,
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
        self.log("Deleting the Namespace instance {0}".format(self.namespace_name))
        try:
            response = self.mgmt_client.namespaces.delete(resource_group_name=self.resource_group,
                                                          namespace_name=self.namespace_name)
        except CloudError as e:
            self.log('Error attempting to delete the Namespace instance.')
            self.fail("Error deleting the Namespace instance: {0}".format(str(e)))

        return True

    def get_namespace(self):
        '''
        Gets the properties of the specified Namespace.

        :return: deserialized Namespace instance state dictionary
        '''
        self.log("Checking if the Namespace instance {0} is present".format(self.namespace_name))
        found = False
        try:
            response = self.mgmt_client.namespaces.get(resource_group_name=self.resource_group,
                                                       namespace_name=self.namespace_name)
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


def main():
    """Main execution"""
    AzureRMNamespaces()


if __name__ == '__main__':
    main()
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
module: azure_rm_powerbidedicatedcapacity
version_added: "2.8"
short_description: Manage Capacity instance.
description:
    - Create, update and delete instance of Capacity.

options:
    resource_group:
        description:
            - "The name of the Azure Resource group of which a given PowerBIDedicated capacity is part. This name must be at least 1 character in length,
               and no more than 90."
        required: True
    dedicated_capacity_name:
        description:
            - The name of the Dedicated capacity. It must be a minimum of 3 characters, and a maximum of 63.
        required: True
    location:
        description:
            - Location of the PowerBI Dedicated resource.
        required: True
    sku:
        description:
            - The SKU of the PowerBI Dedicated resource.
        required: True
        suboptions:
            name:
                description:
                    - Name of the SKU level.
                required: True
            tier:
                description:
                    - The name of the Azure pricing tier to which the SKU applies.
                choices:
                    - 'pbie_azure'
    administration:
        description:
            - A collection of Dedicated capacity administrators
        suboptions:
            members:
                description:
                    - An array of administrator user identities.
                type: list
    state:
      description:
        - Assert the state of the Capacity.
        - Use 'present' to create or update an Capacity and 'absent' to delete it.
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
  - name: Create (or update) Capacity
    azure_rm_powerbidedicatedcapacity:
      resource_group: TestRG
      dedicated_capacity_name: azsdktest
      location: West US
      sku:
        name: A1
        tier: PBIE_Azure
'''

RETURN = '''
id:
    description:
        - An identifier that represents the PowerBI Dedicated resource.
    returned: always
    type: str
    sample: /subscriptions/613192d7-503f-477a-9cfe-4efc3ee2bd60/resourceGroups/TestRG/providers/Microsoft.PowerBIDedicated/capacities/azsdktest
state:
    description:
        - "The current state of PowerBI Dedicated resource. The state is to indicate more states outside of resource provisioning. Possible values include:
           'Deleting', 'Succeeded', 'Failed', 'Paused', 'Suspended', 'Provisioning', 'Updating', 'Suspending', 'Pausing', 'Resuming', 'Preparing',
           'Scaling'"
    returned: always
    type: str
    sample: Provisioning
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.powerbidedicated import PowerBIDedicatedManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMCapacities(AzureRMModuleBase):
    """Configuration class for an Azure RM Capacity resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            dedicated_capacity_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            sku=dict(
                type='dict',
                required=True
            ),
            administration=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.dedicated_capacity_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCapacities, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                    if 'tier' in ev:
                        if ev['tier'] == 'pbie_azure':
                            ev['tier'] = 'PBIE_Azure'
                    self.parameters["sku"] = ev
                elif key == "administration":
                    self.parameters["administration"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(PowerBIDedicatedManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_capacity()

        if not old_response:
            self.log("Capacity instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Capacity instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Capacity instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Capacity instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_capacity()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Capacity instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_capacity()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_capacity():
                time.sleep(20)
        else:
            self.log("Capacity instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_capacity(self):
        '''
        Creates or updates Capacity with the specified configuration.

        :return: deserialized Capacity instance state dictionary
        '''
        self.log("Creating / Updating the Capacity instance {0}".format(self.dedicated_capacity_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.capacities.create(resource_group_name=self.resource_group,
                                                              dedicated_capacity_name=self.dedicated_capacity_name,
                                                              capacity_parameters=self.parameters)
            else:
                response = self.mgmt_client.capacities.update(resource_group_name=self.resource_group,
                                                              dedicated_capacity_name=self.dedicated_capacity_name,
                                                              capacity_update_parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Capacity instance.')
            self.fail("Error creating the Capacity instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_capacity(self):
        '''
        Deletes specified Capacity instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Capacity instance {0}".format(self.dedicated_capacity_name))
        try:
            response = self.mgmt_client.capacities.delete(resource_group_name=self.resource_group,
                                                          dedicated_capacity_name=self.dedicated_capacity_name)
        except CloudError as e:
            self.log('Error attempting to delete the Capacity instance.')
            self.fail("Error deleting the Capacity instance: {0}".format(str(e)))

        return True

    def get_capacity(self):
        '''
        Gets the properties of the specified Capacity.

        :return: deserialized Capacity instance state dictionary
        '''
        self.log("Checking if the Capacity instance {0} is present".format(self.dedicated_capacity_name))
        found = False
        try:
            response = self.mgmt_client.capacities.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Capacity instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Capacity instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMCapacities()


if __name__ == '__main__':
    main()

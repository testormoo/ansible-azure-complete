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
module: azure_rm_computeavailabilityset
version_added: "2.8"
short_description: Manage Availability Set instance.
description:
    - Create, update and delete instance of Availability Set.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    availability_set_name:
        description:
            - The name of the availability set.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    platform_update_domain_count:
        description:
            - Update Domain count.
    platform_fault_domain_count:
        description:
            - Fault Domain count.
    virtual_machines:
        description:
            - A list of references to all virtual machines in the availability set.
        type: list
        suboptions:
            id:
                description:
                    - Resource Id
    sku:
        description:
            - "Sku of the availability set, only name is required to be set. See AvailabilitySetSkuTypes for possible set of values. Use 'Aligned' for
               virtual machines with managed disks and 'Classic' for virtual machines with unmanaged disks. Default value is 'Classic'."
        suboptions:
            name:
                description:
                    - The sku name.
            tier:
                description:
                    - "Specifies the tier of virtual machines in a scale set.<br /><br /> Possible Values:<br /><br /> **Standard**<br /><br /> **Basic**"
            capacity:
                description:
                    - Specifies the number of virtual machines in the scale set.
    state:
      description:
        - Assert the state of the Availability Set.
        - Use 'present' to create or update an Availability Set and 'absent' to delete it.
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
  - name: Create (or update) Availability Set
    azure_rm_computeavailabilityset:
      resource_group: myResourceGroup
      availability_set_name: myAvailabilitySet
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.compute import ComputeManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAvailabilitySets(AzureRMModuleBase):
    """Configuration class for an Azure RM Availability Set resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            availability_set_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            platform_update_domain_count=dict(
                type='int'
            ),
            platform_fault_domain_count=dict(
                type='int'
            ),
            virtual_machines=dict(
                type='list'
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
        self.availability_set_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAvailabilitySets, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "platform_update_domain_count":
                    self.parameters["platform_update_domain_count"] = kwargs[key]
                elif key == "platform_fault_domain_count":
                    self.parameters["platform_fault_domain_count"] = kwargs[key]
                elif key == "virtual_machines":
                    self.parameters["virtual_machines"] = kwargs[key]
                elif key == "sku":
                    self.parameters["sku"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ComputeManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_availabilityset()

        if not old_response:
            self.log("Availability Set instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Availability Set instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Availability Set instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Availability Set instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_availabilityset()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Availability Set instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_availabilityset()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_availabilityset():
                time.sleep(20)
        else:
            self.log("Availability Set instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_availabilityset(self):
        '''
        Creates or updates Availability Set with the specified configuration.

        :return: deserialized Availability Set instance state dictionary
        '''
        self.log("Creating / Updating the Availability Set instance {0}".format(self.availability_set_name))

        try:
            response = self.mgmt_client.availability_sets.create_or_update(resource_group_name=self.resource_group,
                                                                           availability_set_name=self.availability_set_name,
                                                                           parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Availability Set instance.')
            self.fail("Error creating the Availability Set instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_availabilityset(self):
        '''
        Deletes specified Availability Set instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Availability Set instance {0}".format(self.availability_set_name))
        try:
            response = self.mgmt_client.availability_sets.delete(resource_group_name=self.resource_group,
                                                                 availability_set_name=self.availability_set_name)
        except CloudError as e:
            self.log('Error attempting to delete the Availability Set instance.')
            self.fail("Error deleting the Availability Set instance: {0}".format(str(e)))

        return True

    def get_availabilityset(self):
        '''
        Gets the properties of the specified Availability Set.

        :return: deserialized Availability Set instance state dictionary
        '''
        self.log("Checking if the Availability Set instance {0} is present".format(self.availability_set_name))
        found = False
        try:
            response = self.mgmt_client.availability_sets.get(resource_group_name=self.resource_group,
                                                              availability_set_name=self.availability_set_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Availability Set instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Availability Set instance.')
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
    AzureRMAvailabilitySets()


if __name__ == '__main__':
    main()

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
module: azure_rm_dedicatedhsm
version_added: "2.8"
short_description: Manage Dedicated Hsm instance.
description:
    - Create, update and delete instance of Dedicated Hsm.

options:
    resource_group:
        description:
            - The name of the Resource Group to which the resource belongs.
        required: True
    name:
        description:
            - Name of the dedicated Hsm
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - SKU details
        suboptions:
            name:
                description:
                    - SKU of the dedicated HSM.
                choices:
                    - 'safe_net _luna _network _hsm _a790'
    zones:
        description:
            - The Dedicated Hsm zones.
        type: list
    network_profile:
        description:
            - Specifies the network interfaces of the dedicated hsm.
        suboptions:
            subnet:
                description:
                    - Specifies the identifier of the subnet.
                suboptions:
                    id:
                        description:
                            - The ARM resource id in the form of /subscriptions/{SubcriptionId}/resourceGroups/{ResourceGroupName}/...
            network_interfaces:
                description:
                    - Specifies the list of resource Ids for the network interfaces associated with the dedicated HSM.
                type: list
                suboptions:
                    private_ip_address:
                        description:
                            - Private Ip address of the interface
    stamp_id:
        description:
            - This field will be used when RP does not support Availability I(zones).
    state:
      description:
        - Assert the state of the Dedicated Hsm.
        - Use 'present' to create or update an Dedicated Hsm and 'absent' to delete it.
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
  - name: Create (or update) Dedicated Hsm
    azure_rm_dedicatedhsm:
      resource_group: hsm-group
      name: hsm1
      location: eastus
      sku:
        name: SafeNet Luna Network HSM A790
'''

RETURN = '''
id:
    description:
        - The Azure Resource Manager resource ID for the dedicated HSM.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/hsm-group/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/hsm1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.dedicatedhsm import AzureDedicatedHSMResourceProvider
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMDedicatedHsm(AzureRMModuleBase):
    """Configuration class for an Azure RM Dedicated Hsm resource"""

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
            zones=dict(
                type='list'
            ),
            network_profile=dict(
                type='dict'
            ),
            stamp_id=dict(
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
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDedicatedHsm, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                        if ev['name'] == 'safe_net _luna _network _hsm _a790':
                            ev['name'] = 'SafeNet Luna Network HSM A790'
                    self.parameters["sku"] = ev
                elif key == "zones":
                    self.parameters["zones"] = kwargs[key]
                elif key == "network_profile":
                    self.parameters["network_profile"] = kwargs[key]
                elif key == "stamp_id":
                    self.parameters["stamp_id"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureDedicatedHSMResourceProvider,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_dedicatedhsm()

        if not old_response:
            self.log("Dedicated Hsm instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Dedicated Hsm instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Dedicated Hsm instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dedicated Hsm instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dedicatedhsm()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dedicated Hsm instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dedicatedhsm()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_dedicatedhsm():
                time.sleep(20)
        else:
            self.log("Dedicated Hsm instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_dedicatedhsm(self):
        '''
        Creates or updates Dedicated Hsm with the specified configuration.

        :return: deserialized Dedicated Hsm instance state dictionary
        '''
        self.log("Creating / Updating the Dedicated Hsm instance {0}".format(self.name))

        try:
            response = self.mgmt_client.dedicated_hsm.create_or_update(resource_group_name=self.resource_group,
                                                                       name=self.name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Dedicated Hsm instance.')
            self.fail("Error creating the Dedicated Hsm instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_dedicatedhsm(self):
        '''
        Deletes specified Dedicated Hsm instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Dedicated Hsm instance {0}".format(self.name))
        try:
            response = self.mgmt_client.dedicated_hsm.delete(resource_group_name=self.resource_group,
                                                             name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Dedicated Hsm instance.')
            self.fail("Error deleting the Dedicated Hsm instance: {0}".format(str(e)))

        return True

    def get_dedicatedhsm(self):
        '''
        Gets the properties of the specified Dedicated Hsm.

        :return: deserialized Dedicated Hsm instance state dictionary
        '''
        self.log("Checking if the Dedicated Hsm instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.dedicated_hsm.get(resource_group_name=self.resource_group,
                                                          name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Dedicated Hsm instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Dedicated Hsm instance.')
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
    AzureRMDedicatedHsm()


if __name__ == '__main__':
    main()

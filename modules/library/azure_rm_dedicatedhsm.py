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
short_description: Manage Azure Dedicated Hsm instance.
description:
    - Create, update and delete instance of Azure Dedicated Hsm.

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
      network_profile:
        subnet:
          id: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/hsm-group/providers/Microsoft.Network/virtualNetworks/stamp01/subnets/stamp01
        network_interfaces:
          - private_ip_address: 1.0.0.1
      stamp_id: stamp01
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['safe_net _luna _network _hsm _a790']
                    )
                )
            ),
            zones=dict(
                type='list'
            ),
            network_profile=dict(
                type='dict',
                options=dict(
                    subnet=dict(
                        type='dict',
                        options=dict(
                            id=dict(
                                type='str'
                            )
                        )
                    ),
                    network_interfaces=dict(
                        type='list',
                        options=dict(
                            private_ip_address=dict(
                                type='str'
                            )
                        )
                    )
                )
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
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_map(self.parameters, ['sku', 'name'], {'safe_net _luna _network _hsm _a790': 'SafeNet Luna Network HSM A790'})
        dict_resource_id(self.parameters, ['network_profile', 'subnet', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Dedicated Hsm instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_dedicatedhsm()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Dedicated Hsm instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_dedicatedhsm()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Dedicated Hsm instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMDedicatedHsm()


if __name__ == '__main__':
    main()

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
module: azure_rm_iothubprovisioningservicesiotdpsresource
version_added: "2.8"
short_description: Manage Azure Iot Dps Resource instance.
description:
    - Create, update and delete instance of Azure Iot Dps Resource.

options:
    resource_group:
        description:
            - Resource group identifier.
        required: True
    name:
        description:
            - Name of provisioning service to create or update.
        required: True
    location:
        description:
            - The resource location.
            - Required when C(state) is I(present).
    state:
        description:
            - Current state of the provisioning service.
        choices:
            - 'activating'
            - 'active'
            - 'deleting'
            - 'deleted'
            - 'activation_failed'
            - 'deletion_failed'
            - 'transitioning'
            - 'suspending'
            - 'suspended'
            - 'resuming'
            - 'failing_over'
            - 'failover_failed'
    iot_hubs:
        description:
            - List of IoT hubs assosciated with this provisioning service.
        type: list
        suboptions:
            apply_allocation_policy:
                description:
                    - flag for applying allocationPolicy or not for a given iot hub.
            allocation_weight:
                description:
                    - weight to apply for a given iot h.
            connection_string:
                description:
                    - Connection string og the IoT hub.
                    - Required when C(state) is I(present).
            location:
                description:
                    - ARM region of the IoT hub.
                    - Required when C(state) is I(present).
    allocation_policy:
        description:
            - Allocation policy to be used by this provisioning service.
        choices:
            - 'hashed'
            - 'geo_latency'
            - 'static'
    authorization_policies:
        description:
            - List of authorization keys for a provisioning service.
        type: list
        suboptions:
            key_name:
                description:
                    - Name of the key.
                    - Required when C(state) is I(present).
            primary_key:
                description:
                    - Primary SAS key value.
            secondary_key:
                description:
                    - Secondary SAS key value.
            rights:
                description:
                    - Rights that this key has.
                    - Required when C(state) is I(present).
                choices:
                    - 'service_config'
                    - 'enrollment_read'
                    - 'enrollment_write'
                    - 'device_connect'
                    - 'registration_status_read'
                    - 'registration_status_write'
    sku:
        description:
            - Sku info for a provisioning Service.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - Sku name.
                choices:
                    - 's1'
            capacity:
                description:
                    - The number of units to provision
    state:
      description:
        - Assert the state of the Iot Dps Resource.
        - Use 'present' to create or update an Iot Dps Resource and 'absent' to delete it.
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
  - name: Create (or update) Iot Dps Resource
    azure_rm_iothubprovisioningservicesiotdpsresource:
      resource_group: myResourceGroup
      name: myFirstProvisioningService
      location: East US
      sku:
        name: S1
        capacity: 1
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: "/subscriptions/91d12660-3dec-467a-be2a-213b5544ddc0/resourceGroups/myResourceGroup/providers/Microsoft.Devices/ProvisioningServices/myFirstProvi
            sioningService"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.iothubprovisioningservices import IotDpsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIotDpsResource(AzureRMModuleBase):
    """Configuration class for an Azure RM Iot Dps Resource resource"""

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
            state=dict(
                type='str',
                choices=['activating',
                         'active',
                         'deleting',
                         'deleted',
                         'activation_failed',
                         'deletion_failed',
                         'transitioning',
                         'suspending',
                         'suspended',
                         'resuming',
                         'failing_over',
                         'failover_failed']
            ),
            iot_hubs=dict(
                type='list',
                options=dict(
                    apply_allocation_policy=dict(
                        type='str'
                    ),
                    allocation_weight=dict(
                        type='int'
                    ),
                    connection_string=dict(
                        type='str'
                    ),
                    location=dict(
                        type='str'
                    )
                )
            ),
            allocation_policy=dict(
                type='str',
                choices=['hashed',
                         'geo_latency',
                         'static']
            ),
            authorization_policies=dict(
                type='list',
                options=dict(
                    key_name=dict(
                        type='str'
                    ),
                    primary_key=dict(
                        type='str'
                    ),
                    secondary_key=dict(
                        type='str'
                    ),
                    rights=dict(
                        type='str',
                        choices=['service_config',
                                 'enrollment_read',
                                 'enrollment_write',
                                 'device_connect',
                                 'registration_status_read',
                                 'registration_status_write']
                    )
                )
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['s1']
                    ),
                    capacity=dict(
                        type='int'
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.iot_dps_description = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIotDpsResource, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.iot_dps_description[key] = kwargs[key]

        dict_expand(self.iot_dps_description, ['state'])
        dict_camelize(self.iot_dps_description, ['state'], True)
        dict_expand(self.iot_dps_description, ['iot_hubs'])
        dict_expand(self.iot_dps_description, ['allocation_policy'])
        dict_camelize(self.iot_dps_description, ['allocation_policy'], True)
        dict_camelize(self.iot_dps_description, ['authorization_policies', 'rights'], True)
        dict_expand(self.iot_dps_description, ['authorization_policies'])
        dict_camelize(self.iot_dps_description, ['sku', 'name'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(IotDpsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_iotdpsresource()

        if not old_response:
            self.log("Iot Dps Resource instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Iot Dps Resource instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.iot_dps_description, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Iot Dps Resource instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_iotdpsresource()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Iot Dps Resource instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_iotdpsresource()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Iot Dps Resource instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_iotdpsresource(self):
        '''
        Creates or updates Iot Dps Resource with the specified configuration.

        :return: deserialized Iot Dps Resource instance state dictionary
        '''
        self.log("Creating / Updating the Iot Dps Resource instance {0}".format(self.resource_group))

        try:
            response = self.mgmt_client.iot_dps_resource.create_or_update(resource_group_name=self.resource_group,
                                                                          provisioning_service_name=self.name,
                                                                          iot_dps_description=self.iot_dps_description)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Iot Dps Resource instance.')
            self.fail("Error creating the Iot Dps Resource instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_iotdpsresource(self):
        '''
        Deletes specified Iot Dps Resource instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Iot Dps Resource instance {0}".format(self.resource_group))
        try:
            response = self.mgmt_client.iot_dps_resource.delete(provisioning_service_name=self.name,
                                                                resource_group_name=self.resource_group)
        except CloudError as e:
            self.log('Error attempting to delete the Iot Dps Resource instance.')
            self.fail("Error deleting the Iot Dps Resource instance: {0}".format(str(e)))

        return True

    def get_iotdpsresource(self):
        '''
        Gets the properties of the specified Iot Dps Resource.

        :return: deserialized Iot Dps Resource instance state dictionary
        '''
        self.log("Checking if the Iot Dps Resource instance {0} is present".format(self.resource_group))
        found = False
        try:
            response = self.mgmt_client.iot_dps_resource.get(provisioning_service_name=self.name,
                                                             resource_group_name=self.resource_group)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Iot Dps Resource instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Iot Dps Resource instance.')
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


def main():
    """Main execution"""
    AzureRMIotDpsResource()


if __name__ == '__main__':
    main()

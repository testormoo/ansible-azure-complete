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
short_description: Manage Iot Dps Resource instance.
description:
    - Create, update and delete instance of Iot Dps Resource.

options:
    resource_group:
        description:
            - Resource group identifier.
        required: True
    provisioning_service_name:
        description:
            - Name of provisioning service to create or update.
        required: True
    iot_dps_description:
        description:
            - Description of the provisioning service to create or update.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
                required: True
            etag:
                description:
                    - "The Etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal ETag
                       convention."
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
            provisioning_state:
                description:
                    - The ARM provisioning I(state) of the provisioning service.
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
                        required: True
                    location:
                        description:
                            - ARM region of the IoT hub.
                        required: True
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
                        required: True
                    primary_key:
                        description:
                            - Primary SAS key value.
                    secondary_key:
                        description:
                            - Secondary SAS key value.
                    rights:
                        description:
                            - Rights that this key has.
                        required: True
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
                required: True
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
      provisioning_service_name: myFirstProvisioningService
      iot_dps_description:
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
            provisioning_service_name=dict(
                type='str',
                required=True
            ),
            iot_dps_description=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.provisioning_service_name = None
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
                if key == "location":
                    self.iot_dps_description["location"] = kwargs[key]
                elif key == "etag":
                    self.iot_dps_description["etag"] = kwargs[key]
                elif key == "state":
                    self.iot_dps_description.setdefault("properties", {})["state"] = _snake_to_camel(kwargs[key], True)
                elif key == "provisioning_state":
                    self.iot_dps_description.setdefault("properties", {})["provisioning_state"] = kwargs[key]
                elif key == "iot_hubs":
                    self.iot_dps_description.setdefault("properties", {})["iot_hubs"] = kwargs[key]
                elif key == "allocation_policy":
                    self.iot_dps_description.setdefault("properties", {})["allocation_policy"] = _snake_to_camel(kwargs[key], True)
                elif key == "authorization_policies":
                    ev = kwargs[key]
                    if 'rights' in ev:
                        if ev['rights'] == 'service_config':
                            ev['rights'] = 'ServiceConfig'
                        elif ev['rights'] == 'enrollment_read':
                            ev['rights'] = 'EnrollmentRead'
                        elif ev['rights'] == 'enrollment_write':
                            ev['rights'] = 'EnrollmentWrite'
                        elif ev['rights'] == 'device_connect':
                            ev['rights'] = 'DeviceConnect'
                        elif ev['rights'] == 'registration_status_read':
                            ev['rights'] = 'RegistrationStatusRead'
                        elif ev['rights'] == 'registration_status_write':
                            ev['rights'] = 'RegistrationStatusWrite'
                    self.iot_dps_description.setdefault("properties", {})["authorization_policies"] = ev
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 's1':
                            ev['name'] = 'S1'
                    self.iot_dps_description["sku"] = ev

        old_response = None
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
                self.log("Need to check if Iot Dps Resource instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Iot Dps Resource instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_iotdpsresource()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Iot Dps Resource instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_iotdpsresource()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_iotdpsresource():
                time.sleep(20)
        else:
            self.log("Iot Dps Resource instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_iotdpsresource(self):
        '''
        Creates or updates Iot Dps Resource with the specified configuration.

        :return: deserialized Iot Dps Resource instance state dictionary
        '''
        self.log("Creating / Updating the Iot Dps Resource instance {0}".format(self.resource_group))

        try:
            response = self.mgmt_client.iot_dps_resource.create_or_update(resource_group_name=self.resource_group,
                                                                          provisioning_service_name=self.provisioning_service_name,
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
            response = self.mgmt_client.iot_dps_resource.delete(provisioning_service_name=self.provisioning_service_name,
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
            response = self.mgmt_client.iot_dps_resource.get(provisioning_service_name=self.provisioning_service_name,
                                                             resource_group_name=self.resource_group)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Iot Dps Resource instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Iot Dps Resource instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMIotDpsResource()


if __name__ == '__main__':
    main()

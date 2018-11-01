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
module: azure_rm_notificationhubsnamespace
version_added: "2.8"
short_description: Manage Namespace instance.
description:
    - Create, update and delete instance of Namespace.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    namespace_name:
        description:
            - The namespace name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The sku of the created namespace
        suboptions:
            name:
                description:
                    - Name of the notification hub sku.
                required: True
                choices:
                    - 'free'
                    - 'basic'
                    - 'standard'
            tier:
                description:
                    - The tier of particular sku
            size:
                description:
                    - The Sku size
            family:
                description:
                    - The Sku Family
            capacity:
                description:
                    - The capacity of the resource
    namespace_create_or_update_parameters_name:
        description:
            - The name of the namespace.
    provisioning_state:
        description:
            - Provisioning state of the Namespace.
    region:
        description:
            - "Specifies the targeted region in which the namespace should be created. It can be any of the following values: Australia EastAustralia
               SoutheastCentral USEast USEast US 2West USNorth Central USSouth Central USEast AsiaSoutheast AsiaBrazil SouthJapan EastJapan WestNorth
               EuropeWest Europe"
    status:
        description:
            - "Status of the namespace. It can be any of these values:1 = Created/Active2 = Creating3 = Suspended4 = Deleting"
    created_at:
        description:
            - The time the namespace was created.
    updated_at:
        description:
            - The time the namespace was updated.
    service_bus_endpoint:
        description:
            - Endpoint you can use to perform C(notification_hub) operations.
    subscription_id:
        description:
            - The Id of the Azure subscription associated with the namespace.
    scale_unit:
        description:
            - ScaleUnit where the namespace gets created
    enabled:
        description:
            - Whether or not the namespace is currently enabled.
    critical:
        description:
            - Whether or not the namespace is set as Critical.
    data_center:
        description:
            - Data center for the namespace
    namespace_type:
        description:
            - The namespace type.
        choices:
            - 'messaging'
            - 'notification_hub'
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
    azure_rm_notificationhubsnamespace:
      resource_group: 5ktrial
      namespace_name: nh-sdk-ns
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
    sample: /subscriptions/29cfa613-cbbc-4512-b1d6-1b3a92c7fa40/resourceGroups/ArunMonocle/providers/Microsoft.NotificationHubs/namespaces/sdk-Namespace-2924
status:
    description:
        - "Status of the namespace. It can be any of these values:1 = Created/Active2 = Creating3 = Suspended4 = Deleting"
    returned: always
    type: str
    sample: status
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.notificationhubs import NotificationHubsManagementClient
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
            namespace_create_or_update_parameters_name=dict(
                type='str'
            ),
            provisioning_state=dict(
                type='str'
            ),
            region=dict(
                type='str'
            ),
            status=dict(
                type='str'
            ),
            created_at=dict(
                type='datetime'
            ),
            updated_at=dict(
                type='datetime'
            ),
            service_bus_endpoint=dict(
                type='str'
            ),
            subscription_id=dict(
                type='str'
            ),
            scale_unit=dict(
                type='str'
            ),
            enabled=dict(
                type='str'
            ),
            critical=dict(
                type='str'
            ),
            data_center=dict(
                type='str'
            ),
            namespace_type=dict(
                type='str',
                choices=['messaging',
                         'notification_hub']
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
                        if ev['name'] == 'free':
                            ev['name'] = 'Free'
                        elif ev['name'] == 'basic':
                            ev['name'] = 'Basic'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                    self.parameters["sku"] = ev
                elif key == "namespace_create_or_update_parameters_name":
                    self.parameters["namespace_create_or_update_parameters_name"] = kwargs[key]
                elif key == "provisioning_state":
                    self.parameters["provisioning_state"] = kwargs[key]
                elif key == "region":
                    self.parameters["region"] = kwargs[key]
                elif key == "status":
                    self.parameters["status"] = kwargs[key]
                elif key == "created_at":
                    self.parameters["created_at"] = kwargs[key]
                elif key == "updated_at":
                    self.parameters["updated_at"] = kwargs[key]
                elif key == "service_bus_endpoint":
                    self.parameters["service_bus_endpoint"] = kwargs[key]
                elif key == "subscription_id":
                    self.parameters["subscription_id"] = kwargs[key]
                elif key == "scale_unit":
                    self.parameters["scale_unit"] = kwargs[key]
                elif key == "enabled":
                    self.parameters["enabled"] = kwargs[key]
                elif key == "critical":
                    self.parameters["critical"] = kwargs[key]
                elif key == "data_center":
                    self.parameters["data_center"] = kwargs[key]
                elif key == "namespace_type":
                    self.parameters["namespace_type"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NotificationHubsManagementClient,
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
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMNamespaces()


if __name__ == '__main__':
    main()

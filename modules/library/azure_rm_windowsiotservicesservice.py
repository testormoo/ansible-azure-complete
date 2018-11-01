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
module: azure_rm_windowsiotservicesservice
version_added: "2.8"
short_description: Manage Service instance.
description:
    - Create, update and delete instance of Service.

options:
    resource_group:
        description:
            - The name of the resource group that contains the Windows IoT Device Service.
        required: True
    device_name:
        description:
            - The name of the Windows IoT Device Service.
        required: True
    device_service:
        description:
            - The Windows IoT Device Service metadata and security metadata.
        required: True
        suboptions:
            location:
                description:
                    - The Azure Region where the resource lives
            etag:
                description:
                    - "The Etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal ETag
                       convention."
            notes:
                description:
                    - Windows IoT Device Service notes.
            quantity:
                description:
                    - Windows IoT Device Service device allocation,
            admin_domain_name:
                description:
                    - Windows IoT Device Service OEM AAD domain
    if_match:
        description:
            - "ETag of the Windows IoT Device Service. Do not specify for creating a new Windows IoT Device Service. Required to update an existing Windows
               IoT Device Service."
    state:
      description:
        - Assert the state of the Service.
        - Use 'present' to create or update an Service and 'absent' to delete it.
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
  - name: Create (or update) Service
    azure_rm_windowsiotservicesservice:
      resource_group: res9101
      device_name: service4445
      device_service:
        notes: blah
        quantity: 1000000
        admin_domain_name: d.e.f
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
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
    from azure.mgmt.windowsiotservices import DeviceServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMServices(AzureRMModuleBase):
    """Configuration class for an Azure RM Service resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            device_name=dict(
                type='str',
                required=True
            ),
            device_service=dict(
                type='dict',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.device_name = None
        self.device_service = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMServices, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.device_service["location"] = kwargs[key]
                elif key == "etag":
                    self.device_service["etag"] = kwargs[key]
                elif key == "notes":
                    self.device_service["notes"] = kwargs[key]
                elif key == "quantity":
                    self.device_service["quantity"] = kwargs[key]
                elif key == "admin_domain_name":
                    self.device_service["admin_domain_name"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DeviceServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_service()

        if not old_response:
            self.log("Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Service instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_service()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_service()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_service():
                time.sleep(20)
        else:
            self.log("Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_service(self):
        '''
        Creates or updates Service with the specified configuration.

        :return: deserialized Service instance state dictionary
        '''
        self.log("Creating / Updating the Service instance {0}".format(self.device_name))

        try:
            response = self.mgmt_client.services.create_or_update(resource_group_name=self.resource_group,
                                                                  device_name=self.device_name,
                                                                  device_service=self.device_service)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Service instance.')
            self.fail("Error creating the Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_service(self):
        '''
        Deletes specified Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Service instance {0}".format(self.device_name))
        try:
            response = self.mgmt_client.services.delete(resource_group_name=self.resource_group,
                                                        device_name=self.device_name)
        except CloudError as e:
            self.log('Error attempting to delete the Service instance.')
            self.fail("Error deleting the Service instance: {0}".format(str(e)))

        return True

    def get_service(self):
        '''
        Gets the properties of the specified Service.

        :return: deserialized Service instance state dictionary
        '''
        self.log("Checking if the Service instance {0} is present".format(self.device_name))
        found = False
        try:
            response = self.mgmt_client.services.get(resource_group_name=self.resource_group,
                                                     device_name=self.device_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Service instance.')
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
    AzureRMServices()


if __name__ == '__main__':
    main()

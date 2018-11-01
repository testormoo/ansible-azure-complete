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
module: azure_rm_datamigrationservice
version_added: "2.8"
short_description: Manage Service instance.
description:
    - Create, update and delete instance of Service.

options:
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    etag:
        description:
            - HTTP strong entity tag value. Ignored if submitted
    kind:
        description:
            - "The resource kind. Only 'vm' (the default) is supported."
    public_key:
        description:
            - The public key of the service, used to encrypt secrets sent to the service
    virtual_subnet_id:
        description:
            - The ID of the Microsoft.Network/virtualNetworks/subnets resource to which the service should be joined
        required: True
    sku:
        description:
            - Service SKU
        suboptions:
            name:
                description:
                    - "The unique name of the SKU, such as 'P3'"
            tier:
                description:
                    - "The tier of the SKU, such as 'Basic', 'General Purpose', or 'Business Critical'"
            family:
                description:
                    - "The SKU family, used when the service has multiple performance classes within a I(tier), such as 'A', 'D', etc. for virtual machines"
            size:
                description:
                    - "The size of the SKU, used when the name alone does not denote a service size or when a SKU has multiple performance classes within a
                       I(family), e.g. 'A1' for virtual machines"
            capacity:
                description:
                    - The capacity of the SKU, if it supports scaling
    group_name:
        description:
            - Name of the resource group
        required: True
    service_name:
        description:
            - Name of the service
        required: True
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
    azure_rm_datamigrationservice:
      location: eastus
      sku:
        name: Basic_1vCore
      group_name: DmsSdkRg
      service_name: DmsSdkService
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/fc04246f-04c5-437e-ac5e-206a19e7193f/resourceGroups/DmsSdkRg/providers/Microsoft.DataMigration/services/DmsSdkService
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datamigration import DataMigrationServiceClient
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
            location=dict(
                type='str'
            ),
            etag=dict(
                type='str'
            ),
            kind=dict(
                type='str'
            ),
            public_key=dict(
                type='str'
            ),
            virtual_subnet_id=dict(
                type='str',
                required=True
            ),
            sku=dict(
                type='dict'
            ),
            group_name=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.parameters = dict()
        self.group_name = None
        self.service_name = None

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
                    self.parameters["location"] = kwargs[key]
                elif key == "etag":
                    self.parameters["etag"] = kwargs[key]
                elif key == "kind":
                    self.parameters["kind"] = kwargs[key]
                elif key == "public_key":
                    self.parameters["public_key"] = kwargs[key]
                elif key == "virtual_subnet_id":
                    self.parameters["virtual_subnet_id"] = kwargs[key]
                elif key == "sku":
                    self.parameters["sku"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataMigrationServiceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

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
        self.log("Creating / Updating the Service instance {0}".format(self.service_name))

        try:
            response = self.mgmt_client.services.create_or_update(parameters=self.parameters,
                                                                  group_name=self.group_name,
                                                                  service_name=self.service_name)
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
        self.log("Deleting the Service instance {0}".format(self.service_name))
        try:
            response = self.mgmt_client.services.delete(group_name=self.group_name,
                                                        service_name=self.service_name)
        except CloudError as e:
            self.log('Error attempting to delete the Service instance.')
            self.fail("Error deleting the Service instance: {0}".format(str(e)))

        return True

    def get_service(self):
        '''
        Gets the properties of the specified Service.

        :return: deserialized Service instance state dictionary
        '''
        self.log("Checking if the Service instance {0} is present".format(self.service_name))
        found = False
        try:
            response = self.mgmt_client.services.get(group_name=self.group_name,
                                                     service_name=self.service_name)
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

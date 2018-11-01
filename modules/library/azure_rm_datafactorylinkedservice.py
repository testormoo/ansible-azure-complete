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
module: azure_rm_datafactorylinkedservice
version_added: "2.8"
short_description: Manage Linked Service instance.
description:
    - Create, update and delete instance of Linked Service.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    factory_name:
        description:
            - The factory name.
        required: True
    linked_service_name:
        description:
            - The linked service name.
        required: True
    if_match:
        description:
            - "ETag of the linkedService entity.  Should only be specified for update, for which it should match existing entity or can be * for
               unconditional update."
    additional_properties:
        description:
            - Unmatched properties from the message are deserialized this collection
    connect_via:
        description:
            - The integration runtime reference.
        suboptions:
            type:
                description:
                    - Type of integration runtime.
                required: True
            reference_name:
                description:
                    - Reference integration runtime name.
                required: True
            parameters:
                description:
                    - Arguments for integration runtime.
    description:
        description:
            - Linked service description.
    parameters:
        description:
            - Parameters for linked service.
    annotations:
        description:
            - List of tags that can be used for describing the Dataset.
        type: list
    type:
        description:
            - Constant filled by server.
        required: True
    state:
      description:
        - Assert the state of the Linked Service.
        - Use 'present' to create or update an Linked Service and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Linked Service
    azure_rm_datafactorylinkedservice:
      resource_group: exampleResourceGroup
      factory_name: exampleFactoryName
      linked_service_name: exampleLinkedService
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: "/subscriptions/12345678-1234-1234-1234-12345678abc/resourceGroups/exampleResourceGroup/providers/Microsoft.DataFactory/factories/exampleFactoryN
            ame/linkedservices/exampleLinkedService"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datafactory import DataFactoryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMLinkedServices(AzureRMModuleBase):
    """Configuration class for an Azure RM Linked Service resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            factory_name=dict(
                type='str',
                required=True
            ),
            linked_service_name=dict(
                type='str',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            additional_properties=dict(
                type='dict'
            ),
            connect_via=dict(
                type='dict'
            ),
            description=dict(
                type='str'
            ),
            parameters=dict(
                type='dict'
            ),
            annotations=dict(
                type='list'
            ),
            type=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.factory_name = None
        self.linked_service_name = None
        self.if_match = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLinkedServices, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "additional_properties":
                    self.properties["additional_properties"] = kwargs[key]
                elif key == "connect_via":
                    self.properties["connect_via"] = kwargs[key]
                elif key == "description":
                    self.properties["description"] = kwargs[key]
                elif key == "parameters":
                    self.properties["parameters"] = kwargs[key]
                elif key == "annotations":
                    self.properties["annotations"] = kwargs[key]
                elif key == "type":
                    self.properties["type"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DataFactoryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_linkedservice()

        if not old_response:
            self.log("Linked Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Linked Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Linked Service instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Linked Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_linkedservice()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Linked Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_linkedservice()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_linkedservice():
                time.sleep(20)
        else:
            self.log("Linked Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_linkedservice(self):
        '''
        Creates or updates Linked Service with the specified configuration.

        :return: deserialized Linked Service instance state dictionary
        '''
        self.log("Creating / Updating the Linked Service instance {0}".format(self.linked_service_name))

        try:
            response = self.mgmt_client.linked_services.create_or_update(resource_group_name=self.resource_group,
                                                                         factory_name=self.factory_name,
                                                                         linked_service_name=self.linked_service_name,
                                                                         properties=self.properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Linked Service instance.')
            self.fail("Error creating the Linked Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_linkedservice(self):
        '''
        Deletes specified Linked Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Linked Service instance {0}".format(self.linked_service_name))
        try:
            response = self.mgmt_client.linked_services.delete(resource_group_name=self.resource_group,
                                                               factory_name=self.factory_name,
                                                               linked_service_name=self.linked_service_name)
        except CloudError as e:
            self.log('Error attempting to delete the Linked Service instance.')
            self.fail("Error deleting the Linked Service instance: {0}".format(str(e)))

        return True

    def get_linkedservice(self):
        '''
        Gets the properties of the specified Linked Service.

        :return: deserialized Linked Service instance state dictionary
        '''
        self.log("Checking if the Linked Service instance {0} is present".format(self.linked_service_name))
        found = False
        try:
            response = self.mgmt_client.linked_services.get(resource_group_name=self.resource_group,
                                                            factory_name=self.factory_name,
                                                            linked_service_name=self.linked_service_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Linked Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Linked Service instance.')
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
    AzureRMLinkedServices()


if __name__ == '__main__':
    main()

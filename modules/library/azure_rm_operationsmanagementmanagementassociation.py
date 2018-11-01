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
module: azure_rm_operationsmanagementmanagementassociation
version_added: "2.8"
short_description: Manage Management Association instance.
description:
    - Create, update and delete instance of Management Association.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
        required: True
    self.config.provider_name:
        description:
            - Provider name for the parent resource.
        required: True
    self.config.resource_type:
        description:
            - Resource type for the parent resource
        required: True
    self.config.resource_name:
        description:
            - Parent resource name.
        required: True
    management_association_name:
        description:
            - User ManagementAssociation Name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    application_id:
        description:
            - The applicationId of the appliance for this association.
        required: True
    state:
      description:
        - Assert the state of the Management Association.
        - Use 'present' to create or update an Management Association and 'absent' to delete it.
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
  - name: Create (or update) Management Association
    azure_rm_operationsmanagementmanagementassociation:
      resource_group: rg1
      self.config.provider_name: NOT FOUND
      self.config.resource_type: NOT FOUND
      self.config.resource_name: NOT FOUND
      management_association_name: managementAssociation1
      location: eastus
      application_id: /subscriptions/sub1/resourcegroups/rg1/providers/Microsoft.Appliance/Appliances/appliance1
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/subid/resourcegroups/rg1/providers/Microsoft.OperationalInsights/workspaces/ws1/Microsoft.OperationsManagement/ManagementAssociat
            ions/managementAssociation1"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.operationsmanagement import OperationsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagementAssociations(AzureRMModuleBase):
    """Configuration class for an Azure RM Management Association resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            self.config.provider_name=dict(
                type='str',
                required=True
            ),
            self.config.resource_type=dict(
                type='str',
                required=True
            ),
            self.config.resource_name=dict(
                type='str',
                required=True
            ),
            management_association_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            application_id=dict(
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
        self.self.config.provider_name = None
        self.self.config.resource_type = None
        self.self.config.resource_name = None
        self.management_association_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagementAssociations, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "application_id":
                    self.parameters.setdefault("properties", {})["application_id"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(OperationsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_managementassociation()

        if not old_response:
            self.log("Management Association instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Management Association instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Management Association instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Management Association instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_managementassociation()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Management Association instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_managementassociation()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_managementassociation():
                time.sleep(20)
        else:
            self.log("Management Association instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_managementassociation(self):
        '''
        Creates or updates Management Association with the specified configuration.

        :return: deserialized Management Association instance state dictionary
        '''
        self.log("Creating / Updating the Management Association instance {0}".format(self.management_association_name))

        try:
            response = self.mgmt_client.management_associations.create_or_update(resource_group_name=self.resource_group,
                                                                                 self.config.provider_name=self.self.config.provider_name,
                                                                                 self.config.resource_type=self.self.config.resource_type,
                                                                                 self.config.resource_name=self.self.config.resource_name,
                                                                                 management_association_name=self.management_association_name,
                                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Management Association instance.')
            self.fail("Error creating the Management Association instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_managementassociation(self):
        '''
        Deletes specified Management Association instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Management Association instance {0}".format(self.management_association_name))
        try:
            response = self.mgmt_client.management_associations.delete(resource_group_name=self.resource_group,
                                                                       self.config.provider_name=self.self.config.provider_name,
                                                                       self.config.resource_type=self.self.config.resource_type,
                                                                       self.config.resource_name=self.self.config.resource_name,
                                                                       management_association_name=self.management_association_name)
        except CloudError as e:
            self.log('Error attempting to delete the Management Association instance.')
            self.fail("Error deleting the Management Association instance: {0}".format(str(e)))

        return True

    def get_managementassociation(self):
        '''
        Gets the properties of the specified Management Association.

        :return: deserialized Management Association instance state dictionary
        '''
        self.log("Checking if the Management Association instance {0} is present".format(self.management_association_name))
        found = False
        try:
            response = self.mgmt_client.management_associations.get(resource_group_name=self.resource_group,
                                                                    self.config.provider_name=self.self.config.provider_name,
                                                                    self.config.resource_type=self.self.config.resource_type,
                                                                    self.config.resource_name=self.self.config.resource_name,
                                                                    management_association_name=self.management_association_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Management Association instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Management Association instance.')
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
    AzureRMManagementAssociations()


if __name__ == '__main__':
    main()

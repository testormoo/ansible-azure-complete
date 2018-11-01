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
module: azure_rm_applicationinsightsworkitemconfiguration
version_added: "2.8"
short_description: Manage Work Item Configuration instance.
description:
    - Create, update and delete instance of Work Item Configuration.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    resource_name:
        description:
            - The name of the Application Insights component resource.
        required: True
    work_item_configuration_properties:
        description:
            - Properties that need to be specified to create a work item configuration of a Application Insights component.
        required: True
        suboptions:
            connector_id:
                description:
                    - Unique connector id
            connector_data_configuration:
                description:
                    - Serialized JSON object for detaile d properties
            validate_only:
                description:
                    - Boolean indicating validate only
            work_item_properties:
                description:
                    - Custom work item properties
    state:
      description:
        - Assert the state of the Work Item Configuration.
        - Use 'present' to create or update an Work Item Configuration and 'absent' to delete it.
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
  - name: Create (or update) Work Item Configuration
    azure_rm_applicationinsightsworkitemconfiguration:
      resource_group: my-resource-group
      resource_name: my-component
      work_item_configuration_properties:
        connector_id: d334e2a4-6733-488e-8645-a9fdc1694f41
        connector_data_configuration: {
  "VSOAccountBaseUrl": "https://testtodelete.visualstudio.com",
  "ProjectCollection": "DefaultCollection",
  "Project": "todeletefirst",
  "ResourceId": "d0662b05-439a-4a1b-840b-33a7f8b42ebf",
  "Custom": "{\"/fields/System.WorkItemType\":\"Bug\",\"/fields/System.AreaPath\":\"todeletefirst\",\"/fields/System.AssignedTo\":\"\"}"
}
        validate_only: true
        work_item_properties: [
  {
    "name": "Title",
    "value": "Validate Only Title"
  },
  {
    "name": "Description",
    "value": "Validate Only Description"
  }
]
'''

RETURN = '''
id:
    description:
        - Unique Id for work item
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
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWorkItemConfigurations(AzureRMModuleBase):
    """Configuration class for an Azure RM Work Item Configuration resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            work_item_configuration_properties=dict(
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
        self.resource_name = None
        self.work_item_configuration_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWorkItemConfigurations, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "connector_id":
                    self.work_item_configuration_properties["connector_id"] = kwargs[key]
                elif key == "connector_data_configuration":
                    self.work_item_configuration_properties["connector_data_configuration"] = kwargs[key]
                elif key == "validate_only":
                    self.work_item_configuration_properties["validate_only"] = kwargs[key]
                elif key == "work_item_properties":
                    self.work_item_configuration_properties["work_item_properties"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_workitemconfiguration()

        if not old_response:
            self.log("Work Item Configuration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Work Item Configuration instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Work Item Configuration instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Work Item Configuration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_workitemconfiguration()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Work Item Configuration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_workitemconfiguration()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_workitemconfiguration():
                time.sleep(20)
        else:
            self.log("Work Item Configuration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_workitemconfiguration(self):
        '''
        Creates or updates Work Item Configuration with the specified configuration.

        :return: deserialized Work Item Configuration instance state dictionary
        '''
        self.log("Creating / Updating the Work Item Configuration instance {0}".format(self.work_item_config_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.work_item_configurations.create(resource_group_name=self.resource_group,
                                                                            resource_name=self.resource_name,
                                                                            work_item_configuration_properties=self.work_item_configuration_properties)
            else:
                response = self.mgmt_client.work_item_configurations.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Work Item Configuration instance.')
            self.fail("Error creating the Work Item Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_workitemconfiguration(self):
        '''
        Deletes specified Work Item Configuration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Work Item Configuration instance {0}".format(self.work_item_config_id))
        try:
            response = self.mgmt_client.work_item_configurations.delete(resource_group_name=self.resource_group,
                                                                        resource_name=self.resource_name,
                                                                        work_item_config_id=self.work_item_config_id)
        except CloudError as e:
            self.log('Error attempting to delete the Work Item Configuration instance.')
            self.fail("Error deleting the Work Item Configuration instance: {0}".format(str(e)))

        return True

    def get_workitemconfiguration(self):
        '''
        Gets the properties of the specified Work Item Configuration.

        :return: deserialized Work Item Configuration instance state dictionary
        '''
        self.log("Checking if the Work Item Configuration instance {0} is present".format(self.work_item_config_id))
        found = False
        try:
            response = self.mgmt_client.work_item_configurations.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("Work Item Configuration instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Work Item Configuration instance.')
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
    AzureRMWorkItemConfigurations()


if __name__ == '__main__':
    main()

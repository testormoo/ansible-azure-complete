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
module: azure_rm_applicationinsightsexportconfiguration
version_added: "2.8"
short_description: Manage Azure Export Configuration instance.
description:
    - Create, update and delete instance of Azure Export Configuration.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Application Insights component resource.
        required: True
    record_types:
        description:
            - "The document types to be exported, as comma separated values. Allowed values include 'Requests', 'Event', 'Exceptions', 'Metrics',
               'PageViews', 'PageViewPerformance', 'Rdd', 'PerformanceCounters', 'Availability', 'Messages'."
    destination_type:
        description:
            - "The Continuous Export destination type. This has to be 'Blob'."
    destination_address:
        description:
            - The SAS URL for the destination storage container. It must grant write permission.
    is_enabled:
        description:
            - "Set to 'true' to create a Continuous Export configuration as enabled, otherwise set it to 'false'."
    notification_queue_enabled:
        description:
            - Deprecated
    notification_queue_uri:
        description:
            - Deprecated
    destination_storage_subscription_id:
        description:
            - The subscription ID of the destination storage container.
    destination_storage_location_id:
        description:
            - The location ID of the destination storage container.
    destination_account_id:
        description:
            - The name of destination storage account.
    state:
      description:
        - Assert the state of the Export Configuration.
        - Use 'present' to create or update an Export Configuration and 'absent' to delete it.
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
  - name: Create (or update) Export Configuration
    azure_rm_applicationinsightsexportconfiguration:
      resource_group: my-resource-group
      name: my-component
      record_types: Requests, Event, Exceptions, Metrics, PageViews, PageViewPerformance, Rdd, PerformanceCounters, Availability
      destination_type: Blob
      destination_address: https://mystorageblob.blob.core.windows.net/testexport?sv=2015-04-05&sr=c&sig=token
      is_enabled: true
      notification_queue_enabled: false
      destination_storage_subscription_id: subid
      destination_storage_location_id: eastus
      destination_account_id: /subscriptions/subid/resourceGroups/my-resource-group/providers/Microsoft.ClassicStorage/storageAccounts/mystorageblob
'''

RETURN = '''
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMExportConfiguration(AzureRMModuleBase):
    """Configuration class for an Azure RM Export Configuration resource"""

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
            record_types=dict(
                type='str'
            ),
            destination_type=dict(
                type='str'
            ),
            destination_address=dict(
                type='str'
            ),
            is_enabled=dict(
                type='str'
            ),
            notification_queue_enabled=dict(
                type='str'
            ),
            notification_queue_uri=dict(
                type='str'
            ),
            destination_storage_subscription_id=dict(
                type='str'
            ),
            destination_storage_location_id=dict(
                type='str'
            ),
            destination_account_id=dict(
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
        self.export_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMExportConfiguration, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.export_properties[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_exportconfiguration()

        if not old_response:
            self.log("Export Configuration instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Export Configuration instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.export_properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Export Configuration instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_exportconfiguration()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Export Configuration instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_exportconfiguration()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Export Configuration instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                })
        return self.results

    def create_update_exportconfiguration(self):
        '''
        Creates or updates Export Configuration with the specified configuration.

        :return: deserialized Export Configuration instance state dictionary
        '''
        self.log("Creating / Updating the Export Configuration instance {0}".format(self.export_id))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.export_configurations.create(resource_group_name=self.resource_group,
                                                                         resource_name=self.name,
                                                                         export_properties=self.export_properties)
            else:
                response = self.mgmt_client.export_configurations.update(resource_group_name=self.resource_group,
                                                                         resource_name=self.name,
                                                                         export_id=self.export_id,
                                                                         export_properties=self.export_properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Export Configuration instance.')
            self.fail("Error creating the Export Configuration instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_exportconfiguration(self):
        '''
        Deletes specified Export Configuration instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Export Configuration instance {0}".format(self.export_id))
        try:
            response = self.mgmt_client.export_configurations.delete(resource_group_name=self.resource_group,
                                                                     resource_name=self.name,
                                                                     export_id=self.export_id)
        except CloudError as e:
            self.log('Error attempting to delete the Export Configuration instance.')
            self.fail("Error deleting the Export Configuration instance: {0}".format(str(e)))

        return True

    def get_exportconfiguration(self):
        '''
        Gets the properties of the specified Export Configuration.

        :return: deserialized Export Configuration instance state dictionary
        '''
        self.log("Checking if the Export Configuration instance {0} is present".format(self.export_id))
        found = False
        try:
            response = self.mgmt_client.export_configurations.get(resource_group_name=self.resource_group,
                                                                  resource_name=self.name,
                                                                  export_id=self.export_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Export Configuration instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Export Configuration instance.')
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


def main():
    """Main execution"""
    AzureRMExportConfiguration()


if __name__ == '__main__':
    main()

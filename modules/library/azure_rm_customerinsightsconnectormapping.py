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
module: azure_rm_customerinsightsconnectormapping
version_added: "2.8"
short_description: Manage Connector Mapping instance.
description:
    - Create, update and delete instance of Connector Mapping.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    connector_name:
        description:
            - The name of the connector.
        required: True
    mapping_name:
        description:
            - The name of the connector mapping.
        required: True
    connector_type:
        description:
            - Type of connector.
        choices:
            - 'none'
            - 'crm'
            - 'azure_blob'
            - 'salesforce'
            - 'exchange_online'
            - 'outbound'
    entity_type:
        description:
            - Defines which entity type the file should map to.
        required: True
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    entity_type_name:
        description:
            - The mapping entity name.
        required: True
    display_name:
        description:
            - Display name for the connector mapping.
    description:
        description:
            - The description of the connector mapping.
    mapping_properties:
        description:
            - The properties of the mapping.
        required: True
        suboptions:
            folder_path:
                description:
                    - The folder path for the mapping.
            file_filter:
                description:
                    - The file filter for the mapping.
            has_header:
                description:
                    - If the file contains a header or not.
            error_management:
                description:
                    - The error management setting for the mapping.
                required: True
                suboptions:
                    error_management_type:
                        description:
                            - The type of error management to use for the mapping.
                        required: True
                        choices:
                            - 'reject_and_continue'
                            - 'stop_import'
                            - 'reject_until_limit'
                    error_limit:
                        description:
                            - The error limit allowed while importing data.
            format:
                description:
                    - The format of mapping property.
                required: True
                suboptions:
                    format_type:
                        description:
                            - The type mapping format.
                        required: True
                    column_delimiter:
                        description:
                            - The character that signifies a break between columns.
                    accept_language:
                        description:
                            - The oData language.
                    quote_character:
                        description:
                            - Quote character, used to indicate enquoted fields.
                    quote_escape_character:
                        description:
                            - Escape character for quotes, can be the same as the I(quote_character).
                    array_separator:
                        description:
                            - Character separating array elements.
            availability:
                description:
                    - The availability of mapping property.
                required: True
                suboptions:
                    frequency:
                        description:
                            - The frequency to update.
                        choices:
                            - 'minute'
                            - 'hour'
                            - 'day'
                            - 'week'
                            - 'month'
                    interval:
                        description:
                            - The interval of the given I(frequency) to use.
                        required: True
            structure:
                description:
                    - Ingestion mapping information at property level.
                required: True
                type: list
                suboptions:
                    property_name:
                        description:
                            - The property name of the mapping entity.
                        required: True
                    column_name:
                        description:
                            - The column name of the import file.
                        required: True
                    custom_format_specifier:
                        description:
                            - Custom format specifier for input parsing.
                    is_encrypted:
                        description:
                            - Indicates if the column is encrypted.
            complete_operation:
                description:
                    - The operation after import is done.
                required: True
                suboptions:
                    completion_operation_type:
                        description:
                            - The type of completion operation.
                        choices:
                            - 'do_nothing'
                            - 'delete_file'
                            - 'move_file'
                    destination_folder:
                        description:
                            - The destination folder where files will be moved to once the import is done.
    state:
      description:
        - Assert the state of the Connector Mapping.
        - Use 'present' to create or update an Connector Mapping and 'absent' to delete it.
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
  - name: Create (or update) Connector Mapping
    azure_rm_customerinsightsconnectormapping:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      connector_name: testConnector8858
      mapping_name: testMapping12491
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/sdkTestHub/connectors/tes
            tConnector8858/mappings/testMapping12491"
state:
    description:
        - "State of connector mapping. Possible values include: 'Creating', 'Created', 'Failed', 'Ready', 'Running', 'Stopped', 'Expiring'"
    returned: always
    type: str
    sample: Created
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMConnectorMappings(AzureRMModuleBase):
    """Configuration class for an Azure RM Connector Mapping resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            connector_name=dict(
                type='str',
                required=True
            ),
            mapping_name=dict(
                type='str',
                required=True
            ),
            connector_type=dict(
                type='str',
                choices=['none',
                         'crm',
                         'azure_blob',
                         'salesforce',
                         'exchange_online',
                         'outbound']
            ),
            entity_type=dict(
                type='str',
                choices=['none',
                         'profile',
                         'interaction',
                         'relationship'],
                required=True
            ),
            entity_type_name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            mapping_properties=dict(
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
        self.hub_name = None
        self.connector_name = None
        self.mapping_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConnectorMappings, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "connector_type":
                    ev = kwargs[key]
                    if ev == 'crm':
                        ev = 'CRM'
                    self.parameters["connector_type"] = _snake_to_camel(ev, True)
                elif key == "entity_type":
                    self.parameters["entity_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "entity_type_name":
                    self.parameters["entity_type_name"] = kwargs[key]
                elif key == "display_name":
                    self.parameters["display_name"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "mapping_properties":
                    self.parameters["mapping_properties"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_connectormapping()

        if not old_response:
            self.log("Connector Mapping instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Connector Mapping instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Connector Mapping instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Connector Mapping instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_connectormapping()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Connector Mapping instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_connectormapping()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_connectormapping():
                time.sleep(20)
        else:
            self.log("Connector Mapping instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_connectormapping(self):
        '''
        Creates or updates Connector Mapping with the specified configuration.

        :return: deserialized Connector Mapping instance state dictionary
        '''
        self.log("Creating / Updating the Connector Mapping instance {0}".format(self.mapping_name))

        try:
            response = self.mgmt_client.connector_mappings.create_or_update(resource_group_name=self.resource_group,
                                                                            hub_name=self.hub_name,
                                                                            connector_name=self.connector_name,
                                                                            mapping_name=self.mapping_name,
                                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Connector Mapping instance.')
            self.fail("Error creating the Connector Mapping instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_connectormapping(self):
        '''
        Deletes specified Connector Mapping instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Connector Mapping instance {0}".format(self.mapping_name))
        try:
            response = self.mgmt_client.connector_mappings.delete(resource_group_name=self.resource_group,
                                                                  hub_name=self.hub_name,
                                                                  connector_name=self.connector_name,
                                                                  mapping_name=self.mapping_name)
        except CloudError as e:
            self.log('Error attempting to delete the Connector Mapping instance.')
            self.fail("Error deleting the Connector Mapping instance: {0}".format(str(e)))

        return True

    def get_connectormapping(self):
        '''
        Gets the properties of the specified Connector Mapping.

        :return: deserialized Connector Mapping instance state dictionary
        '''
        self.log("Checking if the Connector Mapping instance {0} is present".format(self.mapping_name))
        found = False
        try:
            response = self.mgmt_client.connector_mappings.get(resource_group_name=self.resource_group,
                                                               hub_name=self.hub_name,
                                                               connector_name=self.connector_name,
                                                               mapping_name=self.mapping_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Connector Mapping instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Connector Mapping instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMConnectorMappings()


if __name__ == '__main__':
    main()

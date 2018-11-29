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
short_description: Manage Azure Connector Mapping instance.
description:
    - Create, update and delete instance of Azure Connector Mapping.

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
    name:
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
            - Required when C(state) is I(present).
        choices:
            - 'none'
            - 'profile'
            - 'interaction'
            - 'relationship'
    entity_type_name:
        description:
            - The mapping entity name.
            - Required when C(state) is I(present).
    display_name:
        description:
            - Display name for the connector mapping.
    description:
        description:
            - The description of the connector mapping.
    mapping_properties:
        description:
            - The properties of the mapping.
            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
                suboptions:
                    error_management_type:
                        description:
                            - The type of error management to use for the mapping.
                            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
                suboptions:
                    format_type:
                        description:
                            - The type mapping format.
                            - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
            structure:
                description:
                    - Ingestion mapping information at property level.
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    property_name:
                        description:
                            - The property name of the mapping entity.
                            - Required when C(state) is I(present).
                    column_name:
                        description:
                            - The column name of the import file.
                            - Required when C(state) is I(present).
                    custom_format_specifier:
                        description:
                            - Custom format specifier for input parsing.
                    is_encrypted:
                        description:
                            - Indicates if the column is encrypted.
            complete_operation:
                description:
                    - The operation after import is done.
                    - Required when C(state) is I(present).
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
      name: testMapping12491
      entity_type: Interaction
      entity_type_name: TestInteractionType2967
      display_name: testMapping12491
      description: Test mapping
      mapping_properties:
        folder_path: http://sample.dne/file
        file_filter: unknown
        has_header: False
        error_management:
          error_management_type: StopImport
          error_limit: 10
        format:
          format_type: TextFormat
          column_delimiter: |
        availability:
          frequency: Hour
          interval: 5
        structure:
          - property_name: unknwon1
            column_name: unknown1
            is_encrypted: False
        complete_operation:
          completion_operation_type: DeleteFile
          destination_folder: fakePath
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMConnectorMapping(AzureRMModuleBase):
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
            name=dict(
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
                         'relationship']
            ),
            entity_type_name=dict(
                type='str'
            ),
            display_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            mapping_properties=dict(
                type='dict',
                options=dict(
                    folder_path=dict(
                        type='str'
                    ),
                    file_filter=dict(
                        type='str'
                    ),
                    has_header=dict(
                        type='str'
                    ),
                    error_management=dict(
                        type='dict',
                        options=dict(
                            error_management_type=dict(
                                type='str',
                                choices=['reject_and_continue',
                                         'stop_import',
                                         'reject_until_limit']
                            ),
                            error_limit=dict(
                                type='int'
                            )
                        )
                    ),
                    format=dict(
                        type='dict',
                        options=dict(
                            format_type=dict(
                                type='str'
                            ),
                            column_delimiter=dict(
                                type='str'
                            ),
                            accept_language=dict(
                                type='str'
                            ),
                            quote_character=dict(
                                type='str'
                            ),
                            quote_escape_character=dict(
                                type='str'
                            ),
                            array_separator=dict(
                                type='str'
                            )
                        )
                    ),
                    availability=dict(
                        type='dict',
                        options=dict(
                            frequency=dict(
                                type='str',
                                choices=['minute',
                                         'hour',
                                         'day',
                                         'week',
                                         'month']
                            ),
                            interval=dict(
                                type='int'
                            )
                        )
                    ),
                    structure=dict(
                        type='list',
                        options=dict(
                            property_name=dict(
                                type='str'
                            ),
                            column_name=dict(
                                type='str'
                            ),
                            custom_format_specifier=dict(
                                type='str'
                            ),
                            is_encrypted=dict(
                                type='str'
                            )
                        )
                    ),
                    complete_operation=dict(
                        type='dict',
                        options=dict(
                            completion_operation_type=dict(
                                type='str',
                                choices=['do_nothing',
                                         'delete_file',
                                         'move_file']
                            ),
                            destination_folder=dict(
                                type='str'
                            )
                        )
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
        self.hub_name = None
        self.connector_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConnectorMapping, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['connector_type'], True)
        dict_map(self.parameters, ['connector_type'], {'crm': 'CRM'})
        dict_camelize(self.parameters, ['entity_type'], True)
        dict_camelize(self.parameters, ['mapping_properties', 'error_management', 'error_management_type'], True)
        dict_camelize(self.parameters, ['mapping_properties', 'availability', 'frequency'], True)
        dict_camelize(self.parameters, ['mapping_properties', 'complete_operation', 'completion_operation_type'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Connector Mapping instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_connectormapping()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Connector Mapping instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_connectormapping()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Connector Mapping instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None)
                })
        return self.results

    def create_update_connectormapping(self):
        '''
        Creates or updates Connector Mapping with the specified configuration.

        :return: deserialized Connector Mapping instance state dictionary
        '''
        self.log("Creating / Updating the Connector Mapping instance {0}".format(self.name))

        try:
            response = self.mgmt_client.connector_mappings.create_or_update(resource_group_name=self.resource_group,
                                                                            hub_name=self.hub_name,
                                                                            connector_name=self.connector_name,
                                                                            mapping_name=self.name,
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
        self.log("Deleting the Connector Mapping instance {0}".format(self.name))
        try:
            response = self.mgmt_client.connector_mappings.delete(resource_group_name=self.resource_group,
                                                                  hub_name=self.hub_name,
                                                                  connector_name=self.connector_name,
                                                                  mapping_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Connector Mapping instance.')
            self.fail("Error deleting the Connector Mapping instance: {0}".format(str(e)))

        return True

    def get_connectormapping(self):
        '''
        Gets the properties of the specified Connector Mapping.

        :return: deserialized Connector Mapping instance state dictionary
        '''
        self.log("Checking if the Connector Mapping instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.connector_mappings.get(resource_group_name=self.resource_group,
                                                               hub_name=self.hub_name,
                                                               connector_name=self.connector_name,
                                                               mapping_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Connector Mapping instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Connector Mapping instance.')
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def main():
    """Main execution"""
    AzureRMConnectorMapping()


if __name__ == '__main__':
    main()

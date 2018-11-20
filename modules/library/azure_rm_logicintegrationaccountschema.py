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
module: azure_rm_logicintegrationaccountschema
version_added: "2.8"
short_description: Manage Integration Account Schema instance.
description:
    - Create, update and delete instance of Integration Account Schema.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    name:
        description:
            - The integration account I(schema) name.
        required: True
    schema:
        description:
            - The integration account schema.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            schema_type:
                description:
                    - The schema type.
                    - Required when C(state) is I(present).
                choices:
                    - 'not_specified'
                    - 'xml'
            target_namespace:
                description:
                    - The target namespace of the schema.
            document_name:
                description:
                    - The document name.
            file_name:
                description:
                    - The file name.
            metadata:
                description:
                    - The metadata.
            content:
                description:
                    - The content.
            content_type:
                description:
                    - The I(content) type.
    state:
      description:
        - Assert the state of the Integration Account Schema.
        - Use 'present' to create or update an Integration Account Schema and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Schema
    azure_rm_logicintegrationaccountschema:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      name: testSchema
      schema:
        location: westus
        schema_type: Xml
        metadata: {}
        content: <?xml version="1.0" encoding="utf-16"?>
<xs:schema xmlns:b="http://schemas.microsoft.com/BizTalk/2003" xmlns="http://Inbound_EDI.OrderFile" targetNamespace="http://Inbound_EDI.OrderFile" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:annotation>
    <xs:appinfo>
      <b:schemaInfo default_pad_char=" " count_positions_by_byte="false" parser_optimization="speed" lookahead_depth="3" suppress_empty_nodes="false" generate_empty_nodes="true" allow_early_termination="false" early_terminate_optional_fields="false" allow_message_breakup_of_infix_root="false" compile_parse_tables="false" standard="Flat File" root_reference="OrderFile" />
      <schemaEditorExtension:schemaInfo namespaceAlias="b" extensionClass="Microsoft.BizTalk.FlatFileExtension.FlatFileExtension" standardName="Flat File" xmlns:schemaEditorExtension="http://schemas.microsoft.com/BizTalk/2003/SchemaEditorExtensions" />
    </xs:appinfo>
  </xs:annotation>
  <xs:element name="OrderFile">
    <xs:annotation>
      <xs:appinfo>
        <b:recordInfo structure="delimited" preserve_delimiter_for_empty_data="true" suppress_trailing_delimiters="false" sequence_number="1" />
      </xs:appinfo>
    </xs:annotation>
    <xs:complexType>
      <xs:sequence>
        <xs:annotation>
          <xs:appinfo>
            <b:groupInfo sequence_number="0" />
          </xs:appinfo>
        </xs:annotation>
        <xs:element name="Order">
          <xs:annotation>
            <xs:appinfo>
              <b:recordInfo sequence_number="1" structure="delimited" preserve_delimiter_for_empty_data="true" suppress_trailing_delimiters="false" child_delimiter_type="hex" child_delimiter="0x0D 0x0A" child_order="infix" />
            </xs:appinfo>
          </xs:annotation>
          <xs:complexType>
            <xs:sequence>
              <xs:annotation>
                <xs:appinfo>
                  <b:groupInfo sequence_number="0" />
                </xs:appinfo>
              </xs:annotation>
              <xs:element name="Header">
                <xs:annotation>
                  <xs:appinfo>
                    <b:recordInfo sequence_number="1" structure="delimited" preserve_delimiter_for_empty_data="true" suppress_trailing_delimiters="false" child_delimiter_type="char" child_delimiter="|" child_order="infix" tag_name="HDR|" />
                  </xs:appinfo>
                </xs:annotation>
                <xs:complexType>
                  <xs:sequence>
                    <xs:annotation>
                      <xs:appinfo>
                        <b:groupInfo sequence_number="0" />
                      </xs:appinfo>
                    </xs:annotation>
                    <xs:element name="PODate" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="1" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="PONumber" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo justification="left" sequence_number="2" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="CustomerID" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="3" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="CustomerContactName" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="4" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="CustomerContactPhone" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="5" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
              <xs:element minOccurs="1" maxOccurs="unbounded" name="LineItems">
                <xs:annotation>
                  <xs:appinfo>
                    <b:recordInfo sequence_number="2" structure="delimited" preserve_delimiter_for_empty_data="true" suppress_trailing_delimiters="false" child_delimiter_type="char" child_delimiter="|" child_order="infix" tag_name="DTL|" />
                  </xs:appinfo>
                </xs:annotation>
                <xs:complexType>
                  <xs:sequence>
                    <xs:annotation>
                      <xs:appinfo>
                        <b:groupInfo sequence_number="0" />
                      </xs:appinfo>
                    </xs:annotation>
                    <xs:element name="PONumber" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="1" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="ItemOrdered" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="2" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="Quantity" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="3" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="UOM" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="4" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="Price" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="5" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="ExtendedPrice" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="6" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                    <xs:element name="Description" type="xs:string">
                      <xs:annotation>
                        <xs:appinfo>
                          <b:fieldInfo sequence_number="7" justification="left" />
                        </xs:appinfo>
                      </xs:annotation>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
        content_type: application/xml
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/testIntegrati
            onAccount/schemas/testSchema"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIntegrationAccountSchemas(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Schema resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            integration_account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            schema=dict(
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
        self.integration_account_name = None
        self.name = None
        self.schema = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountSchemas, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                               supports_check_mode=True,
                                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.schema["location"] = kwargs[key]
                elif key == "schema_type":
                    self.schema["schema_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "target_namespace":
                    self.schema["target_namespace"] = kwargs[key]
                elif key == "document_name":
                    self.schema["document_name"] = kwargs[key]
                elif key == "file_name":
                    self.schema["file_name"] = kwargs[key]
                elif key == "metadata":
                    self.schema["metadata"] = kwargs[key]
                elif key == "content":
                    self.schema["content"] = kwargs[key]
                elif key == "content_type":
                    self.schema["content_type"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountschema()

        if not old_response:
            self.log("Integration Account Schema instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Schema instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Schema instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountschema()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Schema instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountschema()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccountschema():
                time.sleep(20)
        else:
            self.log("Integration Account Schema instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccountschema(self):
        '''
        Creates or updates Integration Account Schema with the specified configuration.

        :return: deserialized Integration Account Schema instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Schema instance {0}".format(self.name))

        try:
            response = self.mgmt_client.integration_account_schemas.create_or_update(resource_group_name=self.resource_group,
                                                                                     integration_account_name=self.integration_account_name,
                                                                                     schema_name=self.name,
                                                                                     schema=self.schema)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Schema instance.')
            self.fail("Error creating the Integration Account Schema instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountschema(self):
        '''
        Deletes specified Integration Account Schema instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Schema instance {0}".format(self.name))
        try:
            response = self.mgmt_client.integration_account_schemas.delete(resource_group_name=self.resource_group,
                                                                           integration_account_name=self.integration_account_name,
                                                                           schema_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Schema instance.')
            self.fail("Error deleting the Integration Account Schema instance: {0}".format(str(e)))

        return True

    def get_integrationaccountschema(self):
        '''
        Gets the properties of the specified Integration Account Schema.

        :return: deserialized Integration Account Schema instance state dictionary
        '''
        self.log("Checking if the Integration Account Schema instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.integration_account_schemas.get(resource_group_name=self.resource_group,
                                                                        integration_account_name=self.integration_account_name,
                                                                        schema_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Schema instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Schema instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMIntegrationAccountSchemas()


if __name__ == '__main__':
    main()

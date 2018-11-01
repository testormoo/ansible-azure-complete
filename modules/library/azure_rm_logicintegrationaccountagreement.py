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
module: azure_rm_logicintegrationaccountagreement
version_added: "2.8"
short_description: Manage Integration Account Agreement instance.
description:
    - Create, update and delete instance of Integration Account Agreement.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    agreement_name:
        description:
            - The integration account I(agreement) name.
        required: True
    agreement:
        description:
            - The integration account agreement.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            metadata:
                description:
                    - The metadata.
            agreement_type:
                description:
                    - The agreement type.
                required: True
                choices:
                    - 'not_specified'
                    - 'as2'
                    - 'x12'
                    - 'edifact'
            host_partner:
                description:
                    - The integration account partner that is set as host partner for this agreement.
                required: True
            guest_partner:
                description:
                    - The integration account partner that is set as guest partner for this agreement.
                required: True
            host_identity:
                description:
                    - The business identity of the host partner.
                required: True
                suboptions:
                    qualifier:
                        description:
                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                        required: True
                    value:
                        description:
                            - The user defined business identity value.
                        required: True
            guest_identity:
                description:
                    - The business identity of the guest partner.
                required: True
                suboptions:
                    qualifier:
                        description:
                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                        required: True
                    value:
                        description:
                            - The user defined business identity value.
                        required: True
            content:
                description:
                    - The agreement content.
                required: True
                suboptions:
                    a_s2:
                        description:
                            - The AS2 agreement content.
                        suboptions:
                            receive_agreement:
                                description:
                                    - The AS2 one-way receive agreement.
                                required: True
                                suboptions:
                                    sender_business_identity:
                                        description:
                                            - The sender business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    receiver_business_identity:
                                        description:
                                            - The receiver business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    protocol_settings:
                                        description:
                                            - The AS2 protocol settings.
                                        required: True
                                        suboptions:
                                            message_connection_settings:
                                                description:
                                                    - The message connection settings.
                                                required: True
                                            acknowledgement_connection_settings:
                                                description:
                                                    - The acknowledgement connection settings.
                                                required: True
                                            mdn_settings:
                                                description:
                                                    - The MDN settings.
                                                required: True
                                            security_settings:
                                                description:
                                                    - The security settings.
                                                required: True
                                            validation_settings:
                                                description:
                                                    - The validation settings.
                                                required: True
                                            envelope_settings:
                                                description:
                                                    - The envelope settings.
                                                required: True
                                            error_settings:
                                                description:
                                                    - The error settings.
                                                required: True
                            send_agreement:
                                description:
                                    - The AS2 one-way send agreement.
                                required: True
                                suboptions:
                                    sender_business_identity:
                                        description:
                                            - The sender business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    receiver_business_identity:
                                        description:
                                            - The receiver business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    protocol_settings:
                                        description:
                                            - The AS2 protocol settings.
                                        required: True
                                        suboptions:
                                            message_connection_settings:
                                                description:
                                                    - The message connection settings.
                                                required: True
                                            acknowledgement_connection_settings:
                                                description:
                                                    - The acknowledgement connection settings.
                                                required: True
                                            mdn_settings:
                                                description:
                                                    - The MDN settings.
                                                required: True
                                            security_settings:
                                                description:
                                                    - The security settings.
                                                required: True
                                            validation_settings:
                                                description:
                                                    - The validation settings.
                                                required: True
                                            envelope_settings:
                                                description:
                                                    - The envelope settings.
                                                required: True
                                            error_settings:
                                                description:
                                                    - The error settings.
                                                required: True
                    x12:
                        description:
                            - The X12 agreement content.
                        suboptions:
                            receive_agreement:
                                description:
                                    - The X12 one-way receive agreement.
                                required: True
                                suboptions:
                                    sender_business_identity:
                                        description:
                                            - The sender business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    receiver_business_identity:
                                        description:
                                            - The receiver business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    protocol_settings:
                                        description:
                                            - The X12 protocol settings.
                                        required: True
                                        suboptions:
                                            validation_settings:
                                                description:
                                                    - The X12 validation settings.
                                                required: True
                                            framing_settings:
                                                description:
                                                    - The X12 framing settings.
                                                required: True
                                            envelope_settings:
                                                description:
                                                    - The X12 envelope settings.
                                                required: True
                                            acknowledgement_settings:
                                                description:
                                                    - The X12 acknowledgment settings.
                                                required: True
                                            message_filter:
                                                description:
                                                    - The X12 message filter.
                                                required: True
                                            security_settings:
                                                description:
                                                    - The X12 security settings.
                                                required: True
                                            processing_settings:
                                                description:
                                                    - The X12 processing settings.
                                                required: True
                                            envelope_overrides:
                                                description:
                                                    - The X12 envelope override settings.
                                                type: list
                                            validation_overrides:
                                                description:
                                                    - The X12 validation override settings.
                                                type: list
                                            message_filter_list:
                                                description:
                                                    - The X12 message filter list.
                                                type: list
                                            schema_references:
                                                description:
                                                    - The X12 schema references.
                                                required: True
                                                type: list
                                            x12_delimiter_overrides:
                                                description:
                                                    - The X12 delimiter override settings.
                                                type: list
                            send_agreement:
                                description:
                                    - The X12 one-way send agreement.
                                required: True
                                suboptions:
                                    sender_business_identity:
                                        description:
                                            - The sender business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    receiver_business_identity:
                                        description:
                                            - The receiver business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    protocol_settings:
                                        description:
                                            - The X12 protocol settings.
                                        required: True
                                        suboptions:
                                            validation_settings:
                                                description:
                                                    - The X12 validation settings.
                                                required: True
                                            framing_settings:
                                                description:
                                                    - The X12 framing settings.
                                                required: True
                                            envelope_settings:
                                                description:
                                                    - The X12 envelope settings.
                                                required: True
                                            acknowledgement_settings:
                                                description:
                                                    - The X12 acknowledgment settings.
                                                required: True
                                            message_filter:
                                                description:
                                                    - The X12 message filter.
                                                required: True
                                            security_settings:
                                                description:
                                                    - The X12 security settings.
                                                required: True
                                            processing_settings:
                                                description:
                                                    - The X12 processing settings.
                                                required: True
                                            envelope_overrides:
                                                description:
                                                    - The X12 envelope override settings.
                                                type: list
                                            validation_overrides:
                                                description:
                                                    - The X12 validation override settings.
                                                type: list
                                            message_filter_list:
                                                description:
                                                    - The X12 message filter list.
                                                type: list
                                            schema_references:
                                                description:
                                                    - The X12 schema references.
                                                required: True
                                                type: list
                                            x12_delimiter_overrides:
                                                description:
                                                    - The X12 delimiter override settings.
                                                type: list
                    edifact:
                        description:
                            - The EDIFACT agreement content.
                        suboptions:
                            receive_agreement:
                                description:
                                    - The EDIFACT one-way receive agreement.
                                required: True
                                suboptions:
                                    sender_business_identity:
                                        description:
                                            - The sender business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    receiver_business_identity:
                                        description:
                                            - The receiver business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    protocol_settings:
                                        description:
                                            - The EDIFACT protocol settings.
                                        required: True
                                        suboptions:
                                            validation_settings:
                                                description:
                                                    - The EDIFACT validation settings.
                                                required: True
                                            framing_settings:
                                                description:
                                                    - The EDIFACT framing settings.
                                                required: True
                                            envelope_settings:
                                                description:
                                                    - The EDIFACT envelope settings.
                                                required: True
                                            acknowledgement_settings:
                                                description:
                                                    - The EDIFACT acknowledgement settings.
                                                required: True
                                            message_filter:
                                                description:
                                                    - The EDIFACT message filter.
                                                required: True
                                            processing_settings:
                                                description:
                                                    - The EDIFACT processing Settings.
                                                required: True
                                            envelope_overrides:
                                                description:
                                                    - The EDIFACT envelope override settings.
                                                type: list
                                            message_filter_list:
                                                description:
                                                    - The EDIFACT message filter list.
                                                type: list
                                            schema_references:
                                                description:
                                                    - The EDIFACT schema references.
                                                required: True
                                                type: list
                                            validation_overrides:
                                                description:
                                                    - The EDIFACT validation override settings.
                                                type: list
                                            edifact_delimiter_overrides:
                                                description:
                                                    - The EDIFACT delimiter override settings.
                                                type: list
                            send_agreement:
                                description:
                                    - The EDIFACT one-way send agreement.
                                required: True
                                suboptions:
                                    sender_business_identity:
                                        description:
                                            - The sender business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    receiver_business_identity:
                                        description:
                                            - The receiver business identity
                                        required: True
                                        suboptions:
                                            qualifier:
                                                description:
                                                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                                required: True
                                            value:
                                                description:
                                                    - The user defined business identity value.
                                                required: True
                                    protocol_settings:
                                        description:
                                            - The EDIFACT protocol settings.
                                        required: True
                                        suboptions:
                                            validation_settings:
                                                description:
                                                    - The EDIFACT validation settings.
                                                required: True
                                            framing_settings:
                                                description:
                                                    - The EDIFACT framing settings.
                                                required: True
                                            envelope_settings:
                                                description:
                                                    - The EDIFACT envelope settings.
                                                required: True
                                            acknowledgement_settings:
                                                description:
                                                    - The EDIFACT acknowledgement settings.
                                                required: True
                                            message_filter:
                                                description:
                                                    - The EDIFACT message filter.
                                                required: True
                                            processing_settings:
                                                description:
                                                    - The EDIFACT processing Settings.
                                                required: True
                                            envelope_overrides:
                                                description:
                                                    - The EDIFACT envelope override settings.
                                                type: list
                                            message_filter_list:
                                                description:
                                                    - The EDIFACT message filter list.
                                                type: list
                                            schema_references:
                                                description:
                                                    - The EDIFACT schema references.
                                                required: True
                                                type: list
                                            validation_overrides:
                                                description:
                                                    - The EDIFACT validation override settings.
                                                type: list
                                            edifact_delimiter_overrides:
                                                description:
                                                    - The EDIFACT delimiter override settings.
                                                type: list
    state:
      description:
        - Assert the state of the Integration Account Agreement.
        - Use 'present' to create or update an Integration Account Agreement and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Agreement
    azure_rm_logicintegrationaccountagreement:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      agreement_name: testAgreement
      agreement:
        location: westus
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/IntegrationAc
            count4533/agreements/<IntegrationAccountAgreementName>"
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


class AzureRMIntegrationAccountAgreements(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Agreement resource"""

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
            agreement_name=dict(
                type='str',
                required=True
            ),
            agreement=dict(
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
        self.agreement_name = None
        self.agreement = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountAgreements, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                  supports_check_mode=True,
                                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.agreement["location"] = kwargs[key]
                elif key == "metadata":
                    self.agreement["metadata"] = kwargs[key]
                elif key == "agreement_type":
                    ev = kwargs[key]
                    if ev == 'as2':
                        ev = 'AS2'
                    self.agreement["agreement_type"] = _snake_to_camel(ev, True)
                elif key == "host_partner":
                    self.agreement["host_partner"] = kwargs[key]
                elif key == "guest_partner":
                    self.agreement["guest_partner"] = kwargs[key]
                elif key == "host_identity":
                    self.agreement["host_identity"] = kwargs[key]
                elif key == "guest_identity":
                    self.agreement["guest_identity"] = kwargs[key]
                elif key == "content":
                    self.agreement["content"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountagreement()

        if not old_response:
            self.log("Integration Account Agreement instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Agreement instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Integration Account Agreement instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Agreement instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountagreement()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Agreement instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountagreement()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccountagreement():
                time.sleep(20)
        else:
            self.log("Integration Account Agreement instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccountagreement(self):
        '''
        Creates or updates Integration Account Agreement with the specified configuration.

        :return: deserialized Integration Account Agreement instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Agreement instance {0}".format(self.agreement_name))

        try:
            response = self.mgmt_client.integration_account_agreements.create_or_update(resource_group_name=self.resource_group,
                                                                                        integration_account_name=self.integration_account_name,
                                                                                        agreement_name=self.agreement_name,
                                                                                        agreement=self.agreement)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Agreement instance.')
            self.fail("Error creating the Integration Account Agreement instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountagreement(self):
        '''
        Deletes specified Integration Account Agreement instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Agreement instance {0}".format(self.agreement_name))
        try:
            response = self.mgmt_client.integration_account_agreements.delete(resource_group_name=self.resource_group,
                                                                              integration_account_name=self.integration_account_name,
                                                                              agreement_name=self.agreement_name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Agreement instance.')
            self.fail("Error deleting the Integration Account Agreement instance: {0}".format(str(e)))

        return True

    def get_integrationaccountagreement(self):
        '''
        Gets the properties of the specified Integration Account Agreement.

        :return: deserialized Integration Account Agreement instance state dictionary
        '''
        self.log("Checking if the Integration Account Agreement instance {0} is present".format(self.agreement_name))
        found = False
        try:
            response = self.mgmt_client.integration_account_agreements.get(resource_group_name=self.resource_group,
                                                                           integration_account_name=self.integration_account_name,
                                                                           agreement_name=self.agreement_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Agreement instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Agreement instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMIntegrationAccountAgreements()


if __name__ == '__main__':
    main()

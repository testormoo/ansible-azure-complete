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
short_description: Manage Azure Integration Account Agreement instance.
description:
    - Create, update and delete instance of Azure Integration Account Agreement.

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
            - The integration account agreement name.
        required: True
    location:
        description:
            - The resource location.
    metadata:
        description:
            - The metadata.
    agreement_type:
        description:
            - The agreement type.
            - Required when C(state) is I(present).
        choices:
            - 'not_specified'
            - 'as2'
            - 'x12'
            - 'edifact'
    host_partner:
        description:
            - The integration account partner that is set as host partner for this agreement.
            - Required when C(state) is I(present).
    guest_partner:
        description:
            - The integration account partner that is set as guest partner for this agreement.
            - Required when C(state) is I(present).
    host_identity:
        description:
            - The business identity of the host partner.
            - Required when C(state) is I(present).
        suboptions:
            qualifier:
                description:
                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                    - Required when C(state) is I(present).
            value:
                description:
                    - The user defined business identity value.
                    - Required when C(state) is I(present).
    guest_identity:
        description:
            - The business identity of the guest partner.
            - Required when C(state) is I(present).
        suboptions:
            qualifier:
                description:
                    - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                    - Required when C(state) is I(present).
            value:
                description:
                    - The user defined business identity value.
                    - Required when C(state) is I(present).
    content:
        description:
            - The agreement content.
            - Required when C(state) is I(present).
        suboptions:
            a_s2:
                description:
                    - The AS2 agreement content.
                suboptions:
                    receive_agreement:
                        description:
                            - The AS2 one-way receive agreement.
                            - Required when C(state) is I(present).
                        suboptions:
                            sender_business_identity:
                                description:
                                    - The sender business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            receiver_business_identity:
                                description:
                                    - The receiver business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            protocol_settings:
                                description:
                                    - The AS2 protocol settings.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    message_connection_settings:
                                        description:
                                            - The message connection settings.
                                            - Required when C(state) is I(present).
                                    acknowledgement_connection_settings:
                                        description:
                                            - The acknowledgement connection settings.
                                            - Required when C(state) is I(present).
                                    mdn_settings:
                                        description:
                                            - The MDN settings.
                                            - Required when C(state) is I(present).
                                    security_settings:
                                        description:
                                            - The security settings.
                                            - Required when C(state) is I(present).
                                    validation_settings:
                                        description:
                                            - The validation settings.
                                            - Required when C(state) is I(present).
                                    envelope_settings:
                                        description:
                                            - The envelope settings.
                                            - Required when C(state) is I(present).
                                    error_settings:
                                        description:
                                            - The error settings.
                                            - Required when C(state) is I(present).
                    send_agreement:
                        description:
                            - The AS2 one-way send agreement.
                            - Required when C(state) is I(present).
                        suboptions:
                            sender_business_identity:
                                description:
                                    - The sender business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            receiver_business_identity:
                                description:
                                    - The receiver business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            protocol_settings:
                                description:
                                    - The AS2 protocol settings.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    message_connection_settings:
                                        description:
                                            - The message connection settings.
                                            - Required when C(state) is I(present).
                                    acknowledgement_connection_settings:
                                        description:
                                            - The acknowledgement connection settings.
                                            - Required when C(state) is I(present).
                                    mdn_settings:
                                        description:
                                            - The MDN settings.
                                            - Required when C(state) is I(present).
                                    security_settings:
                                        description:
                                            - The security settings.
                                            - Required when C(state) is I(present).
                                    validation_settings:
                                        description:
                                            - The validation settings.
                                            - Required when C(state) is I(present).
                                    envelope_settings:
                                        description:
                                            - The envelope settings.
                                            - Required when C(state) is I(present).
                                    error_settings:
                                        description:
                                            - The error settings.
                                            - Required when C(state) is I(present).
            x12:
                description:
                    - The X12 agreement content.
                suboptions:
                    receive_agreement:
                        description:
                            - The X12 one-way receive agreement.
                            - Required when C(state) is I(present).
                        suboptions:
                            sender_business_identity:
                                description:
                                    - The sender business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            receiver_business_identity:
                                description:
                                    - The receiver business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            protocol_settings:
                                description:
                                    - The X12 protocol settings.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    validation_settings:
                                        description:
                                            - The X12 validation settings.
                                            - Required when C(state) is I(present).
                                    framing_settings:
                                        description:
                                            - The X12 framing settings.
                                            - Required when C(state) is I(present).
                                    envelope_settings:
                                        description:
                                            - The X12 envelope settings.
                                            - Required when C(state) is I(present).
                                    acknowledgement_settings:
                                        description:
                                            - The X12 acknowledgment settings.
                                            - Required when C(state) is I(present).
                                    message_filter:
                                        description:
                                            - The X12 message filter.
                                            - Required when C(state) is I(present).
                                    security_settings:
                                        description:
                                            - The X12 security settings.
                                            - Required when C(state) is I(present).
                                    processing_settings:
                                        description:
                                            - The X12 processing settings.
                                            - Required when C(state) is I(present).
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
                                            - Required when C(state) is I(present).
                                        type: list
                                    x12_delimiter_overrides:
                                        description:
                                            - The X12 delimiter override settings.
                                        type: list
                    send_agreement:
                        description:
                            - The X12 one-way send agreement.
                            - Required when C(state) is I(present).
                        suboptions:
                            sender_business_identity:
                                description:
                                    - The sender business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            receiver_business_identity:
                                description:
                                    - The receiver business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            protocol_settings:
                                description:
                                    - The X12 protocol settings.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    validation_settings:
                                        description:
                                            - The X12 validation settings.
                                            - Required when C(state) is I(present).
                                    framing_settings:
                                        description:
                                            - The X12 framing settings.
                                            - Required when C(state) is I(present).
                                    envelope_settings:
                                        description:
                                            - The X12 envelope settings.
                                            - Required when C(state) is I(present).
                                    acknowledgement_settings:
                                        description:
                                            - The X12 acknowledgment settings.
                                            - Required when C(state) is I(present).
                                    message_filter:
                                        description:
                                            - The X12 message filter.
                                            - Required when C(state) is I(present).
                                    security_settings:
                                        description:
                                            - The X12 security settings.
                                            - Required when C(state) is I(present).
                                    processing_settings:
                                        description:
                                            - The X12 processing settings.
                                            - Required when C(state) is I(present).
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
                                            - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
                        suboptions:
                            sender_business_identity:
                                description:
                                    - The sender business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            receiver_business_identity:
                                description:
                                    - The receiver business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            protocol_settings:
                                description:
                                    - The EDIFACT protocol settings.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    validation_settings:
                                        description:
                                            - The EDIFACT validation settings.
                                            - Required when C(state) is I(present).
                                    framing_settings:
                                        description:
                                            - The EDIFACT framing settings.
                                            - Required when C(state) is I(present).
                                    envelope_settings:
                                        description:
                                            - The EDIFACT envelope settings.
                                            - Required when C(state) is I(present).
                                    acknowledgement_settings:
                                        description:
                                            - The EDIFACT acknowledgement settings.
                                            - Required when C(state) is I(present).
                                    message_filter:
                                        description:
                                            - The EDIFACT message filter.
                                            - Required when C(state) is I(present).
                                    processing_settings:
                                        description:
                                            - The EDIFACT processing Settings.
                                            - Required when C(state) is I(present).
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
                                            - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
                        suboptions:
                            sender_business_identity:
                                description:
                                    - The sender business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            receiver_business_identity:
                                description:
                                    - The receiver business identity
                                    - Required when C(state) is I(present).
                                suboptions:
                                    qualifier:
                                        description:
                                            - The business identity qualifier e.g. as2identity, ZZ, ZZZ, 31, 32
                                            - Required when C(state) is I(present).
                                    value:
                                        description:
                                            - The user defined business identity value.
                                            - Required when C(state) is I(present).
                            protocol_settings:
                                description:
                                    - The EDIFACT protocol settings.
                                    - Required when C(state) is I(present).
                                suboptions:
                                    validation_settings:
                                        description:
                                            - The EDIFACT validation settings.
                                            - Required when C(state) is I(present).
                                    framing_settings:
                                        description:
                                            - The EDIFACT framing settings.
                                            - Required when C(state) is I(present).
                                    envelope_settings:
                                        description:
                                            - The EDIFACT envelope settings.
                                            - Required when C(state) is I(present).
                                    acknowledgement_settings:
                                        description:
                                            - The EDIFACT acknowledgement settings.
                                            - Required when C(state) is I(present).
                                    message_filter:
                                        description:
                                            - The EDIFACT message filter.
                                            - Required when C(state) is I(present).
                                    processing_settings:
                                        description:
                                            - The EDIFACT processing Settings.
                                            - Required when C(state) is I(present).
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
                                            - Required when C(state) is I(present).
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
      name: testAgreement
      location: westus
      metadata: {}
      agreement_type: AS2
      host_partner: HostPartner
      guest_partner: GuestPartner
      host_identity:
        qualifier: ZZ
        value: ZZ
      guest_identity:
        qualifier: AA
        value: AA
      content:
        a_s2:
          receive_agreement:
            sender_business_identity:
              qualifier: AA
              value: AA
            receiver_business_identity:
              qualifier: ZZ
              value: ZZ
            protocol_settings:
              message_connection_settings: {
  "ignoreCertificateNameMismatch": true,
  "supportHttpStatusCodeContinue": true,
  "keepHttpConnectionAlive": true,
  "unfoldHttpHeaders": true
}
              acknowledgement_connection_settings: {
  "ignoreCertificateNameMismatch": true,
  "supportHttpStatusCodeContinue": true,
  "keepHttpConnectionAlive": true,
  "unfoldHttpHeaders": true
}
              mdn_settings: {
  "needMdn": true,
  "signMdn": true,
  "sendMdnAsynchronously": true,
  "receiptDeliveryUrl": "http://tempuri.org",
  "dispositionNotificationTo": "http://tempuri.org",
  "signOutboundMdnIfOptional": true,
  "mdnText": "Sample",
  "sendInboundMdnToMessageBox": true,
  "micHashingAlgorithm": "SHA1"
}
              security_settings: {
  "overrideGroupSigningCertificate": false,
  "enableNrrForInboundEncodedMessages": true,
  "enableNrrForInboundDecodedMessages": true,
  "enableNrrForOutboundMdn": true,
  "enableNrrForOutboundEncodedMessages": true,
  "enableNrrForOutboundDecodedMessages": true,
  "enableNrrForInboundMdn": true
}
              validation_settings: {
  "overrideMessageProperties": true,
  "encryptMessage": false,
  "signMessage": false,
  "compressMessage": true,
  "checkDuplicateMessage": true,
  "interchangeDuplicatesValidityDays": "100",
  "checkCertificateRevocationListOnSend": true,
  "checkCertificateRevocationListOnReceive": true,
  "encryptionAlgorithm": "AES128"
}
              envelope_settings: {
  "messageContentType": "text/plain",
  "transmitFileNameInMimeHeader": true,
  "fileNameTemplate": "Test",
  "suspendMessageOnFileNameGenerationError": true,
  "autogenerateFileName": true
}
              error_settings: {
  "suspendDuplicateMessage": true,
  "resendIfMdnNotReceived": true
}
          send_agreement:
            sender_business_identity:
              qualifier: ZZ
              value: ZZ
            receiver_business_identity:
              qualifier: AA
              value: AA
            protocol_settings:
              message_connection_settings: {
  "ignoreCertificateNameMismatch": true,
  "supportHttpStatusCodeContinue": true,
  "keepHttpConnectionAlive": true,
  "unfoldHttpHeaders": true
}
              acknowledgement_connection_settings: {
  "ignoreCertificateNameMismatch": true,
  "supportHttpStatusCodeContinue": true,
  "keepHttpConnectionAlive": true,
  "unfoldHttpHeaders": true
}
              mdn_settings: {
  "needMdn": true,
  "signMdn": true,
  "sendMdnAsynchronously": true,
  "receiptDeliveryUrl": "http://tempuri.org",
  "dispositionNotificationTo": "http://tempuri.org",
  "signOutboundMdnIfOptional": true,
  "mdnText": "Sample",
  "sendInboundMdnToMessageBox": true,
  "micHashingAlgorithm": "SHA1"
}
              security_settings: {
  "overrideGroupSigningCertificate": false,
  "enableNrrForInboundEncodedMessages": true,
  "enableNrrForInboundDecodedMessages": true,
  "enableNrrForOutboundMdn": true,
  "enableNrrForOutboundEncodedMessages": true,
  "enableNrrForOutboundDecodedMessages": true,
  "enableNrrForInboundMdn": true
}
              validation_settings: {
  "overrideMessageProperties": true,
  "encryptMessage": false,
  "signMessage": false,
  "compressMessage": true,
  "checkDuplicateMessage": true,
  "interchangeDuplicatesValidityDays": "100",
  "checkCertificateRevocationListOnSend": true,
  "checkCertificateRevocationListOnReceive": true,
  "encryptionAlgorithm": "AES128"
}
              envelope_settings: {
  "messageContentType": "text/plain",
  "transmitFileNameInMimeHeader": true,
  "fileNameTemplate": "Test",
  "suspendMessageOnFileNameGenerationError": true,
  "autogenerateFileName": true
}
              error_settings: {
  "suspendDuplicateMessage": true,
  "resendIfMdnNotReceived": true
}
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMIntegrationAccountAgreement(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            metadata=dict(
                type='str'
            ),
            agreement_type=dict(
                type='str',
                choices=['not_specified',
                         'as2',
                         'x12',
                         'edifact']
            ),
            host_partner=dict(
                type='str'
            ),
            guest_partner=dict(
                type='str'
            ),
            host_identity=dict(
                type='dict',
                options=dict(
                    qualifier=dict(
                        type='str'
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            guest_identity=dict(
                type='dict',
                options=dict(
                    qualifier=dict(
                        type='str'
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            content=dict(
                type='dict',
                options=dict(
                    a_s2=dict(
                        type='dict',
                        options=dict(
                            receive_agreement=dict(
                                type='dict',
                                options=dict(
                                    sender_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    receiver_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    protocol_settings=dict(
                                        type='dict',
                                        options=dict(
                                            message_connection_settings=dict(
                                                type='dict'
                                            ),
                                            acknowledgement_connection_settings=dict(
                                                type='dict'
                                            ),
                                            mdn_settings=dict(
                                                type='dict'
                                            ),
                                            security_settings=dict(
                                                type='dict'
                                            ),
                                            validation_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_settings=dict(
                                                type='dict'
                                            ),
                                            error_settings=dict(
                                                type='dict'
                                            )
                                        )
                                    )
                                )
                            ),
                            send_agreement=dict(
                                type='dict',
                                options=dict(
                                    sender_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    receiver_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    protocol_settings=dict(
                                        type='dict',
                                        options=dict(
                                            message_connection_settings=dict(
                                                type='dict'
                                            ),
                                            acknowledgement_connection_settings=dict(
                                                type='dict'
                                            ),
                                            mdn_settings=dict(
                                                type='dict'
                                            ),
                                            security_settings=dict(
                                                type='dict'
                                            ),
                                            validation_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_settings=dict(
                                                type='dict'
                                            ),
                                            error_settings=dict(
                                                type='dict'
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    x12=dict(
                        type='dict',
                        options=dict(
                            receive_agreement=dict(
                                type='dict',
                                options=dict(
                                    sender_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    receiver_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    protocol_settings=dict(
                                        type='dict',
                                        options=dict(
                                            validation_settings=dict(
                                                type='dict'
                                            ),
                                            framing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_settings=dict(
                                                type='dict'
                                            ),
                                            acknowledgement_settings=dict(
                                                type='dict'
                                            ),
                                            message_filter=dict(
                                                type='dict'
                                            ),
                                            security_settings=dict(
                                                type='dict'
                                            ),
                                            processing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_overrides=dict(
                                                type='list'
                                            ),
                                            validation_overrides=dict(
                                                type='list'
                                            ),
                                            message_filter_list=dict(
                                                type='list'
                                            ),
                                            schema_references=dict(
                                                type='list'
                                            ),
                                            x12_delimiter_overrides=dict(
                                                type='list'
                                            )
                                        )
                                    )
                                )
                            ),
                            send_agreement=dict(
                                type='dict',
                                options=dict(
                                    sender_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    receiver_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    protocol_settings=dict(
                                        type='dict',
                                        options=dict(
                                            validation_settings=dict(
                                                type='dict'
                                            ),
                                            framing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_settings=dict(
                                                type='dict'
                                            ),
                                            acknowledgement_settings=dict(
                                                type='dict'
                                            ),
                                            message_filter=dict(
                                                type='dict'
                                            ),
                                            security_settings=dict(
                                                type='dict'
                                            ),
                                            processing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_overrides=dict(
                                                type='list'
                                            ),
                                            validation_overrides=dict(
                                                type='list'
                                            ),
                                            message_filter_list=dict(
                                                type='list'
                                            ),
                                            schema_references=dict(
                                                type='list'
                                            ),
                                            x12_delimiter_overrides=dict(
                                                type='list'
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    edifact=dict(
                        type='dict',
                        options=dict(
                            receive_agreement=dict(
                                type='dict',
                                options=dict(
                                    sender_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    receiver_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    protocol_settings=dict(
                                        type='dict',
                                        options=dict(
                                            validation_settings=dict(
                                                type='dict'
                                            ),
                                            framing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_settings=dict(
                                                type='dict'
                                            ),
                                            acknowledgement_settings=dict(
                                                type='dict'
                                            ),
                                            message_filter=dict(
                                                type='dict'
                                            ),
                                            processing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_overrides=dict(
                                                type='list'
                                            ),
                                            message_filter_list=dict(
                                                type='list'
                                            ),
                                            schema_references=dict(
                                                type='list'
                                            ),
                                            validation_overrides=dict(
                                                type='list'
                                            ),
                                            edifact_delimiter_overrides=dict(
                                                type='list'
                                            )
                                        )
                                    )
                                )
                            ),
                            send_agreement=dict(
                                type='dict',
                                options=dict(
                                    sender_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    receiver_business_identity=dict(
                                        type='dict',
                                        options=dict(
                                            qualifier=dict(
                                                type='str'
                                            ),
                                            value=dict(
                                                type='str'
                                            )
                                        )
                                    ),
                                    protocol_settings=dict(
                                        type='dict',
                                        options=dict(
                                            validation_settings=dict(
                                                type='dict'
                                            ),
                                            framing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_settings=dict(
                                                type='dict'
                                            ),
                                            acknowledgement_settings=dict(
                                                type='dict'
                                            ),
                                            message_filter=dict(
                                                type='dict'
                                            ),
                                            processing_settings=dict(
                                                type='dict'
                                            ),
                                            envelope_overrides=dict(
                                                type='list'
                                            ),
                                            message_filter_list=dict(
                                                type='list'
                                            ),
                                            schema_references=dict(
                                                type='list'
                                            ),
                                            validation_overrides=dict(
                                                type='list'
                                            ),
                                            edifact_delimiter_overrides=dict(
                                                type='list'
                                            )
                                        )
                                    )
                                )
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
        self.integration_account_name = None
        self.name = None
        self.agreement = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountAgreement, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                   supports_check_mode=True,
                                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.agreement[key] = kwargs[key]

        dict_camelize(self.agreement, ['agreement_type'], True)
        dict_map(self.agreement, ['agreement_type'], {'as2': 'AS2'})

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
                if (not default_compare(self.agreement, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Agreement instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountagreement()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Agreement instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountagreement()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Integration Account Agreement instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_integrationaccountagreement(self):
        '''
        Creates or updates Integration Account Agreement with the specified configuration.

        :return: deserialized Integration Account Agreement instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Agreement instance {0}".format(self.name))

        try:
            response = self.mgmt_client.integration_account_agreements.create_or_update(resource_group_name=self.resource_group,
                                                                                        integration_account_name=self.integration_account_name,
                                                                                        agreement_name=self.name,
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
        self.log("Deleting the Integration Account Agreement instance {0}".format(self.name))
        try:
            response = self.mgmt_client.integration_account_agreements.delete(resource_group_name=self.resource_group,
                                                                              integration_account_name=self.integration_account_name,
                                                                              agreement_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Agreement instance.')
            self.fail("Error deleting the Integration Account Agreement instance: {0}".format(str(e)))

        return True

    def get_integrationaccountagreement(self):
        '''
        Gets the properties of the specified Integration Account Agreement.

        :return: deserialized Integration Account Agreement instance state dictionary
        '''
        self.log("Checking if the Integration Account Agreement instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.integration_account_agreements.get(resource_group_name=self.resource_group,
                                                                           integration_account_name=self.integration_account_name,
                                                                           agreement_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Agreement instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Agreement instance.')
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
    AzureRMIntegrationAccountAgreement()


if __name__ == '__main__':
    main()

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
module: azure_rm_logicintegrationaccountagreement_facts
version_added: "2.8"
short_description: Get Azure Integration Account Agreement facts.
description:
    - Get facts of Azure Integration Account Agreement.

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
            - The integration account agreement name.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Integration Account Agreement
    azure_rm_logicintegrationaccountagreement_facts:
      resource_group: resource_group_name
      integration_account_name: integration_account_name
      agreement_name: agreement_name
'''

RETURN = '''
integration_account_agreements:
    description: A list of dictionaries containing facts for Integration Account Agreement.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testResourceGroup/providers/Microsoft.Logic/integrationAccounts/<Inte
                    grationAccountName>/agreements/<IntegrationAccountAgreementName>"
        name:
            description:
                - Gets the resource name.
            returned: always
            type: str
            sample: <IntegrationAccountAgreementName>
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: tags
        metadata:
            description:
                - The metadata.
            returned: always
            type: str
            sample: {}
        content:
            description:
                - The agreement content.
            returned: always
            type: complex
            sample: content
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIntegrationAccountAgreementsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
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
            tags=dict(
                type='list'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.integration_account_name = None
        self.agreement_name = None
        self.tags = None
        super(AzureRMIntegrationAccountAgreementsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['integration_account_agreements'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_account_agreements.get(resource_group_name=self.resource_group,
                                                                           integration_account_name=self.integration_account_name,
                                                                           agreement_name=self.agreement_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IntegrationAccountAgreements.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'metadata': d.get('metadata', None),
            'content': {
            }
        }
        return d


def main():
    AzureRMIntegrationAccountAgreementsFacts()


if __name__ == '__main__':
    main()

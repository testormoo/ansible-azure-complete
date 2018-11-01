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
module: azure_rm_logicintegrationaccountsession_facts
version_added: "2.8"
short_description: Get Azure Integration Account Session facts.
description:
    - Get facts of Azure Integration Account Session.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    session_name:
        description:
            - The integration account session name.
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
  - name: Get instance of Integration Account Session
    azure_rm_logicintegrationaccountsession_facts:
      resource_group: resource_group_name
      integration_account_name: integration_account_name
      session_name: session_name
'''

RETURN = '''
integration_account_sessions:
    description: A list of dictionaries containing facts for Integration Account Session.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The resource id.
            returned: always
            type: str
            sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testrg123/providers/Microsoft.Logic/integrationAccounts/testia123/ses
                    sions/testsession123-ICN"
        name:
            description:
                - Gets the resource name.
            returned: always
            type: str
            sample: testsession123-ICN
        tags:
            description:
                - The resource tags.
            returned: always
            type: complex
            sample: tags
        content:
            description:
                - The session content.
            returned: always
            type: str
            sample: "{\n  'controlNumber': '1234',\n  'controlNumberChangedTime': '2017-02-21T22:30:11.9923759Z'\n}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIntegrationAccountSessionsFacts(AzureRMModuleBase):
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
            session_name=dict(
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
        self.session_name = None
        self.tags = None
        super(AzureRMIntegrationAccountSessionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['integration_account_sessions'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.integration_account_sessions.get(resource_group_name=self.resource_group,
                                                                         integration_account_name=self.integration_account_name,
                                                                         session_name=self.session_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for IntegrationAccountSessions.')

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
            'content': d.get('content', None)
        }
        return d


def main():
    AzureRMIntegrationAccountSessionsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_automationnodecountinformation_facts
version_added: "2.8"
short_description: Get Azure Node Count Information facts.
description:
    - Get facts of Azure Node Count Information.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    self.config.count_type:
        description:
            - The type of counts to retrieve
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Node Count Information
    azure_rm_automationnodecountinformation_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      self.config.count_type: self.config.count_type
'''

RETURN = '''
node_count_information:
    description: A list of dictionaries containing facts for Node Count Information.
    returned: always
    type: complex
    contains:
        value:
            description:
                - Gets an array of counts
            returned: always
            type: complex
            sample: value
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNodeCountInformationFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            self.config.count_type=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.automation_account_name = None
        self.self.config.count_type = None
        super(AzureRMNodeCountInformationFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['node_count_information'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.node_count_information.get(resource_group_name=self.resource_group,
                                                                   automation_account_name=self.automation_account_name,
                                                                   self.config.count_type=self.self.config.count_type)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for NodeCountInformation.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'value': {
            }
        }
        return d


def main():
    AzureRMNodeCountInformationFacts()


if __name__ == '__main__':
    main()

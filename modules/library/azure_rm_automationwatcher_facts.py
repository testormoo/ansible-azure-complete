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
module: azure_rm_automationwatcher_facts
version_added: "2.8"
short_description: Get Azure Watcher facts.
description:
    - Get facts of Azure Watcher.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    watcher_name:
        description:
            - The watcher name.
    filter:
        description:
            - The filter to apply on the operation.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Watcher
    azure_rm_automationwatcher_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      watcher_name: watcher_name

  - name: List instances of Watcher
    azure_rm_automationwatcher_facts:
      resource_group: resource_group_name
      automation_account_name: automation_account_name
      filter: filter
'''

RETURN = '''
watcher:
    description: A list of dictionaries containing facts for Watcher.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified resource Id for the resource
            returned: always
            type: str
            sample: /subscriptions/subId/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/MyTestAutomationAccount/watchers/MyTestWatcher
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: MyTestWatcher
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - The Azure Region where the resource lives
            returned: always
            type: str
            sample: location
        status:
            description:
                - Gets the current status of the watcher.
            returned: always
            type: str
            sample: Running
        description:
            description:
                - Gets or sets the description.
            returned: always
            type: str
            sample: description
        etag:
            description:
                - Gets or sets the etag of the resource.
            returned: always
            type: str
            sample: etag
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMWatcherFacts(AzureRMModuleBase):
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
            watcher_name=dict(
                type='str'
            ),
            filter=dict(
                type='str'
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
        self.automation_account_name = None
        self.watcher_name = None
        self.filter = None
        self.tags = None
        super(AzureRMWatcherFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.watcher_name is not None:
            self.results['watcher'] = self.get()
        else:
            self.results['watcher'] = self.list_by_automation_account()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.watcher.get(resource_group_name=self.resource_group,
                                                    automation_account_name=self.automation_account_name,
                                                    watcher_name=self.watcher_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Watcher.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_automation_account(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.watcher.list_by_automation_account(resource_group_name=self.resource_group,
                                                                           automation_account_name=self.automation_account_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Watcher.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'status': d.get('status', None),
            'description': d.get('description', None),
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMWatcherFacts()


if __name__ == '__main__':
    main()

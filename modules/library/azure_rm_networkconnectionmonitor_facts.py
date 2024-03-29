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
module: azure_rm_networkconnectionmonitor_facts
version_added: "2.8"
short_description: Get Azure Connection Monitor facts.
description:
    - Get facts of Azure Connection Monitor.

options:
    resource_group:
        description:
            - The name of the resource group containing Network Watcher.
        required: True
    network_watcher_name:
        description:
            - The name of the Network Watcher resource.
        required: True
    name:
        description:
            - The name of the connection monitor.
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
  - name: Get instance of Connection Monitor
    azure_rm_networkconnectionmonitor_facts:
      resource_group: resource_group_name
      network_watcher_name: network_watcher_name
      name: connection_monitor_name
'''

RETURN = '''
connection_monitors:
    description: A list of dictionaries containing facts for Connection Monitor.
    returned: always
    type: complex
    contains:
        id:
            description:
                - ID of the connection monitor.
            returned: always
            type: str
            sample: id
        tags:
            description:
                - Connection monitor tags.
            returned: always
            type: complex
            sample: tags
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMConnectionMonitorFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            network_watcher_name=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.network_watcher_name = None
        self.name = None
        self.tags = None
        super(AzureRMConnectionMonitorFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['connection_monitors'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.connection_monitors.get(resource_group_name=self.resource_group,
                                                                network_watcher_name=self.network_watcher_name,
                                                                connection_monitor_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Connection Monitor.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'tags': d.get('tags', None)
        }
        return d


def main():
    AzureRMConnectionMonitorFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_sqljobagent_facts
version_added: "2.8"
short_description: Get Azure Job Agent facts.
description:
    - Get facts of Azure Job Agent.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the job agent to be retrieved.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Job Agent
    azure_rm_sqljobagent_facts:
      resource_group: resource_group_name
      server_name: server_name
      name: job_agent_name

  - name: List instances of Job Agent
    azure_rm_sqljobagent_facts:
      resource_group: resource_group_name
      server_name: server_name
'''

RETURN = '''
job_agents:
    description: A list of dictionaries containing facts for Job Agent.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: agent1
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: southeastasia
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        sku:
            description:
                - The name and tier of the SKU.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - The name of the SKU. Ex - P3. It is typically a letter+number code
                    returned: always
                    type: str
                    sample: Agent
                capacity:
                    description:
                        - "If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource
                           this may be omitted."
                    returned: always
                    type: int
                    sample: 100
        state:
            description:
                - "The state of the job agent. Possible values include: 'Creating', 'Ready', 'Updating', 'Deleting', 'Disabled'"
            returned: always
            type: str
            sample: state
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMJobAgentsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
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
        self.server_name = None
        self.name = None
        self.tags = None
        super(AzureRMJobAgentsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['job_agents'] = self.get()
        else:
            self.results['job_agents'] = self.list_by_server()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_agents.get(resource_group_name=self.resource_group,
                                                       server_name=self.server_name,
                                                       job_agent_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobAgents.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.job_agents.list_by_server(resource_group_name=self.resource_group,
                                                                  server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for JobAgents.')

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
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            },
            'state': d.get('state', None)
        }
        return d


def main():
    AzureRMJobAgentsFacts()


if __name__ == '__main__':
    main()

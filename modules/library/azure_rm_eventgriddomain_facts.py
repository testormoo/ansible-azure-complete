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
module: azure_rm_eventgriddomain_facts
version_added: "2.8"
short_description: Get Azure Domain facts.
description:
    - Get facts of Azure Domain.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription."
    domain_name:
        description:
            - Name of the domain
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Domain
    azure_rm_eventgriddomain_facts:
      resource_group: resource_group_name
      domain_name: domain_name

  - name: List instances of Domain
    azure_rm_eventgriddomain_facts:
      resource_group: resource_group_name

  - name: List instances of Domain
    azure_rm_eventgriddomain_facts:
'''

RETURN = '''
domains:
    description: A list of dictionaries containing facts for Domain.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Fully qualified identifier of the resource
            returned: always
            type: str
            sample: /subscriptions/5b4b650e-28b9-4790-b3ab-ddbd88d727c4/resourceGroups/examplerg/providers/Microsoft.EventGrid/domains/exampledomain2
        name:
            description:
                - Name of the resource
            returned: always
            type: str
            sample: exampledomain2
        location:
            description:
                - Location of the resource
            returned: always
            type: str
            sample: westcentralus
        tags:
            description:
                - Tags of the resource
            returned: always
            type: complex
            sample: "{\n  'tag1': 'value1',\n  'tag2': 'value2'\n}"
        endpoint:
            description:
                - Endpoint for the domain.
            returned: always
            type: str
            sample: "https://exampledomain2.westcentralus-1.eventgrid.azure.net/api/events"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.eventgrid import EventGridManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDomainsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            domain_name=dict(
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
        self.domain_name = None
        self.tags = None
        super(AzureRMDomainsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(EventGridManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.domain_name is not None):
            self.results['domains'] = self.get()
        elif self.resource_group is not None:
            self.results['domains'] = self.list_by_resource_group()
        else:
            self.results['domains'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.domains.get(resource_group_name=self.resource_group,
                                                    domain_name=self.domain_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Domains.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.domains.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Domains.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.domains.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Domains.')

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
            'endpoint': d.get('endpoint', None)
        }
        return d


def main():
    AzureRMDomainsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_domainservice_facts
version_added: "2.8"
short_description: Get Azure Domain Service facts.
description:
    - Get facts of Azure Domain Service.

options:
    resource_group:
        description:
            - "The name of the resource group within the user's subscription. The name is case insensitive."
        required: True
    name:
        description:
            - The name of the domain service in the specified subscription and resource group.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Domain Service
    azure_rm_domainservice_facts:
      resource_group: resource_group_name
      name: domain_service_name

  - name: List instances of Domain Service
    azure_rm_domainservice_facts:
      resource_group: resource_group_name
'''

RETURN = '''
domain_services:
    description: A list of dictionaries containing facts for Domain Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: /subscriptions/1639790a-76a2-4ac4-98d9-8562f5dfcb4d/resourceGroups/sva-tt-WUS/providers/Microsoft.AAD/domainServices/zdomain.zforest.com
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: zdomain.zforest.com
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  'Owner': 'jicha'\n}"
        etag:
            description:
                - Resource etag
            returned: always
            type: str
            sample: "W/'datetime'2017-04-10T04%3A42%3A19.7067387Z''"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.domainservices import DomainServicesResourceProvider
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDomainServicesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
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
        self.name = None
        self.tags = None
        super(AzureRMDomainServicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(DomainServicesResourceProvider,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['domain_services'] = self.get()
        else:
            self.results['domain_services'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.domain_services.get(resource_group_name=self.resource_group,
                                                            domain_service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DomainServices.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.domain_services.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for DomainServices.')

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
            'etag': d.get('etag', None)
        }
        return d


def main():
    AzureRMDomainServicesFacts()


if __name__ == '__main__':
    main()

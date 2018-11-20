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
module: azure_rm_cdncustomdomain_facts
version_added: "2.8"
short_description: Get Azure Custom Domain facts.
description:
    - Get facts of Azure Custom Domain.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    profile_name:
        description:
            - Name of the CDN profile which is unique within the resource group.
        required: True
    endpoint_name:
        description:
            - Name of the endpoint under the profile which is unique globally.
        required: True
    name:
        description:
            - Name of the custom domain within an endpoint.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Custom Domain
    azure_rm_cdncustomdomain_facts:
      resource_group: resource_group_name
      profile_name: profile_name
      endpoint_name: endpoint_name
      name: custom_domain_name

  - name: List instances of Custom Domain
    azure_rm_cdncustomdomain_facts:
      resource_group: resource_group_name
      profile_name: profile_name
      endpoint_name: endpoint_name
'''

RETURN = '''
custom_domains:
    description: A list of dictionaries containing facts for Custom Domain.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourcegroups/RG/providers/Microsoft.Cdn/profiles/profile1/endpoints/endpoint1/customdomains/www-someDomain-net
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: www-someDomain-net
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.cdn import CdnManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMCustomDomainsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            endpoint_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.profile_name = None
        self.endpoint_name = None
        self.name = None
        super(AzureRMCustomDomainsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(CdnManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['custom_domains'] = self.get()
        else:
            self.results['custom_domains'] = self.list_by_endpoint()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.custom_domains.get(resource_group_name=self.resource_group,
                                                           profile_name=self.profile_name,
                                                           endpoint_name=self.endpoint_name,
                                                           custom_domain_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for CustomDomains.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_endpoint(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.custom_domains.list_by_endpoint(resource_group_name=self.resource_group,
                                                                        profile_name=self.profile_name,
                                                                        endpoint_name=self.endpoint_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for CustomDomains.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMCustomDomainsFacts()


if __name__ == '__main__':
    main()

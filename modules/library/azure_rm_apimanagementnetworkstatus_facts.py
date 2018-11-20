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
module: azure_rm_apimanagementnetworkstatus_facts
version_added: "2.8"
short_description: Get Azure Network Status facts.
description:
    - Get facts of Azure Network Status.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    service_name:
        description:
            - The name of the API Management service.
        required: True
    name:
        description:
            - Location in which the API Management service is deployed. This is one of the Azure Regions like West US, East US, South Central US.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Network Status
    azure_rm_apimanagementnetworkstatus_facts:
      resource_group: resource_group_name
      service_name: service_name
      name: location_name

  - name: List instances of Network Status
    azure_rm_apimanagementnetworkstatus_facts:
      resource_group: resource_group_name
      service_name: service_name
'''

RETURN = '''
network_status:
    description: A list of dictionaries containing facts for Network Status.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.apimanagement import ApiManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNetworkStatusFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_name=dict(
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
        self.service_name = None
        self.name = None
        super(AzureRMNetworkStatusFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['network_status'] = self.list_by_location()
        else:
            self.results['network_status'] = self.list_by_service()
        return self.results

    def list_by_location(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.network_status.list_by_location(resource_group_name=self.resource_group,
                                                                        service_name=self.service_name,
                                                                        location_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for NetworkStatus.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_service(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.network_status.list_by_service(resource_group_name=self.resource_group,
                                                                       service_name=self.service_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for NetworkStatus.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMNetworkStatusFacts()


if __name__ == '__main__':
    main()

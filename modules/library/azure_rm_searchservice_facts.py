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
module: azure_rm_searchservice_facts
version_added: "2.8"
short_description: Get Azure Service facts.
description:
    - Get facts of Azure Service.

options:
    resource_group:
        description:
            - The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the Azure Search service associated with the specified resource group.
    search_management_request_options:
        description:
            - Additional parameters for the operation
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Service
    azure_rm_searchservice_facts:
      resource_group: resource_group_name
      name: search_service_name
      search_management_request_options: search_management_request_options

  - name: List instances of Service
    azure_rm_searchservice_facts:
      resource_group: resource_group_name
      search_management_request_options: search_management_request_options
'''

RETURN = '''
services:
    description: A list of dictionaries containing facts for Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The ID of the resource. This can be used with the Azure Resource Manager to link resources together.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Search/searchServices/mysearchservice
        name:
            description:
                - The name of the resource.
            returned: always
            type: str
            sample: mysearchservice
        location:
            description:
                - "The geographic location of the resource. This must be one of the supported and registered Azure Geo Regions (for example, West US, East
                   US, Southeast Asia, and so forth). This property is required when creating a new resource."
            returned: always
            type: str
            sample: westus
        tags:
            description:
                - Tags to help categorize the resource in the Azure portal.
            returned: always
            type: complex
            sample: "{\n  'app-name': 'My e-commerce app'\n}"
        status:
            description:
                - "The status of the Search service. Possible values include: 'running': The Search service is running and no provisioning operations are
                   underway. 'provisioning': The Search service is being provisioned or scaled up or down. 'deleting': The Search service is being deleted.
                   'degraded': The Search service is degraded. This can occur when the underlying search units are not healthy. The Search service is most
                   likely operational, but performance might be slow and some requests might be dropped. 'disabled': The Search service is disabled. In
                   this state, the service will reject all API requests. 'error': The Search service is in an error state. If your service is in the
                   degraded, disabled, or error states, it means the Azure Search team is actively investigating the underlying issue. Dedicated services
                   in these states are still chargeable based on the number of search units provisioned. Possible values include: 'running',
                   'provisioning', 'deleting', 'degraded', 'disabled', 'error'"
            returned: always
            type: str
            sample: running
        sku:
            description:
                - The SKU of the Search Service, which determines price tier and capacity limits. This property is required when creating a new Search Service.
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - "The SKU of the Search service. Valid values include: 'free': Shared service. 'basic': Dedicated service with up to 3 replicas.
                           'standard': Dedicated service with up to 12 partitions and 12 replicas. 'standard2': Similar to standard, but with more capacity
                           per search unit. 'standard3': Offers maximum capacity per search unit with up to 12 partitions and 12 replicas (or up to 3
                           partitions with more indexes if you also set the hostingMode property to 'highDensity'). Possible values include: 'free',
                           'basic', 'standard', 'standard2', 'standard3'"
                    returned: always
                    type: str
                    sample: standard
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.search import SearchManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServicesFacts(AzureRMModuleBase):
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
            search_management_request_options=dict(
                type='dict'
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
        self.search_management_request_options = None
        self.tags = None
        super(AzureRMServicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SearchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['services'] = self.get()
        else:
            self.results['services'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.services.get(resource_group_name=self.resource_group,
                                                     search_service_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Services.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.services.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Services.')

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
            'status': d.get('status', None),
            'sku': {
                'name': d.get('sku', {}).get('name', None)
            }
        }
        return d


def main():
    AzureRMServicesFacts()


if __name__ == '__main__':
    main()

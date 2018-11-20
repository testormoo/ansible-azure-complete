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
module: azure_rm_sqlmanagedinstance_facts
version_added: "2.8"
short_description: Get Azure Managed Instance facts.
description:
    - Get facts of Azure Managed Instance.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - The name of the managed instance.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Managed Instance
    azure_rm_sqlmanagedinstance_facts:
      resource_group: resource_group_name
      name: managed_instance_name

  - name: List instances of Managed Instance
    azure_rm_sqlmanagedinstance_facts:
      resource_group: resource_group_name
'''

RETURN = '''
managed_instances:
    description: A list of dictionaries containing facts for Managed Instance.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/20d7082a-0fc7-4468-82bd-542694d5042b/resourceGroups/testrg/providers/Microsoft.Sql/managedInstances/testcl
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: testcl
        location:
            description:
                - Resource location.
            returned: always
            type: str
            sample: onebox
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: tags
        sku:
            description:
                - Managed instance sku
            returned: always
            type: complex
            sample: sku
            contains:
                name:
                    description:
                        - The name of the SKU. Ex - P3. It is typically a letter+number code
                    returned: always
                    type: str
                    sample: CLS3
                tier:
                    description:
                        - This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
                    returned: always
                    type: str
                    sample: Standard
                family:
                    description:
                        - If the service has different generations of hardware, for the same SKU, then that can be captured here.
                    returned: always
                    type: str
                    sample: Gen4
                capacity:
                    description:
                        - "If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource
                           this may be omitted."
                    returned: always
                    type: int
                    sample: 1
        fully_qualified_domain_name:
            description:
                - The fully qualified domain name of the managed instance.
            returned: always
            type: str
            sample: fully_qualified_domain_name
        state:
            description:
                - The state of the managed instance.
            returned: always
            type: str
            sample: Ready
        collation:
            description:
                - Collation of the managed instance.
            returned: always
            type: str
            sample: SQL_Latin1_General_CP1_CI_AS
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagedInstancesFacts(AzureRMModuleBase):
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
        super(AzureRMManagedInstancesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['managed_instances'] = self.get()
        else:
            self.results['managed_instances'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managed_instances.get(resource_group_name=self.resource_group,
                                                              managed_instance_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ManagedInstances.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.managed_instances.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ManagedInstances.')

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
                'tier': d.get('sku', {}).get('tier', None),
                'family': d.get('sku', {}).get('family', None),
                'capacity': d.get('sku', {}).get('capacity', None)
            },
            'fully_qualified_domain_name': d.get('fully_qualified_domain_name', None),
            'state': d.get('state', None),
            'collation': d.get('collation', None)
        }
        return d


def main():
    AzureRMManagedInstancesFacts()


if __name__ == '__main__':
    main()

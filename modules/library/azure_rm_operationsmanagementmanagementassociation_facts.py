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
module: azure_rm_operationsmanagementmanagementassociation_facts
version_added: "2.8"
short_description: Get Azure Management Association facts.
description:
    - Get facts of Azure Management Association.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
    self.config.provider_name:
        description:
            - Provider name for the parent resource.
    self.config.resource_type:
        description:
            - Resource type for the parent resource
    self.config.resource_name:
        description:
            - Parent resource name.
    management_association_name:
        description:
            - User ManagementAssociation Name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Management Association
    azure_rm_operationsmanagementmanagementassociation_facts:
      resource_group: resource_group_name
      self.config.provider_name: self.config.provider_name
      self.config.resource_type: self.config.resource_type
      self.config.resource_name: self.config.resource_name
      management_association_name: management_association_name

  - name: List instances of Management Association
    azure_rm_operationsmanagementmanagementassociation_facts:
'''

RETURN = '''
management_associations:
    description: A list of dictionaries containing facts for Management Association.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/subid/resourcegroups/rg1/providers/Microsoft.OperationalInsights/workspaces/ws1/Microsoft.OperationsManagement/Management
                    Associations/managementAssociation1"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: managementAssociation1
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: East US
        properties:
            description:
                - Properties for ManagementAssociation object supported by the OperationsManagement resource provider.
            returned: always
            type: complex
            sample: properties
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.operationsmanagement import OperationsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMManagementAssociationsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            self.config.provider_name=dict(
                type='str'
            ),
            self.config.resource_type=dict(
                type='str'
            ),
            self.config.resource_name=dict(
                type='str'
            ),
            management_association_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.self.config.provider_name = None
        self.self.config.resource_type = None
        self.self.config.resource_name = None
        self.management_association_name = None
        super(AzureRMManagementAssociationsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(OperationsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.self.config.provider_name is not None and
                self.self.config.resource_type is not None and
                self.self.config.resource_name is not None and
                self.management_association_name is not None):
            self.results['management_associations'] = self.get()
        else:
            self.results['management_associations'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.management_associations.get(resource_group_name=self.resource_group,
                                                                    self.config.provider_name=self.self.config.provider_name,
                                                                    self.config.resource_type=self.self.config.resource_type,
                                                                    self.config.resource_name=self.self.config.resource_name,
                                                                    management_association_name=self.management_association_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ManagementAssociations.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.management_associations.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ManagementAssociations.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'properties': {
            }
        }
        return d


def main():
    AzureRMManagementAssociationsFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_operationsmanagementsolution_facts
version_added: "2.8"
short_description: Get Azure Solution facts.
description:
    - Get facts of Azure Solution.

options:
    resource_group:
        description:
            - The name of the resource group to get. The name is case insensitive.
    name:
        description:
            - User Solution Name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Solution
    azure_rm_operationsmanagementsolution_facts:
      resource_group: resource_group_name
      name: solution_name

  - name: List instances of Solution
    azure_rm_operationsmanagementsolution_facts:
      resource_group: resource_group_name

  - name: List instances of Solution
    azure_rm_operationsmanagementsolution_facts:
'''

RETURN = '''
solutions:
    description: A list of dictionaries containing facts for Solution.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.OperationsManagement/solutions/solution1
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: solution1
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: East US
        plan:
            description:
                - Plan for solution object supported by the OperationsManagement resource provider.
            returned: always
            type: complex
            sample: plan
            contains:
                name:
                    description:
                        - "name of the solution to be created. For Microsoft published solution it should be in the format of solutionType(workspaceName).
                           SolutionType part is case sensitive. For third party solution, it can be anything."
                    returned: always
                    type: str
                    sample: name1
                publisher:
                    description:
                        - Publisher name. For gallery solution, it is Microsoft.
                    returned: always
                    type: str
                    sample: publisher1
                product:
                    description:
                        - "name of the solution to enabled/add. For Microsoft published gallery solution it should be in the format of
                           OMSGallery/<solutionType>. This is case sensitive"
                    returned: always
                    type: str
                    sample: product1
        properties:
            description:
                - Properties for solution object supported by the OperationsManagement resource provider.
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


class AzureRMSolutionsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
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
        self.name = None
        super(AzureRMSolutionsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(OperationsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['solutions'] = self.get()
        elif self.resource_group is not None:
            self.results['solutions'] = self.list_by_resource_group()
        else:
            self.results['solutions'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.solutions.get(resource_group_name=self.resource_group,
                                                      solution_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Solutions.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.solutions.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Solutions.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.solutions.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Solutions.')

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
            'plan': {
                'name': d.get('plan', {}).get('name', None),
                'publisher': d.get('plan', {}).get('publisher', None),
                'product': d.get('plan', {}).get('product', None)
            },
            'properties': {
            }
        }
        return d


def main():
    AzureRMSolutionsFacts()


if __name__ == '__main__':
    main()

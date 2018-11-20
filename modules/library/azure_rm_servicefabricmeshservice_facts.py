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
module: azure_rm_servicefabricmeshservice_facts
version_added: "2.8"
short_description: Get Azure Service facts.
description:
    - Get facts of Azure Service.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    application_resource_name:
        description:
            - The identity of the application.
        required: True
    name:
        description:
            - The identity of the service.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Service
    azure_rm_servicefabricmeshservice_facts:
      resource_group: resource_group_name
      application_resource_name: application_resource_name
      name: service_resource_name
'''

RETURN = '''
service:
    description: A list of dictionaries containing facts for Service.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified identifier for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/sbz_demo/providers/Microsoft.ServiceFabricMesh/applications/sampleApp
                    lication/services/helloWorldService"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: helloWorldService
        description:
            description:
                - User readable description of the service.
            returned: always
            type: str
            sample: SeaBreeze Hello World Service.
        status:
            description:
                - "Status of the service. Possible values include: 'Unknown', 'Ready', 'Upgrading', 'Creating', 'Deleting', 'Failed'"
            returned: always
            type: str
            sample: Ready
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.servicefabricmesh import ServiceFabricMeshManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServiceFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            application_resource_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.application_resource_name = None
        self.name = None
        super(AzureRMServiceFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['service'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.service.get(resource_group_name=self.resource_group,
                                                    application_resource_name=self.application_resource_name,
                                                    service_resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Service.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMServiceFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_deploymentmanagerserviceunit_facts
version_added: "2.8"
short_description: Get Azure Service Unit facts.
description:
    - Get facts of Azure Service Unit.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    service_topology_name:
        description:
            - The name of the service topology .
        required: True
    service_name:
        description:
            - The name of the service resource.
        required: True
    name:
        description:
            - The name of the service unit resource.
        required: True
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Service Unit
    azure_rm_deploymentmanagerserviceunit_facts:
      resource_group: resource_group_name
      service_topology_name: service_topology_name
      service_name: service_name
      name: service_unit_name
'''

RETURN = '''
service_units:
    description: A list of dictionaries containing facts for Service Unit.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
            returned: always
            type: str
            sample: id
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: myServiceUnit
        tags:
            description:
                - Resource tags.
            returned: always
            type: complex
            sample: {}
        location:
            description:
                - The geo-location where the resource lives
            returned: always
            type: str
            sample: centralus
        artifacts:
            description:
                - The artifacts for the service unit.
            returned: always
            type: complex
            sample: artifacts
            contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.deploymentmanager import AzureDeploymentManager
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServiceUnitFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            service_topology_name=dict(
                type='str',
                required=True
            ),
            service_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
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
        self.service_topology_name = None
        self.service_name = None
        self.name = None
        self.tags = None
        super(AzureRMServiceUnitFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureDeploymentManager,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['service_units'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.service_units.get(resource_group_name=self.resource_group,
                                                          service_topology_name=self.service_topology_name,
                                                          service_name=self.service_name,
                                                          service_unit_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Service Unit.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'location': d.get('location', None),
            'artifacts': {
            }
        }
        return d


def main():
    AzureRMServiceUnitFacts()


if __name__ == '__main__':
    main()

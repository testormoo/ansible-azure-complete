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
module: azure_rm_servicefabricmeshservicereplica_facts
version_added: "2.8"
short_description: Get Azure Service Replica facts.
description:
    - Get facts of Azure Service Replica.

options:
    resource_group:
        description:
            - Azure resource group name
        required: True
    application_resource_name:
        description:
            - The identity of the application.
        required: True
    service_resource_name:
        description:
            - The identity of the service.
        required: True
    name:
        description:
            - Service Fabric replica name.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Service Replica
    azure_rm_servicefabricmeshservicereplica_facts:
      resource_group: resource_group_name
      application_resource_name: application_resource_name
      service_resource_name: service_resource_name
      name: replica_name
'''

RETURN = '''
service_replica:
    description: A list of dictionaries containing facts for Service Replica.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.servicefabricmesh import ServiceFabricMeshManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServiceReplicaFacts(AzureRMModuleBase):
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
            service_resource_name=dict(
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
        self.service_resource_name = None
        self.name = None
        super(AzureRMServiceReplicaFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceFabricMeshManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['service_replica'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.service_replica.get(resource_group_name=self.resource_group,
                                                            application_resource_name=self.application_resource_name,
                                                            service_resource_name=self.service_resource_name,
                                                            replica_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for ServiceReplica.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMServiceReplicaFacts()


if __name__ == '__main__':
    main()

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
module: azure_rm_trafficmanagerendpoint_facts
version_added: "2.8"
short_description: Get Azure Endpoint facts.
description:
    - Get facts of Azure Endpoint.

options:
    resource_group:
        description:
            - The name of the resource group containing the Traffic Manager endpoint.
        required: True
    profile_name:
        description:
            - The name of the Traffic Manager profile.
        required: True
    endpoint_type:
        description:
            - The type of the Traffic Manager endpoint.
        required: True
    name:
        description:
            - The name of the Traffic Manager endpoint.
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Endpoint
    azure_rm_trafficmanagerendpoint_facts:
      resource_group: resource_group_name
      profile_name: profile_name
      endpoint_type: endpoint_type
      name: endpoint_name
'''

RETURN = '''
endpoints:
    description: A list of dictionaries containing facts for Endpoint.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
            returned: always
            type: str
            sample: "/subscriptions/{subscription-id}/resourceGroups/azuresdkfornetautoresttrafficmanager2191/providers/Microsoft.Network/trafficManagerProfi
                    les/azuresdkfornetautoresttrafficmanager8224/externalEndpoints/My external endpoint"
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: My external endpoint
        target:
            description:
                - "The fully-qualified DNS name or IP address of the endpoint. Traffic Manager returns this value in DNS responses to direct traffic to this
                   endpoint."
            returned: always
            type: str
            sample: foobar.contoso.com
        weight:
            description:
                - "The weight of this endpoint when using the 'Weighted' traffic routing method. Possible values are from 1 to 1000."
            returned: always
            type: int
            sample: 1
        priority:
            description:
                - "The priority of this endpoint when using the 'Priority' traffic routing method. Possible values are from 1 to 1000, lower values
                   represent higher priority. This is an optional parameter.  If specified, it must be specified on all endpoints, and no two endpoints can
                   share the same priority value."
            returned: always
            type: int
            sample: 1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.trafficmanager import TrafficManagerManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMEndpointsFacts(AzureRMModuleBase):
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
            endpoint_type=dict(
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
        self.profile_name = None
        self.endpoint_type = None
        self.name = None
        super(AzureRMEndpointsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(TrafficManagerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['endpoints'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.endpoints.get(resource_group_name=self.resource_group,
                                                      profile_name=self.profile_name,
                                                      endpoint_type=self.endpoint_type,
                                                      endpoint_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Endpoints.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'target': d.get('target', None),
            'weight': d.get('weight', None),
            'priority': d.get('priority', None)
        }
        return d


def main():
    AzureRMEndpointsFacts()


if __name__ == '__main__':
    main()

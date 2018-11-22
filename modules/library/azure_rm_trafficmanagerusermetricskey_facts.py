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
module: azure_rm_trafficmanagerusermetricskey_facts
version_added: "2.8"
short_description: Get Azure Traffic Manager User Metrics Key facts.
description:
    - Get facts of Azure Traffic Manager User Metrics Key.

options:

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Traffic Manager User Metrics Key
    azure_rm_trafficmanagerusermetricskey_facts:
'''

RETURN = '''
traffic_manager_user_metrics_keys:
    description: A list of dictionaries containing facts for Traffic Manager User Metrics Key.
    returned: always
    type: complex
    contains:
        id:
            description:
                - "Fully qualified resource Id for the resource. Ex -
                   /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}"
            returned: always
            type: str
            sample: /providers/Microsoft.Network/trafficManagerUserMetricsKeys/default
        name:
            description:
                - The name of the resource
            returned: always
            type: str
            sample: default
        key:
            description:
                - The key returned by the User Metrics operation.
            returned: always
            type: str
            sample: 9ea056eb38f145a0891b5d5dc15e9aa2
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.trafficmanager import TrafficManagerManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMTrafficManagerUserMetricsKeyFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        super(AzureRMTrafficManagerUserMetricsKeyFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(TrafficManagerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['traffic_manager_user_metrics_keys'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.traffic_manager_user_metrics_keys.get()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Traffic Manager User Metrics Key.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'key': d.get('key', None)
        }
        return d


def main():
    AzureRMTrafficManagerUserMetricsKeyFacts()


if __name__ == '__main__':
    main()

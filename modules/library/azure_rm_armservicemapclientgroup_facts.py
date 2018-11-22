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
module: azure_rm_armservicemapclientgroup_facts
version_added: "2.8"
short_description: Get Azure Client Group facts.
description:
    - Get facts of Azure Client Group.

options:
    resource_group:
        description:
            - Resource group name within the specified subscriptionId.
        required: True
    workspace_name:
        description:
            - OMS workspace containing the resources of interest.
        required: True
    name:
        description:
            - Client Group resource name.
        required: True
    start_time:
        description:
            - UTC date and time specifying the start time of an interval. When not specified the service uses DateTime.UtcNow - 10m
    end_time:
        description:
            - UTC date and time specifying the end time of an interval. When not specified the service uses DateTime.UtcNow

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Client Group
    azure_rm_armservicemapclientgroup_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      name: client_group_name
      start_time: start_time
      end_time: end_time
'''

RETURN = '''
client_groups:
    description: A list of dictionaries containing facts for Client Group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/63BE4E24-FDF0-4E9C-9342-6A5D5A359722/resourceGroups/rg-sm/providers/Microsoft.OperationalInsights/workspaces/D6F79F14-E56
                    3-469B-84B5-9286D2803B2F/clientGroups/m!m-A4AB1C69-03E9-42D2-B822-B42555569FB4!b!b-c0a8010a_10000"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: m!m-A4AB1C69-03E9-42D2-B822-B42555569FB4!b!b-c0a8010a_10000
        kind:
            description:
                - Constant filled by server.
            returned: always
            type: str
            sample: clientGroup
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.armservicemap import ServiceMap
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMClientGroupFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workspace_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            start_time=dict(
                type='datetime'
            ),
            end_time=dict(
                type='datetime'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.workspace_name = None
        self.name = None
        self.start_time = None
        self.end_time = None
        super(AzureRMClientGroupFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceMap,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['client_groups'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.client_groups.get(resource_group_name=self.resource_group,
                                                          workspace_name=self.workspace_name,
                                                          client_group_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Client Group.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'kind': d.get('kind', None)
        }
        return d


def main():
    AzureRMClientGroupFacts()


if __name__ == '__main__':
    main()

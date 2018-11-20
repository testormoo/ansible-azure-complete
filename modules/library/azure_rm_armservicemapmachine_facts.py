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
module: azure_rm_armservicemapmachine_facts
version_added: "2.8"
short_description: Get Azure Machine facts.
description:
    - Get facts of Azure Machine.

options:
    resource_group:
        description:
            - Resource group name within the specified subscriptionId.
        required: True
    workspace_name:
        description:
            - OMS workspace containing the resources of interest.
        required: True
    live:
        description:
            - "Specifies whether to return live resources (true) or inventory resources (false). Defaults to **true**. When retrieving live resources, the
               start time (`I(start_time)`) and end time (`I(end_time)`) of the desired interval should be included. When retrieving inventory resources,
               an optional I(timestamp) (`I(timestamp)`) parameter can be specified to return the version of each resource closest (not-after) that
               I(timestamp)."
    start_time:
        description:
            - UTC date and time specifying the start time of an interval. When not specified the service uses DateTime.UtcNow - 10m
    end_time:
        description:
            - UTC date and time specifying the end time of an interval. When not specified the service uses DateTime.UtcNow
    timestamp:
        description:
            - "UTC date and time specifying a time instance relative to which to evaluate each machine resource. Only applies when `I(live)=false`. When not
               specified, the service uses DateTime.UtcNow."
    top:
        description:
            - Page size to use. When not specified, the default page size is 100 records.
    name:
        description:
            - Machine resource name.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Machine
    azure_rm_armservicemapmachine_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      live: live
      start_time: start_time
      end_time: end_time
      timestamp: timestamp
      top: top

  - name: Get instance of Machine
    azure_rm_armservicemapmachine_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      name: machine_name
      timestamp: timestamp
'''

RETURN = '''
machines:
    description: A list of dictionaries containing facts for Machine.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource identifier.
            returned: always
            type: str
            sample: "/subscriptions/63BE4E24-FDF0-4E9C-9342-6A5D5A359722/resourceGroups/rg-sm/providers/Microsoft.OperationalInsights/workspaces/D6F79F14-E56
                    3-469B-84B5-9286D2803B2F/machines/m-A4AB1C69-03E9-42D2-B822-B42555569FB4"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: m-A4AB1C69-03E9-42D2-B822-B42555569FB4
        kind:
            description:
                - Constant filled by server.
            returned: always
            type: str
            sample: machine
        fully_qualified_domain_name:
            description:
                - Fully-qualified name of the machine, e.g., server.company.com
            returned: always
            type: str
            sample: fully_qualified_domain_name
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.armservicemap import ServiceMap
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMachinesFacts(AzureRMModuleBase):
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
            live=dict(
                type='str'
            ),
            start_time=dict(
                type='datetime'
            ),
            end_time=dict(
                type='datetime'
            ),
            timestamp=dict(
                type='datetime'
            ),
            top=dict(
                type='int'
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
        self.workspace_name = None
        self.live = None
        self.start_time = None
        self.end_time = None
        self.timestamp = None
        self.top = None
        self.name = None
        super(AzureRMMachinesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceMap,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        else:
            self.results['machines'] = self.list_by_workspace()
        elif self.name is not None:
            self.results['machines'] = self.get()
        return self.results

    def list_by_workspace(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.machines.list_by_workspace(resource_group_name=self.resource_group,
                                                                   workspace_name=self.workspace_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Machines.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.machines.get(resource_group_name=self.resource_group,
                                                     workspace_name=self.workspace_name,
                                                     machine_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Machines.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'kind': d.get('kind', None),
            'fully_qualified_domain_name': d.get('fully_qualified_domain_name', None)
        }
        return d


def main():
    AzureRMMachinesFacts()


if __name__ == '__main__':
    main()

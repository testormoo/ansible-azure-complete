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
module: azure_rm_armservicemapport_facts
version_added: "2.8"
short_description: Get Azure Port facts.
description:
    - Get facts of Azure Port.

options:
    resource_group:
        description:
            - Resource group name within the specified subscriptionId.
        required: True
    workspace_name:
        description:
            - OMS workspace containing the resources of interest.
        required: True
    machine_name:
        description:
            - Machine resource name.
        required: True
    port_name:
        description:
            - Port resource name.
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
  - name: Get instance of Port
    azure_rm_armservicemapport_facts:
      resource_group: resource_group_name
      workspace_name: workspace_name
      machine_name: machine_name
      port_name: port_name
      start_time: start_time
      end_time: end_time
'''

RETURN = '''
ports:
    description: A list of dictionaries containing facts for Port.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource identifier.
            returned: always
            type: str
            sample: id
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.armservicemap import ServiceMap
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPortsFacts(AzureRMModuleBase):
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
            machine_name=dict(
                type='str',
                required=True
            ),
            port_name=dict(
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
        self.machine_name = None
        self.port_name = None
        self.start_time = None
        self.end_time = None
        super(AzureRMPortsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ServiceMap,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['ports'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.ports.get(resource_group_name=self.resource_group,
                                                  workspace_name=self.workspace_name,
                                                  machine_name=self.machine_name,
                                                  port_name=self.port_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Ports.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None)
        }
        return d


def main():
    AzureRMPortsFacts()


if __name__ == '__main__':
    main()

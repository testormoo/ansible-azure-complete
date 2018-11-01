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
module: azure_rm_sqlinstancefailovergroup_facts
version_added: "2.8"
short_description: Get Azure Instance Failover Group facts.
description:
    - Get facts of Azure Instance Failover Group.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    location_name:
        description:
            - The name of the region where the resource is located.
        required: True
    failover_group_name:
        description:
            - The name of the failover group.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Instance Failover Group
    azure_rm_sqlinstancefailovergroup_facts:
      resource_group: resource_group_name
      location_name: location_name
      failover_group_name: failover_group_name

  - name: List instances of Instance Failover Group
    azure_rm_sqlinstancefailovergroup_facts:
      resource_group: resource_group_name
      location_name: location_name
'''

RETURN = '''
instance_failover_groups:
    description: A list of dictionaries containing facts for Instance Failover Group.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default/providers/Microsoft.Sql/locations/JapanEast/instanceFailoverG
                    roups/failover-group-test-3"
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: failover-group-test-3
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMInstanceFailoverGroupsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            location_name=dict(
                type='str',
                required=True
            ),
            failover_group_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.location_name = None
        self.failover_group_name = None
        super(AzureRMInstanceFailoverGroupsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.failover_group_name is not None:
            self.results['instance_failover_groups'] = self.get()
        else:
            self.results['instance_failover_groups'] = self.list_by_location()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.instance_failover_groups.get(resource_group_name=self.resource_group,
                                                                     location_name=self.location_name,
                                                                     failover_group_name=self.failover_group_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for InstanceFailoverGroups.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_location(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.instance_failover_groups.list_by_location(resource_group_name=self.resource_group,
                                                                                  location_name=self.location_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for InstanceFailoverGroups.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMInstanceFailoverGroupsFacts()


if __name__ == '__main__':
    main()

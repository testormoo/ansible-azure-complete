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
module: azure_rm_netappmounttarget_facts
version_added: "2.8"
short_description: Get Azure Mount Target facts.
description:
    - Get facts of Azure Mount Target.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    account_name:
        description:
            - The name of the NetApp account
        required: True
    pool_name:
        description:
            - The name of the capacity pool
        required: True
    volume_name:
        description:
            - The name of the volume
        required: True
    mount_target_name:
        description:
            - The name of the mount target
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
  - name: Get instance of Mount Target
    azure_rm_netappmounttarget_facts:
      resource_group: resource_group
      account_name: account_name
      pool_name: pool_name
      volume_name: volume_name
      mount_target_name: mount_target_name
'''

RETURN = '''
mount_targets:
    description: A list of dictionaries containing facts for Mount Target.
    returned: always
    type: complex
    contains:
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: eastus
        id:
            description:
                - Resource Id
            returned: always
            type: str
            sample: id
        name:
            description:
                - Resource name
            returned: always
            type: str
            sample: mountTarget1
        tags:
            description:
                - Resource tags
            returned: always
            type: str
            sample: tags
        gateway:
            description:
                - The gateway of the IPv4 address range to use when creating a new mount target
            returned: always
            type: str
            sample: 1.2.3.4
        netmask:
            description:
                - The netmask of the IPv4 address range to use when creating a new mount target
            returned: always
            type: str
            sample: 255.255.255.0
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.netapp import AzureNetAppFilesManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMMountTargetsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            pool_name=dict(
                type='str',
                required=True
            ),
            volume_name=dict(
                type='str',
                required=True
            ),
            mount_target_name=dict(
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
        self.account_name = None
        self.pool_name = None
        self.volume_name = None
        self.mount_target_name = None
        self.tags = None
        super(AzureRMMountTargetsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(AzureNetAppFilesManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['mount_targets'] = self.get()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.mount_targets.get(resource_group=self.resource_group,
                                                          account_name=self.account_name,
                                                          pool_name=self.pool_name,
                                                          volume_name=self.volume_name,
                                                          mount_target_name=self.mount_target_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for MountTargets.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_item(response))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'location': d.get('location', None),
            'id': d.get('id', None),
            'name': d.get('name', None),
            'tags': d.get('tags', None),
            'gateway': d.get('gateway', None),
            'netmask': d.get('netmask', None)
        }
        return d


def main():
    AzureRMMountTargetsFacts()


if __name__ == '__main__':
    main()

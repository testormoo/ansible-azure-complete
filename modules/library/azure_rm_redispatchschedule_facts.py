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
module: azure_rm_redispatchschedule_facts
version_added: "2.8"
short_description: Get Azure Patch Schedule facts.
description:
    - Get facts of Azure Patch Schedule.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the redis cache.
    default:
        description:
            - Default string modeled as parameter for auto generation to work correctly.
    name:
        description:
            - The name of the Redis cache.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Patch Schedule
    azure_rm_redispatchschedule_facts:
      resource_group: resource_group_name
      name: name
      default: default

  - name: List instances of Patch Schedule
    azure_rm_redispatchschedule_facts:
      resource_group: resource_group_name
      name: cache_name
'''

RETURN = '''
patch_schedules:
    description: A list of dictionaries containing facts for Patch Schedule.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Cache/Redis/cache1/patchSchedules/default
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: default
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.redis import RedisManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPatchSchedulesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            default=dict(
                type='str'
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
        self.name = None
        self.default = None
        self.name = None
        super(AzureRMPatchSchedulesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(RedisManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.name is not None and
                self.default is not None):
            self.results['patch_schedules'] = self.get()
        elif self.name is not None:
            self.results['patch_schedules'] = self.list_by_redis_resource()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.patch_schedules.get(resource_group_name=self.resource_group,
                                                            name=self.name,
                                                            default=self.default)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for PatchSchedules.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_redis_resource(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.patch_schedules.list_by_redis_resource(resource_group_name=self.resource_group,
                                                                               cache_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for PatchSchedules.')

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
    AzureRMPatchSchedulesFacts()


if __name__ == '__main__':
    main()

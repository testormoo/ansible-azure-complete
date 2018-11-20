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
module: azure_rm_workloadmonitornotificationsetting_facts
version_added: "2.8"
short_description: Get Azure Notification Setting facts.
description:
    - Get facts of Azure Notification Setting.

options:
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    resource_namespace:
        description:
            - The Namespace of the resource.
        required: True
    resource_type:
        description:
            - The type of the resource.
        required: True
    name:
        description:
            - Name of the resource.
        required: True
    skiptoken:
        description:
            - The page-continuation token to use with a paged version of this API.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: List instances of Notification Setting
    azure_rm_workloadmonitornotificationsetting_facts:
      resource_group: resource_group_name
      resource_namespace: resource_namespace
      resource_type: resource_type
      name: resource_name
      skiptoken: skiptoken
'''

RETURN = '''
notification_settings:
    description: A list of dictionaries containing facts for Notification Setting.
    returned: always
    type: complex
    contains:
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.workloadmonitor import WorkloadMonitorAPI
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMNotificationSettingsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_namespace=dict(
                type='str',
                required=True
            ),
            resource_type=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            skiptoken=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.resource_group = None
        self.resource_namespace = None
        self.resource_type = None
        self.name = None
        self.skiptoken = None
        super(AzureRMNotificationSettingsFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(WorkloadMonitorAPI,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        self.results['notification_settings'] = self.list_by_resource()
        return self.results

    def list_by_resource(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.notification_settings.list_by_resource(resource_group_name=self.resource_group,
                                                                               resource_namespace=self.resource_namespace,
                                                                               resource_type=self.resource_type,
                                                                               resource_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for NotificationSettings.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
        }
        return d


def main():
    AzureRMNotificationSettingsFacts()


if __name__ == '__main__':
    main()

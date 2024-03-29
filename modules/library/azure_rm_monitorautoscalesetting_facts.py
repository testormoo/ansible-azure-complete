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
module: azure_rm_monitorautoscalesetting_facts
version_added: "2.8"
short_description: Get Azure Autoscale Setting facts.
description:
    - Get facts of Azure Autoscale Setting.

options:
    resource_group:
        description:
            - The name of the resource group.
    name:
        description:
            - The autoscale setting name.
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Autoscale Setting
    azure_rm_monitorautoscalesetting_facts:
      resource_group: resource_group_name
      name: autoscale_setting_name

  - name: List instances of Autoscale Setting
    azure_rm_monitorautoscalesetting_facts:
      resource_group: resource_group_name

  - name: List instances of Autoscale Setting
    azure_rm_monitorautoscalesetting_facts:
'''

RETURN = '''
autoscale_settings:
    description: A list of dictionaries containing facts for Autoscale Setting.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Azure resource Id
            returned: always
            type: str
            sample: "/subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/TestingMetricsScaleSet/providers/microsoft.insights/autoscalesettings
                    /MySetting"
        name:
            description:
                - Azure resource name
            returned: always
            type: str
            sample: MySetting
        location:
            description:
                - Resource location
            returned: always
            type: str
            sample: West US
        tags:
            description:
                - Resource tags
            returned: always
            type: complex
            sample: "{\n  '$type': 'Microsoft.WindowsAzure.Management.Common.Storage.CasePreservedDictionary,
                     Microsoft.WindowsAzure.Management.Common.Storage'\n}"
        profiles:
            description:
                - "the collection of automatic scaling profiles that specify different scaling parameters for different time periods. A maximum of 20
                   profiles can be specified."
            returned: always
            type: complex
            sample: profiles
            contains:
        notifications:
            description:
                - the collection of notifications.
            returned: always
            type: complex
            sample: notifications
            contains:
        enabled:
            description:
                - "the enabled flag. Specifies whether automatic scaling is enabled for the resource. The default value is 'true'."
            returned: always
            type: str
            sample: True
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMAutoscaleSettingFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str'
            ),
            name=dict(
                type='str'
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
        self.name = None
        self.tags = None
        super(AzureRMAutoscaleSettingFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.name is not None):
            self.results['autoscale_settings'] = self.get()
        elif self.resource_group is not None:
            self.results['autoscale_settings'] = self.list_by_resource_group()
        else:
            self.results['autoscale_settings'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.autoscale_settings.get(resource_group_name=self.resource_group,
                                                               autoscale_setting_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Autoscale Setting.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.autoscale_settings.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Autoscale Setting.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.autoscale_settings.list_by_subscription()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Autoscale Setting.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'location': d.get('location', None),
            'tags': d.get('tags', None),
            'profiles': {
            },
            'notifications': {
            },
            'enabled': d.get('enabled', None)
        }
        return d


def main():
    AzureRMAutoscaleSettingFacts()


if __name__ == '__main__':
    main()

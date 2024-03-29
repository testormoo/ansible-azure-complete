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
module: azure_rm_frontdoorhealthprobesetting_facts
version_added: "2.8"
short_description: Get Azure Health Probe Setting facts.
description:
    - Get facts of Azure Health Probe Setting.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    front_door_name:
        description:
            - Name of the Front Door which is globally unique.
        required: True
    name:
        description:
            - Name of the health probe settings which is unique within the Front Door.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Health Probe Setting
    azure_rm_frontdoorhealthprobesetting_facts:
      resource_group: resource_group_name
      front_door_name: front_door_name
      name: health_probe_settings_name

  - name: List instances of Health Probe Setting
    azure_rm_frontdoorhealthprobesetting_facts:
      resource_group: resource_group_name
      front_door_name: front_door_name
'''

RETURN = '''
health_probe_settings:
    description: A list of dictionaries containing facts for Health Probe Setting.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/frontDoors/frontDoor1/healthProbeSettings/healthProbeSettings1
        path:
            description:
                - The path to use for the health probe. Default is /
            returned: always
            type: str
            sample: /
        protocol:
            description:
                - "Protocol scheme to use for this probe. Possible values include: 'Http', 'Https'"
            returned: always
            type: str
            sample: Http
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: healthProbeSettings1
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.frontdoor import FrontDoorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMHealthProbeSettingFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            front_door_name=dict(
                type='str',
                required=True
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
        self.front_door_name = None
        self.name = None
        super(AzureRMHealthProbeSettingFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(FrontDoorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.name is not None:
            self.results['health_probe_settings'] = self.get()
        else:
            self.results['health_probe_settings'] = self.list_by_front_door()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.health_probe_settings.get(resource_group_name=self.resource_group,
                                                                  front_door_name=self.front_door_name,
                                                                  health_probe_settings_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Health Probe Setting.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_front_door(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.health_probe_settings.list_by_front_door(resource_group_name=self.resource_group,
                                                                                 front_door_name=self.front_door_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Health Probe Setting.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'path': d.get('path', None),
            'protocol': d.get('protocol', None),
            'name': d.get('name', None)
        }
        return d


def main():
    AzureRMHealthProbeSettingFacts()


if __name__ == '__main__':
    main()

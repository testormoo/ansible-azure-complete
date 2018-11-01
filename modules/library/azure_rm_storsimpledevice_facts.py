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
module: azure_rm_storsimpledevice_facts
version_added: "2.8"
short_description: Get Azure Device facts.
description:
    - Get facts of Azure Device.

options:
    device_name:
        description:
            - The device name.
    resource_group:
        description:
            - The resource group name
        required: True
    manager_name:
        description:
            - The manager name
        required: True
    expand:
        description:
            - Specify $expand=details to populate additional fields related to the device.

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Device
    azure_rm_storsimpledevice_facts:
      device_name: device_name
      resource_group: resource_group_name
      manager_name: manager_name
      expand: expand

  - name: List instances of Device
    azure_rm_storsimpledevice_facts:
      resource_group: resource_group_name
      manager_name: manager_name
      expand: expand
'''

RETURN = '''
devices:
    description: A list of dictionaries containing facts for Device.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The identifier.
            returned: always
            type: str
            sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzur
                    eSDKOperations/devices/HSDK-ARCSX4MVKZ"
        name:
            description:
                - The name.
            returned: always
            type: str
            sample: HSDK-ARCSX4MVKZ
        culture:
            description:
                - "Language culture setting on the device. For eg: 'en-US'"
            returned: always
            type: str
            sample: en-US
        status:
            description:
                - "Current status of the device. Possible values include: 'Unknown', 'Online', 'Offline', 'RequiresAttention', 'MaintenanceMode',
                   'Creating', 'Provisioning', 'Deleted', 'ReadyToSetup', 'Deactivated', 'Deactivating'"
            returned: always
            type: str
            sample: Online
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDevicesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            device_name=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            manager_name=dict(
                type='str',
                required=True
            ),
            expand=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.device_name = None
        self.resource_group = None
        self.manager_name = None
        self.expand = None
        super(AzureRMDevicesFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.device_name is not None:
            self.results['devices'] = self.get()
        else:
            self.results['devices'] = self.list_by_manager()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.devices.get(device_name=self.device_name,
                                                    resource_group_name=self.resource_group,
                                                    manager_name=self.manager_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Devices.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_manager(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.devices.list_by_manager(resource_group_name=self.resource_group,
                                                                manager_name=self.manager_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Devices.')

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'culture': d.get('culture', None),
            'status': d.get('status', None)
        }
        return d


def main():
    AzureRMDevicesFacts()


if __name__ == '__main__':
    main()

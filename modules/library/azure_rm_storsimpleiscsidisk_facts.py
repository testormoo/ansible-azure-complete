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
module: azure_rm_storsimpleiscsidisk_facts
version_added: "2.8"
short_description: Get Azure Iscsi Disk facts.
description:
    - Get facts of Azure Iscsi Disk.

options:
    device_name:
        description:
            - The device name.
        required: True
    iscsi_server_name:
        description:
            - The iscsi server name.
    disk_name:
        description:
            - The disk name.
    resource_group:
        description:
            - The resource group name
        required: True
    name:
        description:
            - The manager name
        required: True

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Iscsi Disk
    azure_rm_storsimpleiscsidisk_facts:
      device_name: device_name
      iscsi_server_name: iscsi_server_name
      disk_name: disk_name
      resource_group: resource_group_name
      name: manager_name

  - name: List instances of Iscsi Disk
    azure_rm_storsimpleiscsidisk_facts:
      device_name: device_name
      iscsi_server_name: iscsi_server_name
      resource_group: resource_group_name
      name: manager_name

  - name: List instances of Iscsi Disk
    azure_rm_storsimpleiscsidisk_facts:
      device_name: device_name
      resource_group: resource_group_name
      name: manager_name
'''

RETURN = '''
iscsi_disks:
    description: A list of dictionaries containing facts for Iscsi Disk.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The identifier.
            returned: always
            type: str
            sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzur
                    eSDKOperations/devices/HSDK-0NZI14MDTF/iscsiServers/HSDK-0NZI14MDTF/disks/Auto-TestIscsiDisk1"
        name:
            description:
                - The name.
            returned: always
            type: str
            sample: Auto-TestIscsiDisk1
        description:
            description:
                - The description.
            returned: always
            type: str
            sample: Demo IscsiDisk for SDK Test Tiered
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMIscsiDiskFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            device_name=dict(
                type='str',
                required=True
            ),
            iscsi_server_name=dict(
                type='str'
            ),
            disk_name=dict(
                type='str'
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.mgmt_client = None
        self.device_name = None
        self.iscsi_server_name = None
        self.disk_name = None
        self.resource_group = None
        self.name = None
        super(AzureRMIscsiDiskFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.iscsi_server_name is not None and
                self.disk_name is not None):
            self.results['iscsi_disks'] = self.get()
        elif self.iscsi_server_name is not None:
            self.results['iscsi_disks'] = self.list_by_iscsi_server()
        else:
            self.results['iscsi_disks'] = self.list_by_device()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iscsi_disks.get(device_name=self.device_name,
                                                        iscsi_server_name=self.iscsi_server_name,
                                                        disk_name=self.disk_name,
                                                        resource_group_name=self.resource_group,
                                                        manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iscsi Disk.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_iscsi_server(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iscsi_disks.list_by_iscsi_server(device_name=self.device_name,
                                                                         iscsi_server_name=self.iscsi_server_name,
                                                                         resource_group_name=self.resource_group,
                                                                         manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iscsi Disk.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def list_by_device(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.iscsi_disks.list_by_device(device_name=self.device_name,
                                                                   resource_group_name=self.resource_group,
                                                                   manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Iscsi Disk.')

        if response is not None:
            for item in response:
                results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'id': d.get('id', None),
            'name': d.get('name', None),
            'description': d.get('description', None)
        }
        return d


def main():
    AzureRMIscsiDiskFacts()


if __name__ == '__main__':
    main()

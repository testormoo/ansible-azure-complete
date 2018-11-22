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
module: azure_rm_packetcapture
version_added: "2.8"
short_description: Manage Azure Packet Capture instance.
description:
    - Create, update and delete instance of Azure Packet Capture.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    network_watcher_name:
        description:
            - The name of the network watcher.
        required: True
    name:
        description:
            - The name of the packet capture session.
        required: True
    target:
        description:
            - The ID of the targeted resource, only VM is currently supported.
            - Required when C(state) is I(present).
    bytes_to_capture_per_packet:
        description:
            - Number of bytes captured per packet, the remaining bytes are truncated.
    total_bytes_per_session:
        description:
            - Maximum size of the capture output.
    time_limit_in_seconds:
        description:
            - Maximum duration of the capture session in seconds.
    storage_location:
        description:
            - Required when C(state) is I(present).
        suboptions:
            storage_id:
                description:
                    - The ID of the storage account to save the packet capture session. Required if no local file path is provided.
            storage_path:
                description:
                    - The URI of the storage path to save the packet capture. Must be a well-formed URI describing the location to save the packet capture.
            file_path:
                description:
                    - "A valid local path on the targeting VM. Must include the name of the capture file (*.cap). For linux virtual machine it must start
                       with /var/captures. Required if no storage ID is provided, otherwise optional."
    filters:
        description:
        type: list
        suboptions:
            protocol:
                description:
                    - Protocol to be filtered on.
                choices:
                    - 'tcp'
                    - 'udp'
                    - 'any'
            local_ip_address:
                description:
                    - "Local IP Address to be filtered on. Notation: '127.0.0.1' for single address entry. '127.0.0.1-127.0.0.255' for range.
                       '127.0.0.1;127.0.0.5'? for multiple entries. Multiple ranges not currently supported. Mixing ranges with multiple entries not
                       currently supported. Default = null."
            remote_ip_address:
                description:
                    - "Local IP Address to be filtered on. Notation: '127.0.0.1' for single address entry. '127.0.0.1-127.0.0.255' for range.
                       '127.0.0.1;127.0.0.5;' for multiple entries. Multiple ranges not currently supported. Mixing ranges with multiple entries not
                       currently supported. Default = null."
            local_port:
                description:
                    - "Local port to be filtered on. Notation: '80' for single port entry.'80-85' for range. '80;443;' for multiple entries. Multiple ranges
                       not currently supported. Mixing ranges with multiple entries not currently supported. Default = null."
            remote_port:
                description:
                    - "Remote port to be filtered on. Notation: '80' for single port entry.'80-85' for range. '80;443;' for multiple entries. Multiple
                       ranges not currently supported. Mixing ranges with multiple entries not currently supported. Default = null."
    state:
      description:
        - Assert the state of the Packet Capture.
        - Use 'present' to create or update an Packet Capture and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Packet Capture
    azure_rm_packetcapture:
      resource_group: NOT FOUND
      network_watcher_name: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - ID of the packet capture operation.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMPacketCapture(AzureRMModuleBase):
    """Configuration class for an Azure RM Packet Capture resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            network_watcher_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            target=dict(
                type='str'
            ),
            bytes_to_capture_per_packet=dict(
                type='int'
            ),
            total_bytes_per_session=dict(
                type='int'
            ),
            time_limit_in_seconds=dict(
                type='int'
            ),
            storage_location=dict(
                type='dict'
            ),
            filters=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.network_watcher_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMPacketCapture, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_upper(self.parameters, ['filters', 'protocol'])
        dict_map(self.parameters, ['filters', 'protocol'], {'any': 'Any'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(NetworkManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_packetcapture()

        if not old_response:
            self.log("Packet Capture instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Packet Capture instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Packet Capture instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_packetcapture()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Packet Capture instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_packetcapture()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_packetcapture():
                time.sleep(20)
        else:
            self.log("Packet Capture instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_packetcapture(self):
        '''
        Creates or updates Packet Capture with the specified configuration.

        :return: deserialized Packet Capture instance state dictionary
        '''
        self.log("Creating / Updating the Packet Capture instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.packet_captures.create(resource_group_name=self.resource_group,
                                                                   network_watcher_name=self.network_watcher_name,
                                                                   packet_capture_name=self.name,
                                                                   parameters=self.parameters)
            else:
                response = self.mgmt_client.packet_captures.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Packet Capture instance.')
            self.fail("Error creating the Packet Capture instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_packetcapture(self):
        '''
        Deletes specified Packet Capture instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Packet Capture instance {0}".format(self.name))
        try:
            response = self.mgmt_client.packet_captures.delete(resource_group_name=self.resource_group,
                                                               network_watcher_name=self.network_watcher_name,
                                                               packet_capture_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Packet Capture instance.')
            self.fail("Error deleting the Packet Capture instance: {0}".format(str(e)))

        return True

    def get_packetcapture(self):
        '''
        Gets the properties of the specified Packet Capture.

        :return: deserialized Packet Capture instance state dictionary
        '''
        self.log("Checking if the Packet Capture instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.packet_captures.get(resource_group_name=self.resource_group,
                                                            network_watcher_name=self.network_watcher_name,
                                                            packet_capture_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Packet Capture instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Packet Capture instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path, result):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            result['compare'] = 'changed [' + path + '] old dict is null'
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k, result):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
            result['compare'] = 'changed [' + path + '] length is different or null'
            return False
        if isinstance(old[0], dict):
            key = None
            if 'id' in old[0] and 'id' in new[0]:
                key = 'id'
            elif 'name' in old[0] and 'name' in new[0]:
                key = 'name'
            new = sorted(new, key=lambda x: x.get(key, None))
            old = sorted(old, key=lambda x: x.get(key, None))
        else:
            new = sorted(new)
            old = sorted(old)
        for i in range(len(new)):
            if not default_compare(new[i], old[i], path + '/*', result):
                return False
        return True
    else:
        if path == '/location':
            new = new.replace(' ', '').lower()
            old = new.replace(' ', '').lower()
        if new == old:
            return True
        else:
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMPacketCapture()


if __name__ == '__main__':
    main()

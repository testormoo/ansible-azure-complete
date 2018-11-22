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
module: azure_rm_medialiveoutput
version_added: "2.8"
short_description: Manage Azure Live Output instance.
description:
    - Create, update and delete instance of Azure Live Output.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    live_event_name:
        description:
            - The name of the Live Event.
        required: True
    name:
        description:
            - The name of the Live Output.
        required: True
    description:
        description:
            - The description of the Live Output.
    asset_name:
        description:
            - The asset name.
            - Required when C(state) is I(present).
    archive_window_length:
        description:
            - ISO 8601 timespan duration of the archive window length. This is duration that customer want to retain the recorded content.
            - Required when C(state) is I(present).
    manifest_name:
        description:
            - The manifest file name.  If not provided, the service will generate one automatically.
    hls:
        description:
            - The HLS configuration.
        suboptions:
            fragments_per_ts_segment:
                description:
                    - The amount of fragments per HTTP Live Streaming (HLS) segment.
    output_snap_time:
        description:
            - The output snapshot time.
    state:
      description:
        - Assert the state of the Live Output.
        - Use 'present' to create or update an Live Output and 'absent' to delete it.
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
  - name: Create (or update) Live Output
    azure_rm_medialiveoutput:
      resource_group: mediaresources
      account_name: slitestmedia10
      live_event_name: myLiveEvent1
      name: myLiveOutput1
      description: test live output 1
      asset_name: 6f3264f5-a189-48b4-a29a-a40f22575212
      archive_window_length: PT5M
      manifest_name: testmanifest
      hls:
        fragments_per_ts_segment: 5
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: "/subscriptions/0a6ec948-5a62-437d-b9df-934dc7c1b722/resourceGroups/mediaresources/providers/Microsoft.Media/mediaservices/slitestmedia10/liveeve
            nts/myLiveEvent1/liveoutputs/myLiveOutput1"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMLiveOutput(AzureRMModuleBase):
    """Configuration class for an Azure RM Live Output resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            live_event_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            asset_name=dict(
                type='str'
            ),
            archive_window_length=dict(
                type='str'
            ),
            manifest_name=dict(
                type='str'
            ),
            hls=dict(
                type='dict'
            ),
            output_snap_time=dict(
                type='int'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.live_event_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLiveOutput, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_liveoutput()

        if not old_response:
            self.log("Live Output instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Live Output instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Live Output instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_liveoutput()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Live Output instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_liveoutput()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_liveoutput():
                time.sleep(20)
        else:
            self.log("Live Output instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_liveoutput(self):
        '''
        Creates or updates Live Output with the specified configuration.

        :return: deserialized Live Output instance state dictionary
        '''
        self.log("Creating / Updating the Live Output instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.live_outputs.create(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                live_event_name=self.live_event_name,
                                                                live_output_name=self.name,
                                                                parameters=self.parameters)
            else:
                response = self.mgmt_client.live_outputs.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Live Output instance.')
            self.fail("Error creating the Live Output instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_liveoutput(self):
        '''
        Deletes specified Live Output instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Live Output instance {0}".format(self.name))
        try:
            response = self.mgmt_client.live_outputs.delete(resource_group_name=self.resource_group,
                                                            account_name=self.account_name,
                                                            live_event_name=self.live_event_name,
                                                            live_output_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Live Output instance.')
            self.fail("Error deleting the Live Output instance: {0}".format(str(e)))

        return True

    def get_liveoutput(self):
        '''
        Gets the properties of the specified Live Output.

        :return: deserialized Live Output instance state dictionary
        '''
        self.log("Checking if the Live Output instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.live_outputs.get(resource_group_name=self.resource_group,
                                                         account_name=self.account_name,
                                                         live_event_name=self.live_event_name,
                                                         live_output_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Live Output instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Live Output instance.')
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
    AzureRMLiveOutput()


if __name__ == '__main__':
    main()

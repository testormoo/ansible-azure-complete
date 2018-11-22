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
module: azure_rm_mediaassetfilter
version_added: "2.8"
short_description: Manage Azure Asset Filter instance.
description:
    - Create, update and delete instance of Azure Asset Filter.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    asset_name:
        description:
            - The Asset name.
        required: True
    name:
        description:
            - The Asset Filter name
        required: True
    presentation_time_range:
        description:
            - The presentation time range.
        suboptions:
            start_timestamp:
                description:
                    - The absolute start time boundary.
                    - Required when C(state) is I(present).
            end_timestamp:
                description:
                    - The absolute end time boundary.
                    - Required when C(state) is I(present).
            presentation_window_duration:
                description:
                    - The relative to end sliding window.
                    - Required when C(state) is I(present).
            live_backoff_duration:
                description:
                    - The relative to end right edge.
                    - Required when C(state) is I(present).
            timescale:
                description:
                    - The time scale of time stamps.
                    - Required when C(state) is I(present).
            force_end_timestamp:
                description:
                    - The indicator of forcing exsiting of end time stamp.
                    - Required when C(state) is I(present).
    first_quality:
        description:
            - The first quality.
        suboptions:
            bitrate:
                description:
                    - The first quality bitrate.
                    - Required when C(state) is I(present).
    tracks:
        description:
            - The tracks selection conditions.
        type: list
        suboptions:
            track_selections:
                description:
                    - The track selections.
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    property:
                        description:
                            - The track property C(type).
                            - Required when C(state) is I(present).
                        choices:
                            - 'unknown'
                            - 'type'
                            - 'name'
                            - 'language'
                            - 'four_cc'
                            - 'bitrate'
                    value:
                        description:
                            - The track proprty value.
                            - Required when C(state) is I(present).
                    operation:
                        description:
                            - The track I(property) condition operation.
                            - Required when C(state) is I(present).
                        choices:
                            - 'equal'
                            - 'not_equal'
    state:
      description:
        - Assert the state of the Asset Filter.
        - Use 'present' to create or update an Asset Filter and 'absent' to delete it.
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
  - name: Create (or update) Asset Filter
    azure_rm_mediaassetfilter:
      resource_group: contoso
      account_name: contosomedia
      asset_name: ClimbingMountRainer
      name: newAssetFilter
      presentation_time_range:
        start_timestamp: 0
        end_timestamp: 170000000
        presentation_window_duration: 9223372036854776000
        live_backoff_duration: 0
        timescale: 10000000
        force_end_timestamp: False
      first_quality:
        bitrate: 128000
      tracks:
        - track_selections:
            - property: Type
              value: Audio
              operation: Equal
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso/providers/Microsoft.Media/mediaservices/contosomedia/assets/ClimbingM
            ountRainer/assetFilters/assetFilterWithTimeWindowAndTrack"
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


class AzureRMAssetFilter(AzureRMModuleBase):
    """Configuration class for an Azure RM Asset Filter resource"""

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
            asset_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            presentation_time_range=dict(
                type='dict'
            ),
            first_quality=dict(
                type='dict'
            ),
            tracks=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.asset_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAssetFilter, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['tracks', 'track_selections', 'property'], True)
        dict_map(self.parameters, ['tracks', 'track_selections', 'property'], {'four_cc': 'FourCC'})
        dict_camelize(self.parameters, ['tracks', 'track_selections', 'operation'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_assetfilter()

        if not old_response:
            self.log("Asset Filter instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Asset Filter instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Asset Filter instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_assetfilter()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Asset Filter instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_assetfilter()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_assetfilter():
                time.sleep(20)
        else:
            self.log("Asset Filter instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_assetfilter(self):
        '''
        Creates or updates Asset Filter with the specified configuration.

        :return: deserialized Asset Filter instance state dictionary
        '''
        self.log("Creating / Updating the Asset Filter instance {0}".format(self.name))

        try:
            response = self.mgmt_client.asset_filters.create_or_update(resource_group_name=self.resource_group,
                                                                       account_name=self.account_name,
                                                                       asset_name=self.asset_name,
                                                                       filter_name=self.name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Asset Filter instance.')
            self.fail("Error creating the Asset Filter instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_assetfilter(self):
        '''
        Deletes specified Asset Filter instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Asset Filter instance {0}".format(self.name))
        try:
            response = self.mgmt_client.asset_filters.delete(resource_group_name=self.resource_group,
                                                             account_name=self.account_name,
                                                             asset_name=self.asset_name,
                                                             filter_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Asset Filter instance.')
            self.fail("Error deleting the Asset Filter instance: {0}".format(str(e)))

        return True

    def get_assetfilter(self):
        '''
        Gets the properties of the specified Asset Filter.

        :return: deserialized Asset Filter instance state dictionary
        '''
        self.log("Checking if the Asset Filter instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.asset_filters.get(resource_group_name=self.resource_group,
                                                          account_name=self.account_name,
                                                          asset_name=self.asset_name,
                                                          filter_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Asset Filter instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Asset Filter instance.')
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
    AzureRMAssetFilter()


if __name__ == '__main__':
    main()

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
short_description: Manage Live Output instance.
description:
    - Create, update and delete instance of Live Output.

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
    live_output_name:
        description:
            - The name of the Live Output.
        required: True
    description:
        description:
            - The description of the Live Output.
    asset_name:
        description:
            - The asset name.
        required: True
    archive_window_length:
        description:
            - ISO 8601 timespan duration of the archive window length. This is duration that customer want to retain the recorded content.
        required: True
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
      live_output_name: myLiveOutput1
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


class AzureRMLiveOutputs(AzureRMModuleBase):
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
            live_output_name=dict(
                type='str',
                required=True
            ),
            description=dict(
                type='str'
            ),
            asset_name=dict(
                type='str',
                required=True
            ),
            archive_window_length=dict(
                type='str',
                required=True
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
        self.live_output_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLiveOutputs, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "asset_name":
                    self.parameters["asset_name"] = kwargs[key]
                elif key == "archive_window_length":
                    self.parameters["archive_window_length"] = kwargs[key]
                elif key == "manifest_name":
                    self.parameters["manifest_name"] = kwargs[key]
                elif key == "hls":
                    self.parameters["hls"] = kwargs[key]
                elif key == "output_snap_time":
                    self.parameters["output_snap_time"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Live Output instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Live Output instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_liveoutput()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
        return self.results

    def create_update_liveoutput(self):
        '''
        Creates or updates Live Output with the specified configuration.

        :return: deserialized Live Output instance state dictionary
        '''
        self.log("Creating / Updating the Live Output instance {0}".format(self.live_output_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.live_outputs.create(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                live_event_name=self.live_event_name,
                                                                live_output_name=self.live_output_name,
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
        self.log("Deleting the Live Output instance {0}".format(self.live_output_name))
        try:
            response = self.mgmt_client.live_outputs.delete(resource_group_name=self.resource_group,
                                                            account_name=self.account_name,
                                                            live_event_name=self.live_event_name,
                                                            live_output_name=self.live_output_name)
        except CloudError as e:
            self.log('Error attempting to delete the Live Output instance.')
            self.fail("Error deleting the Live Output instance: {0}".format(str(e)))

        return True

    def get_liveoutput(self):
        '''
        Gets the properties of the specified Live Output.

        :return: deserialized Live Output instance state dictionary
        '''
        self.log("Checking if the Live Output instance {0} is present".format(self.live_output_name))
        found = False
        try:
            response = self.mgmt_client.live_outputs.get(resource_group_name=self.resource_group,
                                                         account_name=self.account_name,
                                                         live_event_name=self.live_event_name,
                                                         live_output_name=self.live_output_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Live Output instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Live Output instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMLiveOutputs()


if __name__ == '__main__':
    main()

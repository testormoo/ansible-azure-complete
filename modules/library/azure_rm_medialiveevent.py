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
module: azure_rm_medialiveevent
version_added: "2.8"
short_description: Manage Live Event instance.
description:
    - Create, update and delete instance of Live Event.

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
    auto_start:
        description:
            - The flag indicates if the resource should be automatically started on creation.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    description:
        description:
            - The Live Event description.
    input:
        description:
            - The Live Event input.
        required: True
        suboptions:
            streaming_protocol:
                description:
                    - The streaming protocol for the Live Event.  This is specified at creation time and cannot be updated.
                required: True
                choices:
                    - 'fragmented_mp4'
                    - 'rtmp'
            access_control:
                description:
                    - The access control for LiveEvent Input.
                suboptions:
                    ip:
                        description:
                            - The IP access control properties.
                        suboptions:
                            allow:
                                description:
                                    - The IP allow list.
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - The friendly name for the IP I(address) range.
                                    address:
                                        description:
                                            - The IP address.
                                    subnet_prefix_length:
                                        description:
                                            - The subnet mask prefix length (see CIDR notation).
            key_frame_interval_duration:
                description:
                    - ISO 8601 timespan duration of the key frame interval duration.
            access_token:
                description:
                    - "A unique identifier for a stream.  This can be specified at creation time but cannot be updated.  If omitted, the service will
                       generate a unique value."
            endpoints:
                description:
                    - The input endpoints for the Live Event.
                type: list
                suboptions:
                    protocol:
                        description:
                            - The endpoint protocol.
                    url:
                        description:
                            - The endpoint URL.
    preview:
        description:
            - The Live Event preview.
        suboptions:
            endpoints:
                description:
                    - The endpoints for preview.
                type: list
                suboptions:
                    protocol:
                        description:
                            - The endpoint protocol.
                    url:
                        description:
                            - The endpoint URL.
            access_control:
                description:
                    - The access control for LiveEvent preview.
                suboptions:
                    ip:
                        description:
                            - The IP access control properties.
                        suboptions:
                            allow:
                                description:
                                    - The IP allow list.
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - The friendly name for the IP I(address) range.
                                    address:
                                        description:
                                            - The IP address.
                                    subnet_prefix_length:
                                        description:
                                            - The subnet mask prefix length (see CIDR notation).
            preview_locator:
                description:
                    - "The identifier of the preview locator in Guid format.  Specifying this at creation time allows the caller to know the preview locator
                       url before the event is created.  If omitted, the service will generate a random identifier.  This value cannot be updated once the
                       live event is created."
            streaming_policy_name:
                description:
                    - The name of streaming policy used for the LiveEvent preview.  This value is specified at creation time and cannot be updated.
            alternative_media_id:
                description:
                    - "An Alternative Media Identifier associated with the StreamingLocator created for the preview.  This value is specified at creation
                       time and cannot be updated.  The identifier can be used in the CustomLicenseAcquisitionUrlTemplate or the
                       CustomKeyAcquisitionUrlTemplate of the StreamingPolicy specified in the I(streaming_policy_name) field."
    encoding:
        description:
            - The Live Event encoding.
        suboptions:
            encoding_type:
                description:
                    - The encoding type for Live Event.  This value is specified at creation time and cannot be updated.
                choices:
                    - 'none'
                    - 'basic'
            preset_name:
                description:
                    - The encoding preset name.  This value is specified at creation time and cannot be updated.
    cross_site_access_policies:
        description:
            - The Live Event access policies.
        suboptions:
            client_access_policy:
                description:
                    - The content of clientaccesspolicy.xml used by Silverlight.
            cross_domain_policy:
                description:
                    - The content of crossdomain.xml used by Silverlight.
    vanity_url:
        description:
            - Specifies whether to use a vanity url with the Live Event.  This value is specified at creation time and cannot be updated.
    stream_options:
        description:
            - The options to use for the LiveEvent.  This value is specified at creation time and cannot be updated.
        type: list
    state:
      description:
        - Assert the state of the Live Event.
        - Use 'present' to create or update an Live Event and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Live Event
    azure_rm_medialiveevent:
      resource_group: mediaresources
      account_name: slitestmedia10
      live_event_name: myLiveEvent1
      auto_start: NOT FOUND
      location: eastus
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: "/subscriptions/0a6ec948-5a62-437d-b9df-934dc7c1b722/resourceGroups/mediaresources/providers/Microsoft.Media/mediaservices/slitestmedia10/liveeve
            nts/myLiveEvent1"
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


class AzureRMLiveEvents(AzureRMModuleBase):
    """Configuration class for an Azure RM Live Event resource"""

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
            auto_start=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            input=dict(
                type='dict',
                required=True
            ),
            preview=dict(
                type='dict'
            ),
            encoding=dict(
                type='dict'
            ),
            cross_site_access_policies=dict(
                type='dict'
            ),
            vanity_url=dict(
                type='str'
            ),
            stream_options=dict(
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
        self.live_event_name = None
        self.auto_start = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMLiveEvents, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "input":
                    ev = kwargs[key]
                    if 'streaming_protocol' in ev:
                        if ev['streaming_protocol'] == 'fragmented_mp4':
                            ev['streaming_protocol'] = 'FragmentedMP4'
                        elif ev['streaming_protocol'] == 'rtmp':
                            ev['streaming_protocol'] = 'RTMP'
                    self.parameters["input"] = ev
                elif key == "preview":
                    self.parameters["preview"] = kwargs[key]
                elif key == "encoding":
                    ev = kwargs[key]
                    if 'encoding_type' in ev:
                        if ev['encoding_type'] == 'none':
                            ev['encoding_type'] = 'None'
                        elif ev['encoding_type'] == 'basic':
                            ev['encoding_type'] = 'Basic'
                    self.parameters["encoding"] = ev
                elif key == "cross_site_access_policies":
                    self.parameters["cross_site_access_policies"] = kwargs[key]
                elif key == "vanity_url":
                    self.parameters["vanity_url"] = kwargs[key]
                elif key == "stream_options":
                    self.parameters["stream_options"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_liveevent()

        if not old_response:
            self.log("Live Event instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Live Event instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Live Event instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Live Event instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_liveevent()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Live Event instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_liveevent()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_liveevent():
                time.sleep(20)
        else:
            self.log("Live Event instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_liveevent(self):
        '''
        Creates or updates Live Event with the specified configuration.

        :return: deserialized Live Event instance state dictionary
        '''
        self.log("Creating / Updating the Live Event instance {0}".format(self.live_event_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.live_events.create(resource_group_name=self.resource_group,
                                                               account_name=self.account_name,
                                                               live_event_name=self.live_event_name,
                                                               parameters=self.parameters)
            else:
                response = self.mgmt_client.live_events.update(resource_group_name=self.resource_group,
                                                               account_name=self.account_name,
                                                               live_event_name=self.live_event_name,
                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Live Event instance.')
            self.fail("Error creating the Live Event instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_liveevent(self):
        '''
        Deletes specified Live Event instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Live Event instance {0}".format(self.live_event_name))
        try:
            response = self.mgmt_client.live_events.delete(resource_group_name=self.resource_group,
                                                           account_name=self.account_name,
                                                           live_event_name=self.live_event_name)
        except CloudError as e:
            self.log('Error attempting to delete the Live Event instance.')
            self.fail("Error deleting the Live Event instance: {0}".format(str(e)))

        return True

    def get_liveevent(self):
        '''
        Gets the properties of the specified Live Event.

        :return: deserialized Live Event instance state dictionary
        '''
        self.log("Checking if the Live Event instance {0} is present".format(self.live_event_name))
        found = False
        try:
            response = self.mgmt_client.live_events.get(resource_group_name=self.resource_group,
                                                        account_name=self.account_name,
                                                        live_event_name=self.live_event_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Live Event instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Live Event instance.')
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
    AzureRMLiveEvents()


if __name__ == '__main__':
    main()

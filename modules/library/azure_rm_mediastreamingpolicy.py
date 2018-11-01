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
module: azure_rm_mediastreamingpolicy
version_added: "2.8"
short_description: Manage Streaming Policy instance.
description:
    - Create, update and delete instance of Streaming Policy.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    streaming_policy_name:
        description:
            - The Streaming Policy name.
        required: True
    default_content_key_policy_name:
        description:
            - Default ContentKey used by current Streaming Policy
    envelope_encryption:
        description:
            - Configuration of EnvelopeEncryption
        suboptions:
            enabled_protocols:
                description:
                    - Representing supported protocols
                suboptions:
                    download:
                        description:
                            - Enable Download protocol or not
                        required: True
                    dash:
                        description:
                            - Enable DASH protocol or not
                        required: True
                    hls:
                        description:
                            - Enable HLS protocol or not
                        required: True
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                        required: True
            clear_tracks:
                description:
                    - Representing which tracks should not be encrypted
                type: list
                suboptions:
                    track_selections:
                        description:
                            - TrackSelections is a track property condition list which can specify track(s)
                        type: list
                        suboptions:
                            property:
                                description:
                                    - Track property type.
                                required: True
                                choices:
                                    - 'unknown'
                                    - 'four_cc'
                            operation:
                                description:
                                    - Track I(property) condition operation.
                                required: True
                                choices:
                                    - 'unknown'
                                    - 'equal'
                            value:
                                description:
                                    - Track I(property) value
            content_keys:
                description:
                    - Representing default content key for each encryption scheme and separate content keys for specific tracks
                suboptions:
                    default_key:
                        description:
                            - Default content key for an encryption scheme
                        suboptions:
                            label:
                                description:
                                    - Label can be used to specify Content Key when creating a Streaming Locator
                            policy_name:
                                description:
                                    - Policy used by Default Key
                    key_to_track_mappings:
                        description:
                            - Representing tracks needs separate content key
                        type: list
                        suboptions:
                            label:
                                description:
                                    - Label can be used to specify Content Key when creating a Streaming Locator
                            policy_name:
                                description:
                                    - Policy used by Content Key
                            tracks:
                                description:
                                    - Tracks which use this content key
                                type: list
                                suboptions:
                                    track_selections:
                                        description:
                                            - TrackSelections is a track property condition list which can specify track(s)
                                        type: list
            custom_key_acquisition_url_template:
                description:
                    - KeyAcquistionUrlTemplate is used to point to user specified service to delivery content keys
    common_encryption_cenc:
        description:
            - Configuration of CommonEncryptionCenc
        suboptions:
            enabled_protocols:
                description:
                    - Representing supported protocols
                suboptions:
                    download:
                        description:
                            - Enable Download protocol or not
                        required: True
                    dash:
                        description:
                            - Enable DASH protocol or not
                        required: True
                    hls:
                        description:
                            - Enable HLS protocol or not
                        required: True
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                        required: True
            clear_tracks:
                description:
                    - Representing which tracks should not be encrypted
                type: list
                suboptions:
                    track_selections:
                        description:
                            - TrackSelections is a track property condition list which can specify track(s)
                        type: list
                        suboptions:
                            property:
                                description:
                                    - Track property type.
                                required: True
                                choices:
                                    - 'unknown'
                                    - 'four_cc'
                            operation:
                                description:
                                    - Track I(property) condition operation.
                                required: True
                                choices:
                                    - 'unknown'
                                    - 'equal'
                            value:
                                description:
                                    - Track I(property) value
            content_keys:
                description:
                    - Representing default content key for each encryption scheme and separate content keys for specific tracks
                suboptions:
                    default_key:
                        description:
                            - Default content key for an encryption scheme
                        suboptions:
                            label:
                                description:
                                    - Label can be used to specify Content Key when creating a Streaming Locator
                            policy_name:
                                description:
                                    - Policy used by Default Key
                    key_to_track_mappings:
                        description:
                            - Representing tracks needs separate content key
                        type: list
                        suboptions:
                            label:
                                description:
                                    - Label can be used to specify Content Key when creating a Streaming Locator
                            policy_name:
                                description:
                                    - Policy used by Content Key
                            tracks:
                                description:
                                    - Tracks which use this content key
                                type: list
                                suboptions:
                                    track_selections:
                                        description:
                                            - TrackSelections is a track property condition list which can specify track(s)
                                        type: list
            drm:
                description:
                    - Configuration of DRMs for CommonEncryptionCenc encryption scheme
                suboptions:
                    play_ready:
                        description:
                            - PlayReady configurations
                        suboptions:
                            custom_license_acquisition_url_template:
                                description:
                                    - "The template for a customer service to deliver keys to end users.  Not needed when using Azure Media Services for
                                       issuing keys."
                            play_ready_custom_attributes:
                                description:
                                    - Custom attributes for PlayReady
                    widevine:
                        description:
                            - Widevine configurations
                        suboptions:
                            custom_license_acquisition_url_template:
                                description:
                                    - "The template for a customer service to deliver keys to end users.  Not needed when using Azure Media Services for
                                       issuing keys."
    common_encryption_cbcs:
        description:
            - Configuration of CommonEncryptionCbcs
        suboptions:
            enabled_protocols:
                description:
                    - Representing supported protocols
                suboptions:
                    download:
                        description:
                            - Enable Download protocol or not
                        required: True
                    dash:
                        description:
                            - Enable DASH protocol or not
                        required: True
                    hls:
                        description:
                            - Enable HLS protocol or not
                        required: True
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                        required: True
            clear_tracks:
                description:
                    - Representing which tracks should not be encrypted
                type: list
                suboptions:
                    track_selections:
                        description:
                            - TrackSelections is a track property condition list which can specify track(s)
                        type: list
                        suboptions:
                            property:
                                description:
                                    - Track property type.
                                required: True
                                choices:
                                    - 'unknown'
                                    - 'four_cc'
                            operation:
                                description:
                                    - Track I(property) condition operation.
                                required: True
                                choices:
                                    - 'unknown'
                                    - 'equal'
                            value:
                                description:
                                    - Track I(property) value
            content_keys:
                description:
                    - Representing default content key for each encryption scheme and separate content keys for specific tracks
                suboptions:
                    default_key:
                        description:
                            - Default content key for an encryption scheme
                        suboptions:
                            label:
                                description:
                                    - Label can be used to specify Content Key when creating a Streaming Locator
                            policy_name:
                                description:
                                    - Policy used by Default Key
                    key_to_track_mappings:
                        description:
                            - Representing tracks needs separate content key
                        type: list
                        suboptions:
                            label:
                                description:
                                    - Label can be used to specify Content Key when creating a Streaming Locator
                            policy_name:
                                description:
                                    - Policy used by Content Key
                            tracks:
                                description:
                                    - Tracks which use this content key
                                type: list
                                suboptions:
                                    track_selections:
                                        description:
                                            - TrackSelections is a track property condition list which can specify track(s)
                                        type: list
            drm:
                description:
                    - Configuration of DRMs for current encryption scheme
                suboptions:
                    fair_play:
                        description:
                            - FairPlay configurations
                        suboptions:
                            custom_license_acquisition_url_template:
                                description:
                                    - "The template for a customer service to deliver keys to end users.  Not needed when using Azure Media Services for
                                       issuing keys."
                            allow_persistent_license:
                                description:
                                    - All license to be persistent or not
                                required: True
                    play_ready:
                        description:
                            - PlayReady configurations
                        suboptions:
                            custom_license_acquisition_url_template:
                                description:
                                    - "The template for a customer service to deliver keys to end users.  Not needed when using Azure Media Services for
                                       issuing keys."
                            play_ready_custom_attributes:
                                description:
                                    - Custom attributes for PlayReady
                    widevine:
                        description:
                            - Widevine configurations
                        suboptions:
                            custom_license_acquisition_url_template:
                                description:
                                    - "The template for a customer service to deliver keys to end users.  Not needed when using Azure Media Services for
                                       issuing keys."
    no_encryption:
        description:
            - Configurations of NoEncryption
        suboptions:
            enabled_protocols:
                description:
                    - Representing supported protocols
                suboptions:
                    download:
                        description:
                            - Enable Download protocol or not
                        required: True
                    dash:
                        description:
                            - Enable DASH protocol or not
                        required: True
                    hls:
                        description:
                            - Enable HLS protocol or not
                        required: True
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                        required: True
    state:
      description:
        - Assert the state of the Streaming Policy.
        - Use 'present' to create or update an Streaming Policy and 'absent' to delete it.
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
  - name: Create (or update) Streaming Policy
    azure_rm_mediastreamingpolicy:
      resource_group: contoso
      account_name: contosomedia
      streaming_policy_name: UserCreatedClearStreamingPolicy
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
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
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMStreamingPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Streaming Policy resource"""

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
            streaming_policy_name=dict(
                type='str',
                required=True
            ),
            default_content_key_policy_name=dict(
                type='str'
            ),
            envelope_encryption=dict(
                type='dict'
            ),
            common_encryption_cenc=dict(
                type='dict'
            ),
            common_encryption_cbcs=dict(
                type='dict'
            ),
            no_encryption=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.streaming_policy_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStreamingPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "default_content_key_policy_name":
                    self.parameters["default_content_key_policy_name"] = kwargs[key]
                elif key == "envelope_encryption":
                    self.parameters["envelope_encryption"] = kwargs[key]
                elif key == "common_encryption_cenc":
                    self.parameters["common_encryption_cenc"] = kwargs[key]
                elif key == "common_encryption_cbcs":
                    self.parameters["common_encryption_cbcs"] = kwargs[key]
                elif key == "no_encryption":
                    self.parameters["no_encryption"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_streamingpolicy()

        if not old_response:
            self.log("Streaming Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Streaming Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Streaming Policy instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Streaming Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_streamingpolicy()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Streaming Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_streamingpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_streamingpolicy():
                time.sleep(20)
        else:
            self.log("Streaming Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_streamingpolicy(self):
        '''
        Creates or updates Streaming Policy with the specified configuration.

        :return: deserialized Streaming Policy instance state dictionary
        '''
        self.log("Creating / Updating the Streaming Policy instance {0}".format(self.streaming_policy_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.streaming_policies.create(resource_group_name=self.resource_group,
                                                                      account_name=self.account_name,
                                                                      streaming_policy_name=self.streaming_policy_name,
                                                                      parameters=self.parameters)
            else:
                response = self.mgmt_client.streaming_policies.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Streaming Policy instance.')
            self.fail("Error creating the Streaming Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_streamingpolicy(self):
        '''
        Deletes specified Streaming Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Streaming Policy instance {0}".format(self.streaming_policy_name))
        try:
            response = self.mgmt_client.streaming_policies.delete(resource_group_name=self.resource_group,
                                                                  account_name=self.account_name,
                                                                  streaming_policy_name=self.streaming_policy_name)
        except CloudError as e:
            self.log('Error attempting to delete the Streaming Policy instance.')
            self.fail("Error deleting the Streaming Policy instance: {0}".format(str(e)))

        return True

    def get_streamingpolicy(self):
        '''
        Gets the properties of the specified Streaming Policy.

        :return: deserialized Streaming Policy instance state dictionary
        '''
        self.log("Checking if the Streaming Policy instance {0} is present".format(self.streaming_policy_name))
        found = False
        try:
            response = self.mgmt_client.streaming_policies.get(resource_group_name=self.resource_group,
                                                               account_name=self.account_name,
                                                               streaming_policy_name=self.streaming_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Streaming Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Streaming Policy instance.')
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
    AzureRMStreamingPolicies()


if __name__ == '__main__':
    main()
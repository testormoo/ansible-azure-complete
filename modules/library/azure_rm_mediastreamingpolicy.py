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
short_description: Manage Azure Streaming Policy instance.
description:
    - Create, update and delete instance of Azure Streaming Policy.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    name:
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
                            - Required when C(state) is I(present).
                    dash:
                        description:
                            - Enable DASH protocol or not
                            - Required when C(state) is I(present).
                    hls:
                        description:
                            - Enable HLS protocol or not
                            - Required when C(state) is I(present).
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                            - Required when C(state) is I(present).
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
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'unknown'
                                    - 'four_cc'
                            operation:
                                description:
                                    - Track I(property) condition operation.
                                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
                    dash:
                        description:
                            - Enable DASH protocol or not
                            - Required when C(state) is I(present).
                    hls:
                        description:
                            - Enable HLS protocol or not
                            - Required when C(state) is I(present).
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                            - Required when C(state) is I(present).
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
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'unknown'
                                    - 'four_cc'
                            operation:
                                description:
                                    - Track I(property) condition operation.
                                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
                    dash:
                        description:
                            - Enable DASH protocol or not
                            - Required when C(state) is I(present).
                    hls:
                        description:
                            - Enable HLS protocol or not
                            - Required when C(state) is I(present).
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                            - Required when C(state) is I(present).
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
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'unknown'
                                    - 'four_cc'
                            operation:
                                description:
                                    - Track I(property) condition operation.
                                    - Required when C(state) is I(present).
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
                                    - Required when C(state) is I(present).
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
                            - Required when C(state) is I(present).
                    dash:
                        description:
                            - Enable DASH protocol or not
                            - Required when C(state) is I(present).
                    hls:
                        description:
                            - Enable HLS protocol or not
                            - Required when C(state) is I(present).
                    smooth_streaming:
                        description:
                            - Enable SmoothStreaming protocol or not
                            - Required when C(state) is I(present).
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
      name: UserCreatedClearStreamingPolicy
      no_encryption:
        enabled_protocols:
          download: True
          dash: True
          hls: True
          smooth_streaming: True
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMStreamingPolicy(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            default_content_key_policy_name=dict(
                type='str'
            ),
            envelope_encryption=dict(
                type='dict'
                options=dict(
                    enabled_protocols=dict(
                        type='dict'
                        options=dict(
                            download=dict(
                                type='str'
                            ),
                            dash=dict(
                                type='str'
                            ),
                            hls=dict(
                                type='str'
                            ),
                            smooth_streaming=dict(
                                type='str'
                            )
                        )
                    ),
                    clear_tracks=dict(
                        type='list'
                        options=dict(
                            track_selections=dict(
                                type='list'
                                options=dict(
                                    property=dict(
                                        type='str',
                                        choices=['unknown',
                                                 'four_cc']
                                    ),
                                    operation=dict(
                                        type='str',
                                        choices=['unknown',
                                                 'equal']
                                    ),
                                    value=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    content_keys=dict(
                        type='dict'
                        options=dict(
                            default_key=dict(
                                type='dict'
                                options=dict(
                                    label=dict(
                                        type='str'
                                    ),
                                    policy_name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            key_to_track_mappings=dict(
                                type='list'
                                options=dict(
                                    label=dict(
                                        type='str'
                                    ),
                                    policy_name=dict(
                                        type='str'
                                    ),
                                    tracks=dict(
                                        type='list'
                                        options=dict(
                                            track_selections=dict(
                                                type='list'
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    custom_key_acquisition_url_template=dict(
                        type='str'
                    )
                )
            ),
            common_encryption_cenc=dict(
                type='dict'
                options=dict(
                    enabled_protocols=dict(
                        type='dict'
                        options=dict(
                            download=dict(
                                type='str'
                            ),
                            dash=dict(
                                type='str'
                            ),
                            hls=dict(
                                type='str'
                            ),
                            smooth_streaming=dict(
                                type='str'
                            )
                        )
                    ),
                    clear_tracks=dict(
                        type='list'
                        options=dict(
                            track_selections=dict(
                                type='list'
                                options=dict(
                                    property=dict(
                                        type='str',
                                        choices=['unknown',
                                                 'four_cc']
                                    ),
                                    operation=dict(
                                        type='str',
                                        choices=['unknown',
                                                 'equal']
                                    ),
                                    value=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    content_keys=dict(
                        type='dict'
                        options=dict(
                            default_key=dict(
                                type='dict'
                                options=dict(
                                    label=dict(
                                        type='str'
                                    ),
                                    policy_name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            key_to_track_mappings=dict(
                                type='list'
                                options=dict(
                                    label=dict(
                                        type='str'
                                    ),
                                    policy_name=dict(
                                        type='str'
                                    ),
                                    tracks=dict(
                                        type='list'
                                        options=dict(
                                            track_selections=dict(
                                                type='list'
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    drm=dict(
                        type='dict'
                        options=dict(
                            play_ready=dict(
                                type='dict'
                                options=dict(
                                    custom_license_acquisition_url_template=dict(
                                        type='str'
                                    ),
                                    play_ready_custom_attributes=dict(
                                        type='str'
                                    )
                                )
                            ),
                            widevine=dict(
                                type='dict'
                                options=dict(
                                    custom_license_acquisition_url_template=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            common_encryption_cbcs=dict(
                type='dict'
                options=dict(
                    enabled_protocols=dict(
                        type='dict'
                        options=dict(
                            download=dict(
                                type='str'
                            ),
                            dash=dict(
                                type='str'
                            ),
                            hls=dict(
                                type='str'
                            ),
                            smooth_streaming=dict(
                                type='str'
                            )
                        )
                    ),
                    clear_tracks=dict(
                        type='list'
                        options=dict(
                            track_selections=dict(
                                type='list'
                                options=dict(
                                    property=dict(
                                        type='str',
                                        choices=['unknown',
                                                 'four_cc']
                                    ),
                                    operation=dict(
                                        type='str',
                                        choices=['unknown',
                                                 'equal']
                                    ),
                                    value=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    ),
                    content_keys=dict(
                        type='dict'
                        options=dict(
                            default_key=dict(
                                type='dict'
                                options=dict(
                                    label=dict(
                                        type='str'
                                    ),
                                    policy_name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            key_to_track_mappings=dict(
                                type='list'
                                options=dict(
                                    label=dict(
                                        type='str'
                                    ),
                                    policy_name=dict(
                                        type='str'
                                    ),
                                    tracks=dict(
                                        type='list'
                                        options=dict(
                                            track_selections=dict(
                                                type='list'
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    drm=dict(
                        type='dict'
                        options=dict(
                            fair_play=dict(
                                type='dict'
                                options=dict(
                                    custom_license_acquisition_url_template=dict(
                                        type='str'
                                    ),
                                    allow_persistent_license=dict(
                                        type='str'
                                    )
                                )
                            ),
                            play_ready=dict(
                                type='dict'
                                options=dict(
                                    custom_license_acquisition_url_template=dict(
                                        type='str'
                                    ),
                                    play_ready_custom_attributes=dict(
                                        type='str'
                                    )
                                )
                            ),
                            widevine=dict(
                                type='dict'
                                options=dict(
                                    custom_license_acquisition_url_template=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            no_encryption=dict(
                type='dict'
                options=dict(
                    enabled_protocols=dict(
                        type='dict'
                        options=dict(
                            download=dict(
                                type='str'
                            ),
                            dash=dict(
                                type='str'
                            ),
                            hls=dict(
                                type='str'
                            ),
                            smooth_streaming=dict(
                                type='str'
                            )
                        )
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStreamingPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['envelope_encryption', 'clear_tracks', 'track_selections', 'property'], True)
        dict_map(self.parameters, ['envelope_encryption', 'clear_tracks', 'track_selections', 'property'], {'four_cc': 'FourCC'})
        dict_camelize(self.parameters, ['envelope_encryption', 'clear_tracks', 'track_selections', 'operation'], True)
        dict_camelize(self.parameters, ['common_encryption_cenc', 'clear_tracks', 'track_selections', 'property'], True)
        dict_map(self.parameters, ['common_encryption_cenc', 'clear_tracks', 'track_selections', 'property'], {'four_cc': 'FourCC'})
        dict_camelize(self.parameters, ['common_encryption_cenc', 'clear_tracks', 'track_selections', 'operation'], True)
        dict_camelize(self.parameters, ['common_encryption_cbcs', 'clear_tracks', 'track_selections', 'property'], True)
        dict_map(self.parameters, ['common_encryption_cbcs', 'clear_tracks', 'track_selections', 'property'], {'four_cc': 'FourCC'})
        dict_camelize(self.parameters, ['common_encryption_cbcs', 'clear_tracks', 'track_selections', 'operation'], True)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Streaming Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_streamingpolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Streaming Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_streamingpolicy()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Streaming Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_streamingpolicy(self):
        '''
        Creates or updates Streaming Policy with the specified configuration.

        :return: deserialized Streaming Policy instance state dictionary
        '''
        self.log("Creating / Updating the Streaming Policy instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.streaming_policies.create(resource_group_name=self.resource_group,
                                                                      account_name=self.account_name,
                                                                      streaming_policy_name=self.name,
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
        self.log("Deleting the Streaming Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.streaming_policies.delete(resource_group_name=self.resource_group,
                                                                  account_name=self.account_name,
                                                                  streaming_policy_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Streaming Policy instance.')
            self.fail("Error deleting the Streaming Policy instance: {0}".format(str(e)))

        return True

    def get_streamingpolicy(self):
        '''
        Gets the properties of the specified Streaming Policy.

        :return: deserialized Streaming Policy instance state dictionary
        '''
        self.log("Checking if the Streaming Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.streaming_policies.get(resource_group_name=self.resource_group,
                                                               account_name=self.account_name,
                                                               streaming_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Streaming Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Streaming Policy instance.')
        if found is True:
            return response.as_dict()

        return False


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


def main():
    """Main execution"""
    AzureRMStreamingPolicy()


if __name__ == '__main__':
    main()

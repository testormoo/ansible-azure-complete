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
module: azure_rm_mediastreaminglocator
version_added: "2.8"
short_description: Manage Azure Streaming Locator instance.
description:
    - Create, update and delete instance of Azure Streaming Locator.

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
            - The Streaming Locator name.
        required: True
    asset_name:
        description:
            - Asset Name
            - Required when C(state) is I(present).
    start_time:
        description:
            - The start time of the Streaming Locator.
    end_time:
        description:
            - The end time of the Streaming Locator.
    streaming_locator_id:
        description:
            - The StreamingLocatorId of the Streaming Locator.
    streaming_policy_name:
        description:
            - "Name of the Streaming Policy used by this Streaming Locator. Either specify the name of Streaming Policy you created or use one of the
               predefined Streaming Policies. The predefined Streaming Policies available are: 'Predefined_DownloadOnly', 'Predefined_ClearStreamingOnly',
               'Predefined_DownloadAndClearStreaming', 'Predefined_ClearKey', 'Predefined_MultiDrmCencStreaming' and 'Predefined_MultiDrmStreaming'"
            - Required when C(state) is I(present).
    default_content_key_policy_name:
        description:
            - Name of the default ContentKeyPolicy used by this Streaming Locator.
    content_keys:
        description:
            - The ContentKeys used by this Streaming Locator.
        type: list
        suboptions:
            id:
                description:
                    - ID of Content Key
                    - Required when C(state) is I(present).
            label_reference_in_streaming_policy:
                description:
                    - Label of Content Key as specified in the Streaming Policy
            value:
                description:
                    - Value of  of Content Key
    alternative_media_id:
        description:
            - Alternative Media ID of this Streaming Locator
    state:
      description:
        - Assert the state of the Streaming Locator.
        - Use 'present' to create or update an Streaming Locator and 'absent' to delete it.
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
  - name: Create (or update) Streaming Locator
    azure_rm_mediastreaminglocator:
      resource_group: contoso
      account_name: contosomedia
      name: UserCreatedClearStreamingLocator
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


class AzureRMStreamingLocator(AzureRMModuleBase):
    """Configuration class for an Azure RM Streaming Locator resource"""

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
            asset_name=dict(
                type='str'
            ),
            start_time=dict(
                type='datetime'
            ),
            end_time=dict(
                type='datetime'
            ),
            streaming_locator_id=dict(
                type='str'
            ),
            streaming_policy_name=dict(
                type='str'
            ),
            default_content_key_policy_name=dict(
                type='str'
            ),
            content_keys=dict(
                type='list'
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    label_reference_in_streaming_policy=dict(
                        type='str'
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            alternative_media_id=dict(
                type='str'
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

        super(AzureRMStreamingLocator, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_resource_id(self.parameters, ['content_keys', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_streaminglocator()

        if not old_response:
            self.log("Streaming Locator instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Streaming Locator instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Streaming Locator instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_streaminglocator()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Streaming Locator instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_streaminglocator()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Streaming Locator instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_streaminglocator(self):
        '''
        Creates or updates Streaming Locator with the specified configuration.

        :return: deserialized Streaming Locator instance state dictionary
        '''
        self.log("Creating / Updating the Streaming Locator instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.streaming_locators.create(resource_group_name=self.resource_group,
                                                                      account_name=self.account_name,
                                                                      streaming_locator_name=self.name,
                                                                      parameters=self.parameters)
            else:
                response = self.mgmt_client.streaming_locators.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Streaming Locator instance.')
            self.fail("Error creating the Streaming Locator instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_streaminglocator(self):
        '''
        Deletes specified Streaming Locator instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Streaming Locator instance {0}".format(self.name))
        try:
            response = self.mgmt_client.streaming_locators.delete(resource_group_name=self.resource_group,
                                                                  account_name=self.account_name,
                                                                  streaming_locator_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Streaming Locator instance.')
            self.fail("Error deleting the Streaming Locator instance: {0}".format(str(e)))

        return True

    def get_streaminglocator(self):
        '''
        Gets the properties of the specified Streaming Locator.

        :return: deserialized Streaming Locator instance state dictionary
        '''
        self.log("Checking if the Streaming Locator instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.streaming_locators.get(resource_group_name=self.resource_group,
                                                               account_name=self.account_name,
                                                               streaming_locator_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Streaming Locator instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Streaming Locator instance.')
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
    AzureRMStreamingLocator()


if __name__ == '__main__':
    main()

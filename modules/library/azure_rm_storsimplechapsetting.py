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
module: azure_rm_storsimplechapsetting
version_added: "2.8"
short_description: Manage Azure Chap Setting instance.
description:
    - Create, update and delete instance of Azure Chap Setting.

options:
    device_name:
        description:
            - The device name.
        required: True
    chap_user_name:
        description:
            - The chap user name.
        required: True
    password:
        description:
            - The chap password.
            - Required when C(state) is I(present).
        suboptions:
            value:
                description:
                    - "The value of the secret itself. If the secret is in plaintext then I(encryption_algorithm) will be C(none) and
                       EncryptionCertThumbprint will be null."
                    - Required when C(state) is I(present).
            encryption_certificate_thumbprint:
                description:
                    - "Thumbprint certificate that was used to encrypt 'I(value)'"
            encryption_algorithm:
                description:
                    - "Algorithm used to encrypt 'I(value)'."
                    - Required when C(state) is I(present).
                choices:
                    - 'none'
                    - 'aes256'
                    - 'rsaes_pkcs1_v_1_5'
    resource_group:
        description:
            - The resource group name
        required: True
    name:
        description:
            - The manager name
        required: True
    state:
      description:
        - Assert the state of the Chap Setting.
        - Use 'present' to create or update an Chap Setting and 'absent' to delete it.
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
  - name: Create (or update) Chap Setting
    azure_rm_storsimplechapsetting:
      device_name: HSDK-WSJQERQW3F
      chap_user_name: ChapSettingForSDK
      password:
        value: W4xL3maActbzoehB9Ny1nr16uyjZZfvuJ70f8yBQgtS3vU4SLrOpoggmutOsbcgOgmgNHZnKe73WRZxzJFxzUQqcFNrAV+dReDkO5I/L1GxDjT5rsWn+74dRl8ditTew4z6OcwrT6RXtjG0njkUNsxXuawuylXsdHdvgQtSWbXBSao6KVhSbGQ57/V++CXqBbG2zoGLlHMdZF9OQccvCgh7qwD4ua7FLwqvQ8vYYVXryKm+XDmmT+GYWDqxPly0M2mJl/GLB/c6rNem4oRHBsf/vKfEKm8WGLWNsRZGcbxZKGiGsKC8QsxDHou6Ci3rfphVJE2R/9TxL+/1lUu2poQ==
        encryption_certificate_thumbprint: D73DB57C4CDD6761E159F8D1E8A7D759424983FD
        encryption_algorithm: RSAES_PKCS1_v_1_5
      resource_group: ResourceGroupForSDKTest
      name: hAzureSDKOperations
'''

RETURN = '''
id:
    description:
        - The identifier.
    returned: always
    type: str
    sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzureSDKOper
            ations/devices/HSDK-WSJQERQW3F/chapSettings/ChapSettingForSDK"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMChapSetting(AzureRMModuleBase):
    """Configuration class for an Azure RM Chap Setting resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            device_name=dict(
                type='str',
                required=True
            ),
            chap_user_name=dict(
                type='str',
                required=True
            ),
            password=dict(
                type='dict',
                no_log=True,
                options=dict(
                    value=dict(
                        type='str'
                    ),
                    encryption_certificate_thumbprint=dict(
                        type='str'
                    ),
                    encryption_algorithm=dict(
                        type='str',
                        choices=['none',
                                 'aes256',
                                 'rsaes_pkcs1_v_1_5']
                    )
                )
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.device_name = None
        self.chap_user_name = None
        self.chap_setting = dict()
        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMChapSetting, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.chap_setting[key] = kwargs[key]

        dict_upper(self.chap_setting, ['password', 'encryption_algorithm'])
        dict_map(self.chap_setting, ['password', 'encryption_algorithm'], {'none': 'None', 'rsaes_pkcs1_v_1_5': 'RSAES_PKCS1_v_1_5'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_chapsetting()

        if not old_response:
            self.log("Chap Setting instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Chap Setting instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.chap_setting, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Chap Setting instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_chapsetting()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Chap Setting instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_chapsetting()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Chap Setting instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_chapsetting(self):
        '''
        Creates or updates Chap Setting with the specified configuration.

        :return: deserialized Chap Setting instance state dictionary
        '''
        self.log("Creating / Updating the Chap Setting instance {0}".format(self.name))

        try:
            response = self.mgmt_client.chap_settings.create_or_update(device_name=self.device_name,
                                                                       chap_user_name=self.chap_user_name,
                                                                       chap_setting=self.chap_setting,
                                                                       resource_group_name=self.resource_group,
                                                                       manager_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Chap Setting instance.')
            self.fail("Error creating the Chap Setting instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_chapsetting(self):
        '''
        Deletes specified Chap Setting instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Chap Setting instance {0}".format(self.name))
        try:
            response = self.mgmt_client.chap_settings.delete(device_name=self.device_name,
                                                             chap_user_name=self.chap_user_name,
                                                             resource_group_name=self.resource_group,
                                                             manager_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Chap Setting instance.')
            self.fail("Error deleting the Chap Setting instance: {0}".format(str(e)))

        return True

    def get_chapsetting(self):
        '''
        Gets the properties of the specified Chap Setting.

        :return: deserialized Chap Setting instance state dictionary
        '''
        self.log("Checking if the Chap Setting instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.chap_settings.get(device_name=self.device_name,
                                                          chap_user_name=self.chap_user_name,
                                                          resource_group_name=self.resource_group,
                                                          manager_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Chap Setting instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Chap Setting instance.')
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
            else:
                key = list(old[0])[0]
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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
            return False


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


def main():
    """Main execution"""
    AzureRMChapSetting()


if __name__ == '__main__':
    main()

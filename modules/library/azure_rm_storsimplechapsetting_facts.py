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
module: azure_rm_storsimplechapsetting_facts
version_added: "2.8"
short_description: Get Azure Chap Setting facts.
description:
    - Get facts of Azure Chap Setting.

options:
    device_name:
        description:
            - The device name.
        required: True
    chap_user_name:
        description:
            - The user name of chap to be fetched.
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
  - name: Get instance of Chap Setting
    azure_rm_storsimplechapsetting_facts:
      device_name: device_name
      chap_user_name: chap_user_name
      resource_group: resource_group_name
      name: manager_name

  - name: List instances of Chap Setting
    azure_rm_storsimplechapsetting_facts:
      device_name: device_name
      resource_group: resource_group_name
      name: manager_name
'''

RETURN = '''
chap_settings:
    description: A list of dictionaries containing facts for Chap Setting.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The identifier.
            returned: always
            type: str
            sample: "/subscriptions/9eb689cd-7243-43b4-b6f6-5c65cb296641/resourceGroups/ResourceGroupForSDKTest/providers/Microsoft.StorSimple/managers/hAzur
                    eSDKOperations/devices/HSDK-WSJQERQW3F/chapSettings/ChapSettingForSDK"
        name:
            description:
                - The name.
            returned: always
            type: str
            sample: ChapSettingForSDK
        password:
            description:
                - The chap password.
            returned: always
            type: complex
            sample: password
            contains:
                value:
                    description:
                        - "The value of the secret itself. If the secret is in plaintext then EncryptionAlgorithm will be none and EncryptionCertThumbprint
                           will be null."
                    returned: always
                    type: str
                    sample: "QAabTlWY4Qz7ygqWeYVoUpgg+wtITX9O6uAj1j+ejQkNR45r5/1knhgSroeeavtxGGJtaWFwMGGde1EA31eoueZwhhWODWBlaTAhGhY3SITMIKj+9k+xUJwkq6aqc2qD
                            comW+juLTd72oVwpMCmGALALCPAjNBiKzi7WUV+6U9j/F0dAsz8kmTFBh2rrY3yYTVQ7LjxZ7EPeqiie1ikvLoL/Q8S0jKu+O70m3ES1+WIG61ig4Nl9S/1NlV30wpJd
                            gnnxA4Vg83PEIgoz0nQpfodGguwkDYhaeNYiYZGVXo75UgFMILouVUCHkuKWQOxL48kIleEW3hIL7sZkQQcLwA=="
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.storsimple import StorSimpleManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMChapSettingFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            device_name=dict(
                type='str',
                required=True
            ),
            chap_user_name=dict(
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
        self.chap_user_name = None
        self.resource_group = None
        self.name = None
        super(AzureRMChapSettingFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(StorSimpleManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if self.chap_user_name is not None:
            self.results['chap_settings'] = self.get()
        else:
            self.results['chap_settings'] = self.list_by_device()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.chap_settings.get(device_name=self.device_name,
                                                          chap_user_name=self.chap_user_name,
                                                          resource_group_name=self.resource_group,
                                                          manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Chap Setting.')

        if response is not None:
            results.append(self.format_response(response))

        return results

    def list_by_device(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.chap_settings.list_by_device(device_name=self.device_name,
                                                                     resource_group_name=self.resource_group,
                                                                     manager_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Chap Setting.')

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
            'password': {
                'value': d.get('password', {}).get('value', None)
            }
        }
        return d


def main():
    AzureRMChapSettingFacts()


if __name__ == '__main__':
    main()

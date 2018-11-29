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
module: azure_rm_storetrustedidprovider
version_added: "2.8"
short_description: Manage Azure Trusted Id Provider instance.
description:
    - Create, update and delete instance of Azure Trusted Id Provider.

options:
    resource_group:
        description:
            - The name of the Azure resource group.
        required: True
    account_name:
        description:
            - The name of the Data Lake Store account.
        required: True
    name:
        description:
            - The name of the trusted identity provider. This is used for differentiation of providers in the account.
        required: True
    id_provider:
        description:
            - The URL of this trusted identity provider.
        required: True
    state:
      description:
        - Assert the state of the Trusted Id Provider.
        - Use 'present' to create or update an Trusted Id Provider and 'absent' to delete it.
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
  - name: Create (or update) Trusted Id Provider
    azure_rm_storetrustedidprovider:
      resource_group: contosorg
      account_name: contosoadla
      name: test_trusted_id_provider_name
      id_provider: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: 34adfa4f-cedf-4dc0-ba29-b6d1a69ab345
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.store import DataLakeStoreAccountManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMTrustedIdProvider(AzureRMModuleBase):
    """Configuration class for an Azure RM Trusted Id Provider resource"""

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
            id_provider=dict(
                type='str',
                required=True
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
        self.id_provider = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMTrustedIdProvider, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        self.mgmt_client = self.get_mgmt_svc_client(DataLakeStoreAccountManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_trustedidprovider()

        if not old_response:
            self.log("Trusted Id Provider instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Trusted Id Provider instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Trusted Id Provider instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_trustedidprovider()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Trusted Id Provider instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_trustedidprovider()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Trusted Id Provider instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_trustedidprovider(self):
        '''
        Creates or updates Trusted Id Provider with the specified configuration.

        :return: deserialized Trusted Id Provider instance state dictionary
        '''
        self.log("Creating / Updating the Trusted Id Provider instance {0}".format(self.name))

        try:
            response = self.mgmt_client.trusted_id_providers.create_or_update(resource_group_name=self.resource_group,
                                                                              account_name=self.account_name,
                                                                              trusted_id_provider_name=self.name,
                                                                              id_provider=self.id_provider)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Trusted Id Provider instance.')
            self.fail("Error creating the Trusted Id Provider instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_trustedidprovider(self):
        '''
        Deletes specified Trusted Id Provider instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Trusted Id Provider instance {0}".format(self.name))
        try:
            response = self.mgmt_client.trusted_id_providers.delete(resource_group_name=self.resource_group,
                                                                    account_name=self.account_name,
                                                                    trusted_id_provider_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Trusted Id Provider instance.')
            self.fail("Error deleting the Trusted Id Provider instance: {0}".format(str(e)))

        return True

    def get_trustedidprovider(self):
        '''
        Gets the properties of the specified Trusted Id Provider.

        :return: deserialized Trusted Id Provider instance state dictionary
        '''
        self.log("Checking if the Trusted Id Provider instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.trusted_id_providers.get(resource_group_name=self.resource_group,
                                                                 account_name=self.account_name,
                                                                 trusted_id_provider_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Trusted Id Provider instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Trusted Id Provider instance.')
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


def main():
    """Main execution"""
    AzureRMTrustedIdProvider()


if __name__ == '__main__':
    main()

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
module: azure_rm_recoveryservicesvault
version_added: "2.8"
short_description: Manage Vault instance.
description:
    - Create, update and delete instance of Vault.

options:
    resource_group:
        description:
            - The name of the resource group where the recovery services I(vault) is present.
        required: True
    name:
        description:
            - The name of the recovery services I(vault).
        required: True
    vault:
        description:
            - Recovery Services Vault to be created.
        required: True
        suboptions:
            e_tag:
                description:
                    - Optional ETag.
            location:
                description:
                    - Resource location.
                    - Required when C(state) is I(present).
            upgrade_details:
                description:
            sku:
                description:
                suboptions:
                    name:
                        description:
                            - The Sku name.
                            - Required when C(state) is I(present).
                        choices:
                            - 'standard'
                            - 'rs0'
    state:
      description:
        - Assert the state of the Vault.
        - Use 'present' to create or update an Vault and 'absent' to delete it.
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
  - name: Create (or update) Vault
    azure_rm_recoveryservicesvault:
      resource_group: Default-RecoveryServices-ResourceGroup
      name: swaggerExample
      vault:
        location: West US
        sku:
          name: Standard
'''

RETURN = '''
id:
    description:
        - Resource Id represents the complete path to the resource.
    returned: always
    type: str
    sample: /subscriptions/77777777-b0c6-47a2-b37c-d8e65a629c18/resourceGroups/HelloWorld/providers/Microsoft.RecoveryServices/vaults/swaggerExample
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.recoveryservices import RecoveryServicesClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVaults(AzureRMModuleBase):
    """Configuration class for an Azure RM Vault resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            vault=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.vault = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVaults, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=True,
                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "e_tag":
                    self.vault["e_tag"] = kwargs[key]
                elif key == "location":
                    self.vault["location"] = kwargs[key]
                elif key == "upgrade_details":
                    self.vault.setdefault("properties", {})["upgrade_details"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                        elif ev['name'] == 'rs0':
                            ev['name'] = 'RS0'
                    self.vault["sku"] = ev

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_vault()

        if not old_response:
            self.log("Vault instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Vault instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Vault instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_vault()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Vault instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_vault()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_vault():
                time.sleep(20)
        else:
            self.log("Vault instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_vault(self):
        '''
        Creates or updates Vault with the specified configuration.

        :return: deserialized Vault instance state dictionary
        '''
        self.log("Creating / Updating the Vault instance {0}".format(self.name))

        try:
            response = self.mgmt_client.vaults.create_or_update(resource_group_name=self.resource_group,
                                                                vault_name=self.name,
                                                                vault=self.vault)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Vault instance.')
            self.fail("Error creating the Vault instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_vault(self):
        '''
        Deletes specified Vault instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Vault instance {0}".format(self.name))
        try:
            response = self.mgmt_client.vaults.delete(resource_group_name=self.resource_group,
                                                      vault_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Vault instance.')
            self.fail("Error deleting the Vault instance: {0}".format(str(e)))

        return True

    def get_vault(self):
        '''
        Gets the properties of the specified Vault.

        :return: deserialized Vault instance state dictionary
        '''
        self.log("Checking if the Vault instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.vaults.get(resource_group_name=self.resource_group,
                                                   vault_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Vault instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Vault instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def default_compare(new, old, path):
    if new is None:
        return True
    elif isinstance(new, dict):
        if not isinstance(old, dict):
            return False
        for k in new.keys():
            if not default_compare(new.get(k), old.get(k, None), path + '/' + k):
                return False
        return True
    elif isinstance(new, list):
        if not isinstance(old, list) or len(new) != len(old):
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
            if not default_compare(new[i], old[i], path + '/*'):
                return False
        return True
    else:
        return new == old


def main():
    """Main execution"""
    AzureRMVaults()


if __name__ == '__main__':
    main()

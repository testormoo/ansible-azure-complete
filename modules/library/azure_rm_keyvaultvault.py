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
module: azure_rm_keyvaultvault
version_added: "2.8"
short_description: Manage Azure Vault instance.
description:
    - Create, update and delete instance of Azure Vault.

options:
    resource_group:
        description:
            - The name of the Resource Group to which the server belongs.
        required: True
    name:
        description:
            - Name of the vault
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as C(default).
    tenant_id:
        description:
            - The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.
            - Required when C(state) is I(present).
    sku:
        description:
            - SKU details
            - Required when C(state) is I(present).
        suboptions:
            family:
                description:
                    - SKU family name
                    - Required when C(state) is I(present).
            name:
                description:
                    - SKU name to specify whether the key vault is a C(standard) vault or a C(premium) vault.
                    - Required when C(state) is I(present).
                choices:
                    - 'standard'
                    - 'premium'
    access_policies:
        description:
            - "An array of 0 to 16 identities that have access to the key vault. All identities in the array must use the same tenant ID as the key vault's
               tenant ID."
        type: list
        suboptions:
            tenant_id:
                description:
                    - The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.
                    - Required when C(state) is I(present).
            object_id:
                description:
                    - "The object ID of a user, service principal or security group in the Azure Active Directory tenant for the vault. The object ID must
                       be unique for the list of access policies."
                    - Required when C(state) is I(present).
            application_id:
                description:
                    -  Application ID of the client making request on behalf of a principal
            permissions:
                description:
                    - Permissions the identity has for keys, secrets and certificates.
                    - Required when C(state) is I(present).
                suboptions:
                    keys:
                        description:
                            - Permissions to keys
                        type: list
                    secrets:
                        description:
                            - Permissions to secrets
                        type: list
                    certificates:
                        description:
                            - Permissions to certificates
                        type: list
                    storage:
                        description:
                            - Permissions to storage accounts
                        type: list
    vault_uri:
        description:
            - The URI of the vault for performing operations on keys and secrets.
    enabled_for_deployment:
        description:
            - Property to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.
    enabled_for_disk_encryption:
        description:
            - Property to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.
    enabled_for_template_deployment:
        description:
            - Property to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
    enable_soft_delete:
        description:
            - "Property specifying whether recoverable deletion is enabled for this key vault. Setting this property to true activates the soft delete
               feature, whereby vaults or vault entities can be recovered after deletion. Enabling this functionality is irreversible - that is, the
               property does not accept false as its value."
    create_mode:
        description:
            - "The vault's create mode to indicate whether the vault need to be recovered or not."
        choices:
            - 'recover'
            - 'default'
    enable_purge_protection:
        description:
            - "Property specifying whether protection against purge is enabled for this vault. Setting this property to true activates protection against
               purge for this vault and its content - only the Key Vault service may initiate a hard, irrecoverable deletion. The setting is effective only
               if soft delete is also enabled. Enabling this functionality is irreversible - that is, the property does not accept false as its value."
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
    azure_rm_keyvaultvault:
      resource_group: sample-resource-group
      name: sample-vault
      location: eastus
      tenant_id: 00000000-0000-0000-0000-000000000000
      sku:
        family: A
        name: standard
      access_policies:
        - tenant_id: 00000000-0000-0000-0000-000000000000
          object_id: 00000000-0000-0000-0000-000000000000
          permissions:
            keys:
              - [
  "encrypt",
  "decrypt",
  "wrapKey",
  "unwrapKey",
  "sign",
  "verify",
  "get",
  "list",
  "create",
  "update",
  "import",
  "delete",
  "backup",
  "restore",
  "recover",
  "purge"
]
            secrets:
              - [
  "get",
  "list",
  "set",
  "delete",
  "backup",
  "restore",
  "recover",
  "purge"
]
            certificates:
              - [
  "get",
  "list",
  "delete",
  "create",
  "import",
  "update",
  "managecontacts",
  "getissuers",
  "listissuers",
  "setissuers",
  "deleteissuers",
  "manageissuers",
  "recover",
  "purge"
]
      enabled_for_deployment: True
      enabled_for_disk_encryption: True
      enabled_for_template_deployment: True
'''

RETURN = '''
id:
    description:
        - The Azure Resource Manager resource ID for the key vault.
    returned: always
    type: str
    sample: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/sample-resource-group/providers/Microsoft.KeyVault/vaults/sample-vault
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.keyvault import KeyVaultManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMVault(AzureRMModuleBase):
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
            location=dict(
                type='str'
            ),
            tenant_id=dict(
                type='str'
            ),
            sku=dict(
                type='dict',
                options=dict(
                    family=dict(
                        type='str'
                    ),
                    name=dict(
                        type='str',
                        choices=['standard',
                                 'premium']
                    )
                )
            ),
            access_policies=dict(
                type='list',
                options=dict(
                    tenant_id=dict(
                        type='str'
                    ),
                    object_id=dict(
                        type='str'
                    ),
                    application_id=dict(
                        type='str'
                    ),
                    permissions=dict(
                        type='dict',
                        options=dict(
                            keys=dict(
                                type='list'
                            ),
                            secrets=dict(
                                type='list'
                            ),
                            certificates=dict(
                                type='list'
                            ),
                            storage=dict(
                                type='list'
                            )
                        )
                    )
                )
            ),
            vault_uri=dict(
                type='str'
            ),
            enabled_for_deployment=dict(
                type='str'
            ),
            enabled_for_disk_encryption=dict(
                type='str'
            ),
            enabled_for_template_deployment=dict(
                type='str'
            ),
            enable_soft_delete=dict(
                type='str'
            ),
            create_mode=dict(
                type='str',
                choices=['recover',
                         'default']
            ),
            enable_purge_protection=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMVault, self).__init__(derived_arg_spec=self.module_arg_spec,
                                           supports_check_mode=True,
                                           supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_expand(self.parameters, ['tenant_id'])
        dict_expand(self.parameters, ['sku'])
        dict_expand(self.parameters, ['access_policies'])
        dict_expand(self.parameters, ['vault_uri'])
        dict_expand(self.parameters, ['enabled_for_deployment'])
        dict_expand(self.parameters, ['enabled_for_disk_encryption'])
        dict_expand(self.parameters, ['enabled_for_template_deployment'])
        dict_expand(self.parameters, ['enable_soft_delete'])
        dict_expand(self.parameters, ['create_mode'])
        dict_expand(self.parameters, ['enable_purge_protection'])

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(KeyVaultManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Vault instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
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
                                                                parameters=self.parameters)
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


def main():
    """Main execution"""
    AzureRMVault()


if __name__ == '__main__':
    main()

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
module: azure_rm_recoveryservicesbackupprotectionpolicy
version_added: "2.8"
short_description: Manage Protection Policy instance.
description:
    - Create, update and delete instance of Protection Policy.

options:
    vault_name:
        description:
            - The name of the recovery services vault.
        required: True
    resource_group:
        description:
            - The name of the resource group where the recovery services vault is present.
        required: True
    name:
        description:
            - Backup policy to be created.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    e_tag:
        description:
            - Optional ETag.
    protected_items_count:
        description:
            - Number of items associated with this policy.
    backup_management_type:
        description:
            - Constant filled by server.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the Protection Policy.
        - Use 'present' to create or update an Protection Policy and 'absent' to delete it.
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
  - name: Create (or update) Protection Policy
    azure_rm_recoveryservicesbackupprotectionpolicy:
      vault_name: NetSDKTestRsVault
      resource_group: SwaggerTestRg
      name: testPolicy1
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource Id represents the complete path to the resource.
    returned: always
    type: str
    sample: "/Subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/SwaggerTestRg/providers/Microsoft.RecoveryServices/vaults/NetSDKTestRsVault/b
            ackupPolicies/testPolicy1"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMProtectionPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Protection Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            vault_name=dict(
                type='str',
                required=True
            ),
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
            e_tag=dict(
                type='str'
            ),
            protected_items_count=dict(
                type='int'
            ),
            backup_management_type=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.vault_name = None
        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProtectionPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "e_tag":
                    self.parameters["e_tag"] = kwargs[key]
                elif key == "protected_items_count":
                    self.parameters.setdefault("properties", {})["protected_items_count"] = kwargs[key]
                elif key == "backup_management_type":
                    self.parameters.setdefault("properties", {})["backup_management_type"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(RecoveryServicesBackupClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_protectionpolicy()

        if not old_response:
            self.log("Protection Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Protection Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Protection Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_protectionpolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Protection Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_protectionpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_protectionpolicy():
                time.sleep(20)
        else:
            self.log("Protection Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_protectionpolicy(self):
        '''
        Creates or updates Protection Policy with the specified configuration.

        :return: deserialized Protection Policy instance state dictionary
        '''
        self.log("Creating / Updating the Protection Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.protection_policies.create_or_update(vault_name=self.vault_name,
                                                                             resource_group_name=self.resource_group,
                                                                             policy_name=self.name,
                                                                             parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Protection Policy instance.')
            self.fail("Error creating the Protection Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_protectionpolicy(self):
        '''
        Deletes specified Protection Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Protection Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.protection_policies.delete(vault_name=self.vault_name,
                                                                   resource_group_name=self.resource_group,
                                                                   policy_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Protection Policy instance.')
            self.fail("Error deleting the Protection Policy instance: {0}".format(str(e)))

        return True

    def get_protectionpolicy(self):
        '''
        Gets the properties of the specified Protection Policy.

        :return: deserialized Protection Policy instance state dictionary
        '''
        self.log("Checking if the Protection Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.protection_policies.get(vault_name=self.vault_name,
                                                                resource_group_name=self.resource_group,
                                                                policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Protection Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Protection Policy instance.')
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
    AzureRMProtectionPolicies()


if __name__ == '__main__':
    main()

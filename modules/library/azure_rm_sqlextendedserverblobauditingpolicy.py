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
module: azure_rm_sqlextendedserverblobauditingpolicy
version_added: "2.8"
short_description: Manage Extended Server Blob Auditing Policy instance.
description:
    - Create, update and delete instance of Extended Server Blob Auditing Policy.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the blob auditing policy.
        required: True
    predicate_expression:
        description:
            - Specifies condition of where clause when creating an audit.
    state:
        description:
            - Specifies the state of the policy. If state is C(enabled), I(storage_endpoint) and I(storage_account_access_key) are required.
            - Required when C(state) is I(present).
        choices:
            - 'enabled'
            - 'disabled'
    storage_endpoint:
        description:
            - "Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net). If I(state) is C(enabled), storageEndpoint is required."
    storage_account_access_key:
        description:
            - Specifies the identifier key of the auditing storage account. If I(state) is C(enabled), storageAccountAccessKey is required.
    retention_days:
        description:
            - Specifies the number of days to keep in the audit logs.
    audit_actions_and_groups:
        description:
            - "Specifies the Actions-Groups and Actions to audit.\n"
            - "The recommended set of action groups to use is the following combination - this will audit all the queries and stored procedures executed
               against the database, as well as successful and failed logins:\n"
            - "BATCH_COMPLETED_GROUP,\n"
            - "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP,\n"
            - "FAILED_DATABASE_AUTHENTICATION_GROUP.\n"
            - "This above combination is also the set that is configured by default when enabling auditing from the Azure portal.\n"
            - "The supported action groups to audit are (note: choose only specific groups that cover your auditing needs. Using unnecessary groups could
               lead to very large quantities of audit records):\n"
            - "APPLICATION_ROLE_CHANGE_PASSWORD_GROUP\n"
            - "BACKUP_RESTORE_GROUP\n"
            - "DATABASE_LOGOUT_GROUP\n"
            - "DATABASE_OBJECT_CHANGE_GROUP\n"
            - "DATABASE_OBJECT_OWNERSHIP_CHANGE_GROUP\n"
            - "DATABASE_OBJECT_PERMISSION_CHANGE_GROUP\n"
            - "DATABASE_OPERATION_GROUP\n"
            - "DATABASE_PERMISSION_CHANGE_GROUP\n"
            - "DATABASE_PRINCIPAL_CHANGE_GROUP\n"
            - "DATABASE_PRINCIPAL_IMPERSONATION_GROUP\n"
            - "DATABASE_ROLE_MEMBER_CHANGE_GROUP\n"
            - "FAILED_DATABASE_AUTHENTICATION_GROUP\n"
            - "SCHEMA_OBJECT_ACCESS_GROUP\n"
            - "SCHEMA_OBJECT_CHANGE_GROUP\n"
            - "SCHEMA_OBJECT_OWNERSHIP_CHANGE_GROUP\n"
            - "SCHEMA_OBJECT_PERMISSION_CHANGE_GROUP\n"
            - "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP\n"
            - "USER_CHANGE_PASSWORD_GROUP\n"
            - "BATCH_STARTED_GROUP\n"
            - "BATCH_COMPLETED_GROUP\n"
            - "These are groups that cover all sql statements and stored procedures executed against the database, and should not be used in combination
               with other groups as this will result in duplicate audit logs.\n"
            - "For more information, see [Database-Level Audit Action
               Groups](https://docs.microsoft.com/en-us/sql/relational-databases/security/auditing/sql-server-audit-action-groups-and-actions#database-level
              -audit-action-groups).\n"
            - "For Database auditing policy, specific Actions can also be specified (note that Actions cannot be specified for Server auditing policy). The
               supported actions to audit are:\n"
            - "SELECT\n"
            - "UPDATE\n"
            - "INSERT\n"
            - "DELETE\n"
            - "EXECUTE\n"
            - "RECEIVE\n"
            - "REFERENCES\n"
            - "The general form for defining an action to be audited is:\n"
            - "<action> ON <object> BY <principal>\n"
            - "Note that <object> in the above format can refer to an object like a table, view, or stored procedure, or an entire database or schema. For
               the latter cases, the forms DATABASE::<db_name> and SCHEMA::<schema_name> are used, respectively.\n"
            - "For example:\n"
            - "SELECT on dbo.myTable by public\n"
            - "SELECT on DATABASE::myDatabase by public\n"
            - "SELECT on SCHEMA::mySchema by public\n"
            - "For more information, see [Database-Level Audit
               Actions](https://docs.microsoft.com/en-us/sql/relational-databases/security/auditing/sql-server-audit-action-groups-and-actions#database-leve
              l-audit-actions)"
        type: list
    storage_account_subscription_id:
        description:
            - Specifies the blob storage subscription Id.
    is_storage_secondary_key_in_use:
        description:
            - "Specifies whether I(storage_account_access_key) value is the storage's secondary key."
    state:
      description:
        - Assert the state of the Extended Server Blob Auditing Policy.
        - Use 'present' to create or update an Extended Server Blob Auditing Policy and 'absent' to delete it.
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
  - name: Create (or update) Extended Server Blob Auditing Policy
    azure_rm_sqlextendedserverblobauditingpolicy:
      resource_group: blobauditingtest-4799
      server_name: blobauditingtest-6440
      name: default
      predicate_expression: object_name = 'SensitiveData'
      state: Enabled
      storage_endpoint: https://mystorage.blob.core.windows.net
      storage_account_access_key: sdlfkjabc+sdlfkjsdlkfsjdfLDKFTERLKFDFKLjsdfksjdflsdkfD2342309432849328476458/3RSD==
      retention_days: 6
      audit_actions_and_groups:
        - [
  "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP",
  "FAILED_DATABASE_AUTHENTICATION_GROUP",
  "BATCH_COMPLETED_GROUP"
]
      storage_account_subscription_id: 00000000-1234-0000-5678-000000000000
      is_storage_secondary_key_in_use: False
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/blobauditingtest-4799/providers/Microsoft.Sql/servers/blobauditingtest-6440/e
            xtendedAuditingSettings/default"
state:
    description:
        - "Specifies the state of the policy. If state is Enabled, storageEndpoint and storageAccountAccessKey are required. Possible values include:
           'Enabled', 'Disabled'"
    returned: always
    type: str
    sample: Enabled
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMExtendedServerBlobAuditingPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Extended Server Blob Auditing Policy resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            predicate_expression=dict(
                type='str'
            ),
            state=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            storage_endpoint=dict(
                type='str'
            ),
            storage_account_access_key=dict(
                type='str'
            ),
            retention_days=dict(
                type='int'
            ),
            audit_actions_and_groups=dict(
                type='list'
            ),
            storage_account_subscription_id=dict(
                type='str'
            ),
            is_storage_secondary_key_in_use=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMExtendedServerBlobAuditingPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                        supports_check_mode=True,
                                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "predicate_expression":
                    self.parameters["predicate_expression"] = kwargs[key]
                elif key == "state":
                    self.parameters["state"] = _snake_to_camel(kwargs[key], True)
                elif key == "storage_endpoint":
                    self.parameters["storage_endpoint"] = kwargs[key]
                elif key == "storage_account_access_key":
                    self.parameters["storage_account_access_key"] = kwargs[key]
                elif key == "retention_days":
                    self.parameters["retention_days"] = kwargs[key]
                elif key == "audit_actions_and_groups":
                    self.parameters["audit_actions_and_groups"] = kwargs[key]
                elif key == "storage_account_subscription_id":
                    self.parameters["storage_account_subscription_id"] = kwargs[key]
                elif key == "is_storage_secondary_key_in_use":
                    self.parameters["is_storage_secondary_key_in_use"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_extendedserverblobauditingpolicy()

        if not old_response:
            self.log("Extended Server Blob Auditing Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Extended Server Blob Auditing Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Extended Server Blob Auditing Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_extendedserverblobauditingpolicy()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Extended Server Blob Auditing Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_extendedserverblobauditingpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_extendedserverblobauditingpolicy():
                time.sleep(20)
        else:
            self.log("Extended Server Blob Auditing Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_extendedserverblobauditingpolicy(self):
        '''
        Creates or updates Extended Server Blob Auditing Policy with the specified configuration.

        :return: deserialized Extended Server Blob Auditing Policy instance state dictionary
        '''
        self.log("Creating / Updating the Extended Server Blob Auditing Policy instance {0}".format(self.name))

        try:
            response = self.mgmt_client.extended_server_blob_auditing_policies.create_or_update(resource_group_name=self.resource_group,
                                                                                                server_name=self.server_name,
                                                                                                blob_auditing_policy_name=self.name,
                                                                                                parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Extended Server Blob Auditing Policy instance.')
            self.fail("Error creating the Extended Server Blob Auditing Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_extendedserverblobauditingpolicy(self):
        '''
        Deletes specified Extended Server Blob Auditing Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Extended Server Blob Auditing Policy instance {0}".format(self.name))
        try:
            response = self.mgmt_client.extended_server_blob_auditing_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Extended Server Blob Auditing Policy instance.')
            self.fail("Error deleting the Extended Server Blob Auditing Policy instance: {0}".format(str(e)))

        return True

    def get_extendedserverblobauditingpolicy(self):
        '''
        Gets the properties of the specified Extended Server Blob Auditing Policy.

        :return: deserialized Extended Server Blob Auditing Policy instance state dictionary
        '''
        self.log("Checking if the Extended Server Blob Auditing Policy instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.extended_server_blob_auditing_policies.get(resource_group_name=self.resource_group,
                                                                                   server_name=self.server_name,
                                                                                   blob_auditing_policy_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Extended Server Blob Auditing Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Extended Server Blob Auditing Policy instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMExtendedServerBlobAuditingPolicies()


if __name__ == '__main__':
    main()

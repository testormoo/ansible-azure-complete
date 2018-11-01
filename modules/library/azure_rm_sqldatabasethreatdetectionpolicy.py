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
module: azure_rm_sqldatabasethreatdetectionpolicy
version_added: "2.8"
short_description: Manage Database Threat Detection Policy instance.
description:
    - Create, update and delete instance of Database Threat Detection Policy.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database for which database Threat Detection policy is defined.
        required: True
    security_alert_policy_name:
        description:
            - The name of the security alert policy.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    state:
        description:
            - Specifies the state of the policy. If state is C(C(C(enabled))), I(storage_endpoint) and I(storage_account_access_key) are required.
        required: True
        choices:
            - 'new'
            - 'enabled'
            - 'disabled'
    disabled_alerts:
        description:
            - "Specifies the semicolon-separated list of alerts that are C(C(C(disabled))), or empty string to disable no alerts. Possible values:
               Sql_Injection; Sql_Injection_Vulnerability; Access_Anomaly; Data_Exfiltration; Unsafe_Action."
    email_addresses:
        description:
            - Specifies the semicolon-separated list of e-mail addresses to which the alert is sent.
    email_account_admins:
        description:
            - Specifies that the alert is sent to the account administrators.
        choices:
            - 'enabled'
            - 'disabled'
    storage_endpoint:
        description:
            - "Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net). This blob storage will hold all Threat Detection audit
               logs. If I(state) is C(C(C(enabled))), storageEndpoint is required."
    storage_account_access_key:
        description:
            - Specifies the identifier key of the Threat Detection audit storage account. If I(state) is C(C(C(enabled))), storageAccountAccessKey is required.
    retention_days:
        description:
            - Specifies the number of days to keep in the Threat Detection audit logs.
    use_server_default:
        description:
            - Specifies whether to use the default server policy.
        choices:
            - 'enabled'
            - 'disabled'
    state:
      description:
        - Assert the state of the Database Threat Detection Policy.
        - Use 'present' to create or update an Database Threat Detection Policy and 'absent' to delete it.
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
  - name: Create (or update) Database Threat Detection Policy
    azure_rm_sqldatabasethreatdetectionpolicy:
      resource_group: securityalert-4799
      server_name: securityalert-6440
      database_name: testdb
      security_alert_policy_name: default
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/securityalert-4799/providers/Microsoft.Sql/servers/securityalert-6440/databas
            es/testdb"
state:
    description:
        - "Specifies the state of the policy. If state is Enabled, storageEndpoint and storageAccountAccessKey are required. Possible values include: 'New',
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


class AzureRMDatabaseThreatDetectionPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM Database Threat Detection Policy resource"""

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
            database_name=dict(
                type='str',
                required=True
            ),
            security_alert_policy_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            state=dict(
                type='str',
                choices=['new',
                         'enabled',
                         'disabled'],
                required=True
            ),
            disabled_alerts=dict(
                type='str'
            ),
            email_addresses=dict(
                type='str'
            ),
            email_account_admins=dict(
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
            use_server_default=dict(
                type='str',
                choices=['enabled',
                         'disabled']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.database_name = None
        self.security_alert_policy_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDatabaseThreatDetectionPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.parameters["location"] = kwargs[key]
                elif key == "state":
                    self.parameters["state"] = _snake_to_camel(kwargs[key], True)
                elif key == "disabled_alerts":
                    self.parameters["disabled_alerts"] = kwargs[key]
                elif key == "email_addresses":
                    self.parameters["email_addresses"] = kwargs[key]
                elif key == "email_account_admins":
                    self.parameters["email_account_admins"] = _snake_to_camel(kwargs[key], True)
                elif key == "storage_endpoint":
                    self.parameters["storage_endpoint"] = kwargs[key]
                elif key == "storage_account_access_key":
                    self.parameters["storage_account_access_key"] = kwargs[key]
                elif key == "retention_days":
                    self.parameters["retention_days"] = kwargs[key]
                elif key == "use_server_default":
                    self.parameters["use_server_default"] = _snake_to_camel(kwargs[key], True)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_databasethreatdetectionpolicy()

        if not old_response:
            self.log("Database Threat Detection Policy instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Database Threat Detection Policy instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Database Threat Detection Policy instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Database Threat Detection Policy instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_databasethreatdetectionpolicy()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Database Threat Detection Policy instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_databasethreatdetectionpolicy()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_databasethreatdetectionpolicy():
                time.sleep(20)
        else:
            self.log("Database Threat Detection Policy instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_databasethreatdetectionpolicy(self):
        '''
        Creates or updates Database Threat Detection Policy with the specified configuration.

        :return: deserialized Database Threat Detection Policy instance state dictionary
        '''
        self.log("Creating / Updating the Database Threat Detection Policy instance {0}".format(self.security_alert_policy_name))

        try:
            response = self.mgmt_client.database_threat_detection_policies.create_or_update(resource_group_name=self.resource_group,
                                                                                            server_name=self.server_name,
                                                                                            database_name=self.database_name,
                                                                                            security_alert_policy_name=self.security_alert_policy_name,
                                                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Database Threat Detection Policy instance.')
            self.fail("Error creating the Database Threat Detection Policy instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_databasethreatdetectionpolicy(self):
        '''
        Deletes specified Database Threat Detection Policy instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Database Threat Detection Policy instance {0}".format(self.security_alert_policy_name))
        try:
            response = self.mgmt_client.database_threat_detection_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Database Threat Detection Policy instance.')
            self.fail("Error deleting the Database Threat Detection Policy instance: {0}".format(str(e)))

        return True

    def get_databasethreatdetectionpolicy(self):
        '''
        Gets the properties of the specified Database Threat Detection Policy.

        :return: deserialized Database Threat Detection Policy instance state dictionary
        '''
        self.log("Checking if the Database Threat Detection Policy instance {0} is present".format(self.security_alert_policy_name))
        found = False
        try:
            response = self.mgmt_client.database_threat_detection_policies.get(resource_group_name=self.resource_group,
                                                                               server_name=self.server_name,
                                                                               database_name=self.database_name,
                                                                               security_alert_policy_name=self.security_alert_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Database Threat Detection Policy instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Database Threat Detection Policy instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMDatabaseThreatDetectionPolicies()


if __name__ == '__main__':
    main()

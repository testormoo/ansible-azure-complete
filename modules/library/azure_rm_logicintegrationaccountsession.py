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
module: azure_rm_logicintegrationaccountsession
version_added: "2.8"
short_description: Manage Integration Account Session instance.
description:
    - Create, update and delete instance of Integration Account Session.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    session_name:
        description:
            - The integration account I(session) name.
        required: True
    session:
        description:
            - The integration account session.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            content:
                description:
                    - The session content.
    state:
      description:
        - Assert the state of the Integration Account Session.
        - Use 'present' to create or update an Integration Account Session and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Session
    azure_rm_logicintegrationaccountsession:
      resource_group: testrg123
      integration_account_name: testia123
      session_name: testsession123-ICN
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testrg123/providers/Microsoft.Logic/integrationAccounts/testia123/sessions/te
            stsession123-ICN"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIntegrationAccountSessions(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Session resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            integration_account_name=dict(
                type='str',
                required=True
            ),
            session_name=dict(
                type='str',
                required=True
            ),
            session=dict(
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
        self.integration_account_name = None
        self.session_name = None
        self.session = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountSessions, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                supports_check_mode=True,
                                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.session["location"] = kwargs[key]
                elif key == "content":
                    self.session["content"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountsession()

        if not old_response:
            self.log("Integration Account Session instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Session instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Integration Account Session instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Session instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountsession()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Session instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountsession()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccountsession():
                time.sleep(20)
        else:
            self.log("Integration Account Session instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccountsession(self):
        '''
        Creates or updates Integration Account Session with the specified configuration.

        :return: deserialized Integration Account Session instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Session instance {0}".format(self.session_name))

        try:
            response = self.mgmt_client.integration_account_sessions.create_or_update(resource_group_name=self.resource_group,
                                                                                      integration_account_name=self.integration_account_name,
                                                                                      session_name=self.session_name,
                                                                                      session=self.session)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Session instance.')
            self.fail("Error creating the Integration Account Session instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountsession(self):
        '''
        Deletes specified Integration Account Session instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Session instance {0}".format(self.session_name))
        try:
            response = self.mgmt_client.integration_account_sessions.delete(resource_group_name=self.resource_group,
                                                                            integration_account_name=self.integration_account_name,
                                                                            session_name=self.session_name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Session instance.')
            self.fail("Error deleting the Integration Account Session instance: {0}".format(str(e)))

        return True

    def get_integrationaccountsession(self):
        '''
        Gets the properties of the specified Integration Account Session.

        :return: deserialized Integration Account Session instance state dictionary
        '''
        self.log("Checking if the Integration Account Session instance {0} is present".format(self.session_name))
        found = False
        try:
            response = self.mgmt_client.integration_account_sessions.get(resource_group_name=self.resource_group,
                                                                         integration_account_name=self.integration_account_name,
                                                                         session_name=self.session_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Session instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Session instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMIntegrationAccountSessions()


if __name__ == '__main__':
    main()

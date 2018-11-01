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
module: azure_rm_monitoractiongroup
version_added: "2.8"
short_description: Manage Action Group instance.
description:
    - Create, update and delete instance of Action Group.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    action_group_name:
        description:
            - The name of the action group.
        required: True
    action_group:
        description:
            - The action group to create or use for the update.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                required: True
            group_short_name:
                description:
                    - The short name of the action group. This will be used in SMS messages.
                required: True
            enabled:
                description:
                    - Indicates whether this action group is enabled. If an action group is not enabled, then none of its receivers will receive communications.
                required: True
            email_receivers:
                description:
                    - The list of email receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the email receiver. Names must be unique across all receivers within an action group.
                        required: True
                    email_address:
                        description:
                            - The email address of this receiver.
                        required: True
            sms_receivers:
                description:
                    - The list of SMS receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the SMS receiver. Names must be unique across all receivers within an action group.
                        required: True
                    country_code:
                        description:
                            - The country code of the SMS receiver.
                        required: True
                    phone_number:
                        description:
                            - The phone number of the SMS receiver.
                        required: True
            webhook_receivers:
                description:
                    - The list of webhook receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the webhook receiver. Names must be unique across all receivers within an action group.
                        required: True
                    service_uri:
                        description:
                            - The URI where webhooks should be sent.
                        required: True
            itsm_receivers:
                description:
                    - The list of ITSM receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the Itsm receiver. Names must be unique across all receivers within an action group.
                        required: True
                    workspace_id:
                        description:
                            - OMS LA instance identifier.
                        required: True
                    connection_id:
                        description:
                            - Unique identification of ITSM connection among multiple defined in above workspace.
                        required: True
                    ticket_configuration:
                        description:
                            - JSON blob for the configurations of the ITSM action. CreateMultipleWorkItems option will be part of this blob as well.
                        required: True
                    region:
                        description:
                            - "Region in which workspace resides. Supported
                               values:'centralindia','japaneast','southeastasia','australiasoutheast','uksouth','westcentralus','canadacentral','eastus','we
                              steurope'"
                        required: True
            azure_app_push_receivers:
                description:
                    - The list of AzureAppPush receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the Azure mobile app push receiver. Names must be unique across all receivers within an action group.
                        required: True
                    email_address:
                        description:
                            - The email address registered for the Azure mobile app.
                        required: True
            automation_runbook_receivers:
                description:
                    - The list of AutomationRunbook receivers that are part of this action group.
                type: list
                suboptions:
                    automation_account_id:
                        description:
                            - The Azure automation account Id which holds this runbook and authenticate to Azure resource.
                        required: True
                    runbook_name:
                        description:
                            - The name for this runbook.
                        required: True
                    webhook_resource_id:
                        description:
                            - The resource id for webhook linked to this runbook.
                        required: True
                    is_global_runbook:
                        description:
                            - Indicates whether this instance is global runbook.
                        required: True
                    name:
                        description:
                            - Indicates name of the webhook.
                    service_uri:
                        description:
                            - The URI where webhooks should be sent.
            voice_receivers:
                description:
                    - The list of voice receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the voice receiver. Names must be unique across all receivers within an action group.
                        required: True
                    country_code:
                        description:
                            - The country code of the voice receiver.
                        required: True
                    phone_number:
                        description:
                            - The phone number of the voice receiver.
                        required: True
            logic_app_receivers:
                description:
                    - The list of logic app receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the logic app receiver. Names must be unique across all receivers within an action group.
                        required: True
                    resource_id:
                        description:
                            - The azure resource id of the logic app receiver.
                        required: True
                    callback_url:
                        description:
                            - The callback url where http request sent to.
                        required: True
            azure_function_receivers:
                description:
                    - The list of azure function receivers that are part of this action group.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the azure function receiver. Names must be unique across all receivers within an action group.
                        required: True
                    function_app_resource_id:
                        description:
                            - The azure resource id of the function app.
                        required: True
                    function_name:
                        description:
                            - The function name in the function app.
                        required: True
                    http_trigger_url:
                        description:
                            - The http trigger url where http request sent to.
                        required: True
            arm_role_receivers:
                description:
                    - The list of ARM role receivers that are part of this action group. Roles are Azure RBAC roles and only built-in roles are supported.
                type: list
                suboptions:
                    name:
                        description:
                            - The name of the arm role receiver. Names must be unique across all receivers within an action group.
                        required: True
                    role_id:
                        description:
                            - The arm role id.
                        required: True
    state:
      description:
        - Assert the state of the Action Group.
        - Use 'present' to create or update an Action Group and 'absent' to delete it.
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
  - name: Create (or update) Action Group
    azure_rm_monitoractiongroup:
      resource_group: Default-NotificationRules
      action_group_name: SampleActionGroup
      action_group:
        location: Global
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: "/subscriptions/187f412d-1758-44d9-b052-169e2564721d/resourceGroups/Default-NotificationRules/providers/microsoft.insights/actionGroups/SampleAct
            ionGroup"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.monitor import MonitorManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMActionGroups(AzureRMModuleBase):
    """Configuration class for an Azure RM Action Group resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            action_group_name=dict(
                type='str',
                required=True
            ),
            action_group=dict(
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
        self.action_group_name = None
        self.action_group = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMActionGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.action_group["location"] = kwargs[key]
                elif key == "group_short_name":
                    self.action_group["group_short_name"] = kwargs[key]
                elif key == "enabled":
                    self.action_group["enabled"] = kwargs[key]
                elif key == "email_receivers":
                    self.action_group["email_receivers"] = kwargs[key]
                elif key == "sms_receivers":
                    self.action_group["sms_receivers"] = kwargs[key]
                elif key == "webhook_receivers":
                    self.action_group["webhook_receivers"] = kwargs[key]
                elif key == "itsm_receivers":
                    self.action_group["itsm_receivers"] = kwargs[key]
                elif key == "azure_app_push_receivers":
                    self.action_group["azure_app_push_receivers"] = kwargs[key]
                elif key == "automation_runbook_receivers":
                    self.action_group["automation_runbook_receivers"] = kwargs[key]
                elif key == "voice_receivers":
                    self.action_group["voice_receivers"] = kwargs[key]
                elif key == "logic_app_receivers":
                    self.action_group["logic_app_receivers"] = kwargs[key]
                elif key == "azure_function_receivers":
                    self.action_group["azure_function_receivers"] = kwargs[key]
                elif key == "arm_role_receivers":
                    self.action_group["arm_role_receivers"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_actiongroup()

        if not old_response:
            self.log("Action Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Action Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Action Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Action Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_actiongroup()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Action Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_actiongroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_actiongroup():
                time.sleep(20)
        else:
            self.log("Action Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_actiongroup(self):
        '''
        Creates or updates Action Group with the specified configuration.

        :return: deserialized Action Group instance state dictionary
        '''
        self.log("Creating / Updating the Action Group instance {0}".format(self.action_group_name))

        try:
            response = self.mgmt_client.action_groups.create_or_update(resource_group_name=self.resource_group,
                                                                       action_group_name=self.action_group_name,
                                                                       action_group=self.action_group)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Action Group instance.')
            self.fail("Error creating the Action Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_actiongroup(self):
        '''
        Deletes specified Action Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Action Group instance {0}".format(self.action_group_name))
        try:
            response = self.mgmt_client.action_groups.delete(resource_group_name=self.resource_group,
                                                             action_group_name=self.action_group_name)
        except CloudError as e:
            self.log('Error attempting to delete the Action Group instance.')
            self.fail("Error deleting the Action Group instance: {0}".format(str(e)))

        return True

    def get_actiongroup(self):
        '''
        Gets the properties of the specified Action Group.

        :return: deserialized Action Group instance state dictionary
        '''
        self.log("Checking if the Action Group instance {0} is present".format(self.action_group_name))
        found = False
        try:
            response = self.mgmt_client.action_groups.get(resource_group_name=self.resource_group,
                                                          action_group_name=self.action_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Action Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Action Group instance.')
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
    AzureRMActionGroups()


if __name__ == '__main__':
    main()

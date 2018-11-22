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
short_description: Manage Azure Action Group instance.
description:
    - Create, update and delete instance of Azure Action Group.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the action group.
        required: True
    location:
        description:
            - Resource location
            - Required when C(state) is I(present).
    group_short_name:
        description:
            - The short name of the action group. This will be used in SMS messages.
            - Required when C(state) is I(present).
    enabled:
        description:
            - Indicates whether this action group is enabled. If an action group is not enabled, then none of its receivers will receive communications.
            - Required when C(state) is I(present).
    email_receivers:
        description:
            - The list of email receivers that are part of this action group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the email receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            email_address:
                description:
                    - The email address of this receiver.
                    - Required when C(state) is I(present).
    sms_receivers:
        description:
            - The list of SMS receivers that are part of this action group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the SMS receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            country_code:
                description:
                    - The country code of the SMS receiver.
                    - Required when C(state) is I(present).
            phone_number:
                description:
                    - The phone number of the SMS receiver.
                    - Required when C(state) is I(present).
    webhook_receivers:
        description:
            - The list of webhook receivers that are part of this action group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the webhook receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            service_uri:
                description:
                    - The URI where webhooks should be sent.
                    - Required when C(state) is I(present).
    itsm_receivers:
        description:
            - The list of ITSM receivers that are part of this action group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the Itsm receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            workspace_id:
                description:
                    - OMS LA instance identifier.
                    - Required when C(state) is I(present).
            connection_id:
                description:
                    - Unique identification of ITSM connection among multiple defined in above workspace.
                    - Required when C(state) is I(present).
            ticket_configuration:
                description:
                    - JSON blob for the configurations of the ITSM action. CreateMultipleWorkItems option will be part of this blob as well.
                    - Required when C(state) is I(present).
            region:
                description:
                    - "Region in which workspace resides. Supported
                       values:'centralindia','japaneast','southeastasia','australiasoutheast','uksouth','westcentralus','canadacentral','eastus','westeurope
                      '"
                    - Required when C(state) is I(present).
    azure_app_push_receivers:
        description:
            - The list of AzureAppPush receivers that are part of this action group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the Azure mobile app push receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            email_address:
                description:
                    - The email address registered for the Azure mobile app.
                    - Required when C(state) is I(present).
    automation_runbook_receivers:
        description:
            - The list of AutomationRunbook receivers that are part of this action group.
        type: list
        suboptions:
            automation_account_id:
                description:
                    - The Azure automation account Id which holds this runbook and authenticate to Azure resource.
                    - Required when C(state) is I(present).
            runbook_name:
                description:
                    - The name for this runbook.
                    - Required when C(state) is I(present).
            webhook_resource_id:
                description:
                    - The resource id for webhook linked to this runbook.
                    - Required when C(state) is I(present).
            is_global_runbook:
                description:
                    - Indicates whether this instance is global runbook.
                    - Required when C(state) is I(present).
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
                    - Required when C(state) is I(present).
            country_code:
                description:
                    - The country code of the voice receiver.
                    - Required when C(state) is I(present).
            phone_number:
                description:
                    - The phone number of the voice receiver.
                    - Required when C(state) is I(present).
    logic_app_receivers:
        description:
            - The list of logic app receivers that are part of this action group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the logic app receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            resource_id:
                description:
                    - The azure resource id of the logic app receiver.
                    - Required when C(state) is I(present).
            callback_url:
                description:
                    - The callback url where http request sent to.
                    - Required when C(state) is I(present).
    azure_function_receivers:
        description:
            - The list of azure function receivers that are part of this action group.
        type: list
        suboptions:
            name:
                description:
                    - The name of the azure function receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            function_app_resource_id:
                description:
                    - The azure resource id of the function app.
                    - Required when C(state) is I(present).
            function_name:
                description:
                    - The function name in the function app.
                    - Required when C(state) is I(present).
            http_trigger_url:
                description:
                    - The http trigger url where http request sent to.
                    - Required when C(state) is I(present).
    arm_role_receivers:
        description:
            - The list of ARM role receivers that are part of this action group. Roles are Azure RBAC roles and only built-in roles are supported.
        type: list
        suboptions:
            name:
                description:
                    - The name of the arm role receiver. Names must be unique across all receivers within an action group.
                    - Required when C(state) is I(present).
            role_id:
                description:
                    - The arm role id.
                    - Required when C(state) is I(present).
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
      name: SampleActionGroup
      location: Global
      group_short_name: sample
      enabled: True
      email_receivers:
        - name: John Doe's email
          email_address: johndoe@email.com
      sms_receivers:
        - name: John Doe's mobile
          country_code: 1
          phone_number: 1234567890
      webhook_receivers:
        - name: Sample webhook
          service_uri: http://www.example.com/webhook
      itsm_receivers:
        - name: Sample itsm
          workspace_id: 5def922a-3ed4-49c1-b9fd-05ec533819a3|55dfd1f8-7e59-4f89-bf56-4c82f5ace23c
          connection_id: a3b9076c-ce8e-434e-85b4-aff10cb3c8f1
          ticket_configuration: {"PayloadRevision":0,"WorkItemType":"Incident","UseTemplate":false,"WorkItemData":"{}","CreateOneWIPerCI":false}
          region: westcentralus
      azure_app_push_receivers:
        - name: Sample azureAppPush
          email_address: johndoe@email.com
      automation_runbook_receivers:
        - automation_account_id: /subscriptions/187f412d-1758-44d9-b052-169e2564721d/resourceGroups/runbookTest/providers/Microsoft.Automation/automationAccounts/runbooktest
          runbook_name: Sample runbook
          webhook_resource_id: /subscriptions/187f412d-1758-44d9-b052-169e2564721d/resourceGroups/runbookTest/providers/Microsoft.Automation/automationAccounts/runbooktest/webhooks/Alert1510184037084
          is_global_runbook: False
          name: testRunbook
          service_uri: https://s13events.azure-automation.net/webhooks?token=iimE%2fD19Eg%2bvDy22yUMecIZY6Uiz%2bHfuQ67r8r1wY%2fI%3d
      voice_receivers:
        - name: Sample voice
          country_code: 1
          phone_number: 1234567890
      logic_app_receivers:
        - name: Sample logicApp
          resource_id: /subscriptions/187f412d-1758-44d9-b052-169e2564721d/resourceGroups/LogicApp/providers/Microsoft.Logic/workflows/testLogicApp
          callback_url: https://prod-27.northcentralus.logic.azure.com/workflows/68e572e818e5457ba898763b7db90877/triggers/manual/paths/invoke/azns/test?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Abpsb72UYJxPPvmDo937uzofupO5r_vIeWEx7KVHo7w
      azure_function_receivers:
        - name: Sample azureFunction
          function_app_resource_id: /subscriptions/5def922a-3ed4-49c1-b9fd-05ec533819a3/resourceGroups/aznsTest/providers/Microsoft.Web/sites/testFunctionApp
          function_name: HttpTriggerCSharp1
          http_trigger_url: https://testfunctionapp.azurewebsites.net/api/HttpTriggerCSharp1?code=4CopFfiXqUQC8dvIM7F53J7tIU3Gy9QQIG/vKAXMe2avhHqK3/jVYw==
      arm_role_receivers:
        - name: Sample armRole
          role_id: 8e3af657-a8ff-443c-a75c-2fe8c4bcb635
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


class AzureRMActionGroup(AzureRMModuleBase):
    """Configuration class for an Azure RM Action Group resource"""

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
            group_short_name=dict(
                type='str'
            ),
            enabled=dict(
                type='str'
            ),
            email_receivers=dict(
                type='list'
            ),
            sms_receivers=dict(
                type='list'
            ),
            webhook_receivers=dict(
                type='list'
            ),
            itsm_receivers=dict(
                type='list'
            ),
            azure_app_push_receivers=dict(
                type='list'
            ),
            automation_runbook_receivers=dict(
                type='list'
            ),
            voice_receivers=dict(
                type='list'
            ),
            logic_app_receivers=dict(
                type='list'
            ),
            azure_function_receivers=dict(
                type='list'
            ),
            arm_role_receivers=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.action_group = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMActionGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.action_group[key] = kwargs[key]


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
                if (not default_compare(self.action_group, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Action Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_actiongroup()

            self.results['changed'] = True
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
            self.results.update(self.format_response(response))
        return self.results

    def create_update_actiongroup(self):
        '''
        Creates or updates Action Group with the specified configuration.

        :return: deserialized Action Group instance state dictionary
        '''
        self.log("Creating / Updating the Action Group instance {0}".format(self.name))

        try:
            response = self.mgmt_client.action_groups.create_or_update(resource_group_name=self.resource_group,
                                                                       action_group_name=self.name,
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
        self.log("Deleting the Action Group instance {0}".format(self.name))
        try:
            response = self.mgmt_client.action_groups.delete(resource_group_name=self.resource_group,
                                                             action_group_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Action Group instance.')
            self.fail("Error deleting the Action Group instance: {0}".format(str(e)))

        return True

    def get_actiongroup(self):
        '''
        Gets the properties of the specified Action Group.

        :return: deserialized Action Group instance state dictionary
        '''
        self.log("Checking if the Action Group instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.action_groups.get(resource_group_name=self.resource_group,
                                                          action_group_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Action Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Action Group instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def dict_camelize(d, path, camelize_first):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_camelize(d[i], path, camelize_first)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = _snake_to_camel(old_value, camelize_first)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_camelize(sd, path[1:], camelize_first)


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


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMActionGroup()


if __name__ == '__main__':
    main()

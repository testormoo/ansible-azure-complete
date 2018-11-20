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
module: azure_rm_automationwebhook
version_added: "2.8"
short_description: Manage Webhook instance.
description:
    - Create, update and delete instance of Webhook.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    automation_account_name:
        description:
            - The name of the automation account.
        required: True
    name:
        description:
            - The webhook name.
        required: True
    name:
        description:
            - Gets or sets the name of the webhook.
            - Required when C(state) is I(present).
    is_enabled:
        description:
            - Gets or sets the value of the enabled flag of webhook.
    uri:
        description:
            - Gets or sets the uri.
    expiry_time:
        description:
            - Gets or sets the expiry time.
    parameters:
        description:
            - Gets or sets the parameters of the job.
    runbook:
        description:
            - Gets or sets the runbook.
        suboptions:
            name:
                description:
                    - Gets or sets the name of the runbook.
    run_on:
        description:
            - Gets or sets the name of the hybrid worker group the webhook job will run on.
    state:
      description:
        - Assert the state of the Webhook.
        - Use 'present' to create or update an Webhook and 'absent' to delete it.
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
  - name: Create (or update) Webhook
    azure_rm_automationwebhook:
      resource_group: rg
      automation_account_name: myAutomationAccount33
      name: TestWebhook
      name: TestWebhook
      is_enabled: True
      uri: https://s1events.azure-automation.net/webhooks?token=7u3KfQvM1vUPWaDMFRv2%2fAA4Jqx8QwS8aBuyO6Xsdcw%3d
      expiry_time: 2018-03-29T22:18:13.7002872Z
      runbook:
        name: TestRunbook
'''

RETURN = '''
id:
    description:
        - Fully qualified resource Id for the resource
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Automation/automationAccounts/myAutomationAccount33/webhooks/TestWebhook
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.automation import AutomationClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWebhook(AzureRMModuleBase):
    """Configuration class for an Azure RM Webhook resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            automation_account_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            is_enabled=dict(
                type='str'
            ),
            uri=dict(
                type='str'
            ),
            expiry_time=dict(
                type='datetime'
            ),
            parameters=dict(
                type='dict'
            ),
            runbook=dict(
                type='dict'
            ),
            run_on=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.automation_account_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWebhook, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "name":
                    self.parameters["name"] = kwargs[key]
                elif key == "is_enabled":
                    self.parameters["is_enabled"] = kwargs[key]
                elif key == "uri":
                    self.parameters["uri"] = kwargs[key]
                elif key == "expiry_time":
                    self.parameters["expiry_time"] = kwargs[key]
                elif key == "parameters":
                    self.parameters["parameters"] = kwargs[key]
                elif key == "runbook":
                    self.parameters["runbook"] = kwargs[key]
                elif key == "run_on":
                    self.parameters["run_on"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AutomationClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_webhook()

        if not old_response:
            self.log("Webhook instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Webhook instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Webhook instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_webhook()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Webhook instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_webhook()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_webhook():
                time.sleep(20)
        else:
            self.log("Webhook instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_webhook(self):
        '''
        Creates or updates Webhook with the specified configuration.

        :return: deserialized Webhook instance state dictionary
        '''
        self.log("Creating / Updating the Webhook instance {0}".format(self.name))

        try:
            response = self.mgmt_client.webhook.create_or_update(resource_group_name=self.resource_group,
                                                                 automation_account_name=self.automation_account_name,
                                                                 webhook_name=self.name,
                                                                 parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Webhook instance.')
            self.fail("Error creating the Webhook instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_webhook(self):
        '''
        Deletes specified Webhook instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Webhook instance {0}".format(self.name))
        try:
            response = self.mgmt_client.webhook.delete(resource_group_name=self.resource_group,
                                                       automation_account_name=self.automation_account_name,
                                                       webhook_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Webhook instance.')
            self.fail("Error deleting the Webhook instance: {0}".format(str(e)))

        return True

    def get_webhook(self):
        '''
        Gets the properties of the specified Webhook.

        :return: deserialized Webhook instance state dictionary
        '''
        self.log("Checking if the Webhook instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.webhook.get(resource_group_name=self.resource_group,
                                                    automation_account_name=self.automation_account_name,
                                                    webhook_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Webhook instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Webhook instance.')
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
    AzureRMWebhook()


if __name__ == '__main__':
    main()

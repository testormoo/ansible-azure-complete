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
module: azure_rm_monitordiagnosticsetting
version_added: "2.8"
short_description: Manage Diagnostic Setting instance.
description:
    - Create, update and delete instance of Diagnostic Setting.

options:
    resource_uri:
        description:
            - The identifier of the resource.
        required: True
    storage_account_id:
        description:
            - The resource ID of the storage account to which you would like to send Diagnostic I(logs).
    service_bus_rule_id:
        description:
            - The service bus rule Id of the diagnostic setting. This is here to maintain backwards compatibility.
    event_hub_authorization_rule_id:
        description:
            - The resource Id for the event hub authorization rule.
    event_hub_name:
        description:
            - The name of the event hub. If none is specified, the default event hub will be selected.
    metrics:
        description:
            - the list of metric settings.
        type: list
        suboptions:
            time_grain:
                description:
                    - the timegrain of the metric in ISO8601 format.
            category:
                description:
                    - "Name of a Diagnostic Metric category for a resource type this setting is applied to. To obtain the list of Diagnostic metric
                       categories for a resource, first perform a GET diagnostic settings operation."
            enabled:
                description:
                    - a value indicating whether this I(category) is enabled.
                required: True
            retention_policy:
                description:
                    - the retention policy for this I(category).
                suboptions:
                    enabled:
                        description:
                            - a value indicating whether the retention policy is enabled.
                        required: True
                    days:
                        description:
                            - the number of days for the retention in days. A value of 0 will retain the events indefinitely.
                        required: True
    logs:
        description:
            - the list of logs settings.
        type: list
        suboptions:
            category:
                description:
                    - "Name of a Diagnostic Log category for a resource type this setting is applied to. To obtain the list of Diagnostic Log categories for
                       a resource, first perform a GET diagnostic settings operation."
            enabled:
                description:
                    - a value indicating whether this log is enabled.
                required: True
            retention_policy:
                description:
                    - the retention policy for this log.
                suboptions:
                    enabled:
                        description:
                            - a value indicating whether the retention policy is enabled.
                        required: True
                    days:
                        description:
                            - the number of days for the retention in days. A value of 0 will retain the events indefinitely.
                        required: True
    workspace_id:
        description:
            - "The workspace ID (resource ID of a Log Analytics workspace) for a Log Analytics workspace to which you would like to send Diagnostic I(logs).
               Example:
               /subscriptions/4b9e8510-67ab-4e9a-95a9-e2f1e570ea9c/resourceGroups/insights-integration/providers/Microsoft.OperationalInsights/workspaces/vi
              ruela2"
    name:
        description:
            - The name of the diagnostic setting.
        required: True
    state:
      description:
        - Assert the state of the Diagnostic Setting.
        - Use 'present' to create or update an Diagnostic Setting and 'absent' to delete it.
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
  - name: Create (or update) Diagnostic Setting
    azure_rm_monitordiagnosticsetting:
      resource_uri: subscriptions/1a66ce04-b633-4a0b-b2bc-a912ec8986a6/resourcegroups/viruela1/providers/microsoft.logic/workflows/viruela6
      name: mysetting
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: "/subscriptions/1a66ce04-b633-4a0b-b2bc-a912ec8986a6/resourcegroups/viruela1/providers/microsoft.logic/workflows/viruela6/diagnosticSettings/myse
            tting"
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


class AzureRMDiagnosticSettings(AzureRMModuleBase):
    """Configuration class for an Azure RM Diagnostic Setting resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_uri=dict(
                type='str',
                required=True
            ),
            storage_account_id=dict(
                type='str'
            ),
            service_bus_rule_id=dict(
                type='str'
            ),
            event_hub_authorization_rule_id=dict(
                type='str'
            ),
            event_hub_name=dict(
                type='str'
            ),
            metrics=dict(
                type='list'
            ),
            logs=dict(
                type='list'
            ),
            workspace_id=dict(
                type='str'
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_uri = None
        self.parameters = dict()
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMDiagnosticSettings, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "storage_account_id":
                    self.parameters["storage_account_id"] = kwargs[key]
                elif key == "service_bus_rule_id":
                    self.parameters["service_bus_rule_id"] = kwargs[key]
                elif key == "event_hub_authorization_rule_id":
                    self.parameters["event_hub_authorization_rule_id"] = kwargs[key]
                elif key == "event_hub_name":
                    self.parameters["event_hub_name"] = kwargs[key]
                elif key == "metrics":
                    self.parameters["metrics"] = kwargs[key]
                elif key == "logs":
                    self.parameters["logs"] = kwargs[key]
                elif key == "workspace_id":
                    self.parameters["workspace_id"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_diagnosticsetting()

        if not old_response:
            self.log("Diagnostic Setting instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Diagnostic Setting instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Diagnostic Setting instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Diagnostic Setting instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_diagnosticsetting()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Diagnostic Setting instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_diagnosticsetting()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_diagnosticsetting():
                time.sleep(20)
        else:
            self.log("Diagnostic Setting instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_diagnosticsetting(self):
        '''
        Creates or updates Diagnostic Setting with the specified configuration.

        :return: deserialized Diagnostic Setting instance state dictionary
        '''
        self.log("Creating / Updating the Diagnostic Setting instance {0}".format(self.name))

        try:
            response = self.mgmt_client.diagnostic_settings.create_or_update(resource_uri=self.resource_uri,
                                                                             parameters=self.parameters,
                                                                             name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Diagnostic Setting instance.')
            self.fail("Error creating the Diagnostic Setting instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_diagnosticsetting(self):
        '''
        Deletes specified Diagnostic Setting instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Diagnostic Setting instance {0}".format(self.name))
        try:
            response = self.mgmt_client.diagnostic_settings.delete(resource_uri=self.resource_uri,
                                                                   name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Diagnostic Setting instance.')
            self.fail("Error deleting the Diagnostic Setting instance: {0}".format(str(e)))

        return True

    def get_diagnosticsetting(self):
        '''
        Gets the properties of the specified Diagnostic Setting.

        :return: deserialized Diagnostic Setting instance state dictionary
        '''
        self.log("Checking if the Diagnostic Setting instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.diagnostic_settings.get(resource_uri=self.resource_uri,
                                                                name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Diagnostic Setting instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Diagnostic Setting instance.')
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
    AzureRMDiagnosticSettings()


if __name__ == '__main__':
    main()

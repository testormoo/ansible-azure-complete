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
module: azure_rm_monitoractivitylogalert
version_added: "2.8"
short_description: Manage Activity Log Alert instance.
description:
    - Create, update and delete instance of Activity Log Alert.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the activity log alert.
        required: True
    activity_log_alert:
        description:
            - The activity log alert to create or use for the update.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                    - Required when C(state) is I(present).
            scopes:
                description:
                    - "A list of resourceIds that will be used as prefixes. The alert will only apply to activityLogs with resourceIds that fall under one
                       of these prefixes. This list must include at least one item."
                    - Required when C(state) is I(present).
                type: list
            enabled:
                description:
                    - "Indicates whether this activity log alert is enabled. If an activity log alert is not enabled, then none of its I(actions) will be
                       activated."
            condition:
                description:
                    - The condition that will cause this alert to activate.
                    - Required when C(state) is I(present).
                suboptions:
                    all_of:
                        description:
                            - The list of activity log alert conditions.
                            - Required when C(state) is I(present).
                        type: list
                        suboptions:
                            field:
                                description:
                                    - "The name of the field that this condition will examine. The possible values for this field are (case-insensitive):
                                       'resourceId', 'category', 'caller', 'level', 'operationName', 'resourceGroup', 'resourceProvider', 'status',
                                       'subStatus', 'resourceType', or anything beginning with 'properties.'."
                                    - Required when C(state) is I(present).
                            equals:
                                description:
                                    - The I(field) value will be compared to this value (case-insensitive) to determine if the condition is met.
                                    - Required when C(state) is I(present).
            actions:
                description:
                    - The actions that will activate when the I(condition) is met.
                    - Required when C(state) is I(present).
                suboptions:
                    action_groups:
                        description:
                            - The list of activity log alerts.
                        type: list
                        suboptions:
                            action_group_id:
                                description:
                                    - The resourceId of the action group. This cannot be null or empty.
                                    - Required when C(state) is I(present).
                            webhook_properties:
                                description:
                                    - the dictionary of custom properties to include with the post operation. These data are appended to the webhook payload.
            description:
                description:
                    - A description of this activity log alert.
    state:
      description:
        - Assert the state of the Activity Log Alert.
        - Use 'present' to create or update an Activity Log Alert and 'absent' to delete it.
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
  - name: Create (or update) Activity Log Alert
    azure_rm_monitoractivitylogalert:
      resource_group: Default-ActivityLogAlerts
      name: SampleActivityLogAlert
      activity_log_alert:
        location: Global
        scopes:
          - [
  "subscriptions/187f412d-1758-44d9-b052-169e2564721d"
]
        enabled: True
        condition:
          all_of:
            - field: Category
              equals: Administrative
        actions:
          action_groups:
            - action_group_id: /subscriptions/187f412d-1758-44d9-b052-169e2564721d/resourceGroups/Default-ActionGroups/providers/microsoft.insights/actionGroups/SampleActionGroup
              webhook_properties: {
  "sampleWebhookProperty": "samplePropertyValue"
}
        description: Sample activity log alert description
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: "/subscriptions/187f412d-1758-44d9-b052-169e2564721d/resourceGroups/Default-ActivityLogAlerts/providers/microsoft.insights/activityLogAlerts/Samp
            leActivityLogAlert"
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


class AzureRMActivityLogAlerts(AzureRMModuleBase):
    """Configuration class for an Azure RM Activity Log Alert resource"""

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
            activity_log_alert=dict(
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
        self.activity_log_alert = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMActivityLogAlerts, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.activity_log_alert["location"] = kwargs[key]
                elif key == "scopes":
                    self.activity_log_alert["scopes"] = kwargs[key]
                elif key == "enabled":
                    self.activity_log_alert["enabled"] = kwargs[key]
                elif key == "condition":
                    self.activity_log_alert["condition"] = kwargs[key]
                elif key == "actions":
                    self.activity_log_alert["actions"] = kwargs[key]
                elif key == "description":
                    self.activity_log_alert["description"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_activitylogalert()

        if not old_response:
            self.log("Activity Log Alert instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Activity Log Alert instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Activity Log Alert instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_activitylogalert()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Activity Log Alert instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_activitylogalert()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_activitylogalert():
                time.sleep(20)
        else:
            self.log("Activity Log Alert instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_activitylogalert(self):
        '''
        Creates or updates Activity Log Alert with the specified configuration.

        :return: deserialized Activity Log Alert instance state dictionary
        '''
        self.log("Creating / Updating the Activity Log Alert instance {0}".format(self.name))

        try:
            response = self.mgmt_client.activity_log_alerts.create_or_update(resource_group_name=self.resource_group,
                                                                             activity_log_alert_name=self.name,
                                                                             activity_log_alert=self.activity_log_alert)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Activity Log Alert instance.')
            self.fail("Error creating the Activity Log Alert instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_activitylogalert(self):
        '''
        Deletes specified Activity Log Alert instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Activity Log Alert instance {0}".format(self.name))
        try:
            response = self.mgmt_client.activity_log_alerts.delete(resource_group_name=self.resource_group,
                                                                   activity_log_alert_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Activity Log Alert instance.')
            self.fail("Error deleting the Activity Log Alert instance: {0}".format(str(e)))

        return True

    def get_activitylogalert(self):
        '''
        Gets the properties of the specified Activity Log Alert.

        :return: deserialized Activity Log Alert instance state dictionary
        '''
        self.log("Checking if the Activity Log Alert instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.activity_log_alerts.get(resource_group_name=self.resource_group,
                                                                activity_log_alert_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Activity Log Alert instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Activity Log Alert instance.')
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
    AzureRMActivityLogAlerts()


if __name__ == '__main__':
    main()

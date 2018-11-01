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
module: azure_rm_monitorautoscalesetting
version_added: "2.8"
short_description: Manage Autoscale Setting instance.
description:
    - Create, update and delete instance of Autoscale Setting.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    autoscale_setting_name:
        description:
            - The autoscale setting name.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    profiles:
        description:
            - "the collection of automatic scaling profiles that specify different scaling parameters for different time periods. A maximum of 20 profiles
               can be specified."
        required: True
        type: list
        suboptions:
            name:
                description:
                    - the name of the profile.
                required: True
            capacity:
                description:
                    - the number of instances that can be used during this profile.
                required: True
                suboptions:
                    minimum:
                        description:
                            - the minimum number of instances for the resource.
                        required: True
                    maximum:
                        description:
                            - "the maximum number of instances for the resource. The actual maximum number of instances is limited by the cores that are
                               available in the subscription."
                        required: True
                    default:
                        description:
                            - "the number of instances that will be set if metrics are not available for evaluation. The default is only used if the current
                               instance count is lower than the default."
                        required: True
            rules:
                description:
                    - the collection of rules that provide the triggers and parameters for the scaling action. A maximum of 10 rules can be specified.
                required: True
                type: list
                suboptions:
                    metric_trigger:
                        description:
                            - the trigger that results in a scaling action.
                        required: True
                        suboptions:
                            metric_name:
                                description:
                                    - the name of the metric that defines what the rule monitors.
                                required: True
                            metric_resource_uri:
                                description:
                                    - the resource identifier of the resource the rule monitors.
                                required: True
                            time_grain:
                                description:
                                    - "the granularity of metrics the rule monitors. Must be one of the predefined values returned from metric definitions
                                       for the metric. Must be between 12 hours and 1 minute."
                                required: True
                            statistic:
                                description:
                                    - the metric statistic type. How the metrics from multiple instances are combined.
                                required: True
                                choices:
                                    - 'average'
                                    - 'min'
                                    - 'max'
                                    - 'sum'
                            time_window:
                                description:
                                    - "the range of time in which instance data is collected. This value must be greater than the delay in metric
                                       collection, which can vary from resource-to-resource. Must be between 12 hours and 5 minutes."
                                required: True
                            time_aggregation:
                                description:
                                    - time aggregation type. How the data that is collected should be combined over time. The default value is C(C(average)).
                                required: True
                                choices:
                                    - 'average'
                                    - 'minimum'
                                    - 'maximum'
                                    - 'total'
                                    - 'count'
                                    - 'last'
                            operator:
                                description:
                                    - the operator that is used to compare the metric data and the I(threshold).
                                required: True
                                choices:
                                    - 'equals'
                                    - 'not_equals'
                                    - 'greater_than'
                                    - 'greater_than_or_equal'
                                    - 'less_than'
                                    - 'less_than_or_equal'
                            threshold:
                                description:
                                    - the threshold of the metric that triggers the scale action.
                                required: True
                    scale_action:
                        description:
                            - the parameters for the scaling action.
                        required: True
                        suboptions:
                            direction:
                                description:
                                    - the scale direction. Whether the scaling action increases or decreases the number of instances.
                                required: True
                                choices:
                                    - 'none'
                                    - 'increase'
                                    - 'decrease'
                            type:
                                description:
                                    - the type of action that should occur when the scale rule fires.
                                required: True
                                choices:
                                    - 'change_count'
                                    - 'percent_change_count'
                                    - 'exact_count'
                            value:
                                description:
                                    - the number of instances that are involved in the scaling action. This value must be 1 or greater. The default value is 1.
                            cooldown:
                                description:
                                    - "the amount of time to wait since the last scaling action before this action occurs. It must be between 1 week and 1
                                       minute in ISO 8601 format."
                                required: True
            fixed_date:
                description:
                    - the specific date-time for the profile. This element is not used if the I(recurrence) element is used.
                suboptions:
                    time_zone:
                        description:
                            - "the timezone of the I(start) and I(end) times for the profile. Some examples of valid timezones are: Dateline Standard Time,
                               UTC-11, Hawaiian Standard Time, Alaskan Standard Time, Pacific Standard Time (Mexico), Pacific Standard Time, US Mountain
                               Standard Time, Mountain Standard Time (Mexico), Mountain Standard Time, Central America Standard Time, Central Standard
                               Time, Central Standard Time (Mexico), Canada Central Standard Time, SA Pacific Standard Time, Eastern Standard Time, US
                               Eastern Standard Time, Venezuela Standard Time, Paraguay Standard Time, Atlantic Standard Time, Central Brazilian Standard
                               Time, SA Western Standard Time, Pacific SA Standard Time, Newfoundland Standard Time, E. South America Standard Time,
                               Argentina Standard Time, SA Eastern Standard Time, Greenland Standard Time, Montevideo Standard Time, Bahia Standard Time,
                               UTC-02, Mid-Atlantic Standard Time, Azores Standard Time, Cape Verde Standard Time, Morocco Standard Time, UTC, GMT Standard
                               Time, Greenwich Standard Time, W. Europe Standard Time, Central Europe Standard Time, Romance Standard Time, Central
                               European Standard Time, W. Central Africa Standard Time, Namibia Standard Time, Jordan Standard Time, GTB Standard Time,
                               Middle East Standard Time, Egypt Standard Time, Syria Standard Time, E. Europe Standard Time, South Africa Standard Time,
                               FLE Standard Time, Turkey Standard Time, Israel Standard Time, Kaliningrad Standard Time, Libya Standard Time, Arabic
                               Standard Time, Arab Standard Time, Belarus Standard Time, Russian Standard Time, E. Africa Standard Time, Iran Standard
                               Time, Arabian Standard Time, Azerbaijan Standard Time, Russia Time Zone 3, Mauritius Standard Time, Georgian Standard Time,
                               Caucasus Standard Time, Afghanistan Standard Time, West Asia Standard Time, Ekaterinburg Standard Time, Pakistan Standard
                               Time, India Standard Time, Sri Lanka Standard Time, Nepal Standard Time, Central Asia Standard Time, Bangladesh Standard
                               Time, N. Central Asia Standard Time, Myanmar Standard Time, SE Asia Standard Time, North Asia Standard Time, China Standard
                               Time, North Asia East Standard Time, Singapore Standard Time, W. Australia Standard Time, Taipei Standard Time, Ulaanbaatar
                               Standard Time, Tokyo Standard Time, Korea Standard Time, Yakutsk Standard Time, Cen. Australia Standard Time, AUS Central
                               Standard Time, E. Australia Standard Time, AUS Eastern Standard Time, West Pacific Standard Time, Tasmania Standard Time,
                               Magadan Standard Time, Vladivostok Standard Time, Russia Time Zone 10, Central Pacific Standard Time, Russia Time Zone 11,
                               New Zealand Standard Time, UTC+12, Fiji Standard Time, Kamchatka Standard Time, Tonga Standard Time, Samoa Standard Time,
                               Line Islands Standard Time"
                    start:
                        description:
                            - the start time for the profile in ISO 8601 format.
                        required: True
                    end:
                        description:
                            - the end time for the profile in ISO 8601 format.
                        required: True
            recurrence:
                description:
                    - the repeating times at which this profile begins. This element is not used if the I(fixed_date) element is used.
                suboptions:
                    frequency:
                        description:
                            - "the recurrence frequency. How often the I(schedule) profile should take effect. This value must be C(week), meaning each
                               C(week) will have the same set of profiles. For example, to set a daily I(schedule), set **I(schedule)** to every C(day) of
                               the C(week). The frequency property specifies that the I(schedule) is repeated weekly."
                        required: True
                        choices:
                            - 'none'
                            - 'second'
                            - 'minute'
                            - 'hour'
                            - 'day'
                            - 'week'
                            - 'month'
                            - 'year'
                    schedule:
                        description:
                            - the scheduling constraints for when the profile begins.
                        required: True
                        suboptions:
                            time_zone:
                                description:
                                    - "the timezone for the I(hours) of the profile. Some examples of valid timezones are: Dateline Standard Time, UTC-11,
                                       Hawaiian Standard Time, Alaskan Standard Time, Pacific Standard Time (Mexico), Pacific Standard Time, US Mountain
                                       Standard Time, Mountain Standard Time (Mexico), Mountain Standard Time, Central America Standard Time, Central
                                       Standard Time, Central Standard Time (Mexico), Canada Central Standard Time, SA Pacific Standard Time, Eastern
                                       Standard Time, US Eastern Standard Time, Venezuela Standard Time, Paraguay Standard Time, Atlantic Standard Time,
                                       Central Brazilian Standard Time, SA Western Standard Time, Pacific SA Standard Time, Newfoundland Standard Time, E.
                                       South America Standard Time, Argentina Standard Time, SA Eastern Standard Time, Greenland Standard Time, Montevideo
                                       Standard Time, Bahia Standard Time, UTC-02, Mid-Atlantic Standard Time, Azores Standard Time, Cape Verde Standard
                                       Time, Morocco Standard Time, UTC, GMT Standard Time, Greenwich Standard Time, W. Europe Standard Time, Central
                                       Europe Standard Time, Romance Standard Time, Central European Standard Time, W. Central Africa Standard Time,
                                       Namibia Standard Time, Jordan Standard Time, GTB Standard Time, Middle East Standard Time, Egypt Standard Time,
                                       Syria Standard Time, E. Europe Standard Time, South Africa Standard Time, FLE Standard Time, Turkey Standard Time,
                                       Israel Standard Time, Kaliningrad Standard Time, Libya Standard Time, Arabic Standard Time, Arab Standard Time,
                                       Belarus Standard Time, Russian Standard Time, E. Africa Standard Time, Iran Standard Time, Arabian Standard Time,
                                       Azerbaijan Standard Time, Russia Time Zone 3, Mauritius Standard Time, Georgian Standard Time, Caucasus Standard
                                       Time, Afghanistan Standard Time, West Asia Standard Time, Ekaterinburg Standard Time, Pakistan Standard Time, India
                                       Standard Time, Sri Lanka Standard Time, Nepal Standard Time, Central Asia Standard Time, Bangladesh Standard Time,
                                       N. Central Asia Standard Time, Myanmar Standard Time, SE Asia Standard Time, North Asia Standard Time, China
                                       Standard Time, North Asia East Standard Time, Singapore Standard Time, W. Australia Standard Time, Taipei Standard
                                       Time, Ulaanbaatar Standard Time, Tokyo Standard Time, Korea Standard Time, Yakutsk Standard Time, Cen. Australia
                                       Standard Time, AUS Central Standard Time, E. Australia Standard Time, AUS Eastern Standard Time, West Pacific
                                       Standard Time, Tasmania Standard Time, Magadan Standard Time, Vladivostok Standard Time, Russia Time Zone 10,
                                       Central Pacific Standard Time, Russia Time Zone 11, New Zealand Standard Time, UTC+12, Fiji Standard Time, Kamchatka
                                       Standard Time, Tonga Standard Time, Samoa Standard Time, Line Islands Standard Time"
                                required: True
                            days:
                                description:
                                    - the collection of days that the profile takes effect on. Possible values are Sunday through Saturday.
                                required: True
                                type: list
                            hours:
                                description:
                                    - "A collection of hours that the profile takes effect on. Values supported are 0 to 23 on the 24-hour clock (AM/PM
                                       times are not supported)."
                                required: True
                                type: list
                            minutes:
                                description:
                                    - A collection of minutes at which the profile takes effect at.
                                required: True
                                type: list
    notifications:
        description:
            - the collection of notifications.
        type: list
        suboptions:
            operation:
                description:
                    - "the operation associated with the notification and its value must be 'scale'"
                required: True
            email:
                description:
                    - the email notification.
                suboptions:
                    send_to_subscription_administrator:
                        description:
                            - a value indicating whether to send email to subscription administrator.
                    send_to_subscription_co_administrators:
                        description:
                            - a value indicating whether to send email to subscription co-administrators.
                    custom_emails:
                        description:
                            - the custom e-mails list. This value can be null or empty, in which case this attribute will be ignored.
                        type: list
            webhooks:
                description:
                    - the collection of webhook notifications.
                type: list
                suboptions:
                    service_uri:
                        description:
                            - the service address to receive the notification.
    enabled:
        description:
            - "the enabled flag. Specifies whether automatic scaling is enabled for the resource. The default value is 'true'."
    autoscale_setting_resource_name:
        description:
            - the name of the autoscale setting.
    target_resource_uri:
        description:
            - the resource identifier of the resource that the autoscale setting should be added to.
    state:
      description:
        - Assert the state of the Autoscale Setting.
        - Use 'present' to create or update an Autoscale Setting and 'absent' to delete it.
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
  - name: Create (or update) Autoscale Setting
    azure_rm_monitorautoscalesetting:
      resource_group: TestingMetricsScaleSet
      autoscale_setting_name: MySetting
      location: eastus
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: /subscriptions/b67f7fec-69fc-4974-9099-a26bd6ffeda3/resourceGroups/TestingMetricsScaleSet/providers/microsoft.insights/autoscalesettings/MySetting
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


class AzureRMAutoscaleSettings(AzureRMModuleBase):
    """Configuration class for an Azure RM Autoscale Setting resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            autoscale_setting_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            profiles=dict(
                type='list',
                required=True
            ),
            notifications=dict(
                type='list'
            ),
            enabled=dict(
                type='str'
            ),
            autoscale_setting_resource_name=dict(
                type='str'
            ),
            target_resource_uri=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.autoscale_setting_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAutoscaleSettings, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "profiles":
                    self.parameters["profiles"] = kwargs[key]
                elif key == "notifications":
                    self.parameters["notifications"] = kwargs[key]
                elif key == "enabled":
                    self.parameters["enabled"] = kwargs[key]
                elif key == "autoscale_setting_resource_name":
                    self.parameters["autoscale_setting_resource_name"] = kwargs[key]
                elif key == "target_resource_uri":
                    self.parameters["target_resource_uri"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MonitorManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_autoscalesetting()

        if not old_response:
            self.log("Autoscale Setting instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Autoscale Setting instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Autoscale Setting instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Autoscale Setting instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_autoscalesetting()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Autoscale Setting instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_autoscalesetting()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_autoscalesetting():
                time.sleep(20)
        else:
            self.log("Autoscale Setting instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_autoscalesetting(self):
        '''
        Creates or updates Autoscale Setting with the specified configuration.

        :return: deserialized Autoscale Setting instance state dictionary
        '''
        self.log("Creating / Updating the Autoscale Setting instance {0}".format(self.autoscale_setting_name))

        try:
            response = self.mgmt_client.autoscale_settings.create_or_update(resource_group_name=self.resource_group,
                                                                            autoscale_setting_name=self.autoscale_setting_name,
                                                                            parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Autoscale Setting instance.')
            self.fail("Error creating the Autoscale Setting instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_autoscalesetting(self):
        '''
        Deletes specified Autoscale Setting instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Autoscale Setting instance {0}".format(self.autoscale_setting_name))
        try:
            response = self.mgmt_client.autoscale_settings.delete(resource_group_name=self.resource_group,
                                                                  autoscale_setting_name=self.autoscale_setting_name)
        except CloudError as e:
            self.log('Error attempting to delete the Autoscale Setting instance.')
            self.fail("Error deleting the Autoscale Setting instance: {0}".format(str(e)))

        return True

    def get_autoscalesetting(self):
        '''
        Gets the properties of the specified Autoscale Setting.

        :return: deserialized Autoscale Setting instance state dictionary
        '''
        self.log("Checking if the Autoscale Setting instance {0} is present".format(self.autoscale_setting_name))
        found = False
        try:
            response = self.mgmt_client.autoscale_settings.get(resource_group_name=self.resource_group,
                                                               autoscale_setting_name=self.autoscale_setting_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Autoscale Setting instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Autoscale Setting instance.')
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
    AzureRMAutoscaleSettings()


if __name__ == '__main__':
    main()

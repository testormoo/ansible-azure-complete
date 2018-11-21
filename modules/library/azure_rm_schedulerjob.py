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
module: azure_rm_schedulerjob
version_added: "2.8"
short_description: Manage Job instance.
description:
    - Create, update and delete instance of Job.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    job_collection_name:
        description:
            - The job collection name.
        required: True
    name:
        description:
            - The job name.
        required: True
    start_time:
        description:
            - Gets or sets the job start time.
    action:
        description:
            - Gets or sets the job action.
        suboptions:
            type:
                description:
                    - Gets or sets the job action type.
                choices:
                    - 'http'
                    - 'https'
                    - 'storage_queue'
                    - 'service_bus_queue'
                    - 'service_bus_topic'
            request:
                description:
                    - Gets or sets the C(http) requests.
                suboptions:
                    authentication:
                        description:
                            - Gets or sets the authentication I(method) of the request.
                        suboptions:
                            type:
                                description:
                                    - Constant filled by server.
                                    - Required when C(state) is I(present).
                    uri:
                        description:
                            - Gets or sets the URI of the request.
                    method:
                        description:
                            - Gets or sets the method of the request.
                    body:
                        description:
                            - Gets or sets the request body.
                    headers:
                        description:
                            - Gets or sets the headers.
            queue_message:
                description:
                    - Gets or sets the storage queue message.
                suboptions:
                    storage_account:
                        description:
                            - Gets or sets the storage account name.
                    queue_name:
                        description:
                            - Gets or sets the queue name.
                    sas_token:
                        description:
                            - Gets or sets the SAS key.
                    message:
                        description:
                            - Gets or sets the message.
            service_bus_queue_message:
                description:
                    - Gets or sets the service bus queue message.
                suboptions:
                    authentication:
                        description:
                            - Gets or sets the Service Bus authentication.
                        suboptions:
                            sas_key:
                                description:
                                    - Gets or sets the SAS key.
                            sas_key_name:
                                description:
                                    - Gets or sets the SAS key name.
                            type:
                                description:
                                    - Gets or sets the authentication type.
                                choices:
                                    - 'not_specified'
                                    - 'shared_access_key'
                    brokered_message_properties:
                        description:
                            - Gets or sets the brokered I(message) properties.
                        suboptions:
                            content_type:
                                description:
                                    - Gets or sets the content type.
                            correlation_id:
                                description:
                                    - Gets or sets the correlation ID.
                            force_persistence:
                                description:
                                    - Gets or sets the force persistence.
                            label:
                                description:
                                    - Gets or sets the label.
                            message_id:
                                description:
                                    - Gets or sets the message ID.
                            partition_key:
                                description:
                                    - Gets or sets the partition key.
                            reply_to:
                                description:
                                    - Gets or sets the reply I(to).
                            reply_to_session_id:
                                description:
                                    - Gets or sets the reply I(to) session ID.
                            scheduled_enqueue_time_utc:
                                description:
                                    - Gets or sets the scheduled enqueue time UTC.
                            session_id:
                                description:
                                    - Gets or sets the session ID.
                            time_to_live:
                                description:
                                    - Gets or sets the time I(to) live.
                            to:
                                description:
                                    - Gets or sets the to.
                            via_partition_key:
                                description:
                                    - Gets or sets the via partition key.
                    custom_message_properties:
                        description:
                            - Gets or sets the custom I(message) properties.
                    message:
                        description:
                            - Gets or sets the message.
                    namespace:
                        description:
                            - Gets or sets the namespace.
                    transport_type:
                        description:
                            - Gets or sets the transport type.
                        choices:
                            - 'not_specified'
                            - 'net_messaging'
                            - 'amqp'
                    queue_name:
                        description:
                            - Gets or sets the queue name.
            service_bus_topic_message:
                description:
                    - Gets or sets the service bus topic message.
                suboptions:
                    authentication:
                        description:
                            - Gets or sets the Service Bus authentication.
                        suboptions:
                            sas_key:
                                description:
                                    - Gets or sets the SAS key.
                            sas_key_name:
                                description:
                                    - Gets or sets the SAS key name.
                            type:
                                description:
                                    - Gets or sets the authentication type.
                                choices:
                                    - 'not_specified'
                                    - 'shared_access_key'
                    brokered_message_properties:
                        description:
                            - Gets or sets the brokered I(message) properties.
                        suboptions:
                            content_type:
                                description:
                                    - Gets or sets the content type.
                            correlation_id:
                                description:
                                    - Gets or sets the correlation ID.
                            force_persistence:
                                description:
                                    - Gets or sets the force persistence.
                            label:
                                description:
                                    - Gets or sets the label.
                            message_id:
                                description:
                                    - Gets or sets the message ID.
                            partition_key:
                                description:
                                    - Gets or sets the partition key.
                            reply_to:
                                description:
                                    - Gets or sets the reply I(to).
                            reply_to_session_id:
                                description:
                                    - Gets or sets the reply I(to) session ID.
                            scheduled_enqueue_time_utc:
                                description:
                                    - Gets or sets the scheduled enqueue time UTC.
                            session_id:
                                description:
                                    - Gets or sets the session ID.
                            time_to_live:
                                description:
                                    - Gets or sets the time I(to) live.
                            to:
                                description:
                                    - Gets or sets the to.
                            via_partition_key:
                                description:
                                    - Gets or sets the via partition key.
                    custom_message_properties:
                        description:
                            - Gets or sets the custom I(message) properties.
                    message:
                        description:
                            - Gets or sets the message.
                    namespace:
                        description:
                            - Gets or sets the namespace.
                    transport_type:
                        description:
                            - Gets or sets the transport type.
                        choices:
                            - 'not_specified'
                            - 'net_messaging'
                            - 'amqp'
                    topic_path:
                        description:
                            - Gets or sets the topic path.
            retry_policy:
                description:
                    - Gets or sets the retry policy.
                suboptions:
                    retry_type:
                        description:
                            - Gets or sets the retry strategy to be used.
                        choices:
                            - 'none'
                            - 'fixed'
                    retry_interval:
                        description:
                            - Gets or sets the retry interval between retries, specify duration in ISO 8601 format.
                    retry_count:
                        description:
                            - Gets or sets the number of times a retry should be attempted.
            error_action:
                description:
                    - Gets or sets the error action.
                suboptions:
                    type:
                        description:
                            - Gets or sets the job error action type.
                        choices:
                            - 'http'
                            - 'https'
                            - 'storage_queue'
                            - 'service_bus_queue'
                            - 'service_bus_topic'
                    request:
                        description:
                            - Gets or sets the C(http) requests.
                        suboptions:
                            authentication:
                                description:
                                    - Gets or sets the authentication I(method) of the request.
                                suboptions:
                                    type:
                                        description:
                                            - Constant filled by server.
                                            - Required when C(state) is I(present).
                            uri:
                                description:
                                    - Gets or sets the URI of the request.
                            method:
                                description:
                                    - Gets or sets the method of the request.
                            body:
                                description:
                                    - Gets or sets the request body.
                            headers:
                                description:
                                    - Gets or sets the headers.
                    queue_message:
                        description:
                            - Gets or sets the storage queue message.
                        suboptions:
                            storage_account:
                                description:
                                    - Gets or sets the storage account name.
                            queue_name:
                                description:
                                    - Gets or sets the queue name.
                            sas_token:
                                description:
                                    - Gets or sets the SAS key.
                            message:
                                description:
                                    - Gets or sets the message.
                    service_bus_queue_message:
                        description:
                            - Gets or sets the service bus queue message.
                        suboptions:
                            authentication:
                                description:
                                    - Gets or sets the Service Bus authentication.
                                suboptions:
                                    sas_key:
                                        description:
                                            - Gets or sets the SAS key.
                                    sas_key_name:
                                        description:
                                            - Gets or sets the SAS key name.
                                    type:
                                        description:
                                            - Gets or sets the authentication type.
                                        choices:
                                            - 'not_specified'
                                            - 'shared_access_key'
                            brokered_message_properties:
                                description:
                                    - Gets or sets the brokered I(message) properties.
                                suboptions:
                                    content_type:
                                        description:
                                            - Gets or sets the content type.
                                    correlation_id:
                                        description:
                                            - Gets or sets the correlation ID.
                                    force_persistence:
                                        description:
                                            - Gets or sets the force persistence.
                                    label:
                                        description:
                                            - Gets or sets the label.
                                    message_id:
                                        description:
                                            - Gets or sets the message ID.
                                    partition_key:
                                        description:
                                            - Gets or sets the partition key.
                                    reply_to:
                                        description:
                                            - Gets or sets the reply I(to).
                                    reply_to_session_id:
                                        description:
                                            - Gets or sets the reply I(to) session ID.
                                    scheduled_enqueue_time_utc:
                                        description:
                                            - Gets or sets the scheduled enqueue time UTC.
                                    session_id:
                                        description:
                                            - Gets or sets the session ID.
                                    time_to_live:
                                        description:
                                            - Gets or sets the time I(to) live.
                                    to:
                                        description:
                                            - Gets or sets the to.
                                    via_partition_key:
                                        description:
                                            - Gets or sets the via partition key.
                            custom_message_properties:
                                description:
                                    - Gets or sets the custom I(message) properties.
                            message:
                                description:
                                    - Gets or sets the message.
                            namespace:
                                description:
                                    - Gets or sets the namespace.
                            transport_type:
                                description:
                                    - Gets or sets the transport type.
                                choices:
                                    - 'not_specified'
                                    - 'net_messaging'
                                    - 'amqp'
                            queue_name:
                                description:
                                    - Gets or sets the queue name.
                    service_bus_topic_message:
                        description:
                            - Gets or sets the service bus topic message.
                        suboptions:
                            authentication:
                                description:
                                    - Gets or sets the Service Bus authentication.
                                suboptions:
                                    sas_key:
                                        description:
                                            - Gets or sets the SAS key.
                                    sas_key_name:
                                        description:
                                            - Gets or sets the SAS key name.
                                    type:
                                        description:
                                            - Gets or sets the authentication type.
                                        choices:
                                            - 'not_specified'
                                            - 'shared_access_key'
                            brokered_message_properties:
                                description:
                                    - Gets or sets the brokered I(message) properties.
                                suboptions:
                                    content_type:
                                        description:
                                            - Gets or sets the content type.
                                    correlation_id:
                                        description:
                                            - Gets or sets the correlation ID.
                                    force_persistence:
                                        description:
                                            - Gets or sets the force persistence.
                                    label:
                                        description:
                                            - Gets or sets the label.
                                    message_id:
                                        description:
                                            - Gets or sets the message ID.
                                    partition_key:
                                        description:
                                            - Gets or sets the partition key.
                                    reply_to:
                                        description:
                                            - Gets or sets the reply I(to).
                                    reply_to_session_id:
                                        description:
                                            - Gets or sets the reply I(to) session ID.
                                    scheduled_enqueue_time_utc:
                                        description:
                                            - Gets or sets the scheduled enqueue time UTC.
                                    session_id:
                                        description:
                                            - Gets or sets the session ID.
                                    time_to_live:
                                        description:
                                            - Gets or sets the time I(to) live.
                                    to:
                                        description:
                                            - Gets or sets the to.
                                    via_partition_key:
                                        description:
                                            - Gets or sets the via partition key.
                            custom_message_properties:
                                description:
                                    - Gets or sets the custom I(message) properties.
                            message:
                                description:
                                    - Gets or sets the message.
                            namespace:
                                description:
                                    - Gets or sets the namespace.
                            transport_type:
                                description:
                                    - Gets or sets the transport type.
                                choices:
                                    - 'not_specified'
                                    - 'net_messaging'
                                    - 'amqp'
                            topic_path:
                                description:
                                    - Gets or sets the topic path.
                    retry_policy:
                        description:
                            - Gets or sets the retry policy.
                        suboptions:
                            retry_type:
                                description:
                                    - Gets or sets the retry strategy to be used.
                                choices:
                                    - 'none'
                                    - 'fixed'
                            retry_interval:
                                description:
                                    - Gets or sets the retry interval between retries, specify duration in ISO 8601 format.
                            retry_count:
                                description:
                                    - Gets or sets the number of times a retry should be attempted.
    recurrence:
        description:
            - Gets or sets the job recurrence.
        suboptions:
            frequency:
                description:
                    - Gets or sets the frequency of recurrence (second, C(minute), C(hour), C(day), C(week), C(month)).
                choices:
                    - 'minute'
                    - 'hour'
                    - 'day'
                    - 'week'
                    - 'month'
            interval:
                description:
                    - Gets or sets the interval between retries.
            count:
                description:
                    - Gets or sets the maximum number of times that the job should run.
            end_time:
                description:
                    - Gets or sets the time at which the job will complete.
            schedule:
                description:
                suboptions:
                    week_days:
                        description:
                            - Gets or sets the days of the week that the job should execute on.
                        type: list
                    hours:
                        description:
                            - Gets or sets the hours of the day that the job should execute at.
                        type: list
                    minutes:
                        description:
                            - Gets or sets the minutes of the hour that the job should execute at.
                        type: list
                    month_days:
                        description:
                            - Gets or sets the days of the month that the job should execute on. Must be between 1 and 31.
                        type: list
                    monthly_occurrences:
                        description:
                            - Gets or sets the occurrences of days within a month.
                        type: list
                        suboptions:
                            day:
                                description:
                                    - Gets or sets the day. Must be one of C(monday), C(tuesday), C(wednesday), C(thursday), C(friday), C(saturday), C(sunday).
                                choices:
                                    - 'monday'
                                    - 'tuesday'
                                    - 'wednesday'
                                    - 'thursday'
                                    - 'friday'
                                    - 'saturday'
                                    - 'sunday'
                            occurrence:
                                description:
                                    - Gets or sets the occurrence. Must be between -5 and 5.
    state:
        description:
            - Gets or set the job state.
        choices:
            - 'enabled'
            - 'disabled'
            - 'faulted'
            - 'completed'
    state:
      description:
        - Assert the state of the Job.
        - Use 'present' to create or update an Job and 'absent' to delete it.
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
  - name: Create (or update) Job
    azure_rm_schedulerjob:
      resource_group: NOT FOUND
      job_collection_name: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Gets the job resource identifier.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.scheduler import SchedulerManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMJobs(AzureRMModuleBase):
    """Configuration class for an Azure RM Job resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            job_collection_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            start_time=dict(
                type='datetime'
            ),
            action=dict(
                type='dict'
            ),
            recurrence=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                choices=['enabled',
                         'disabled',
                         'faulted',
                         'completed']
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.job_collection_name = None
        self.name = None
        self.properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobs, self).__init__(derived_arg_spec=self.module_arg_spec,
                                          supports_check_mode=True,
                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "start_time":
                    self.properties["start_time"] = kwargs[key]
                elif key == "action":
                    ev = kwargs[key]
                    if 'type' in ev:
                        if ev['type'] == 'http':
                            ev['type'] = 'Http'
                        elif ev['type'] == 'https':
                            ev['type'] = 'Https'
                        elif ev['type'] == 'storage_queue':
                            ev['type'] = 'StorageQueue'
                        elif ev['type'] == 'service_bus_queue':
                            ev['type'] = 'ServiceBusQueue'
                        elif ev['type'] == 'service_bus_topic':
                            ev['type'] = 'ServiceBusTopic'
                    self.properties["action"] = ev
                elif key == "recurrence":
                    ev = kwargs[key]
                    if 'frequency' in ev:
                        if ev['frequency'] == 'minute':
                            ev['frequency'] = 'Minute'
                        elif ev['frequency'] == 'hour':
                            ev['frequency'] = 'Hour'
                        elif ev['frequency'] == 'day':
                            ev['frequency'] = 'Day'
                        elif ev['frequency'] == 'week':
                            ev['frequency'] = 'Week'
                        elif ev['frequency'] == 'month':
                            ev['frequency'] = 'Month'
                    self.properties["recurrence"] = ev
                elif key == "state":
                    self.properties["state"] = _snake_to_camel(kwargs[key], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SchedulerManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_job()

        if not old_response:
            self.log("Job instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_job()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_job()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_job():
                time.sleep(20)
        else:
            self.log("Job instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_job(self):
        '''
        Creates or updates Job with the specified configuration.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Creating / Updating the Job instance {0}".format(self.name))

        try:
            response = self.mgmt_client.jobs.create_or_update(resource_group_name=self.resource_group,
                                                              job_collection_name=self.job_collection_name,
                                                              job_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job instance.')
            self.fail("Error creating the Job instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_job(self):
        '''
        Deletes specified Job instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job instance {0}".format(self.name))
        try:
            response = self.mgmt_client.jobs.delete(resource_group_name=self.resource_group,
                                                    job_collection_name=self.job_collection_name,
                                                    job_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Job instance.')
            self.fail("Error deleting the Job instance: {0}".format(str(e)))

        return True

    def get_job(self):
        '''
        Gets the properties of the specified Job.

        :return: deserialized Job instance state dictionary
        '''
        self.log("Checking if the Job instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.jobs.get(resource_group_name=self.resource_group,
                                                 job_collection_name=self.job_collection_name,
                                                 job_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job instance.')
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


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMJobs()


if __name__ == '__main__':
    main()
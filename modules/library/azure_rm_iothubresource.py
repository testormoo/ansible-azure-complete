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
module: azure_rm_iothubresource
version_added: "2.8"
short_description: Manage Iot Hub Resource instance.
description:
    - Create, update and delete instance of Iot Hub Resource.

options:
    resource_group:
        description:
            - The name of the resource group that contains the IoT hub.
        required: True
    name:
        description:
            - The name of the IoT hub.
        required: True
    iot_hub_description:
        description:
            - The IoT hub metadata and security metadata.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
                    - Required when C(state) is I(present).
            authorization_policies:
                description:
                    - The shared access policies you can use to secure a connection to the IoT hub.
                type: list
                suboptions:
                    key_name:
                        description:
                            - The name of the shared access policy.
                            - Required when C(state) is I(present).
                    primary_key:
                        description:
                            - The primary key.
                    secondary_key:
                        description:
                            - The secondary key.
                    rights:
                        description:
                            - The permissions assigned to the shared access policy.
                            - Required when C(state) is I(present).
                        choices:
                            - 'registry_read'
                            - 'registry_write'
                            - 'service_connect'
                            - 'device_connect'
                            - 'registry_read, _registry_write'
                            - 'registry_read, _service_connect'
                            - 'registry_read, _device_connect'
                            - 'registry_write, _service_connect'
                            - 'registry_write, _device_connect'
                            - 'service_connect, _device_connect'
                            - 'registry_read, _registry_write, _service_connect'
                            - 'registry_read, _registry_write, _device_connect'
                            - 'registry_read, _service_connect, _device_connect'
                            - 'registry_write, _service_connect, _device_connect'
                            - 'registry_read, _registry_write, _service_connect, _device_connect'
            ip_filter_rules:
                description:
                    - The IP filter rules.
                type: list
                suboptions:
                    filter_name:
                        description:
                            - The name of the IP filter rule.
                            - Required when C(state) is I(present).
                    action:
                        description:
                            - The desired action for requests captured by this rule.
                            - Required when C(state) is I(present).
                        choices:
                            - 'accept'
                            - 'reject'
                    ip_mask:
                        description:
                            - A string that contains the IP address range in CIDR notation for the rule.
                            - Required when C(state) is I(present).
            event_hub_endpoints:
                description:
                    - "The Event Hub-compatible endpoint properties. The possible keys to this dictionary are events and operationsMonitoringEvents. Both of
                       these keys have to be present in the dictionary while making create or update calls for the IoT hub."
            routing:
                description:
                suboptions:
                    endpoints:
                        description:
                        suboptions:
                            service_bus_queues:
                                description:
                                    - The list of Service Bus queue endpoints that IoT hub routes the messages to, based on the routing rules.
                                type: list
                                suboptions:
                                    connection_string:
                                        description:
                                            - The connection string of the service bus queue endpoint.
                                            - Required when C(state) is I(present).
                                    name:
                                        description:
                                            - "The name that identifies this endpoint. The name can only include alphanumeric characters, periods,
                                               underscores, hyphens and has a maximum length of 64 characters. The following names are reserved:  events,
                                               operationsMonitoringEvents, fileNotifications, $default. Endpoint names must be unique across endpoint
                                               types. The name need not be the same as the actual queue name."
                                            - Required when C(state) is I(present).
                                    subscription_id:
                                        description:
                                            - The subscription identifier of the service bus queue endpoint.
                                    resource_group:
                                        description:
                                            - The name of the resource group of the service bus queue endpoint.
                            service_bus_topics:
                                description:
                                    - The list of Service Bus topic endpoints that the IoT hub routes the messages to, based on the routing rules.
                                type: list
                                suboptions:
                                    connection_string:
                                        description:
                                            - The connection string of the service bus topic endpoint.
                                            - Required when C(state) is I(present).
                                    name:
                                        description:
                                            - "The name that identifies this endpoint. The name can only include alphanumeric characters, periods,
                                               underscores, hyphens and has a maximum length of 64 characters. The following names are reserved:  events,
                                               operationsMonitoringEvents, fileNotifications, $default. Endpoint names must be unique across endpoint
                                               types.  The name need not be the same as the actual topic name."
                                            - Required when C(state) is I(present).
                                    subscription_id:
                                        description:
                                            - The subscription identifier of the service bus topic endpoint.
                                    resource_group:
                                        description:
                                            - The name of the resource group of the service bus topic endpoint.
                            event_hubs:
                                description:
                                    - "The list of Event Hubs endpoints that IoT hub routes messages to, based on the routing rules. This list does not
                                       include the built-in Event Hubs endpoint."
                                type: list
                                suboptions:
                                    connection_string:
                                        description:
                                            - The connection string of the event hub endpoint.
                                            - Required when C(state) is I(present).
                                    name:
                                        description:
                                            - "The name that identifies this endpoint. The name can only include alphanumeric characters, periods,
                                               underscores, hyphens and has a maximum length of 64 characters. The following names are reserved:  events,
                                               operationsMonitoringEvents, fileNotifications, $default. Endpoint names must be unique across endpoint
                                               types."
                                            - Required when C(state) is I(present).
                                    subscription_id:
                                        description:
                                            - The subscription identifier of the event hub endpoint.
                                    resource_group:
                                        description:
                                            - The name of the resource group of the event hub endpoint.
                            storage_containers:
                                description:
                                    - The list of storage container endpoints that IoT hub routes messages to, based on the routing rules.
                                type: list
                                suboptions:
                                    connection_string:
                                        description:
                                            - The connection string of the storage account.
                                            - Required when C(state) is I(present).
                                    name:
                                        description:
                                            - "The name that identifies this endpoint. The name can only include alphanumeric characters, periods,
                                               underscores, hyphens and has a maximum length of 64 characters. The following names are reserved:  events,
                                               operationsMonitoringEvents, fileNotifications, $default. Endpoint names must be unique across endpoint
                                               types."
                                            - Required when C(state) is I(present).
                                    subscription_id:
                                        description:
                                            - The subscription identifier of the storage account.
                                    resource_group:
                                        description:
                                            - The name of the resource group of the storage account.
                                    container_name:
                                        description:
                                            - The name of storage container in the storage account.
                                            - Required when C(state) is I(present).
                                    file_name_format:
                                        description:
                                            - "File name format for the blob. Default format is {iothub}/{partition}/{YYYY}/{MM}/{DD}/{HH}/{mm}. All
                                               parameters are mandatory but can be reordered."
                                    batch_frequency_in_seconds:
                                        description:
                                            - "Time interval at which blobs are written to storage. Value should be between 60 and 720 seconds. Default
                                               value is 300 seconds."
                                    max_chunk_size_in_bytes:
                                        description:
                                            - "Maximum number of bytes for each blob written to storage. Value should be between 10485760(10MB) and
                                               524288000(500MB). Default value is 314572800(300MB)."
                                    encoding:
                                        description:
                                            - "Encoding that is used to serialize messages to blobs. Supported values are 'avro' and 'avrodeflate'. Default
                                               value is 'avro'."
                    routes:
                        description:
                            - "The list of user-provided routing rules that the IoT hub uses to route messages to built-in and custom I(endpoints). A
                               maximum of 100 routing rules are allowed for paid hubs and a maximum of 5 routing rules are allowed for free hubs."
                        type: list
                        suboptions:
                            name:
                                description:
                                    - "The name of the route. The name can only include alphanumeric characters, periods, underscores, hyphens, has a
                                       maximum length of 64 characters, and must be unique."
                                    - Required when C(state) is I(present).
                            source:
                                description:
                                    - The source that the routing rule is to be applied to, such as C(device_messages).
                                    - Required when C(state) is I(present).
                                choices:
                                    - 'invalid'
                                    - 'device_messages'
                                    - 'twin_change_events'
                                    - 'device_lifecycle_events'
                                    - 'device_job_lifecycle_events'
                            condition:
                                description:
                                    - "The condition that is evaluated to apply the routing rule. If no condition is provided, it evaluates to true by
                                       default. For grammar, see: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language"
                            endpoint_names:
                                description:
                                    - The list of endpoints to which messages that satisfy the I(condition) are routed. Currently only one endpoint is allowed.
                                    - Required when C(state) is I(present).
                                type: list
                            is_enabled:
                                description:
                                    - Used to specify whether a route is enabled.
                                    - Required when C(state) is I(present).
                    fallback_route:
                        description:
                            - "The properties of the route that is used as a fall-back route when none of the conditions specified in the 'I(routes)'
                               section are met. This is an optional parameter. When this property is not set, the messages which do not meet any of the
                               conditions specified in the 'I(routes)' section get routed to the built-in eventhub endpoint."
                        suboptions:
                            name:
                                description:
                                    - "The name of the route. The name can only include alphanumeric characters, periods, underscores, hyphens, has a
                                       maximum length of 64 characters, and must be unique."
                            source:
                                description:
                                    - The source to which the routing rule is to be applied to. For example, DeviceMessages
                                    - Required when C(state) is I(present).
                            condition:
                                description:
                                    - "The condition which is evaluated in order to apply the fallback route. If the condition is not provided it will
                                       evaluate to true by default. For grammar, See:
                                       https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language"
                            endpoint_names:
                                description:
                                    - "The list of endpoints to which the messages that satisfy the I(condition) are routed to. Currently only 1 endpoint is
                                       allowed."
                                    - Required when C(state) is I(present).
                                type: list
                            is_enabled:
                                description:
                                    - Used to specify whether the fallback route is enabled.
                                    - Required when C(state) is I(present).
            storage_endpoints:
                description:
                    - "The list of Azure Storage endpoints where you can upload files. Currently you can configure only one Azure Storage account and that
                       MUST have its key as $default. Specifying more than one storage account causes an error to be thrown. Not specifying a value for
                       this property when the I(enable_file_upload_notifications) property is set to True, causes an error to be thrown."
            messaging_endpoints:
                description:
                    - The messaging endpoint properties for the file upload notification queue.
            enable_file_upload_notifications:
                description:
                    - If True, file upload notifications are enabled.
            cloud_to_device:
                description:
                suboptions:
                    max_delivery_count:
                        description:
                            - "The max delivery count for cloud-to-device messages in the device queue. See:
                               https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages."
                    default_ttl_as_iso8601:
                        description:
                            - "The default time to live for cloud-to-device messages in the device queue. See:
                               https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages."
                    feedback:
                        description:
                        suboptions:
                            lock_duration_as_iso8601:
                                description:
                                    - "The lock duration for the feedback queue. See:
                                       https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages."
                            ttl_as_iso8601:
                                description:
                                    - "The period of time for which a message is available to consume before it is expired by the IoT hub. See:
                                       https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages."
                            max_delivery_count:
                                description:
                                    - "The number of times the IoT hub attempts to deliver a message on the feedback queue. See:
                                       https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages."
            comments:
                description:
                    - IoT hub comments.
            operations_monitoring_properties:
                description:
                suboptions:
                    events:
                        description:
            features:
                description:
                    - The capabilities and features enabled for the IoT hub.
                choices:
                    - 'none'
                    - 'device_management'
            sku:
                description:
                    - IotHub SKU info
                    - Required when C(state) is I(present).
                suboptions:
                    name:
                        description:
                            - The name of the SKU.
                            - Required when C(state) is I(present).
                        choices:
                            - 'f1'
                            - 's1'
                            - 's2'
                            - 's3'
                            - 'b1'
                            - 'b2'
                            - 'b3'
                    capacity:
                        description:
                            - "The number of provisioned IoT Hub units. See:
                               https://docs.microsoft.com/azure/azure-subscription-service-limits#iot-hub-limits."
    if_match:
        description:
            - ETag of the IoT Hub. Do not specify for creating a brand new IoT Hub. Required to update an existing IoT Hub.
    state:
      description:
        - Assert the state of the Iot Hub Resource.
        - Use 'present' to create or update an Iot Hub Resource and 'absent' to delete it.
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
  - name: Create (or update) Iot Hub Resource
    azure_rm_iothubresource:
      resource_group: myResourceGroup
      name: testHub
      iot_hub_description:
        location: centraluseuap
        event_hub_endpoints: {
  "events": {
    "retentionTimeInDays": "1",
    "partitionCount": "2",
    "partitionIds": [
      "0",
      "1"
    ],
    "path": "iot-dps-cit-hub-1",
    "endpoint": "sb://iothub-ns-iot-dps-ci-245306-76aca8e13b.servicebus.windows.net/"
  },
  "operationsMonitoringEvents": {
    "retentionTimeInDays": "1",
    "partitionCount": "2",
    "partitionIds": [
      "0",
      "1"
    ],
    "path": "iot-dps-cit-hub-1-operationmonitoring",
    "endpoint": "sb://iothub-ns-iot-dps-ci-245306-76aca8e13b.servicebus.windows.net/"
  }
}
        routing:
          fallback_route:
            name: $fallback
            source: DeviceMessages
            condition: true
            endpoint_names:
              - [
  "events"
]
            is_enabled: True
        storage_endpoints: {
  "$default": {
    "sasTtlAsIso8601": "PT1H",
    "connectionString": "",
    "containerName": ""
  }
}
        messaging_endpoints: {
  "fileNotifications": {
    "lockDurationAsIso8601": "PT1M",
    "ttlAsIso8601": "PT1H",
    "maxDeliveryCount": "10"
  }
}
        enable_file_upload_notifications: False
        cloud_to_device:
          max_delivery_count: 10
          default_ttl_as_iso8601: PT1H
          feedback:
            lock_duration_as_iso8601: PT1M
            ttl_as_iso8601: PT1H
            max_delivery_count: 10
        operations_monitoring_properties:
          events: {
  "None": "None",
  "Connections": "None",
  "DeviceTelemetry": "None",
  "C2DCommands": "None",
  "DeviceIdentityOperations": "None",
  "FileUploadOperations": "None",
  "Routes": "None"
}
        features: None
        sku:
          name: S1
          capacity: 1
      if_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - The resource identifier.
    returned: always
    type: str
    sample: /subscriptions/ae24ff83-d2ca-4fc8-9717-05dae4bba489/resourceGroups/myResourceGroup/providers/Microsoft.Devices/IotHubs/testHub
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.iothub import IotHubClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIotHubResource(AzureRMModuleBase):
    """Configuration class for an Azure RM Iot Hub Resource resource"""

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
            iot_hub_description=dict(
                type='dict',
                required=True
            ),
            if_match=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.iot_hub_description = dict()
        self.if_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIotHubResource, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.iot_hub_description["location"] = kwargs[key]
                elif key == "authorization_policies":
                    ev = kwargs[key]
                    if 'rights' in ev:
                        if ev['rights'] == 'registry_read':
                            ev['rights'] = 'RegistryRead'
                        elif ev['rights'] == 'registry_write':
                            ev['rights'] = 'RegistryWrite'
                        elif ev['rights'] == 'service_connect':
                            ev['rights'] = 'ServiceConnect'
                        elif ev['rights'] == 'device_connect':
                            ev['rights'] = 'DeviceConnect'
                        elif ev['rights'] == 'registry_read, _registry_write':
                            ev['rights'] = 'RegistryRead, RegistryWrite'
                        elif ev['rights'] == 'registry_read, _service_connect':
                            ev['rights'] = 'RegistryRead, ServiceConnect'
                        elif ev['rights'] == 'registry_read, _device_connect':
                            ev['rights'] = 'RegistryRead, DeviceConnect'
                        elif ev['rights'] == 'registry_write, _service_connect':
                            ev['rights'] = 'RegistryWrite, ServiceConnect'
                        elif ev['rights'] == 'registry_write, _device_connect':
                            ev['rights'] = 'RegistryWrite, DeviceConnect'
                        elif ev['rights'] == 'service_connect, _device_connect':
                            ev['rights'] = 'ServiceConnect, DeviceConnect'
                        elif ev['rights'] == 'registry_read, _registry_write, _service_connect':
                            ev['rights'] = 'RegistryRead, RegistryWrite, ServiceConnect'
                        elif ev['rights'] == 'registry_read, _registry_write, _device_connect':
                            ev['rights'] = 'RegistryRead, RegistryWrite, DeviceConnect'
                        elif ev['rights'] == 'registry_read, _service_connect, _device_connect':
                            ev['rights'] = 'RegistryRead, ServiceConnect, DeviceConnect'
                        elif ev['rights'] == 'registry_write, _service_connect, _device_connect':
                            ev['rights'] = 'RegistryWrite, ServiceConnect, DeviceConnect'
                        elif ev['rights'] == 'registry_read, _registry_write, _service_connect, _device_connect':
                            ev['rights'] = 'RegistryRead, RegistryWrite, ServiceConnect, DeviceConnect'
                    self.iot_hub_description.setdefault("properties", {})["authorization_policies"] = ev
                elif key == "ip_filter_rules":
                    ev = kwargs[key]
                    if 'action' in ev:
                        if ev['action'] == 'accept':
                            ev['action'] = 'Accept'
                        elif ev['action'] == 'reject':
                            ev['action'] = 'Reject'
                    self.iot_hub_description.setdefault("properties", {})["ip_filter_rules"] = ev
                elif key == "event_hub_endpoints":
                    self.iot_hub_description.setdefault("properties", {})["event_hub_endpoints"] = kwargs[key]
                elif key == "routing":
                    self.iot_hub_description.setdefault("properties", {})["routing"] = kwargs[key]
                elif key == "storage_endpoints":
                    self.iot_hub_description.setdefault("properties", {})["storage_endpoints"] = kwargs[key]
                elif key == "messaging_endpoints":
                    self.iot_hub_description.setdefault("properties", {})["messaging_endpoints"] = kwargs[key]
                elif key == "enable_file_upload_notifications":
                    self.iot_hub_description.setdefault("properties", {})["enable_file_upload_notifications"] = kwargs[key]
                elif key == "cloud_to_device":
                    self.iot_hub_description.setdefault("properties", {})["cloud_to_device"] = kwargs[key]
                elif key == "comments":
                    self.iot_hub_description.setdefault("properties", {})["comments"] = kwargs[key]
                elif key == "operations_monitoring_properties":
                    self.iot_hub_description.setdefault("properties", {})["operations_monitoring_properties"] = kwargs[key]
                elif key == "features":
                    self.iot_hub_description.setdefault("properties", {})["features"] = _snake_to_camel(kwargs[key], True)
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'f1':
                            ev['name'] = 'F1'
                        elif ev['name'] == 's1':
                            ev['name'] = 'S1'
                        elif ev['name'] == 's2':
                            ev['name'] = 'S2'
                        elif ev['name'] == 's3':
                            ev['name'] = 'S3'
                        elif ev['name'] == 'b1':
                            ev['name'] = 'B1'
                        elif ev['name'] == 'b2':
                            ev['name'] = 'B2'
                        elif ev['name'] == 'b3':
                            ev['name'] = 'B3'
                    self.iot_hub_description["sku"] = ev

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(IotHubClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_iothubresource()

        if not old_response:
            self.log("Iot Hub Resource instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Iot Hub Resource instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Iot Hub Resource instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_iothubresource()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Iot Hub Resource instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_iothubresource()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_iothubresource():
                time.sleep(20)
        else:
            self.log("Iot Hub Resource instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_iothubresource(self):
        '''
        Creates or updates Iot Hub Resource with the specified configuration.

        :return: deserialized Iot Hub Resource instance state dictionary
        '''
        self.log("Creating / Updating the Iot Hub Resource instance {0}".format(self.name))

        try:
            response = self.mgmt_client.iot_hub_resource.create_or_update(resource_group_name=self.resource_group,
                                                                          resource_name=self.name,
                                                                          iot_hub_description=self.iot_hub_description)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Iot Hub Resource instance.')
            self.fail("Error creating the Iot Hub Resource instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_iothubresource(self):
        '''
        Deletes specified Iot Hub Resource instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Iot Hub Resource instance {0}".format(self.name))
        try:
            response = self.mgmt_client.iot_hub_resource.delete(resource_group_name=self.resource_group,
                                                                resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Iot Hub Resource instance.')
            self.fail("Error deleting the Iot Hub Resource instance: {0}".format(str(e)))

        return True

    def get_iothubresource(self):
        '''
        Gets the properties of the specified Iot Hub Resource.

        :return: deserialized Iot Hub Resource instance state dictionary
        '''
        self.log("Checking if the Iot Hub Resource instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.iot_hub_resource.get(resource_group_name=self.resource_group,
                                                             resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Iot Hub Resource instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Iot Hub Resource instance.')
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
    AzureRMIotHubResource()


if __name__ == '__main__':
    main()

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
module: azure_rm_timeseriesinsightseventsource
version_added: "2.8"
short_description: Manage Event Source instance.
description:
    - Create, update and delete instance of Event Source.

options:
    resource_group:
        description:
            - Name of an Azure Resource group.
        required: True
    environment_name:
        description:
            - The name of the Time Series Insights environment associated with the specified resource group.
        required: True
    event_source_name:
        description:
            - Name of the event source.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    kind:
        description:
            - Constant filled by server.
        required: True
    state:
      description:
        - Assert the state of the Event Source.
        - Use 'present' to create or update an Event Source and 'absent' to delete it.
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
  - name: Create (or update) Event Source
    azure_rm_timeseriesinsightseventsource:
      resource_group: rg1
      environment_name: env1
      event_source_name: es1
      location: eastus
      kind: Microsoft.EventHub
'''

RETURN = '''
id:
    description:
        - Resource Id
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.TimeSeriesInsights/Environments/env1/eventSources/es1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.timeseriesinsights import TimeSeriesInsightsClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMEventSources(AzureRMModuleBase):
    """Configuration class for an Azure RM Event Source resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            environment_name=dict(
                type='str',
                required=True
            ),
            event_source_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            kind=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.environment_name = None
        self.event_source_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEventSources, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "kind":
                    self.parameters["kind"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(TimeSeriesInsightsClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_eventsource()

        if not old_response:
            self.log("Event Source instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Event Source instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Event Source instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Event Source instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_eventsource()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Event Source instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_eventsource()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_eventsource():
                time.sleep(20)
        else:
            self.log("Event Source instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_eventsource(self):
        '''
        Creates or updates Event Source with the specified configuration.

        :return: deserialized Event Source instance state dictionary
        '''
        self.log("Creating / Updating the Event Source instance {0}".format(self.event_source_name))

        try:
            response = self.mgmt_client.event_sources.create_or_update(resource_group_name=self.resource_group,
                                                                       environment_name=self.environment_name,
                                                                       event_source_name=self.event_source_name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Event Source instance.')
            self.fail("Error creating the Event Source instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_eventsource(self):
        '''
        Deletes specified Event Source instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Event Source instance {0}".format(self.event_source_name))
        try:
            response = self.mgmt_client.event_sources.delete(resource_group_name=self.resource_group,
                                                             environment_name=self.environment_name,
                                                             event_source_name=self.event_source_name)
        except CloudError as e:
            self.log('Error attempting to delete the Event Source instance.')
            self.fail("Error deleting the Event Source instance: {0}".format(str(e)))

        return True

    def get_eventsource(self):
        '''
        Gets the properties of the specified Event Source.

        :return: deserialized Event Source instance state dictionary
        '''
        self.log("Checking if the Event Source instance {0} is present".format(self.event_source_name))
        found = False
        try:
            response = self.mgmt_client.event_sources.get(resource_group_name=self.resource_group,
                                                          environment_name=self.environment_name,
                                                          event_source_name=self.event_source_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Event Source instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Event Source instance.')
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
    AzureRMEventSources()


if __name__ == '__main__':
    main()

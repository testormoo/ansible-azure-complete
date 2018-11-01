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
module: azure_rm_applicationinsightscomponent
version_added: "2.8"
short_description: Manage Component instance.
description:
    - Create, update and delete instance of Component.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    resource_name:
        description:
            - The name of the Application Insights component resource.
        required: True
    insight_properties:
        description:
            - Properties that need to be specified to create an Application Insights component.
        required: True
        suboptions:
            location:
                description:
                    - Resource location
                required: True
            kind:
                description:
                    - "The kind of application that this component refers to, used to customize UI. This value is a freeform string, values should typically
                       be one of the following: C(web), ios, C(other), store, java, phone."
                required: True
            application_type:
                description:
                    - Type of application being monitored.
                required: True
                choices:
                    - 'web'
                    - 'other'
            flow_type:
                description:
                    - "Used by the Application Insights system to determine what I(kind) of flow this component was created by. This is to be set to
                       'C(bluefield)' when creating/updating a component via the C(rest) API."
                choices:
                    - 'bluefield'
            request_source:
                description:
                    - "Describes what tool created this Application Insights component. Customers using this API should set this to the default 'C(rest)'."
                choices:
                    - 'rest'
            hockey_app_id:
                description:
                    - The unique application ID created when a new application is added to HockeyApp, used for communications with HockeyApp.
            sampling_percentage:
                description:
                    - Percentage of the data produced by the application being monitored that is being sampled for Application Insights telemetry.
    state:
      description:
        - Assert the state of the Component.
        - Use 'present' to create or update an Component and 'absent' to delete it.
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
  - name: Create (or update) Component
    azure_rm_applicationinsightscomponent:
      resource_group: my-resource-group
      resource_name: my-component
      insight_properties:
        location: South Central US
        kind: web
'''

RETURN = '''
id:
    description:
        - Azure resource Id
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/my-resource-group/providers/Microsoft.Insights/components/my-component
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMComponents(AzureRMModuleBase):
    """Configuration class for an Azure RM Component resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            insight_properties=dict(
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
        self.resource_name = None
        self.insight_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMComponents, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.insight_properties["location"] = kwargs[key]
                elif key == "kind":
                    self.insight_properties["kind"] = kwargs[key]
                elif key == "application_type":
                    self.insight_properties["application_type"] = kwargs[key]
                elif key == "flow_type":
                    self.insight_properties["flow_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "request_source":
                    self.insight_properties["request_source"] = kwargs[key]
                elif key == "hockey_app_id":
                    self.insight_properties["hockey_app_id"] = kwargs[key]
                elif key == "sampling_percentage":
                    self.insight_properties["sampling_percentage"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApplicationInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_component()

        if not old_response:
            self.log("Component instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Component instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Component instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Component instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_component()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Component instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_component()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_component():
                time.sleep(20)
        else:
            self.log("Component instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_component(self):
        '''
        Creates or updates Component with the specified configuration.

        :return: deserialized Component instance state dictionary
        '''
        self.log("Creating / Updating the Component instance {0}".format(self.resource_name))

        try:
            response = self.mgmt_client.components.create_or_update(resource_group_name=self.resource_group,
                                                                    resource_name=self.resource_name,
                                                                    insight_properties=self.insight_properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Component instance.')
            self.fail("Error creating the Component instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_component(self):
        '''
        Deletes specified Component instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Component instance {0}".format(self.resource_name))
        try:
            response = self.mgmt_client.components.delete(resource_group_name=self.resource_group,
                                                          resource_name=self.resource_name)
        except CloudError as e:
            self.log('Error attempting to delete the Component instance.')
            self.fail("Error deleting the Component instance: {0}".format(str(e)))

        return True

    def get_component(self):
        '''
        Gets the properties of the specified Component.

        :return: deserialized Component instance state dictionary
        '''
        self.log("Checking if the Component instance {0} is present".format(self.resource_name))
        found = False
        try:
            response = self.mgmt_client.components.get(resource_group_name=self.resource_group,
                                                       resource_name=self.resource_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Component instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Component instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMComponents()


if __name__ == '__main__':
    main()

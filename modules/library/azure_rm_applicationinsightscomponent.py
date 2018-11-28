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
short_description: Manage Azure Component instance.
description:
    - Create, update and delete instance of Azure Component.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Application Insights component resource.
        required: True
    location:
        description:
            - Resource location
            - Required when C(state) is I(present).
    kind:
        description:
            - "The kind of application that this component refers to, used to customize UI. This value is a freeform string, values should typically be one
               of the following: C(web), ios, C(other), store, java, phone."
            - Required when C(state) is I(present).
    application_type:
        description:
            - Type of application being monitored.
            - Required when C(state) is I(present).
        choices:
            - 'web'
            - 'other'
    flow_type:
        description:
            - "Used by the Application Insights system to determine what I(kind) of flow this component was created by. This is to be set to 'C(bluefield)'
               when creating/updating a component via the C(rest) API."
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
      name: my-component
      location: South Central US
      kind: web
      application_type: web
      flow_type: Bluefield
      request_source: rest
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMComponent(AzureRMModuleBase):
    """Configuration class for an Azure RM Component resource"""

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
            kind=dict(
                type='str'
            ),
            application_type=dict(
                type='str',
                choices=['web',
                         'other']
            ),
            flow_type=dict(
                type='str',
                choices=['bluefield']
            ),
            request_source=dict(
                type='str',
                choices=['rest']
            ),
            hockey_app_id=dict(
                type='str'
            ),
            sampling_percentage=dict(
                type='float'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.insight_properties = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMComponent, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.insight_properties[key] = kwargs[key]

        dict_camelize(self.insight_properties, ['flow_type'], True)

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
                if (not default_compare(self.insight_properties, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Component instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_component()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Component instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_component()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Component instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_component(self):
        '''
        Creates or updates Component with the specified configuration.

        :return: deserialized Component instance state dictionary
        '''
        self.log("Creating / Updating the Component instance {0}".format(self.name))

        try:
            response = self.mgmt_client.components.create_or_update(resource_group_name=self.resource_group,
                                                                    resource_name=self.name,
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
        self.log("Deleting the Component instance {0}".format(self.name))
        try:
            response = self.mgmt_client.components.delete(resource_group_name=self.resource_group,
                                                          resource_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Component instance.')
            self.fail("Error deleting the Component instance: {0}".format(str(e)))

        return True

    def get_component(self):
        '''
        Gets the properties of the specified Component.

        :return: deserialized Component instance state dictionary
        '''
        self.log("Checking if the Component instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.components.get(resource_group_name=self.resource_group,
                                                       resource_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Component instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Component instance.')
        if found is True:
            return response.as_dict()

        return False


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
            result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
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


def main():
    """Main execution"""
    AzureRMComponent()


if __name__ == '__main__':
    main()

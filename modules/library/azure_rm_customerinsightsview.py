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
module: azure_rm_customerinsightsview
version_added: "2.8"
short_description: Manage Azure View instance.
description:
    - Create, update and delete instance of Azure View.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    hub_name:
        description:
            - The name of the hub.
        required: True
    name:
        description:
            - The name of the view.
        required: True
    user_id:
        description:
            - the user ID.
    display_name:
        description:
            - Localized display name for the view.
    definition:
        description:
            - View definition.
            - Required when C(state) is I(present).
    state:
      description:
        - Assert the state of the View.
        - Use 'present' to create or update an View and 'absent' to delete it.
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
  - name: Create (or update) View
    azure_rm_customerinsightsview:
      resource_group: TestHubRG
      hub_name: sdkTestHub
      name: testView
      user_id: testUser
      display_name: {
  "en": "some name"
}
      definition: {\"isProfileType\":false,\"profileTypes\":[],\"widgets\":[],\"style\":[]}
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/c909e979-ef71-4def-a970-bc7c154db8c5/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/sdkTestHub/views/testView
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.customerinsights import CustomerInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMView(AzureRMModuleBase):
    """Configuration class for an Azure RM View resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            hub_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            user_id=dict(
                type='str'
            ),
            display_name=dict(
                type='dict'
            ),
            definition=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.hub_name = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMView, self).__init__(derived_arg_spec=self.module_arg_spec,
                                          supports_check_mode=True,
                                          supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_view()

        if not old_response:
            self.log("View instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("View instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the View instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_view()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("View instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_view()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("View instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_view(self):
        '''
        Creates or updates View with the specified configuration.

        :return: deserialized View instance state dictionary
        '''
        self.log("Creating / Updating the View instance {0}".format(self.user_id))

        try:
            response = self.mgmt_client.views.create_or_update(resource_group_name=self.resource_group,
                                                               hub_name=self.hub_name,
                                                               view_name=self.name,
                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the View instance.')
            self.fail("Error creating the View instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_view(self):
        '''
        Deletes specified View instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the View instance {0}".format(self.user_id))
        try:
            response = self.mgmt_client.views.delete(resource_group_name=self.resource_group,
                                                     hub_name=self.hub_name,
                                                     view_name=self.name,
                                                     user_id=self.user_id)
        except CloudError as e:
            self.log('Error attempting to delete the View instance.')
            self.fail("Error deleting the View instance: {0}".format(str(e)))

        return True

    def get_view(self):
        '''
        Gets the properties of the specified View.

        :return: deserialized View instance state dictionary
        '''
        self.log("Checking if the View instance {0} is present".format(self.user_id))
        found = False
        try:
            response = self.mgmt_client.views.get(resource_group_name=self.resource_group,
                                                  hub_name=self.hub_name,
                                                  view_name=self.name,
                                                  user_id=self.user_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("View instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the View instance.')
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
            result['compare'] = 'changed [' + path + '] ' + new + ' != ' + old
            return False


def main():
    """Main execution"""
    AzureRMView()


if __name__ == '__main__':
    main()

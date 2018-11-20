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
module: azure_rm_customerinsightshub
version_added: "2.8"
short_description: Manage Hub instance.
description:
    - Create, update and delete instance of Hub.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the Hub.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    tenant_features:
        description:
            - "The bit flags for enabled hub features. Bit 0 is set to 1 indicates graph is enabled, or disabled if set to 0. Bit 1 is set to 1 indicates
               the hub is disabled, or enabled if set to 0."
    hub_billing_info:
        description:
            - Billing settings of the hub.
        suboptions:
            sku_name:
                description:
                    - The sku name.
            min_units:
                description:
                    - The minimum number of units will be billed. One unit is 10,000 Profiles and 100,000 Interactions.
            max_units:
                description:
                    - The maximum number of units can be used.  One unit is 10,000 Profiles and 100,000 Interactions.
    state:
      description:
        - Assert the state of the Hub.
        - Use 'present' to create or update an Hub and 'absent' to delete it.
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
  - name: Create (or update) Hub
    azure_rm_customerinsightshub:
      resource_group: TestHubRG
      name: sdkTestHub
      location: eastus
      hub_billing_info:
        sku_name: B0
        min_units: 1
        max_units: 5
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/TestHubRG/providers/Microsoft.CustomerInsights/hubs/testHub2839
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

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


class AzureRMHubs(AzureRMModuleBase):
    """Configuration class for an Azure RM Hub resource"""

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
            tenant_features=dict(
                type='int'
            ),
            hub_billing_info=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMHubs, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "tenant_features":
                    self.parameters["tenant_features"] = kwargs[key]
                elif key == "hub_billing_info":
                    self.parameters["hub_billing_info"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CustomerInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_hub()

        if not old_response:
            self.log("Hub instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Hub instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Hub instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_hub()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Hub instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_hub()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_hub():
                time.sleep(20)
        else:
            self.log("Hub instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_hub(self):
        '''
        Creates or updates Hub with the specified configuration.

        :return: deserialized Hub instance state dictionary
        '''
        self.log("Creating / Updating the Hub instance {0}".format(self.name))

        try:
            response = self.mgmt_client.hubs.create_or_update(resource_group_name=self.resource_group,
                                                              hub_name=self.name,
                                                              parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Hub instance.')
            self.fail("Error creating the Hub instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_hub(self):
        '''
        Deletes specified Hub instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Hub instance {0}".format(self.name))
        try:
            response = self.mgmt_client.hubs.delete(resource_group_name=self.resource_group,
                                                    hub_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Hub instance.')
            self.fail("Error deleting the Hub instance: {0}".format(str(e)))

        return True

    def get_hub(self):
        '''
        Gets the properties of the specified Hub.

        :return: deserialized Hub instance state dictionary
        '''
        self.log("Checking if the Hub instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.hubs.get(resource_group_name=self.resource_group,
                                                 hub_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Hub instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Hub instance.')
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
    AzureRMHubs()


if __name__ == '__main__':
    main()

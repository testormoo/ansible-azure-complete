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
module: azure_rm_dnszone
version_added: "2.8"
short_description: Manage Zone instance.
description:
    - Create, update and delete instance of Zone.

options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the DNS zone (without a terminating dot).
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    zone_type:
        description:
            - The type of this DNS zone (C(public) or C(private)).
        choices:
            - 'public'
            - 'private'
    registration_virtual_networks:
        description:
            - A list of references to virtual networks that register hostnames in this DNS zone. This is a only when I(zone_type) is C(private).
        type: list
        suboptions:
            id:
                description:
                    - Resource Id.
    resolution_virtual_networks:
        description:
            - A list of references to virtual networks that resolve records in this DNS zone. This is a only when I(zone_type) is C(private).
        type: list
        suboptions:
            id:
                description:
                    - Resource Id.
    if_match:
        description:
            - "The etag of the DNS zone. Omit this value to always overwrite the current zone. Specify the last-seen etag value to prevent accidentally
               overwritting any concurrent changes."
    if_none_match:
        description:
            - "Set to '*' to allow a new DNS zone to be created, but to prevent updating an existing zone. Other values will be ignored."
    state:
      description:
        - Assert the state of the Zone.
        - Use 'present' to create or update an Zone and 'absent' to delete it.
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
  - name: Create (or update) Zone
    azure_rm_dnszone:
      resource_group: rg1
      name: zone1
      location: eastus
      if_match: NOT FOUND
      if_none_match: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/dnsZones/zone1
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.dns import DnsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMZones(AzureRMModuleBase):
    """Configuration class for an Azure RM Zone resource"""

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
            zone_type=dict(
                type='str',
                choices=['public',
                         'private']
            ),
            registration_virtual_networks=dict(
                type='list'
            ),
            resolution_virtual_networks=dict(
                type='list'
            ),
            if_match=dict(
                type='str'
            ),
            if_none_match=dict(
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
        self.parameters = dict()
        self.if_match = None
        self.if_none_match = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMZones, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "zone_type":
                    self.parameters["zone_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "registration_virtual_networks":
                    self.parameters["registration_virtual_networks"] = kwargs[key]
                elif key == "resolution_virtual_networks":
                    self.parameters["resolution_virtual_networks"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DnsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_zone()

        if not old_response:
            self.log("Zone instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Zone instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Zone instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_zone()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Zone instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_zone()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_zone():
                time.sleep(20)
        else:
            self.log("Zone instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_zone(self):
        '''
        Creates or updates Zone with the specified configuration.

        :return: deserialized Zone instance state dictionary
        '''
        self.log("Creating / Updating the Zone instance {0}".format(self.name))

        try:
            response = self.mgmt_client.zones.create_or_update(resource_group_name=self.resource_group,
                                                               zone_name=self.name,
                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Zone instance.')
            self.fail("Error creating the Zone instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_zone(self):
        '''
        Deletes specified Zone instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Zone instance {0}".format(self.name))
        try:
            response = self.mgmt_client.zones.delete(resource_group_name=self.resource_group,
                                                     zone_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Zone instance.')
            self.fail("Error deleting the Zone instance: {0}".format(str(e)))

        return True

    def get_zone(self):
        '''
        Gets the properties of the specified Zone.

        :return: deserialized Zone instance state dictionary
        '''
        self.log("Checking if the Zone instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.zones.get(resource_group_name=self.resource_group,
                                                  zone_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Zone instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Zone instance.')
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
    AzureRMZones()


if __name__ == '__main__':
    main()

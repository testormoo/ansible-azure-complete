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
module: azure_rm_cdnprofile
version_added: "2.8"
short_description: Manage Azure Profile instance.
description:
    - Create, update and delete instance of Azure Profile.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    name:
        description:
            - Name of the CDN profile which is unique within the resource group.
        required: True
    location:
        description:
            - Resource location.
            - Required when C(state) is I(present).
    sku:
        description:
            - The pricing tier (defines a CDN provider, feature list and rate) of the CDN profile.
            - Required when C(state) is I(present).
        suboptions:
            name:
                description:
                    - Name of the pricing tier.
                choices:
                    - 'standard_verizon'
                    - 'premium_verizon'
                    - 'custom_verizon'
                    - 'standard_akamai'
                    - 'standard_china_cdn'
                    - 'standard_microsoft'
    state:
      description:
        - Assert the state of the Profile.
        - Use 'present' to create or update an Profile and 'absent' to delete it.
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
  - name: Create (or update) Profile
    azure_rm_cdnprofile:
      resource_group: RG
      name: profile1
      location: WestCentralUs
      sku:
        name: Standard_Verizon
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: id
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.cdn import CdnManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMProfile(AzureRMModuleBase):
    """Configuration class for an Azure RM Profile resource"""

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
            sku=dict(
                type='dict'
                options=dict(
                    name=dict(
                        type='str',
                        choices=['standard_verizon',
                                 'premium_verizon',
                                 'custom_verizon',
                                 'standard_akamai',
                                 'standard_china_cdn',
                                 'standard_microsoft']
                    )
                )
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.profile = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProfile, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.profile[key] = kwargs[key]

        dict_camelize(self.profile, ['sku', 'name'], True)
        dict_map(self.profile, ['sku', 'name'], {'standard_verizon': 'Standard_Verizon', 'premium_verizon': 'Premium_Verizon', 'custom_verizon': 'Custom_Verizon', 'standard_akamai': 'Standard_Akamai', 'standard_china_cdn': 'Standard_ChinaCdn', 'standard_microsoft': 'Standard_Microsoft'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CdnManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_profile()

        if not old_response:
            self.log("Profile instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Profile instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.profile, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Profile instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_profile()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Profile instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_profile()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Profile instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_profile(self):
        '''
        Creates or updates Profile with the specified configuration.

        :return: deserialized Profile instance state dictionary
        '''
        self.log("Creating / Updating the Profile instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.profiles.create(resource_group_name=self.resource_group,
                                                            profile_name=self.name,
                                                            profile=self.profile)
            else:
                response = self.mgmt_client.profiles.update(resource_group_name=self.resource_group,
                                                            profile_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Profile instance.')
            self.fail("Error creating the Profile instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_profile(self):
        '''
        Deletes specified Profile instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Profile instance {0}".format(self.name))
        try:
            response = self.mgmt_client.profiles.delete(resource_group_name=self.resource_group,
                                                        profile_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Profile instance.')
            self.fail("Error deleting the Profile instance: {0}".format(str(e)))

        return True

    def get_profile(self):
        '''
        Gets the properties of the specified Profile.

        :return: deserialized Profile instance state dictionary
        '''
        self.log("Checking if the Profile instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.profiles.get(resource_group_name=self.resource_group,
                                                     profile_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Profile instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Profile instance.')
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


def dict_map(d, path, map):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_map(d[i], path, map)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = map.get(old_value, old_value)
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_map(sd, path[1:], map)


def main():
    """Main execution"""
    AzureRMProfile()


if __name__ == '__main__':
    main()

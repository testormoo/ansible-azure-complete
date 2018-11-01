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
short_description: Manage Profile instance.
description:
    - Create, update and delete instance of Profile.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    profile_name:
        description:
            - Name of the CDN I(profile) which is unique within the resource group.
        required: True
    profile:
        description:
            - Profile properties needed to create a new profile.
        required: True
        suboptions:
            location:
                description:
                    - Resource location.
                required: True
            sku:
                description:
                    - The pricing tier (defines a CDN provider, feature list and rate) of the CDN profile.
                required: True
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
      profile_name: profile1
      profile:
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


class AzureRMProfiles(AzureRMModuleBase):
    """Configuration class for an Azure RM Profile resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            profile=dict(
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
        self.profile_name = None
        self.profile = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMProfiles, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.profile["location"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'standard_verizon':
                            ev['name'] = 'Standard_Verizon'
                        elif ev['name'] == 'premium_verizon':
                            ev['name'] = 'Premium_Verizon'
                        elif ev['name'] == 'custom_verizon':
                            ev['name'] = 'Custom_Verizon'
                        elif ev['name'] == 'standard_akamai':
                            ev['name'] = 'Standard_Akamai'
                        elif ev['name'] == 'standard_china_cdn':
                            ev['name'] = 'Standard_ChinaCdn'
                        elif ev['name'] == 'standard_microsoft':
                            ev['name'] = 'Standard_Microsoft'
                    self.profile["sku"] = ev

        old_response = None
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
                self.log("Need to check if Profile instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Profile instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_profile()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Profile instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_profile()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_profile():
                time.sleep(20)
        else:
            self.log("Profile instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_profile(self):
        '''
        Creates or updates Profile with the specified configuration.

        :return: deserialized Profile instance state dictionary
        '''
        self.log("Creating / Updating the Profile instance {0}".format(self.profile_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.profiles.create(resource_group_name=self.resource_group,
                                                            profile_name=self.profile_name,
                                                            profile=self.profile)
            else:
                response = self.mgmt_client.profiles.update(resource_group_name=self.resource_group,
                                                            profile_name=self.profile_name)
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
        self.log("Deleting the Profile instance {0}".format(self.profile_name))
        try:
            response = self.mgmt_client.profiles.delete(resource_group_name=self.resource_group,
                                                        profile_name=self.profile_name)
        except CloudError as e:
            self.log('Error attempting to delete the Profile instance.')
            self.fail("Error deleting the Profile instance: {0}".format(str(e)))

        return True

    def get_profile(self):
        '''
        Gets the properties of the specified Profile.

        :return: deserialized Profile instance state dictionary
        '''
        self.log("Checking if the Profile instance {0} is present".format(self.profile_name))
        found = False
        try:
            response = self.mgmt_client.profiles.get(resource_group_name=self.resource_group,
                                                     profile_name=self.profile_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Profile instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Profile instance.')
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
    AzureRMProfiles()


if __name__ == '__main__':
    main()

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
module: azure_rm_cdncustomdomain
version_added: "2.8"
short_description: Manage Custom Domain instance.
description:
    - Create, update and delete instance of Custom Domain.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    profile_name:
        description:
            - Name of the CDN profile which is unique within the resource group.
        required: True
    endpoint_name:
        description:
            - Name of the endpoint under the profile which is unique globally.
        required: True
    custom_domain_name:
        description:
            - Name of the custom domain within an endpoint.
        required: True
    host_name:
        description:
            - The host name of the custom domain. Must be a domain name.
        required: True
    state:
      description:
        - Assert the state of the Custom Domain.
        - Use 'present' to create or update an Custom Domain and 'absent' to delete it.
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
  - name: Create (or update) Custom Domain
    azure_rm_cdncustomdomain:
      resource_group: RG
      profile_name: profile1
      endpoint_name: endpoint1
      custom_domain_name: www-someDomain-net
      host_name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourcegroups/RG/providers/Microsoft.Cdn/profiles/profile1/endpoints/endpoint1/customdomains/www-someDomain-net
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


class AzureRMCustomDomains(AzureRMModuleBase):
    """Configuration class for an Azure RM Custom Domain resource"""

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
            endpoint_name=dict(
                type='str',
                required=True
            ),
            custom_domain_name=dict(
                type='str',
                required=True
            ),
            host_name=dict(
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
        self.profile_name = None
        self.endpoint_name = None
        self.custom_domain_name = None
        self.host_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCustomDomains, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                   supports_check_mode=True,
                                                   supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CdnManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_customdomain()

        if not old_response:
            self.log("Custom Domain instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Custom Domain instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Custom Domain instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Custom Domain instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_customdomain()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Custom Domain instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_customdomain()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_customdomain():
                time.sleep(20)
        else:
            self.log("Custom Domain instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_customdomain(self):
        '''
        Creates or updates Custom Domain with the specified configuration.

        :return: deserialized Custom Domain instance state dictionary
        '''
        self.log("Creating / Updating the Custom Domain instance {0}".format(self.custom_domain_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.custom_domains.create(resource_group_name=self.resource_group,
                                                                  profile_name=self.profile_name,
                                                                  endpoint_name=self.endpoint_name,
                                                                  custom_domain_name=self.custom_domain_name,
                                                                  host_name=self.host_name)
            else:
                response = self.mgmt_client.custom_domains.update()
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Custom Domain instance.')
            self.fail("Error creating the Custom Domain instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_customdomain(self):
        '''
        Deletes specified Custom Domain instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Custom Domain instance {0}".format(self.custom_domain_name))
        try:
            response = self.mgmt_client.custom_domains.delete(resource_group_name=self.resource_group,
                                                              profile_name=self.profile_name,
                                                              endpoint_name=self.endpoint_name,
                                                              custom_domain_name=self.custom_domain_name)
        except CloudError as e:
            self.log('Error attempting to delete the Custom Domain instance.')
            self.fail("Error deleting the Custom Domain instance: {0}".format(str(e)))

        return True

    def get_customdomain(self):
        '''
        Gets the properties of the specified Custom Domain.

        :return: deserialized Custom Domain instance state dictionary
        '''
        self.log("Checking if the Custom Domain instance {0} is present".format(self.custom_domain_name))
        found = False
        try:
            response = self.mgmt_client.custom_domains.get(resource_group_name=self.resource_group,
                                                           profile_name=self.profile_name,
                                                           endpoint_name=self.endpoint_name,
                                                           custom_domain_name=self.custom_domain_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Custom Domain instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Custom Domain instance.')
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
    AzureRMCustomDomains()


if __name__ == '__main__':
    main()

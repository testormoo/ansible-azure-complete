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
module: azure_rm_mediastreamingendpoint
version_added: "2.8"
short_description: Manage Streaming Endpoint instance.
description:
    - Create, update and delete instance of Streaming Endpoint.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    streaming_endpoint_name:
        description:
            - The name of the StreamingEndpoint.
        required: True
    auto_start:
        description:
            - The flag indicates if the resource should be automatically started on creation.
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    description:
        description:
            - The StreamingEndpoint description.
    scale_units:
        description:
            - The number of scale units.  Use the Scale operation to adjust this value.
        required: True
    availability_set_name:
        description:
            - The name of the AvailabilitySet used with this StreamingEndpoint for high availability streaming.  This value can only be set at creation time.
    access_control:
        description:
            - The access control definition of the StreamingEndpoint.
        suboptions:
            akamai:
                description:
                    - The access control of Akamai
                suboptions:
                    akamai_signature_header_authentication_key_list:
                        description:
                            - authentication key list
                        type: list
                        suboptions:
                            identifier:
                                description:
                                    - identifier of the key
                            base64_key:
                                description:
                                    - authentication key
                            expiration:
                                description:
                                    - The expiration time of the authentication key.
            ip:
                description:
                    - The IP access control of the StreamingEndpoint.
                suboptions:
                    allow:
                        description:
                            - The IP allow list.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - The friendly name for the IP I(address) range.
                            address:
                                description:
                                    - The IP address.
                            subnet_prefix_length:
                                description:
                                    - The subnet mask prefix length (see CIDR notation).
    max_cache_age:
        description:
            - Max cache age
    custom_host_names:
        description:
            - The custom host names of the StreamingEndpoint
        type: list
    cdn_enabled:
        description:
            - The CDN enabled flag.
    cdn_provider:
        description:
            - The CDN provider name.
    cdn_profile:
        description:
            - The CDN profile name.
    cross_site_access_policies:
        description:
            - The StreamingEndpoint access policies.
        suboptions:
            client_access_policy:
                description:
                    - The content of clientaccesspolicy.xml used by Silverlight.
            cross_domain_policy:
                description:
                    - The content of crossdomain.xml used by Silverlight.
    state:
      description:
        - Assert the state of the Streaming Endpoint.
        - Use 'present' to create or update an Streaming Endpoint and 'absent' to delete it.
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
  - name: Create (or update) Streaming Endpoint
    azure_rm_mediastreamingendpoint:
      resource_group: mediaresources
      account_name: slitestmedia10
      streaming_endpoint_name: myStreamingEndpoint1
      auto_start: NOT FOUND
      location: eastus
'''

RETURN = '''
id:
    description:
        - Fully qualified resource ID for the resource.
    returned: always
    type: str
    sample: "/subscriptions/0a6ec948-5a62-437d-b9df-934dc7c1b722/resourceGroups/mediaresources/providers/Microsoft.Media/mediaservices/slitestmedia10/streami
            ngendpoints/myStreamingEndpoint1"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.media import AzureMediaServices
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMStreamingEndpoints(AzureRMModuleBase):
    """Configuration class for an Azure RM Streaming Endpoint resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            account_name=dict(
                type='str',
                required=True
            ),
            streaming_endpoint_name=dict(
                type='str',
                required=True
            ),
            auto_start=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            scale_units=dict(
                type='int',
                required=True
            ),
            availability_set_name=dict(
                type='str'
            ),
            access_control=dict(
                type='dict'
            ),
            max_cache_age=dict(
                type='int'
            ),
            custom_host_names=dict(
                type='list'
            ),
            cdn_enabled=dict(
                type='str'
            ),
            cdn_provider=dict(
                type='str'
            ),
            cdn_profile=dict(
                type='str'
            ),
            cross_site_access_policies=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.account_name = None
        self.streaming_endpoint_name = None
        self.auto_start = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStreamingEndpoints, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "description":
                    self.parameters["description"] = kwargs[key]
                elif key == "scale_units":
                    self.parameters["scale_units"] = kwargs[key]
                elif key == "availability_set_name":
                    self.parameters["availability_set_name"] = kwargs[key]
                elif key == "access_control":
                    self.parameters["access_control"] = kwargs[key]
                elif key == "max_cache_age":
                    self.parameters["max_cache_age"] = kwargs[key]
                elif key == "custom_host_names":
                    self.parameters["custom_host_names"] = kwargs[key]
                elif key == "cdn_enabled":
                    self.parameters["cdn_enabled"] = kwargs[key]
                elif key == "cdn_provider":
                    self.parameters["cdn_provider"] = kwargs[key]
                elif key == "cdn_profile":
                    self.parameters["cdn_profile"] = kwargs[key]
                elif key == "cross_site_access_policies":
                    self.parameters["cross_site_access_policies"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(AzureMediaServices,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_streamingendpoint()

        if not old_response:
            self.log("Streaming Endpoint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Streaming Endpoint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Streaming Endpoint instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Streaming Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_streamingendpoint()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Streaming Endpoint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_streamingendpoint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_streamingendpoint():
                time.sleep(20)
        else:
            self.log("Streaming Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_streamingendpoint(self):
        '''
        Creates or updates Streaming Endpoint with the specified configuration.

        :return: deserialized Streaming Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Streaming Endpoint instance {0}".format(self.streaming_endpoint_name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.streaming_endpoints.create(resource_group_name=self.resource_group,
                                                                       account_name=self.account_name,
                                                                       streaming_endpoint_name=self.streaming_endpoint_name,
                                                                       parameters=self.parameters)
            else:
                response = self.mgmt_client.streaming_endpoints.update(resource_group_name=self.resource_group,
                                                                       account_name=self.account_name,
                                                                       streaming_endpoint_name=self.streaming_endpoint_name,
                                                                       parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Streaming Endpoint instance.')
            self.fail("Error creating the Streaming Endpoint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_streamingendpoint(self):
        '''
        Deletes specified Streaming Endpoint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Streaming Endpoint instance {0}".format(self.streaming_endpoint_name))
        try:
            response = self.mgmt_client.streaming_endpoints.delete(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   streaming_endpoint_name=self.streaming_endpoint_name)
        except CloudError as e:
            self.log('Error attempting to delete the Streaming Endpoint instance.')
            self.fail("Error deleting the Streaming Endpoint instance: {0}".format(str(e)))

        return True

    def get_streamingendpoint(self):
        '''
        Gets the properties of the specified Streaming Endpoint.

        :return: deserialized Streaming Endpoint instance state dictionary
        '''
        self.log("Checking if the Streaming Endpoint instance {0} is present".format(self.streaming_endpoint_name))
        found = False
        try:
            response = self.mgmt_client.streaming_endpoints.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                streaming_endpoint_name=self.streaming_endpoint_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Streaming Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Streaming Endpoint instance.')
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
    AzureRMStreamingEndpoints()


if __name__ == '__main__':
    main()

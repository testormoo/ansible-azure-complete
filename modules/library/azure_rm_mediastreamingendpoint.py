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
short_description: Manage Azure Streaming Endpoint instance.
description:
    - Create, update and delete instance of Azure Streaming Endpoint.

options:
    resource_group:
        description:
            - The name of the resource group within the Azure subscription.
        required: True
    account_name:
        description:
            - The Media Services account name.
        required: True
    name:
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
            - Required when C(state) is I(present).
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
      name: myStreamingEndpoint1
      auto_start: NOT FOUND
      location: eastus
      description: test event 1
      scale_units: 1
      availability_set_name: availableset
      access_control:
        akamai:
          akamai_signature_header_authentication_key_list:
            - identifier: id1
              base64_key: dGVzdGlkMQ==
              expiration: 2030-01-01T00:00:00+00:00
        ip:
          allow:
            - name: AllowedIp
              address: 192.168.1.1
      cdn_enabled: False
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
from ansible.module_utils.common.dict_transformations import _snake_to_camel

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


class AzureRMStreamingEndpoint(AzureRMModuleBase):
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
            name=dict(
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
                type='int'
            ),
            availability_set_name=dict(
                type='str'
            ),
            access_control=dict(
                type='dict',
                options=dict(
                    akamai=dict(
                        type='dict',
                        options=dict(
                            akamai_signature_header_authentication_key_list=dict(
                                type='list',
                                options=dict(
                                    identifier=dict(
                                        type='str'
                                    ),
                                    base64_key=dict(
                                        type='str'
                                    ),
                                    expiration=dict(
                                        type='datetime'
                                    )
                                )
                            )
                        )
                    ),
                    ip=dict(
                        type='dict',
                        options=dict(
                            allow=dict(
                                type='list',
                                options=dict(
                                    name=dict(
                                        type='str'
                                    ),
                                    address=dict(
                                        type='str'
                                    ),
                                    subnet_prefix_length=dict(
                                        type='int'
                                    )
                                )
                            )
                        )
                    )
                )
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
                type='dict',
                options=dict(
                    client_access_policy=dict(
                        type='str'
                    ),
                    cross_domain_policy=dict(
                        type='str'
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
        self.account_name = None
        self.name = None
        self.auto_start = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMStreamingEndpoint, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Streaming Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_streamingendpoint()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Streaming Endpoint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_streamingendpoint()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Streaming Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_streamingendpoint(self):
        '''
        Creates or updates Streaming Endpoint with the specified configuration.

        :return: deserialized Streaming Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Streaming Endpoint instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.streaming_endpoints.create(resource_group_name=self.resource_group,
                                                                       account_name=self.account_name,
                                                                       streaming_endpoint_name=self.name,
                                                                       parameters=self.parameters)
            else:
                response = self.mgmt_client.streaming_endpoints.update(resource_group_name=self.resource_group,
                                                                       account_name=self.account_name,
                                                                       streaming_endpoint_name=self.name,
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
        self.log("Deleting the Streaming Endpoint instance {0}".format(self.name))
        try:
            response = self.mgmt_client.streaming_endpoints.delete(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   streaming_endpoint_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Streaming Endpoint instance.')
            self.fail("Error deleting the Streaming Endpoint instance: {0}".format(str(e)))

        return True

    def get_streamingendpoint(self):
        '''
        Gets the properties of the specified Streaming Endpoint.

        :return: deserialized Streaming Endpoint instance state dictionary
        '''
        self.log("Checking if the Streaming Endpoint instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.streaming_endpoints.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                streaming_endpoint_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Streaming Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Streaming Endpoint instance.')
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


def main():
    """Main execution"""
    AzureRMStreamingEndpoint()


if __name__ == '__main__':
    main()

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
module: azure_rm_cdnendpoint
version_added: "2.8"
short_description: Manage Endpoint instance.
description:
    - Create, update and delete instance of Endpoint.

options:
    resource_group:
        description:
            - Name of the Resource group within the Azure subscription.
        required: True
    profile_name:
        description:
            - Name of the CDN profile which is unique within the resource group.
        required: True
    name:
        description:
            - Name of the I(endpoint) under the profile which is unique globally.
        required: True
    endpoint:
        description:
            - Endpoint properties
        required: True
        suboptions:
            location:
                description:
                    - Resource location.
                    - Required when C(state) is I(present).
            origin_host_header:
                description:
                    - "The host header value sent to the origin with each request. If you leave this blank, the request hostname determines this value.
                       Azure CDN I(origins), such as Web Apps, Blob Storage, and Cloud Services require this host header value to match the origin hostname
                       by default."
            origin_path:
                description:
                    - A directory path on the origin that CDN can use to retreive content from, e.g. contoso.cloudapp.net/originpath.
            content_types_to_compress:
                description:
                    - List of content types on which compression applies. The value should be a valid MIME type.
                type: list
            is_compression_enabled:
                description:
                    - "Indicates whether content compression is enabled on CDN. Default value is false. If compression is enabled, content will be served as
                       compressed if user requests for a compressed version. Content won't be compressed on CDN when requested content is smaller than 1
                       byte or larger than 1 MB."
            is_http_allowed:
                description:
                    - Indicates whether HTTP traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
            is_https_allowed:
                description:
                    - Indicates whether HTTPS traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
            query_string_caching_behavior:
                description:
                    - "Defines how CDN caches requests that include query strings. You can ignore any query strings when caching, bypass caching to prevent
                       requests that contain query strings from being cached, or cache every request with a unique URL."
                choices:
                    - 'ignore_query_string'
                    - 'bypass_caching'
                    - 'use_query_string'
                    - 'not_set'
            optimization_type:
                description:
                    - "Specifies what scenario the customer wants this CDN endpoint to optimize for, e.g. Download, Media services. With this information,
                       CDN can apply scenario driven optimization."
                choices:
                    - 'general_web_delivery'
                    - 'general_media_streaming'
                    - 'video_on_demand_media_streaming'
                    - 'large_file_download'
                    - 'dynamic_site_acceleration'
            probe_path:
                description:
                    - "Path to a file hosted on the origin which helps accelerate delivery of the dynamic content and calculate the most optimal routes for
                       the CDN. This is relative to the origin path."
            geo_filters:
                description:
                    - "List of rules defining the user's geo access within a CDN endpoint. Each geo filter defines an acess rule to a specified path or
                       content, e.g. block APAC for path /pictures/"
                type: list
                suboptions:
                    relative_path:
                        description:
                            - "Relative path applicable to geo filter. (e.g. '/mypictures', '/mypicture/kitty.jpg', and etc.)"
                            - Required when C(state) is I(present).
                    action:
                        description:
                            - Action of the geo filter, i.e. C(allow) or C(block) access.
                            - Required when C(state) is I(present).
                        choices:
                            - 'block'
                            - 'allow'
                    country_codes:
                        description:
                            - Two letter country codes defining user country access in a geo filter, e.g. AU, MX, US.
                            - Required when C(state) is I(present).
                        type: list
            delivery_policy:
                description:
                    - A policy that specifies the delivery rules to be used for an endpoint.
                suboptions:
                    description:
                        description:
                            - User-friendly description of the policy.
                    rules:
                        description:
                            - A list of the delivery rules.
                        type: list
                        suboptions:
                            order:
                                description:
                                    - "The order in which the rules are applied for the endpoint. Possible values {0,1,2,3,………}. A rule with a lesser order
                                       will be applied before a rule with a greater order. Rule with order 0 is a special rule. It does not require any
                                       condition and I(actions) listed in it will always be applied."
                                    - Required when C(state) is I(present).
                            actions:
                                description:
                                    - A list of actions that are executed when all the I(conditions) of a rule are satisfied.
                                    - Required when C(state) is I(present).
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - Constant filled by server.
                                            - Required when C(state) is I(present).
                            conditions:
                                description:
                                    - A list of conditions that must be matched for the I(actions) to be executed
                                type: list
                                suboptions:
                                    name:
                                        description:
                                            - Constant filled by server.
                                            - Required when C(state) is I(present).
            origins:
                description:
                    - The source of the content being delivered via CDN.
                    - Required when C(state) is I(present).
                type: list
                suboptions:
                    name:
                        description:
                            - Origin name
                            - Required when C(state) is I(present).
                    host_name:
                        description:
                            - The address of the origin. It can be a domain name, IPv4 address, or IPv6 address.
                            - Required when C(state) is I(present).
                    http_port:
                        description:
                            - The value of the HTTP port. Must be between 1 and 65535
                    https_port:
                        description:
                            - The value of the HTTPS port. Must be between 1 and 65535
    state:
      description:
        - Assert the state of the Endpoint.
        - Use 'present' to create or update an Endpoint and 'absent' to delete it.
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
  - name: Create (or update) Endpoint
    azure_rm_cdnendpoint:
      resource_group: RG
      profile_name: profile1
      name: endpoint1
      endpoint:
        location: WestCentralUs
        origins:
          - name: www-bing-com
            host_name: www.bing.com
            http_port: 80
            https_port: 443
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/subid/resourcegroups/RG/providers/Microsoft.Cdn/profiles/profile1/endpoints/endpoint1
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


class AzureRMEndpoints(AzureRMModuleBase):
    """Configuration class for an Azure RM Endpoint resource"""

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
            name=dict(
                type='str',
                required=True
            ),
            endpoint=dict(
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
        self.name = None
        self.endpoint = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEndpoints, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.endpoint["location"] = kwargs[key]
                elif key == "origin_host_header":
                    self.endpoint["origin_host_header"] = kwargs[key]
                elif key == "origin_path":
                    self.endpoint["origin_path"] = kwargs[key]
                elif key == "content_types_to_compress":
                    self.endpoint["content_types_to_compress"] = kwargs[key]
                elif key == "is_compression_enabled":
                    self.endpoint["is_compression_enabled"] = kwargs[key]
                elif key == "is_http_allowed":
                    self.endpoint["is_http_allowed"] = kwargs[key]
                elif key == "is_https_allowed":
                    self.endpoint["is_https_allowed"] = kwargs[key]
                elif key == "query_string_caching_behavior":
                    self.endpoint["query_string_caching_behavior"] = _snake_to_camel(kwargs[key], True)
                elif key == "optimization_type":
                    self.endpoint["optimization_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "probe_path":
                    self.endpoint["probe_path"] = kwargs[key]
                elif key == "geo_filters":
                    ev = kwargs[key]
                    if 'action' in ev:
                        if ev['action'] == 'block':
                            ev['action'] = 'Block'
                        elif ev['action'] == 'allow':
                            ev['action'] = 'Allow'
                    self.endpoint["geo_filters"] = ev
                elif key == "delivery_policy":
                    self.endpoint["delivery_policy"] = kwargs[key]
                elif key == "origins":
                    self.endpoint["origins"] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(CdnManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_endpoint()

        if not old_response:
            self.log("Endpoint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Endpoint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '')):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Endpoint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_endpoint()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Endpoint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_endpoint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_endpoint():
                time.sleep(20)
        else:
            self.log("Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_endpoint(self):
        '''
        Creates or updates Endpoint with the specified configuration.

        :return: deserialized Endpoint instance state dictionary
        '''
        self.log("Creating / Updating the Endpoint instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.endpoints.create(resource_group_name=self.resource_group,
                                                             profile_name=self.profile_name,
                                                             endpoint_name=self.name,
                                                             endpoint=self.endpoint)
            else:
                response = self.mgmt_client.endpoints.update(resource_group_name=self.resource_group,
                                                             profile_name=self.profile_name,
                                                             endpoint_name=self.name,
                                                             endpoint_update_properties=self.endpoint_update_properties)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Endpoint instance.')
            self.fail("Error creating the Endpoint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_endpoint(self):
        '''
        Deletes specified Endpoint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Endpoint instance {0}".format(self.name))
        try:
            response = self.mgmt_client.endpoints.delete(resource_group_name=self.resource_group,
                                                         profile_name=self.profile_name,
                                                         endpoint_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Endpoint instance.')
            self.fail("Error deleting the Endpoint instance: {0}".format(str(e)))

        return True

    def get_endpoint(self):
        '''
        Gets the properties of the specified Endpoint.

        :return: deserialized Endpoint instance state dictionary
        '''
        self.log("Checking if the Endpoint instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.endpoints.get(resource_group_name=self.resource_group,
                                                      profile_name=self.profile_name,
                                                      endpoint_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Endpoint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Endpoint instance.')
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
    AzureRMEndpoints()


if __name__ == '__main__':
    main()

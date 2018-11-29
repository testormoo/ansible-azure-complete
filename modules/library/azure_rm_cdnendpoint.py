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
short_description: Manage Azure Endpoint instance.
description:
    - Create, update and delete instance of Azure Endpoint.

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
            - Name of the endpoint under the profile which is unique globally.
        required: True
    location:
        description:
            - Resource location.
            - Required when C(state) is I(present).
    origin_host_header:
        description:
            - "The host header value sent to the origin with each request. If you leave this blank, the request hostname determines this value. Azure CDN
               I(origins), such as Web Apps, Blob Storage, and Cloud Services require this host header value to match the origin hostname by default."
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
               compressed if user requests for a compressed version. Content won't be compressed on CDN when requested content is smaller than 1 byte or
               larger than 1 MB."
    is_http_allowed:
        description:
            - Indicates whether HTTP traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
    is_https_allowed:
        description:
            - Indicates whether HTTPS traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
    query_string_caching_behavior:
        description:
            - "Defines how CDN caches requests that include query strings. You can ignore any query strings when caching, bypass caching to prevent requests
               that contain query strings from being cached, or cache every request with a unique URL."
        choices:
            - 'ignore_query_string'
            - 'bypass_caching'
            - 'use_query_string'
            - 'not_set'
    optimization_type:
        description:
            - "Specifies what scenario the customer wants this CDN endpoint to optimize for, e.g. Download, Media services. With this information, CDN can
               apply scenario driven optimization."
        choices:
            - 'general_web_delivery'
            - 'general_media_streaming'
            - 'video_on_demand_media_streaming'
            - 'large_file_download'
            - 'dynamic_site_acceleration'
    probe_path:
        description:
            - "Path to a file hosted on the origin which helps accelerate delivery of the dynamic content and calculate the most optimal routes for the CDN.
               This is relative to the origin path."
    geo_filters:
        description:
            - "List of rules defining the user's geo access within a CDN endpoint. Each geo filter defines an acess rule to a specified path or content,
               e.g. block APAC for path /pictures/"
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
                            - "The order in which the rules are applied for the endpoint. Possible values {0,1,2,3,………}. A rule with a lesser order will be
                               applied before a rule with a greater order. Rule with order 0 is a special rule. It does not require any condition and
                               I(actions) listed in it will always be applied."
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


class AzureRMEndpoint(AzureRMModuleBase):
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
            location=dict(
                type='str'
            ),
            origin_host_header=dict(
                type='str'
            ),
            origin_path=dict(
                type='str'
            ),
            content_types_to_compress=dict(
                type='list'
            ),
            is_compression_enabled=dict(
                type='str'
            ),
            is_http_allowed=dict(
                type='str'
            ),
            is_https_allowed=dict(
                type='str'
            ),
            query_string_caching_behavior=dict(
                type='str',
                choices=['ignore_query_string',
                         'bypass_caching',
                         'use_query_string',
                         'not_set']
            ),
            optimization_type=dict(
                type='str',
                choices=['general_web_delivery',
                         'general_media_streaming',
                         'video_on_demand_media_streaming',
                         'large_file_download',
                         'dynamic_site_acceleration']
            ),
            probe_path=dict(
                type='str'
            ),
            geo_filters=dict(
                type='list',
                options=dict(
                    relative_path=dict(
                        type='str'
                    ),
                    action=dict(
                        type='str',
                        choices=['block',
                                 'allow']
                    ),
                    country_codes=dict(
                        type='list'
                    )
                )
            ),
            delivery_policy=dict(
                type='dict',
                options=dict(
                    description=dict(
                        type='str'
                    ),
                    rules=dict(
                        type='list',
                        options=dict(
                            order=dict(
                                type='int'
                            ),
                            actions=dict(
                                type='list',
                                options=dict(
                                    name=dict(
                                        type='str'
                                    )
                                )
                            ),
                            conditions=dict(
                                type='list',
                                options=dict(
                                    name=dict(
                                        type='str'
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            origins=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    host_name=dict(
                        type='str'
                    ),
                    http_port=dict(
                        type='int'
                    ),
                    https_port=dict(
                        type='int'
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
        self.profile_name = None
        self.name = None
        self.endpoint = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMEndpoint, self).__init__(derived_arg_spec=self.module_arg_spec,
                                              supports_check_mode=True,
                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.endpoint[key] = kwargs[key]

        dict_camelize(self.endpoint, ['query_string_caching_behavior'], True)
        dict_camelize(self.endpoint, ['optimization_type'], True)
        dict_camelize(self.endpoint, ['geo_filters', 'action'], True)

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
                if (not default_compare(self.endpoint, old_response, '', self.results)):
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Endpoint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
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
            else:
                key = list(old[0])[0]
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
    AzureRMEndpoint()


if __name__ == '__main__':
    main()

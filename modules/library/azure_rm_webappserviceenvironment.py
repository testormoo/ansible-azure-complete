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
module: azure_rm_webappserviceenvironment
version_added: "2.8"
short_description: Manage Azure App Service Environment instance.
description:
    - Create, update and delete instance of Azure App Service Environment.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Name of the App Service Environment.
        required: True
    kind:
        description:
            - Kind of resource.
    location:
        description:
            - Resource Location.
            - Required when C(state) is I(present).
    app_service_environment_resource_name:
        description:
            - Name of the App Service Environment.
            - Required when C(state) is I(present).
    app_service_environment_resource_location:
        description:
            - "Location of the App Service Environment, e.g. 'West US'."
            - Required when C(state) is I(present).
    vnet_name:
        description:
            - Name of the Virtual Network for the App Service Environment.
    vnet_resource_group_name:
        description:
            - Resource group of the Virtual Network.
    vnet_subnet_name:
        description:
            - Subnet of the Virtual Network.
    virtual_network:
        description:
            - Description of the Virtual Network.
            - Required when C(state) is I(present).
        suboptions:
            id:
                description:
                    - Resource id of the Virtual Network.
            subnet:
                description:
                    - Subnet within the Virtual Network.
    internal_load_balancing_mode:
        description:
            - Specifies which endpoints to serve internally in the Virtual Network for the App Service Environment.
        choices:
            - 'none'
            - 'web'
            - 'publishing'
    multi_size:
        description:
            - "Front-end VM size, e.g. 'Medium', 'Large'."
    multi_role_count:
        description:
            - Number of front-end instances.
    worker_pools:
        description:
            - Description of worker pools with worker size IDs, VM sizes, and number of workers in each pool.
            - Required when C(state) is I(present).
        type: list
        suboptions:
            worker_size_id:
                description:
                    - Worker size ID for referencing this worker pool.
            compute_mode:
                description:
                    - C(shared) or C(dedicated) app hosting.
                choices:
                    - 'shared'
                    - 'dedicated'
                    - 'dynamic'
            worker_size:
                description:
                    - VM size of the worker pool instances.
            worker_count:
                description:
                    - Number of instances in the worker pool.
    ipssl_address_count:
        description:
            - Number of IP SSL addresses reserved for the App Service Environment.
    dns_suffix:
        description:
            - DNS suffix of the App Service Environment.
    network_access_control_list:
        description:
            - Access control list for controlling traffic to the App Service Environment.
        type: list
        suboptions:
            action:
                description:
                    - Action object.
                choices:
                    - 'permit'
                    - 'deny'
            description:
                description:
                    - Description of network access control entry.
            order:
                description:
                    - Order of precedence.
            remote_subnet:
                description:
                    - Remote subnet.
    front_end_scale_factor:
        description:
            - Scale factor for front-ends.
    api_management_account_id:
        description:
            - API Management Account associated with the App Service Environment.
    suspended:
        description:
            - "<code>true</code> if the App Service Environment is suspended; otherwise, <code>false</code>. The environment can be suspended, e.g. when the
               management endpoint is no longer available"
            -  (most likely because NSG blocked the incoming traffic).
    dynamic_cache_enabled:
        description:
            - "True/false indicating whether the App Service Environment is I(suspended). The environment can be I(suspended) e.g. when the management
               endpoint is no longer available"
            - (most likely because NSG blocked the incoming traffic).
    cluster_settings:
        description:
            - Custom settings for changing the behavior of the App Service Environment.
        type: list
        suboptions:
            name:
                description:
                    - Pair name.
            value:
                description:
                    - Pair value.
    user_whitelisted_ip_ranges:
        description:
            - User added ip ranges to whitelist on ASE db
        type: list
    state:
      description:
        - Assert the state of the App Service Environment.
        - Use 'present' to create or update an App Service Environment and 'absent' to delete it.
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
  - name: Create (or update) App Service Environment
    azure_rm_webappserviceenvironment:
      resource_group: NOT FOUND
      name: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: id
status:
    description:
        - "Current status of the App Service Environment. Possible values include: 'Preparing', 'Ready', 'Scaling', 'Deleting'"
    returned: always
    type: str
    sample: status
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.web import WebSiteManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMAppServiceEnvironment(AzureRMModuleBase):
    """Configuration class for an Azure RM App Service Environment resource"""

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
            kind=dict(
                type='str'
            ),
            location=dict(
                type='str'
            ),
            app_service_environment_resource_name=dict(
                type='str'
            ),
            app_service_environment_resource_location=dict(
                type='str'
            ),
            vnet_name=dict(
                type='str'
            ),
            vnet_resource_group_name=dict(
                type='str'
            ),
            vnet_subnet_name=dict(
                type='str'
            ),
            virtual_network=dict(
                type='dict',
                options=dict(
                    id=dict(
                        type='str'
                    ),
                    subnet=dict(
                        type='str'
                    )
                )
            ),
            internal_load_balancing_mode=dict(
                type='str',
                choices=['none',
                         'web',
                         'publishing']
            ),
            multi_size=dict(
                type='str'
            ),
            multi_role_count=dict(
                type='int'
            ),
            worker_pools=dict(
                type='list',
                options=dict(
                    worker_size_id=dict(
                        type='int'
                    ),
                    compute_mode=dict(
                        type='str',
                        choices=['shared',
                                 'dedicated',
                                 'dynamic']
                    ),
                    worker_size=dict(
                        type='str'
                    ),
                    worker_count=dict(
                        type='int'
                    )
                )
            ),
            ipssl_address_count=dict(
                type='int'
            ),
            dns_suffix=dict(
                type='str'
            ),
            network_access_control_list=dict(
                type='list',
                options=dict(
                    action=dict(
                        type='str',
                        choices=['permit',
                                 'deny']
                    ),
                    description=dict(
                        type='str'
                    ),
                    order=dict(
                        type='int'
                    ),
                    remote_subnet=dict(
                        type='str'
                    )
                )
            ),
            front_end_scale_factor=dict(
                type='int'
            ),
            api_management_account_id=dict(
                type='str'
            ),
            suspended=dict(
                type='str'
            ),
            dynamic_cache_enabled=dict(
                type='str'
            ),
            cluster_settings=dict(
                type='list',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    value=dict(
                        type='str'
                    )
                )
            ),
            user_whitelisted_ip_ranges=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.hosting_environment_envelope = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAppServiceEnvironment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.hosting_environment_envelope[key] = kwargs[key]

        dict_resource_id(self.hosting_environment_envelope, ['virtual_network', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)
        dict_camelize(self.hosting_environment_envelope, ['internal_load_balancing_mode'], True)
        dict_camelize(self.hosting_environment_envelope, ['worker_pools', 'compute_mode'], True)
        dict_camelize(self.hosting_environment_envelope, ['network_access_control_list', 'action'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(WebSiteManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_appserviceenvironment()

        if not old_response:
            self.log("App Service Environment instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("App Service Environment instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.hosting_environment_envelope, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the App Service Environment instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_appserviceenvironment()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("App Service Environment instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_appserviceenvironment()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("App Service Environment instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': response.get('status', None)
                })
        return self.results

    def create_update_appserviceenvironment(self):
        '''
        Creates or updates App Service Environment with the specified configuration.

        :return: deserialized App Service Environment instance state dictionary
        '''
        self.log("Creating / Updating the App Service Environment instance {0}".format(self.name))

        try:
            response = self.mgmt_client.app_service_environments.create_or_update(resource_group_name=self.resource_group,
                                                                                  name=self.name,
                                                                                  hosting_environment_envelope=self.hosting_environment_envelope)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the App Service Environment instance.')
            self.fail("Error creating the App Service Environment instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_appserviceenvironment(self):
        '''
        Deletes specified App Service Environment instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the App Service Environment instance {0}".format(self.name))
        try:
            response = self.mgmt_client.app_service_environments.delete(resource_group_name=self.resource_group,
                                                                        name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the App Service Environment instance.')
            self.fail("Error deleting the App Service Environment instance: {0}".format(str(e)))

        return True

    def get_appserviceenvironment(self):
        '''
        Gets the properties of the specified App Service Environment.

        :return: deserialized App Service Environment instance state dictionary
        '''
        self.log("Checking if the App Service Environment instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.app_service_environments.get(resource_group_name=self.resource_group,
                                                                     name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("App Service Environment instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the App Service Environment instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMAppServiceEnvironment()


if __name__ == '__main__':
    main()

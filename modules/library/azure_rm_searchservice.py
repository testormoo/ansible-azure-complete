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
module: azure_rm_searchservice
version_added: "2.8"
short_description: Manage Azure Service instance.
description:
    - Create, update and delete instance of Azure Service.

options:
    resource_group:
        description:
            - The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    name:
        description:
            - "The name of the Azure Search service to create or update. Search service names must only contain lowercase letters, digits or dashes, cannot
               use dash as the first two or last one characters, cannot contain consecutive dashes, and must be between 2 and 60 characters in length.
               Search service names must be globally unique since they are part of the service URI (https://<name>.search.windows.net). You cannot change
               the service name after the service is created."
        required: True
    location:
        description:
            - "The geographic location of the resource. This must be one of the supported and registered Azure Geo Regions (for example, West US, East US,
               Southeast Asia, and so forth). This property is required when creating a new resource."
    identity:
        description:
            - The identity of the resource.
        suboptions:
            type:
                description:
                    - The identity type.
                    - Required when C(state) is I(present).
    replica_count:
        description:
            - "The number of replicas in the Search service. If specified, it must be a value between 1 and 12 inclusive for standard SKUs or between 1 and
               3 inclusive for basic I(sku)."
    partition_count:
        description:
            - "The number of partitions in the Search service; if specified, it can be 1, 2, 3, 4, 6, or 12. Values greater than 1 are only valid for
               standard SKUs. For 'standard3' services with I(hosting_mode) set to 'C(high_density)', the allowed values are between 1 and 3."
    hosting_mode:
        description:
            - "Applicable only for the standard3 I(sku). You can set this property to enable up to 3 high density partitions that allow up to 1000 indexes,
               which is much higher than the maximum indexes allowed for any other I(sku). For the standard3 I(sku), the value is either 'C(default)' or
               'C(high_density)'. For all other SKUs, this value must be 'C(default)'."
        choices:
            - 'default'
            - 'high_density'
    sku:
        description:
            - The SKU of the Search Service, which determines price tier and capacity limits. This property is required when creating a new Search Service.
        suboptions:
            name:
                description:
                    - "The SKU of the Search service. Valid values include: 'C(free)': Shared service. 'C(basic)': Dedicated service with up to 3 replicas.
                       'C(standard)': Dedicated service with up to 12 partitions and 12 replicas. 'C(standard2)': Similar to C(standard), but with more
                       capacity per search unit. 'C(standard3)': Offers maximum capacity per search unit with up to 12 partitions and 12 replicas (or up to
                       3 partitions with more indexes if you also set the hostingMode property to 'highDensity')."
                choices:
                    - 'free'
                    - 'basic'
                    - 'standard'
                    - 'standard2'
                    - 'standard3'
    client_request_id:
        description:
            - "A client-generated GUID value that identifies this request. If specified, this will be included in response information as a way to track the
               request."
    state:
      description:
        - Assert the state of the Service.
        - Use 'present' to create or update an Service and 'absent' to delete it.
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
  - name: Create (or update) Service
    azure_rm_searchservice:
      resource_group: rg1
      name: mysearchservice
      location: westus
      replica_count: 3
      partition_count: 1
      hosting_mode: default
      sku:
        name: standard
'''

RETURN = '''
id:
    description:
        - The ID of the resource. This can be used with the Azure Resource Manager to link resources together.
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Search/searchServices/mysearchservice
status:
    description:
        - "The status of the Search service. Possible values include: 'running': The Search service is running and no provisioning operations are underway.
           'provisioning': The Search service is being provisioned or scaled up or down. 'deleting': The Search service is being deleted. 'degraded': The
           Search service is degraded. This can occur when the underlying search units are not healthy. The Search service is most likely operational, but
           performance might be slow and some requests might be dropped. 'disabled': The Search service is disabled. In this state, the service will reject
           all API requests. 'error': The Search service is in an error state. If your service is in the degraded, disabled, or error states, it means the
           Azure Search team is actively investigating the underlying issue. Dedicated services in these states are still chargeable based on the number of
           search units provisioned. Possible values include: 'running', 'provisioning', 'deleting', 'degraded', 'disabled', 'error'"
    returned: always
    type: str
    sample: provisioning
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.search import SearchManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMService(AzureRMModuleBase):
    """Configuration class for an Azure RM Service resource"""

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
            identity=dict(
                type='dict'
            ),
            replica_count=dict(
                type='int'
            ),
            partition_count=dict(
                type='int'
            ),
            hosting_mode=dict(
                type='str',
                choices=['default',
                         'high_density']
            ),
            sku=dict(
                type='dict'
            ),
            client_request_id=dict(
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
        self.service = dict()
        self.search_management_request_options = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMService, self).__init__(derived_arg_spec=self.module_arg_spec,
                                             supports_check_mode=True,
                                             supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.service[key] = kwargs[key]

        dict_camelize(self.service, ['hosting_mode'], True)
        dict_map(self.service, ['hosting_mode'], ''high_density': 'highDensity'')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SearchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_service()

        if not old_response:
            self.log("Service instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Service instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.service, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Service instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_service()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Service instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_service()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_service():
                time.sleep(20)
        else:
            self.log("Service instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_service(self):
        '''
        Creates or updates Service with the specified configuration.

        :return: deserialized Service instance state dictionary
        '''
        self.log("Creating / Updating the Service instance {0}".format(self.search_management_request_options))

        try:
            response = self.mgmt_client.services.create_or_update(resource_group_name=self.resource_group,
                                                                  search_service_name=self.name,
                                                                  service=self.service)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Service instance.')
            self.fail("Error creating the Service instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_service(self):
        '''
        Deletes specified Service instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Service instance {0}".format(self.search_management_request_options))
        try:
            response = self.mgmt_client.services.delete(resource_group_name=self.resource_group,
                                                        search_service_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Service instance.')
            self.fail("Error deleting the Service instance: {0}".format(str(e)))

        return True

    def get_service(self):
        '''
        Gets the properties of the specified Service.

        :return: deserialized Service instance state dictionary
        '''
        self.log("Checking if the Service instance {0} is present".format(self.search_management_request_options))
        found = False
        try:
            response = self.mgmt_client.services.get(resource_group_name=self.resource_group,
                                                     search_service_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Service instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Service instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


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


def dict_upper(d, path):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_upper(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                d[path[0]] = old_value.upper()
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_upper(sd, path[1:])


def dict_rename(d, path, new_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_rename(d[i], path, new_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[new_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_rename(sd, path[1:], new_name)


def dict_expand(d, path, outer_dict_name):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_expand(d[i], path, outer_dict_name)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.pop(path[0], None)
            if old_value is not None:
                d[outer_dict_name] = d.get(outer_dict_name, {})
                d[outer_dict_name] = old_value
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_expand(sd, path[1:], outer_dict_name)


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMService()


if __name__ == '__main__':
    main()

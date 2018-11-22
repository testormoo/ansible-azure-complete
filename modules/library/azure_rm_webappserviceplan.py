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
module: azure_rm_webappserviceplan
version_added: "2.8"
short_description: Manage Azure App Service Plan instance.
description:
    - Create, update and delete instance of Azure App Service Plan.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Name of the App Service plan.
        required: True
    kind:
        description:
            - Kind of resource.
    location:
        description:
            - Resource Location.
            - Required when C(state) is I(present).
    app_service_plan_name:
        description:
            - Name for the App Service plan.
    worker_tier_name:
        description:
            - Target worker tier assigned to the App Service plan.
    admin_site_name:
        description:
            - App Service plan administration site.
    hosting_environment_profile:
        description:
            - Specification for the App Service Environment to use for the App Service plan.
        suboptions:
            id:
                description:
                    - Resource ID of the App Service Environment.
    per_site_scaling:
        description:
            - If <code>true</code>, apps assigned to this App Service plan can be scaled independently.
            - If <code>false</code>, apps assigned to this App Service plan will scale to all instances of the plan.
    is_spot:
        description:
            - If <code>true</code>, this App Service Plan owns spot instances.
    spot_expiration_time:
        description:
            - The time when the server farm expires. Valid only if it is a spot server farm.
    reserved:
        description:
            - If Linux app service plan <code>true</code>, <code>false</code> otherwise.
    target_worker_count:
        description:
            - Scaling worker count.
    target_worker_size_id:
        description:
            - Scaling worker size ID.
    sku:
        description:
        suboptions:
            name:
                description:
                    - Name of the resource SKU.
            tier:
                description:
                    - Service tier of the resource SKU.
            size:
                description:
                    - Size specifier of the resource SKU.
            family:
                description:
                    - Family code of the resource SKU.
            capacity:
                description:
                    - Current number of instances assigned to the resource.
            sku_capacity:
                description:
                    - Min, max, and default scale values of the SKU.
                suboptions:
                    minimum:
                        description:
                            - Minimum number of workers for this App Service plan SKU.
                    maximum:
                        description:
                            - Maximum number of workers for this App Service plan SKU.
                    default:
                        description:
                            - Default number of workers for this App Service plan SKU.
                    scale_type:
                        description:
                            - Available scale configurations for an App Service plan.
            locations:
                description:
                    - Locations of the SKU.
                type: list
            capabilities:
                description:
                    - Capabilities of the SKU, e.g., is traffic manager enabled?
                type: list
                suboptions:
                    name:
                        description:
                            - Name of the SKU capability.
                    value:
                        description:
                            - Value of the SKU capability.
                    reason:
                        description:
                            - Reason of the SKU capability.
    state:
      description:
        - Assert the state of the App Service Plan.
        - Use 'present' to create or update an App Service Plan and 'absent' to delete it.
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
  - name: Create (or update) App Service Plan
    azure_rm_webappserviceplan:
      resource_group: testrg123
      name: testsf6141
      kind: app
      location: East US
      app_service_plan_name: testsf6141
      sku:
        name: P1
        tier: Premium
        size: P1
        family: P
        capacity: 1
'''

RETURN = '''
id:
    description:
        - Resource Id.
    returned: always
    type: str
    sample: /subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/testrg123/providers/Microsoft.Web/serverfarms/testsf6141
status:
    description:
        - "App Service plan status. Possible values include: 'Ready', 'Pending', 'Creating'"
    returned: always
    type: str
    sample: Ready
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

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


class AzureRMAppServicePlan(AzureRMModuleBase):
    """Configuration class for an Azure RM App Service Plan resource"""

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
            app_service_plan_name=dict(
                type='str'
            ),
            worker_tier_name=dict(
                type='str'
            ),
            admin_site_name=dict(
                type='str'
            ),
            hosting_environment_profile=dict(
                type='dict'
            ),
            per_site_scaling=dict(
                type='str'
            ),
            is_spot=dict(
                type='str'
            ),
            spot_expiration_time=dict(
                type='datetime'
            ),
            reserved=dict(
                type='str'
            ),
            target_worker_count=dict(
                type='int'
            ),
            target_worker_size_id=dict(
                type='int'
            ),
            sku=dict(
                type='dict'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.name = None
        self.app_service_plan = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMAppServicePlan, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.app_service_plan[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(WebSiteManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_appserviceplan()

        if not old_response:
            self.log("App Service Plan instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("App Service Plan instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.app_service_plan, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the App Service Plan instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_appserviceplan()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("App Service Plan instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_appserviceplan()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_appserviceplan():
                time.sleep(20)
        else:
            self.log("App Service Plan instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_response(response))
        return self.results

    def create_update_appserviceplan(self):
        '''
        Creates or updates App Service Plan with the specified configuration.

        :return: deserialized App Service Plan instance state dictionary
        '''
        self.log("Creating / Updating the App Service Plan instance {0}".format(self.name))

        try:
            response = self.mgmt_client.app_service_plans.create_or_update(resource_group_name=self.resource_group,
                                                                           name=self.name,
                                                                           app_service_plan=self.app_service_plan)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the App Service Plan instance.')
            self.fail("Error creating the App Service Plan instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_appserviceplan(self):
        '''
        Deletes specified App Service Plan instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the App Service Plan instance {0}".format(self.name))
        try:
            response = self.mgmt_client.app_service_plans.delete(resource_group_name=self.resource_group,
                                                                 name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the App Service Plan instance.')
            self.fail("Error deleting the App Service Plan instance: {0}".format(str(e)))

        return True

    def get_appserviceplan(self):
        '''
        Gets the properties of the specified App Service Plan.

        :return: deserialized App Service Plan instance state dictionary
        '''
        self.log("Checking if the App Service Plan instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.app_service_plans.get(resource_group_name=self.resource_group,
                                                              name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("App Service Plan instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the App Service Plan instance.')
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
    AzureRMAppServicePlan()


if __name__ == '__main__':
    main()

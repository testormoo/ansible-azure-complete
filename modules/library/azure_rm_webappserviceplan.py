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
short_description: Manage App Service Plan instance.
description:
    - Create, update and delete instance of App Service Plan.

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
        required: True
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


class AzureRMAppServicePlans(AzureRMModuleBase):
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
                type='str',
                required=True
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

        super(AzureRMAppServicePlans, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "kind":
                    self.app_service_plan["kind"] = kwargs[key]
                elif key == "location":
                    self.app_service_plan["location"] = kwargs[key]
                elif key == "app_service_plan_name":
                    self.app_service_plan["app_service_plan_name"] = kwargs[key]
                elif key == "worker_tier_name":
                    self.app_service_plan["worker_tier_name"] = kwargs[key]
                elif key == "admin_site_name":
                    self.app_service_plan["admin_site_name"] = kwargs[key]
                elif key == "hosting_environment_profile":
                    self.app_service_plan["hosting_environment_profile"] = kwargs[key]
                elif key == "per_site_scaling":
                    self.app_service_plan["per_site_scaling"] = kwargs[key]
                elif key == "is_spot":
                    self.app_service_plan["is_spot"] = kwargs[key]
                elif key == "spot_expiration_time":
                    self.app_service_plan["spot_expiration_time"] = kwargs[key]
                elif key == "reserved":
                    self.app_service_plan["reserved"] = kwargs[key]
                elif key == "target_worker_count":
                    self.app_service_plan["target_worker_count"] = kwargs[key]
                elif key == "target_worker_size_id":
                    self.app_service_plan["target_worker_size_id"] = kwargs[key]
                elif key == "sku":
                    self.app_service_plan["sku"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if App Service Plan instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the App Service Plan instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_appserviceplan()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
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
            self.results.update(self.format_item(response))
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

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': d.get('status', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMAppServicePlans()


if __name__ == '__main__':
    main()

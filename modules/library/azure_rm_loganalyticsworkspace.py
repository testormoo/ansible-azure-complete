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
module: azure_rm_loganalyticsworkspace
version_added: "2.8"
short_description: Manage Workspace instance.
description:
    - Create, update and delete instance of Workspace.

options:
    resource_group:
        description:
            - The resource group name of the workspace.
        required: True
    workspace_name:
        description:
            - The name of the workspace.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    provisioning_state:
        description:
            - The provisioning state of the workspace.
        choices:
            - 'creating'
            - 'succeeded'
            - 'failed'
            - 'canceled'
            - 'deleting'
            - 'provisioning_account'
    source:
        description:
            - "The source of the workspace.  Source defines where the workspace was created. 'Azure' implies it was created in Azure.  'External' implies it
               was created via the Operational Insights Portal. This value is set on the service side and read-only on the client side."
    customer_id:
        description:
            - "The ID associated with the workspace.  Setting this value at creation time allows the workspace being created to be linked to an existing
               workspace."
    portal_url:
        description:
            - The URL of the Operational Insights portal for this workspace.  This value is set on the service side and read-only on the client side.
    sku:
        description:
            - The SKU of the workspace.
        suboptions:
            name:
                description:
                    - The name of the SKU.
                required: True
                choices:
                    - 'free'
                    - 'standard'
                    - 'premium'
                    - 'unlimited'
                    - 'per_node'
                    - 'per_gb2018'
                    - 'standalone'
    retention_in_days:
        description:
            - The workspace data retention in days. -1 means Unlimited retention for the Unlimited I(sku). 730 days is the maximum allowed for all other Skus.
    e_tag:
        description:
            - The ETag of the workspace.
    state:
      description:
        - Assert the state of the Workspace.
        - Use 'present' to create or update an Workspace and 'absent' to delete it.
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
  - name: Create (or update) Workspace
    azure_rm_loganalyticsworkspace:
      resource_group: oiautorest6685
      workspace_name: oiautorest6685
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource Id
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
    from azure.mgmt.loganalytics import OperationalInsightsManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMWorkspaces(AzureRMModuleBase):
    """Configuration class for an Azure RM Workspace resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            workspace_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            provisioning_state=dict(
                type='str',
                choices=['creating',
                         'succeeded',
                         'failed',
                         'canceled',
                         'deleting',
                         'provisioning_account']
            ),
            source=dict(
                type='str'
            ),
            customer_id=dict(
                type='str'
            ),
            portal_url=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            retention_in_days=dict(
                type='int'
            ),
            e_tag=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.workspace_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWorkspaces, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "provisioning_state":
                    self.parameters["provisioning_state"] = _snake_to_camel(kwargs[key], True)
                elif key == "source":
                    self.parameters["source"] = kwargs[key]
                elif key == "customer_id":
                    self.parameters["customer_id"] = kwargs[key]
                elif key == "portal_url":
                    self.parameters["portal_url"] = kwargs[key]
                elif key == "sku":
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'free':
                            ev['name'] = 'Free'
                        elif ev['name'] == 'standard':
                            ev['name'] = 'Standard'
                        elif ev['name'] == 'premium':
                            ev['name'] = 'Premium'
                        elif ev['name'] == 'unlimited':
                            ev['name'] = 'Unlimited'
                        elif ev['name'] == 'per_node':
                            ev['name'] = 'PerNode'
                        elif ev['name'] == 'per_gb2018':
                            ev['name'] = 'PerGB2018'
                        elif ev['name'] == 'standalone':
                            ev['name'] = 'Standalone'
                    self.parameters["sku"] = ev
                elif key == "retention_in_days":
                    self.parameters["retention_in_days"] = kwargs[key]
                elif key == "e_tag":
                    self.parameters["e_tag"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(OperationalInsightsManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_workspace()

        if not old_response:
            self.log("Workspace instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Workspace instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Workspace instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Workspace instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_workspace()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Workspace instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_workspace()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_workspace():
                time.sleep(20)
        else:
            self.log("Workspace instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_workspace(self):
        '''
        Creates or updates Workspace with the specified configuration.

        :return: deserialized Workspace instance state dictionary
        '''
        self.log("Creating / Updating the Workspace instance {0}".format(self.workspace_name))

        try:
            response = self.mgmt_client.workspaces.create_or_update(resource_group_name=self.resource_group,
                                                                    workspace_name=self.workspace_name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Workspace instance.')
            self.fail("Error creating the Workspace instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_workspace(self):
        '''
        Deletes specified Workspace instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Workspace instance {0}".format(self.workspace_name))
        try:
            response = self.mgmt_client.workspaces.delete(resource_group_name=self.resource_group,
                                                          workspace_name=self.workspace_name)
        except CloudError as e:
            self.log('Error attempting to delete the Workspace instance.')
            self.fail("Error deleting the Workspace instance: {0}".format(str(e)))

        return True

    def get_workspace(self):
        '''
        Gets the properties of the specified Workspace.

        :return: deserialized Workspace instance state dictionary
        '''
        self.log("Checking if the Workspace instance {0} is present".format(self.workspace_name))
        found = False
        try:
            response = self.mgmt_client.workspaces.get(resource_group_name=self.resource_group,
                                                       workspace_name=self.workspace_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Workspace instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Workspace instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def _snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return ''.join(x.capitalize() or '_' for x in snake.split('_'))
    else:
        return snake.split('_')[0] + ''.join(x.capitalize() or '_' for x in snake.split('_')[1:])


def main():
    """Main execution"""
    AzureRMWorkspaces()


if __name__ == '__main__':
    main()
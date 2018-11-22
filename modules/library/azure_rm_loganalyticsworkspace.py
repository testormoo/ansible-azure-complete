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
short_description: Manage Azure Workspace instance.
description:
    - Create, update and delete instance of Azure Workspace.

options:
    resource_group:
        description:
            - The resource group name of the workspace.
        required: True
    name:
        description:
            - The name of the workspace.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
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
                    - Required when C(state) is I(present).
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
      name: oiautorest6685
      location: eastus
      sku:
        name: PerNode
      retention_in_days: 30
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


class AzureRMWorkspace(AzureRMModuleBase):
    """Configuration class for an Azure RM Workspace resource"""

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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMWorkspace, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['sku', 'name'], True)
        dict_map(self.parameters, ['sku', 'name'], {'per_gb2018': 'PerGB2018'})

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Workspace instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_workspace()

            self.results['changed'] = True
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
            self.results.update(self.format_response(response))
        return self.results

    def create_update_workspace(self):
        '''
        Creates or updates Workspace with the specified configuration.

        :return: deserialized Workspace instance state dictionary
        '''
        self.log("Creating / Updating the Workspace instance {0}".format(self.name))

        try:
            response = self.mgmt_client.workspaces.create_or_update(resource_group_name=self.resource_group,
                                                                    workspace_name=self.name,
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
        self.log("Deleting the Workspace instance {0}".format(self.name))
        try:
            response = self.mgmt_client.workspaces.delete(resource_group_name=self.resource_group,
                                                          workspace_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Workspace instance.')
            self.fail("Error deleting the Workspace instance: {0}".format(str(e)))

        return True

    def get_workspace(self):
        '''
        Gets the properties of the specified Workspace.

        :return: deserialized Workspace instance state dictionary
        '''
        self.log("Checking if the Workspace instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.workspaces.get(resource_group_name=self.resource_group,
                                                       workspace_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Workspace instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Workspace instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_response(self, d):
        d = {
            'id': d.get('id', None)
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
    AzureRMWorkspace()


if __name__ == '__main__':
    main()

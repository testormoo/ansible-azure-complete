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
module: azure_rm_databricksworkspace
version_added: "2.8"
short_description: Manage Azure Workspace instance.
description:
    - Create, update and delete instance of Azure Workspace.

options:
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    managed_resource_group_id:
        description:
            - The managed resource group Id.
            - Required when C(state) is I(present).
    parameters:
        description:
            - Name and value pairs that define the workspace parameters.
    ui_definition_uri:
        description:
            - The blob URI where the UI definition file is located.
    authorizations:
        description:
            - The workspace provider authorizations.
        type: list
        suboptions:
            principal_id:
                description:
                    - "The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the workspace resources."
                    - Required when C(state) is I(present).
            role_definition_id:
                description:
                    - "The provider's role definition identifier. This role will define all the permissions that the provider must have on the workspace's
                       container resource group. This role definition cannot have permission to delete the resource group."
                    - Required when C(state) is I(present).
    sku:
        description:
            - The SKU of the resource.
        suboptions:
            name:
                description:
                    - The SKU name.
                    - Required when C(state) is I(present).
            tier:
                description:
                    - The SKU tier.
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        required: True
    name:
        description:
            - The name of the workspace.
        required: True
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
    azure_rm_databricksworkspace:
      location: eastus
      managed_resource_group_id: /subscriptions/subid/resourceGroups/myManagedRG
      resource_group: rg
      name: myWorkspace
'''

RETURN = '''
id:
    description:
        - "Fully qualified resource Id for the resource. Ex -
           /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}"
    returned: always
    type: str
    sample: /subscriptions/subid/resourceGroups/rg/providers/Microsoft.Databricks/workspaces/myWorkspace
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.databricks import DatabricksClient
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
            location=dict(
                type='str'
            ),
            managed_resource_group_id=dict(
                type='str'
            ),
            parameters=dict(
                type='str'
            ),
            ui_definition_uri=dict(
                type='str'
            ),
            authorizations=dict(
                type='list',
                options=dict(
                    principal_id=dict(
                        type='str'
                    ),
                    role_definition_id=dict(
                        type='str'
                    )
                )
            ),
            sku=dict(
                type='dict',
                options=dict(
                    name=dict(
                        type='str'
                    ),
                    tier=dict(
                        type='str'
                    )
                )
            ),
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.parameters = dict()
        self.resource_group = None
        self.name = None

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


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(DatabricksClient,
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
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Workspace instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_workspace(self):
        '''
        Creates or updates Workspace with the specified configuration.

        :return: deserialized Workspace instance state dictionary
        '''
        self.log("Creating / Updating the Workspace instance {0}".format(self.name))

        try:
            response = self.mgmt_client.workspaces.create_or_update(parameters=self.parameters,
                                                                    resource_group_name=self.resource_group,
                                                                    workspace_name=self.name)
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


def main():
    """Main execution"""
    AzureRMWorkspace()


if __name__ == '__main__':
    main()

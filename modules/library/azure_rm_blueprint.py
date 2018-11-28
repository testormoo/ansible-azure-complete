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
module: azure_rm_blueprint
version_added: "2.8"
short_description: Manage Azure Blueprint instance.
description:
    - Create, update and delete instance of Azure Blueprint.

options:
    management_group_name:
        description:
            - C(management_group) where blueprint stores.
        required: True
    name:
        description:
            - name of the blueprint.
        required: True
    display_name:
        description:
            - One-liner string explain this resource.
    description:
        description:
            - Multi-line explain this resource.
    target_scope:
        description:
            - The scope where this Blueprint can be applied.
        choices:
            - 'subscription'
            - 'management_group'
    parameters:
        description:
            - Parameters required by this Blueprint definition.
    resource_groups:
        description:
            - Resource group placeholders defined by this Blueprint definition.
    versions:
        description:
            - Published versions of this blueprint.
    layout:
        description:
            - Layout view of the blueprint, for UI reference.
    state:
      description:
        - Assert the state of the Blueprint.
        - Use 'present' to create or update an Blueprint and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Create (or update) Blueprint
    azure_rm_blueprint:
      management_group_name: ContosoOnlineGroup
      name: simpleBlueprint
      description: blueprint contains all artifact kinds {'template', 'rbac', 'policy'}
      target_scope: subscription
      parameters: {
  "storageAccountType": {
    "type": "string",
    "metadata": {
      "displayName": "storage account type."
    }
  },
  "costCenter": {
    "type": "string",
    "metadata": {
      "displayName": "force cost center tag for all resources under given subscription."
    }
  },
  "owners": {
    "type": "array",
    "metadata": {
      "displayName": "assign owners to subscription along with blueprint assignment."
    }
  }
}
      resource_groups: {
  "storageRG": {
    "metadata": {
      "displayName": "storage resource group",
      "description": "Contains storageAccounts that collect all shoebox logs."
    }
  }
}
'''

RETURN = '''
id:
    description:
        - String Id used to locate any resource on Azure.
    returned: always
    type: str
    sample: id
status:
    description:
        - Status of the Blueprint. This field is readonly.
    returned: always
    type: complex
    sample: status
    contains:
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.blueprint import BlueprintManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMBlueprint(AzureRMModuleBase):
    """Configuration class for an Azure RM Blueprint resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            management_group_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            display_name=dict(
                type='str'
            ),
            description=dict(
                type='str'
            ),
            target_scope=dict(
                type='str',
                choices=['subscription',
                         'management_group']
            ),
            parameters=dict(
                type='dict'
            ),
            resource_groups=dict(
                type='dict'
            ),
            versions=dict(
                type='str'
            ),
            layout=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.management_group_name = None
        self.name = None
        self.blueprint = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBlueprint, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.blueprint[key] = kwargs[key]

        dict_camelize(self.blueprint, ['target_scope'], True)
        dict_map(self.blueprint, ['target_scope'], {'management_group': 'managementGroup'})

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BlueprintManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_blueprint()

        if not old_response:
            self.log("Blueprint instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Blueprint instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.blueprint, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Blueprint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_blueprint()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Blueprint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_blueprint()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Blueprint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'status': {
                }
                })
        return self.results

    def create_update_blueprint(self):
        '''
        Creates or updates Blueprint with the specified configuration.

        :return: deserialized Blueprint instance state dictionary
        '''
        self.log("Creating / Updating the Blueprint instance {0}".format(self.name))

        try:
            response = self.mgmt_client.blueprints.create_or_update(management_group_name=self.management_group_name,
                                                                    blueprint_name=self.name,
                                                                    blueprint=self.blueprint)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Blueprint instance.')
            self.fail("Error creating the Blueprint instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_blueprint(self):
        '''
        Deletes specified Blueprint instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Blueprint instance {0}".format(self.name))
        try:
            response = self.mgmt_client.blueprints.delete(management_group_name=self.management_group_name,
                                                          blueprint_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Blueprint instance.')
            self.fail("Error deleting the Blueprint instance: {0}".format(str(e)))

        return True

    def get_blueprint(self):
        '''
        Gets the properties of the specified Blueprint.

        :return: deserialized Blueprint instance state dictionary
        '''
        self.log("Checking if the Blueprint instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.blueprints.get(management_group_name=self.management_group_name,
                                                       blueprint_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Blueprint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Blueprint instance.')
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


def main():
    """Main execution"""
    AzureRMBlueprint()


if __name__ == '__main__':
    main()

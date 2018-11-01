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
short_description: Manage Blueprint instance.
description:
    - Create, update and delete instance of Blueprint.

options:
    management_group_name:
        description:
            - ManagementGroup where I(blueprint) stores.
        required: True
    blueprint_name:
        description:
            - name of the I(blueprint).
        required: True
    blueprint:
        description:
            - Blueprint definition.
        required: True
        suboptions:
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
      blueprint_name: simpleBlueprint
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


class AzureRMBlueprints(AzureRMModuleBase):
    """Configuration class for an Azure RM Blueprint resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            management_group_name=dict(
                type='str',
                required=True
            ),
            blueprint_name=dict(
                type='str',
                required=True
            ),
            blueprint=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.management_group_name = None
        self.blueprint_name = None
        self.blueprint = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBlueprints, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "display_name":
                    self.blueprint["display_name"] = kwargs[key]
                elif key == "description":
                    self.blueprint["description"] = kwargs[key]
                elif key == "target_scope":
                    ev = kwargs[key]
                    if ev == 'management_group':
                        ev = 'managementGroup'
                    self.blueprint["target_scope"] = ev
                elif key == "parameters":
                    self.blueprint["parameters"] = kwargs[key]
                elif key == "resource_groups":
                    self.blueprint["resource_groups"] = kwargs[key]
                elif key == "versions":
                    self.blueprint["versions"] = kwargs[key]
                elif key == "layout":
                    self.blueprint["layout"] = kwargs[key]

        old_response = None
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
                self.log("Need to check if Blueprint instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Blueprint instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_blueprint()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Blueprint instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_blueprint()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_blueprint():
                time.sleep(20)
        else:
            self.log("Blueprint instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_blueprint(self):
        '''
        Creates or updates Blueprint with the specified configuration.

        :return: deserialized Blueprint instance state dictionary
        '''
        self.log("Creating / Updating the Blueprint instance {0}".format(self.blueprint_name))

        try:
            response = self.mgmt_client.blueprints.create_or_update(management_group_name=self.management_group_name,
                                                                    blueprint_name=self.blueprint_name,
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
        self.log("Deleting the Blueprint instance {0}".format(self.blueprint_name))
        try:
            response = self.mgmt_client.blueprints.delete(management_group_name=self.management_group_name,
                                                          blueprint_name=self.blueprint_name)
        except CloudError as e:
            self.log('Error attempting to delete the Blueprint instance.')
            self.fail("Error deleting the Blueprint instance: {0}".format(str(e)))

        return True

    def get_blueprint(self):
        '''
        Gets the properties of the specified Blueprint.

        :return: deserialized Blueprint instance state dictionary
        '''
        self.log("Checking if the Blueprint instance {0} is present".format(self.blueprint_name))
        found = False
        try:
            response = self.mgmt_client.blueprints.get(management_group_name=self.management_group_name,
                                                       blueprint_name=self.blueprint_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Blueprint instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Blueprint instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'status': {
            }
        }
        return d


def main():
    """Main execution"""
    AzureRMBlueprints()


if __name__ == '__main__':
    main()

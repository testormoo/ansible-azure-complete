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
module: azure_rm_logicintegrationaccountmap
version_added: "2.8"
short_description: Manage Integration Account Map instance.
description:
    - Create, update and delete instance of Integration Account Map.

options:
    resource_group:
        description:
            - The resource group name.
        required: True
    integration_account_name:
        description:
            - The integration account name.
        required: True
    map_name:
        description:
            - The integration account I(map) name.
        required: True
    map:
        description:
            - The integration account map.
        required: True
        suboptions:
            location:
                description:
                    - The resource location.
            map_type:
                description:
                    - The map type.
                required: True
                choices:
                    - 'not_specified'
                    - 'xslt'
                    - 'xslt20'
                    - 'xslt30'
                    - 'liquid'
            parameters_schema:
                description:
                    - The parameters schema of integration account map.
                suboptions:
                    ref:
                        description:
                            - The reference name.
            content:
                description:
                    - The content.
            content_type:
                description:
                    - The I(content) type.
            metadata:
                description:
                    - The metadata.
    state:
      description:
        - Assert the state of the Integration Account Map.
        - Use 'present' to create or update an Integration Account Map and 'absent' to delete it.
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
  - name: Create (or update) Integration Account Map
    azure_rm_logicintegrationaccountmap:
      resource_group: testResourceGroup
      integration_account_name: testIntegrationAccount
      map_name: testMap
      map:
        location: westus
'''

RETURN = '''
id:
    description:
        - The resource id.
    returned: always
    type: str
    sample: "/subscriptions/34adfa4f-cedf-4dc0-ba29-b6d1a69ab345/resourceGroups/<resourceGroup>/providers/Microsoft.Logic/integrationAccounts/<IntegrationAcc
            ount>/maps/testMap"
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.logic import LogicManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMIntegrationAccountMaps(AzureRMModuleBase):
    """Configuration class for an Azure RM Integration Account Map resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            integration_account_name=dict(
                type='str',
                required=True
            ),
            map_name=dict(
                type='str',
                required=True
            ),
            map=dict(
                type='dict',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.integration_account_name = None
        self.map_name = None
        self.map = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMIntegrationAccountMaps, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "location":
                    self.map["location"] = kwargs[key]
                elif key == "map_type":
                    self.map["map_type"] = _snake_to_camel(kwargs[key], True)
                elif key == "parameters_schema":
                    self.map["parameters_schema"] = kwargs[key]
                elif key == "content":
                    self.map["content"] = kwargs[key]
                elif key == "content_type":
                    self.map["content_type"] = kwargs[key]
                elif key == "metadata":
                    self.map["metadata"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(LogicManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_integrationaccountmap()

        if not old_response:
            self.log("Integration Account Map instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Integration Account Map instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Integration Account Map instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Integration Account Map instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_integrationaccountmap()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Integration Account Map instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_integrationaccountmap()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_integrationaccountmap():
                time.sleep(20)
        else:
            self.log("Integration Account Map instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_integrationaccountmap(self):
        '''
        Creates or updates Integration Account Map with the specified configuration.

        :return: deserialized Integration Account Map instance state dictionary
        '''
        self.log("Creating / Updating the Integration Account Map instance {0}".format(self.map_name))

        try:
            response = self.mgmt_client.integration_account_maps.create_or_update(resource_group_name=self.resource_group,
                                                                                  integration_account_name=self.integration_account_name,
                                                                                  map_name=self.map_name,
                                                                                  map=self.map)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Integration Account Map instance.')
            self.fail("Error creating the Integration Account Map instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_integrationaccountmap(self):
        '''
        Deletes specified Integration Account Map instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Integration Account Map instance {0}".format(self.map_name))
        try:
            response = self.mgmt_client.integration_account_maps.delete(resource_group_name=self.resource_group,
                                                                        integration_account_name=self.integration_account_name,
                                                                        map_name=self.map_name)
        except CloudError as e:
            self.log('Error attempting to delete the Integration Account Map instance.')
            self.fail("Error deleting the Integration Account Map instance: {0}".format(str(e)))

        return True

    def get_integrationaccountmap(self):
        '''
        Gets the properties of the specified Integration Account Map.

        :return: deserialized Integration Account Map instance state dictionary
        '''
        self.log("Checking if the Integration Account Map instance {0} is present".format(self.map_name))
        found = False
        try:
            response = self.mgmt_client.integration_account_maps.get(resource_group_name=self.resource_group,
                                                                     integration_account_name=self.integration_account_name,
                                                                     map_name=self.map_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Integration Account Map instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Integration Account Map instance.')
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
    AzureRMIntegrationAccountMaps()


if __name__ == '__main__':
    main()

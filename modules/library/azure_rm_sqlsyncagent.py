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
module: azure_rm_sqlsyncagent
version_added: "2.8"
short_description: Manage Azure Sync Agent instance.
description:
    - Create, update and delete instance of Azure Sync Agent.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server on which the sync agent is hosted.
        required: True
    name:
        description:
            - The name of the sync agent.
        required: True
    sync_database_id:
        description:
            - ARM resource id of the sync database in the sync agent.
    state:
      description:
        - Assert the state of the Sync Agent.
        - Use 'present' to create or update an Sync Agent and 'absent' to delete it.
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
  - name: Create (or update) Sync Agent
    azure_rm_sqlsyncagent:
      resource_group: syncagentcrud-65440
      server_name: syncagentcrud-8475
      name: syncagentcrud-3187
      sync_database_id: NOT FOUND
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default-SQL-Onebox/providers/Microsoft.Sql/servers/syncagentcrud-8475/syncAge
            nts/syncagentcrud-3187"
state:
    description:
        - "State of the sync agent. Possible values include: 'Online', 'Offline', 'NeverConnected'"
    returned: always
    type: str
    sample: NeverConnected
version:
    description:
        - Version of the sync agent.
    returned: always
    type: str
    sample: 4.2.0.0
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMSyncAgent(AzureRMModuleBase):
    """Configuration class for an Azure RM Sync Agent resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            sync_database_id=dict(
                type='str'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.name = None
        self.sync_database_id = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMSyncAgent, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_syncagent()

        if not old_response:
            self.log("Sync Agent instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Sync Agent instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Sync Agent instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_syncagent()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Sync Agent instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_syncagent()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Sync Agent instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'state': response.get('state', None),
                'version': response.get('version', None)
                })
        return self.results

    def create_update_syncagent(self):
        '''
        Creates or updates Sync Agent with the specified configuration.

        :return: deserialized Sync Agent instance state dictionary
        '''
        self.log("Creating / Updating the Sync Agent instance {0}".format(self.name))

        try:
            response = self.mgmt_client.sync_agents.create_or_update(resource_group_name=self.resource_group,
                                                                     server_name=self.server_name,
                                                                     sync_agent_name=self.name)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Sync Agent instance.')
            self.fail("Error creating the Sync Agent instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_syncagent(self):
        '''
        Deletes specified Sync Agent instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Sync Agent instance {0}".format(self.name))
        try:
            response = self.mgmt_client.sync_agents.delete(resource_group_name=self.resource_group,
                                                           server_name=self.server_name,
                                                           sync_agent_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Sync Agent instance.')
            self.fail("Error deleting the Sync Agent instance: {0}".format(str(e)))

        return True

    def get_syncagent(self):
        '''
        Gets the properties of the specified Sync Agent.

        :return: deserialized Sync Agent instance state dictionary
        '''
        self.log("Checking if the Sync Agent instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.sync_agents.get(resource_group_name=self.resource_group,
                                                        server_name=self.server_name,
                                                        sync_agent_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Sync Agent instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Sync Agent instance.')
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
    AzureRMSyncAgent()


if __name__ == '__main__':
    main()

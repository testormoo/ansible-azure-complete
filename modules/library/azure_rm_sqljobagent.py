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
module: azure_rm_sqljobagent
version_added: "2.8"
short_description: Manage Job Agent instance.
description:
    - Create, update and delete instance of Job Agent.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    job_agent_name:
        description:
            - The name of the job agent to be created or updated.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    sku:
        description:
            - The name and tier of the SKU.
        suboptions:
            name:
                description:
                    - The name of the SKU. Ex - P3. It is typically a letter+number code
                required: True
            tier:
                description:
                    - This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
            size:
                description:
                    - The SKU size. When the name field is the combination of I(tier) and some other value, this would be the standalone code.
            family:
                description:
                    - If the service has different generations of hardware, for the same SKU, then that can be captured here.
            capacity:
                description:
                    - "If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource this
                       may be omitted."
    database_id:
        description:
            - Resource ID of the database to store job metadata in.
        required: True
    state:
      description:
        - Assert the state of the Job Agent.
        - Use 'present' to create or update an Job Agent and 'absent' to delete it.
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
  - name: Create (or update) Job Agent
    azure_rm_sqljobagent:
      resource_group: group1
      server_name: server1
      job_agent_name: agent1
      location: eastus
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/group1/providers/Microsoft.Sql/servers/server1/jobAgents/agent1
state:
    description:
        - "The state of the job agent. Possible values include: 'Creating', 'Ready', 'Updating', 'Deleting', 'Disabled'"
    returned: always
    type: str
    sample: state
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

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


class AzureRMJobAgents(AzureRMModuleBase):
    """Configuration class for an Azure RM Job Agent resource"""

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
            job_agent_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str'
            ),
            sku=dict(
                type='dict'
            ),
            database_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.job_agent_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMJobAgents, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                elif key == "sku":
                    self.parameters["sku"] = kwargs[key]
                elif key == "database_id":
                    self.parameters["database_id"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        if "location" not in self.parameters:
            self.parameters["location"] = resource_group.location

        old_response = self.get_jobagent()

        if not old_response:
            self.log("Job Agent instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Job Agent instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Job Agent instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Job Agent instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_jobagent()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Job Agent instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_jobagent()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_jobagent():
                time.sleep(20)
        else:
            self.log("Job Agent instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_jobagent(self):
        '''
        Creates or updates Job Agent with the specified configuration.

        :return: deserialized Job Agent instance state dictionary
        '''
        self.log("Creating / Updating the Job Agent instance {0}".format(self.job_agent_name))

        try:
            response = self.mgmt_client.job_agents.create_or_update(resource_group_name=self.resource_group,
                                                                    server_name=self.server_name,
                                                                    job_agent_name=self.job_agent_name,
                                                                    parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Job Agent instance.')
            self.fail("Error creating the Job Agent instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_jobagent(self):
        '''
        Deletes specified Job Agent instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Job Agent instance {0}".format(self.job_agent_name))
        try:
            response = self.mgmt_client.job_agents.delete(resource_group_name=self.resource_group,
                                                          server_name=self.server_name,
                                                          job_agent_name=self.job_agent_name)
        except CloudError as e:
            self.log('Error attempting to delete the Job Agent instance.')
            self.fail("Error deleting the Job Agent instance: {0}".format(str(e)))

        return True

    def get_jobagent(self):
        '''
        Gets the properties of the specified Job Agent.

        :return: deserialized Job Agent instance state dictionary
        '''
        self.log("Checking if the Job Agent instance {0} is present".format(self.job_agent_name))
        found = False
        try:
            response = self.mgmt_client.job_agents.get(resource_group_name=self.resource_group,
                                                       server_name=self.server_name,
                                                       job_agent_name=self.job_agent_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Job Agent instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Job Agent instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None),
            'state': d.get('state', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMJobAgents()


if __name__ == '__main__':
    main()
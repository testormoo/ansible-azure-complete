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
module: azure_rm_sqlfailovergroup
version_added: "2.8"
short_description: Manage Failover Group instance.
description:
    - Create, update and delete instance of Failover Group.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server containing the failover group.
        required: True
    failover_group_name:
        description:
            - The name of the failover group.
        required: True
    read_write_endpoint:
        description:
            - Read-write endpoint of the failover group instance.
        required: True
        suboptions:
            failover_policy:
                description:
                    - "Failover policy of the read-write endpoint for the failover group. If failoverPolicy is C(automatic) then
                       I(failover_with_data_loss_grace_period_minutes) is required."
                required: True
                choices:
                    - 'manual'
                    - 'automatic'
            failover_with_data_loss_grace_period_minutes:
                description:
                    - "Grace period before failover with data loss is attempted for the read-write endpoint. If I(failover_policy) is C(automatic) then
                       failoverWithDataLossGracePeriodMinutes is required."
    read_only_endpoint:
        description:
            - Read-only endpoint of the failover group instance.
        suboptions:
            failover_policy:
                description:
                    - Failover policy of the read-only endpoint for the failover group.
                choices:
                    - 'disabled'
                    - 'enabled'
    partner_servers:
        description:
            - List of partner server information for the failover group.
        required: True
        type: list
        suboptions:
            id:
                description:
                    - Resource identifier of the partner server.
                required: True
    databases:
        description:
            - List of databases in the failover group.
        type: list
    state:
      description:
        - Assert the state of the Failover Group.
        - Use 'present' to create or update an Failover Group and 'absent' to delete it.
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
  - name: Create (or update) Failover Group
    azure_rm_sqlfailovergroup:
      resource_group: Default
      server_name: failover-group-primary-server
      failover_group_name: failover-group-test-3
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default/providers/Microsoft.Sql/servers/failover-group-primary-server/failove
            rGroups/failover-group-test-3"
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


class AzureRMFailoverGroups(AzureRMModuleBase):
    """Configuration class for an Azure RM Failover Group resource"""

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
            failover_group_name=dict(
                type='str',
                required=True
            ),
            read_write_endpoint=dict(
                type='dict',
                required=True
            ),
            read_only_endpoint=dict(
                type='dict'
            ),
            partner_servers=dict(
                type='list',
                required=True
            ),
            databases=dict(
                type='list'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.server_name = None
        self.failover_group_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFailoverGroups, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "read_write_endpoint":
                    ev = kwargs[key]
                    if 'failover_policy' in ev:
                        if ev['failover_policy'] == 'manual':
                            ev['failover_policy'] = 'Manual'
                        elif ev['failover_policy'] == 'automatic':
                            ev['failover_policy'] = 'Automatic'
                    self.parameters["read_write_endpoint"] = ev
                elif key == "read_only_endpoint":
                    ev = kwargs[key]
                    if 'failover_policy' in ev:
                        if ev['failover_policy'] == 'disabled':
                            ev['failover_policy'] = 'Disabled'
                        elif ev['failover_policy'] == 'enabled':
                            ev['failover_policy'] = 'Enabled'
                    self.parameters["read_only_endpoint"] = ev
                elif key == "partner_servers":
                    self.parameters["partner_servers"] = kwargs[key]
                elif key == "databases":
                    self.parameters["databases"] = kwargs[key]

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        resource_group = self.get_resource_group(self.resource_group)

        old_response = self.get_failovergroup()

        if not old_response:
            self.log("Failover Group instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Failover Group instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log("Need to check if Failover Group instance has to be deleted or may be updated")
                self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Failover Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_failovergroup()

            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Failover Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_failovergroup()
            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure.
            while self.get_failovergroup():
                time.sleep(20)
        else:
            self.log("Failover Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update(self.format_item(response))
        return self.results

    def create_update_failovergroup(self):
        '''
        Creates or updates Failover Group with the specified configuration.

        :return: deserialized Failover Group instance state dictionary
        '''
        self.log("Creating / Updating the Failover Group instance {0}".format(self.failover_group_name))

        try:
            response = self.mgmt_client.failover_groups.create_or_update(resource_group_name=self.resource_group,
                                                                         server_name=self.server_name,
                                                                         failover_group_name=self.failover_group_name,
                                                                         parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Failover Group instance.')
            self.fail("Error creating the Failover Group instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_failovergroup(self):
        '''
        Deletes specified Failover Group instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Failover Group instance {0}".format(self.failover_group_name))
        try:
            response = self.mgmt_client.failover_groups.delete(resource_group_name=self.resource_group,
                                                               server_name=self.server_name,
                                                               failover_group_name=self.failover_group_name)
        except CloudError as e:
            self.log('Error attempting to delete the Failover Group instance.')
            self.fail("Error deleting the Failover Group instance: {0}".format(str(e)))

        return True

    def get_failovergroup(self):
        '''
        Gets the properties of the specified Failover Group.

        :return: deserialized Failover Group instance state dictionary
        '''
        self.log("Checking if the Failover Group instance {0} is present".format(self.failover_group_name))
        found = False
        try:
            response = self.mgmt_client.failover_groups.get(resource_group_name=self.resource_group,
                                                            server_name=self.server_name,
                                                            failover_group_name=self.failover_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Failover Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Failover Group instance.')
        if found is True:
            return response.as_dict()

        return False

    def format_item(self, d):
        d = {
            'id': d.get('id', None)
        }
        return d


def main():
    """Main execution"""
    AzureRMFailoverGroups()


if __name__ == '__main__':
    main()

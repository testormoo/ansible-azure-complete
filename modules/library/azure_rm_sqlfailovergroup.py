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
short_description: Manage Azure Failover Group instance.
description:
    - Create, update and delete instance of Azure Failover Group.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server containing the failover group.
        required: True
    name:
        description:
            - The name of the failover group.
        required: True
    read_write_endpoint:
        description:
            - Read-write endpoint of the failover group instance.
            - Required when C(state) is I(present).
        suboptions:
            failover_policy:
                description:
                    - "Failover policy of the read-write endpoint for the failover group. If failoverPolicy is C(automatic) then
                       I(failover_with_data_loss_grace_period_minutes) is required."
                    - Required when C(state) is I(present).
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
                    - "Failover policy of the read-only endpoint for the failover group. Possible values include: 'Disabled', 'Enabled'"
                type: bool
    partner_servers:
        description:
            - List of partner server information for the failover group.
            - Required when C(state) is I(present).
        type: list
        suboptions:
            id:
                description:
                    - Resource identifier of the partner server.
                    - Required when C(state) is I(present).
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
      name: failover-group-test-3
      read_write_endpoint:
        failover_policy: Automatic
        failover_with_data_loss_grace_period_minutes: 480
      read_only_endpoint:
        failover_policy: failover_policy
      partner_servers:
        - id: /subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default/providers/Microsoft.Sql/servers/failover-group-secondary-server
      databases:
        - [
  "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default/providers/Microsoft.Sql/servers/failover-group-primary-server/databases/testdb-1",
  "/subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/Default/providers/Microsoft.Sql/servers/failover-group-primary-server/databases/testdb-2"
]
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


class AzureRMFailoverGroup(AzureRMModuleBase):
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
            name=dict(
                type='str',
                required=True
            ),
            read_write_endpoint=dict(
                type='dict',
                options=dict(
                    failover_policy=dict(
                        type='str',
                        choices=['manual',
                                 'automatic']
                    ),
                    failover_with_data_loss_grace_period_minutes=dict(
                        type='int'
                    )
                )
            ),
            read_only_endpoint=dict(
                type='dict',
                options=dict(
                    failover_policy=dict(
                        type='bool'
                    )
                )
            ),
            partner_servers=dict(
                type='list',
                options=dict(
                    id=dict(
                        type='str'
                    )
                )
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
        self.name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMFailoverGroup, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                    supports_check_mode=True,
                                                    supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        dict_camelize(self.parameters, ['read_write_endpoint', 'failover_policy'], True)
        dict_map(self.parameters, ['read_only_endpoint', 'failover_policy'], {True: 'Enabled', False: 'Disabled'})
        dict_resource_id(self.parameters, ['partner_servers', 'id'], subscription_id=self.subscription_id, resource_group=self.resource_group)

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
                if (not default_compare(self.parameters, old_response, '', self.results)):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Failover Group instance")

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_failovergroup()

            self.results['changed'] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Failover Group instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_failovergroup()
            # This currently doesnt' work as there is a bug in SDK / Service
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        else:
            self.log("Failover Group instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None)
                })
        return self.results

    def create_update_failovergroup(self):
        '''
        Creates or updates Failover Group with the specified configuration.

        :return: deserialized Failover Group instance state dictionary
        '''
        self.log("Creating / Updating the Failover Group instance {0}".format(self.name))

        try:
            response = self.mgmt_client.failover_groups.create_or_update(resource_group_name=self.resource_group,
                                                                         server_name=self.server_name,
                                                                         failover_group_name=self.name,
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
        self.log("Deleting the Failover Group instance {0}".format(self.name))
        try:
            response = self.mgmt_client.failover_groups.delete(resource_group_name=self.resource_group,
                                                               server_name=self.server_name,
                                                               failover_group_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Failover Group instance.')
            self.fail("Error deleting the Failover Group instance: {0}".format(str(e)))

        return True

    def get_failovergroup(self):
        '''
        Gets the properties of the specified Failover Group.

        :return: deserialized Failover Group instance state dictionary
        '''
        self.log("Checking if the Failover Group instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.failover_groups.get(resource_group_name=self.resource_group,
                                                            server_name=self.server_name,
                                                            failover_group_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Failover Group instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Failover Group instance.')
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


def dict_resource_id(d, path, **kwargs):
    if isinstance(d, list):
        for i in range(len(d)):
            dict_resource_id(d[i], path)
    elif isinstance(d, dict):
        if len(path) == 1:
            old_value = d.get(path[0], None)
            if old_value is not None:
                if isinstance(old_value, dict):
                    resource_id = format_resource_id(val=self.target['name'],
                                                    subscription_id=self.target.get('subscription_id') or self.subscription_id,
                                                    namespace=self.target['namespace'],
                                                    types=self.target['types'],
                                                    resource_group=self.target.get('resource_group') or self.resource_group)
                    d[path[0]] = resource_id
        else:
            sd = d.get(path[0], None)
            if sd is not None:
                dict_resource_id(sd, path[1:])


def main():
    """Main execution"""
    AzureRMFailoverGroup()


if __name__ == '__main__':
    main()
